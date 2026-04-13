from __future__ import annotations

import csv
from io import StringIO, BytesIO
from pathlib import Path

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, send_file, url_for
from flask_login import current_user, login_required

from ..extensions import db
from ..forms import KPIActualForm, KPIForm, MonthlyEntryForm, UserForm
from ..models import Branch, KPIDefinition, KPIQuarterlyActual, MonthlyEntry, ProgramArea, StrategicGoal, StrategicPriority, User
from ..services import board_scorecard_rows, current_fiscal_year, dashboard_summary


main_bp = Blueprint('main', __name__)


def get_priority(priority_id: int | None = None) -> StrategicPriority:
    query = StrategicPriority.query.order_by(StrategicPriority.id)
    if priority_id:
        priority = db.session.get(StrategicPriority, priority_id)
        if not priority:
            abort(404)
        return priority
    requested = request.args.get('priority_id', type=int)
    if requested:
        priority = db.session.get(StrategicPriority, requested)
        if priority:
            return priority
    priority = query.first()
    if not priority:
        abort(404)
    return priority


@main_bp.app_context_processor
def inject_globals():
    selected = None
    try:
        selected = get_priority()
    except Exception:
        selected = None
    return {
        'current_fiscal_year': current_fiscal_year(),
        'all_priorities': StrategicPriority.query.order_by(StrategicPriority.id).all(),
        'selected_priority': selected,
    }


def require_editor():
    if not current_user.is_authenticated or not current_user.can_edit():
        abort(403)


def populate_kpi_form(form: KPIForm, priority: StrategicPriority) -> None:
    goals = StrategicGoal.query.filter_by(priority_id=priority.id).order_by(StrategicGoal.code).all()
    form.goal_id.choices = [(g.id, f'{g.code} - {g.title}') for g in goals]


def populate_entry_form(form: MonthlyEntryForm, priority: StrategicPriority) -> None:
    branches = Branch.query.filter_by(active=True).order_by(Branch.name).all()
    goals = StrategicGoal.query.filter_by(priority_id=priority.id).order_by(StrategicGoal.code).all()
    areas = ProgramArea.query.filter_by(priority_id=priority.id).order_by(ProgramArea.name).all()
    form.branch_id.choices = [(b.id, b.name) for b in branches]
    form.goal_id.choices = [(g.id, f'{g.code} - {g.title}') for g in goals]
    form.program_area_id.choices = [(a.id, a.name) for a in areas]


@main_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))


@main_bp.route('/switch-priority')
@login_required
def switch_priority():
    priority = get_priority()
    target = request.args.get('next', 'main.dashboard')
    try:
        return redirect(url_for(target, priority_id=priority.id))
    except Exception:
        return redirect(url_for('main.dashboard', priority_id=priority.id))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    priority = get_priority()
    year = int(request.args.get('year', current_fiscal_year()))
    summary = dashboard_summary(priority.id, year)
    latest_entries = (
        MonthlyEntry.query.filter_by(priority_id=priority.id)
        .order_by(MonthlyEntry.entry_month.desc(), MonthlyEntry.id.desc())
        .limit(10).all()
    )
    return render_template('main/dashboard.html', year=year, latest_entries=latest_entries, **summary)


@main_bp.route('/kpis')
@login_required
def kpis():
    priority = get_priority()
    items = (
        KPIDefinition.query.filter_by(priority_id=priority.id)
        .order_by(KPIDefinition.sort_order, KPIDefinition.name)
        .all()
    )
    return render_template('main/kpi_list.html', items=items, priority=priority)


@main_bp.route('/kpis/new', methods=['GET', 'POST'])
@login_required
def kpi_new():
    require_editor()
    priority = get_priority()
    form = KPIForm()
    populate_kpi_form(form, priority)
    if form.validate_on_submit():
        item = KPIDefinition(
            priority_id=priority.id,
            goal_id=form.goal_id.data,
            name=form.name.data.strip(),
            community_need=form.community_need.data.strip(),
            definition=form.definition.data.strip(),
            measure_type=form.measure_type.data.strip(),
            data_source=form.data_source.data.strip(),
            frequency=form.frequency.data.strip(),
            owner=form.owner.data.strip(),
            target_approach=form.target_approach.data.strip(),
            dashboard_level=form.dashboard_level.data,
            is_board_metric=form.is_board_metric.data,
            baseline_value=form.baseline_value.data,
            annual_target=form.annual_target.data,
            unit_label=form.unit_label.data.strip() if form.unit_label.data else None,
            sort_order=form.sort_order.data or 0,
        )
        db.session.add(item)
        db.session.commit()
        flash('KPI created.', 'success')
        return redirect(url_for('main.kpis', priority_id=priority.id))
    return render_template('main/kpi_form.html', form=form, title='New KPI', priority=priority)


