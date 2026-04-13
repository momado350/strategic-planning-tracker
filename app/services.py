from __future__ import annotations

from collections import Counter
from datetime import date

from sqlalchemy import extract, func

from .extensions import db
from .models import KPIQuarterlyActual, KPIDefinition, MonthlyEntry, StrategicPriority, avg_metric


def current_fiscal_year(today: date | None = None) -> int:
    today = today or date.today()
    return today.year + 1 if today.month >= 7 else today.year


def quarter_label(month: int) -> str:
    if month in (7, 8, 9):
        return 'Q1'
    if month in (10, 11, 12):
        return 'Q2'
    if month in (1, 2, 3):
        return 'Q3'
    return 'Q4'


def dashboard_summary(priority_id: int, year: int) -> dict:
    priority = db.session.get(StrategicPriority, priority_id)
    board_metrics = (
        KPIDefinition.query.filter_by(priority_id=priority_id, is_board_metric=True)
        .order_by(KPIDefinition.sort_order, KPIDefinition.name)
        .all()
    )
    quarterly = KPIQuarterlyActual.query.join(KPIDefinition).filter(
        KPIDefinition.priority_id == priority_id,
        KPIQuarterlyActual.year == year,
    ).all()
    status_counts = Counter(actual.status for actual in quarterly)

    monthly = MonthlyEntry.query.filter(
        MonthlyEntry.priority_id == priority_id,
        extract('year', MonthlyEntry.entry_month) == year,
    ).all()

    totals = {
        'entries': len(monthly),
        'attendance': sum(m.attendance_or_uses for m in monthly),
        'unique_users': sum(m.unique_users for m in monthly),
        'referrals': sum(m.referrals_made for m in monthly),
        'avg_satisfaction': avg_metric([m.avg_satisfaction for m in monthly]),
        'avg_belonging': avg_metric([m.belonging_gain_pct for m in monthly]),
        'avg_ease_of_use': avg_metric([m.ease_of_use_pct for m in monthly]),
        'multilingual_share': round((sum(1 for m in monthly if m.multilingual_support) / len(monthly)) * 100, 2) if monthly else None,
    }

    branch_rows = (
        db.session.query(
            MonthlyEntry.branch_id,
            func.count(MonthlyEntry.id),
            func.sum(MonthlyEntry.attendance_or_uses),
            func.sum(MonthlyEntry.unique_users),
        )
        .filter(
            MonthlyEntry.priority_id == priority_id,
            extract('year', MonthlyEntry.entry_month) == year,
        )
        .group_by(MonthlyEntry.branch_id)
        .all()
    )

    return {
        'priority': priority,
        'board_metrics': board_metrics,
        'status_counts': status_counts,
        'totals': totals,
        'branch_rows': branch_rows,
    }


def board_scorecard_rows(priority_id: int, year: int) -> list[dict]:
    kpis = (
        KPIDefinition.query.filter_by(priority_id=priority_id, is_board_metric=True)
        .order_by(KPIDefinition.sort_order, KPIDefinition.name)
        .all()
    )
    rows = []
    for kpi in kpis:
        quarter_map = {q.quarter: q for q in kpi.quarterly_actuals if q.year == year}
        annual_actual = kpi.annual_actual_for_year(year)
        final_status = quarter_map.get('Q4') or quarter_map.get('Q3') or quarter_map.get('Q2') or quarter_map.get('Q1')
        rows.append(
            {
                'kpi': kpi,
                'q1': quarter_map.get('Q1'),
                'q2': quarter_map.get('Q2'),
                'q3': quarter_map.get('Q3'),
                'q4': quarter_map.get('Q4'),
                'annual_actual': annual_actual,
                'annual_status': final_status.status if final_status else 'not_started',
            }
        )
    return rows