@main_bp.route('/kpis/<int:kpi_id>/edit', methods=['GET', 'POST'])
@login_required
def kpi_edit(kpi_id: int):
    require_editor()
    item = KPIDefinition.query.get_or_404(kpi_id)
    priority = item.priority
    form = KPIForm(obj=item)
    populate_kpi_form(form, priority)
    if form.validate_on_submit():
        form.populate_obj(item)
        item.unit_label = form.unit_label.data.strip() if form.unit_label.data else None
        db.session.commit()
        flash('KPI updated.', 'success')
        return redirect(url_for('main.kpis', priority_id=priority.id))
    return render_template('main/kpi_form.html', form=form, title='Edit KPI', priority=priority)


@main_bp.route('/kpis/<int:kpi_id>/quarterly', methods=['GET', 'POST'])
@login_required
def kpi_quarterly_update(kpi_id: int):
    require_editor()
    item = KPIDefinition.query.get_or_404(kpi_id)
    form = KPIActualForm(year=current_fiscal_year())
    if form.validate_on_submit():
        actual = KPIQuarterlyActual.query.filter_by(kpi_id=item.id, year=form.year.data, quarter=form.quarter.data).first()
        if not actual:
            actual = KPIQuarterlyActual(kpi_id=item.id, year=form.year.data, quarter=form.quarter.data)
            db.session.add(actual)
        actual.actual_value = form.actual_value.data
        actual.target_value = form.target_value.data if form.target_value.data is not None else item.annual_target
        actual.notes = form.notes.data.strip() if form.notes.data else None
        actual.updated_by_id = current_user.id
        actual.sync_status()
        db.session.commit()
        flash('Quarterly KPI update saved.', 'success')
        return redirect(url_for('main.kpis', priority_id=item.priority_id))
    return render_template('main/kpi_quarterly_form.html', form=form, item=item, priority=item.priority)


@main_bp.route('/entries')
@login_required
def entries():
    priority = get_priority()
    year = int(request.args.get('year', current_fiscal_year()))
    branch_id = request.args.get('branch_id', type=int)
    query = MonthlyEntry.query.filter_by(priority_id=priority.id).order_by(MonthlyEntry.entry_month.desc(), MonthlyEntry.id.desc())
    if year:
        query = query.filter(db.extract('year', MonthlyEntry.entry_month) == year)
    if branch_id:
        query = query.filter(MonthlyEntry.branch_id == branch_id)
    items = query.limit(150).all()
    branches = Branch.query.filter_by(active=True).order_by(Branch.name).all()
    return render_template('main/entry_list.html', items=items, branches=branches, year=year, branch_id=branch_id, priority=priority)


@main_bp.route('/entries/new', methods=['GET', 'POST'])
@login_required
def entry_new():
    require_editor()
    priority = get_priority()
    form = MonthlyEntryForm()
    populate_entry_form(form, priority)
    if form.validate_on_submit():
        entry = MonthlyEntry(
            priority_id=priority.id,
            entry_month=form.entry_month.data,
            branch_id=form.branch_id.data,
            goal_id=form.goal_id.data,
            program_area_id=form.program_area_id.data,
            service_name=form.service_name.data.strip(),
            audience_group=form.audience_group.data.strip() if form.audience_group.data else None,
            partner_name=form.partner_name.data.strip() if form.partner_name.data else None,
            multilingual_support=form.multilingual_support.data,
            inclusive_design=form.inclusive_design.data,
            referral_support=form.referral_support.data,
            sessions_offered=form.sessions_offered.data,
            attendance_or_uses=form.attendance_or_uses.data,
            unique_users=form.unique_users.data,
            completions=form.completions.data,
            avg_satisfaction=form.avg_satisfaction.data,
            belonging_gain_pct=form.belonging_gain_pct.data,
            ease_of_use_pct=form.ease_of_use_pct.data,
            referrals_made=form.referrals_made.data,
            materials_or_resource_uses=form.materials_or_resource_uses.data,
            notes=form.notes.data.strip() if form.notes.data else None,
            entered_by_id=current_user.id,
        )
        db.session.add(entry)
        db.session.commit()
        flash('Monthly entry added.', 'success')
        return redirect(url_for('main.entries', priority_id=priority.id))
    return render_template('main/entry_form.html', form=form, title='New monthly entry', priority=priority)


@main_bp.route('/entries/<int:entry_id>/edit', methods=['GET', 'POST'])
@login_required
def entry_edit(entry_id: int):
    require_editor()
    entry = MonthlyEntry.query.get_or_404(entry_id)
    priority = entry.priority
    form = MonthlyEntryForm(obj=entry)
    populate_entry_form(form, priority)
    if form.validate_on_submit():
        form.populate_obj(entry)
        entry.audience_group = form.audience_group.data.strip() if form.audience_group.data else None
        entry.partner_name = form.partner_name.data.strip() if form.partner_name.data else None
        entry.notes = form.notes.data.strip() if form.notes.data else None
        db.session.commit()
        flash('Monthly entry updated.', 'success')
        return redirect(url_for('main.entries', priority_id=priority.id))
    return render_template('main/entry_form.html', form=form, title='Edit monthly entry', priority=priority)


@main_bp.route('/scorecard')
@login_required
def scorecard():
    priority = get_priority()
    year = int(request.args.get('year', current_fiscal_year()))
    rows = board_scorecard_rows(priority.id, year)
    return render_template('main/scorecard.html', rows=rows, priority=priority, year=year)


@main_bp.route('/reference-workbook')
@login_required
def download_reference_workbook():
    priority = get_priority()
    if not priority.workbook_filename:
        abort(404)
    path = Path(current_app.root_path).parent / 'reference_workbooks' / priority.workbook_filename
    if not path.exists():
        abort(404)
    return send_file(path, as_attachment=True, download_name=priority.workbook_filename)


@main_bp.route('/export/monthly-entries.csv')
@login_required
def export_entries():
    priority = get_priority()
    year = int(request.args.get('year', current_fiscal_year()))
    entries = MonthlyEntry.query.filter(
        MonthlyEntry.priority_id == priority.id,
        db.extract('year', MonthlyEntry.entry_month) == year,
    ).order_by(MonthlyEntry.entry_month).all()
    stream = StringIO()
    writer = csv.writer(stream)
    writer.writerow([
        'priority', 'entry_month', 'branch', 'goal', 'program_area', 'service_name', 'audience_group', 'partner_name',
        'multilingual_support', 'inclusive_design', 'referral_support', 'sessions_offered', 'attendance_or_uses',
        'unique_users', 'completions', 'avg_satisfaction', 'belonging_gain_pct', 'ease_of_use_pct',
        'referrals_made', 'materials_or_resource_uses', 'notes'
    ])
    for entry in entries:
        writer.writerow([
            priority.name, entry.entry_month.isoformat(), entry.branch.name, entry.goal.code if entry.goal else '',
            entry.program_area.name if entry.program_area else '', entry.service_name, entry.audience_group or '',
            entry.partner_name or '', entry.multilingual_support, entry.inclusive_design, entry.referral_support,
            entry.sessions_offered, entry.attendance_or_uses, entry.unique_users, entry.completions,
            entry.avg_satisfaction if entry.avg_satisfaction is not None else '',
            entry.belonging_gain_pct if entry.belonging_gain_pct is not None else '',
            entry.ease_of_use_pct if entry.ease_of_use_pct is not None else '',
            entry.referrals_made, entry.materials_or_resource_uses, entry.notes or ''
        ])
    bio = BytesIO(stream.getvalue().encode('utf-8'))
    slug = priority.slug.replace('-', '_')
    return send_file(bio, mimetype='text/csv', as_attachment=True, download_name=f'{slug}_monthly_entries_{year}.csv')


@main_bp.route('/admin/users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.role != 'admin':
        abort(403)
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            full_name=form.full_name.data.strip(),
            email=form.email.data.strip().lower(),
            role=form.role.data,
        )
        if not form.password.data:
            flash('Password is required for new users.', 'danger')
        else:
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('User created.', 'success')
            return redirect(url_for('main.manage_users', priority_id=get_priority().id))
    users = User.query.order_by(User.full_name).all()
    return render_template('main/users.html', form=form, users=users)
