from __future__ import annotations

from datetime import date, datetime
from statistics import mean

from flask_login import UserMixin
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db, login_manager


ROLE_CHOICES = ('admin', 'editor', 'viewer')
QUARTER_CHOICES = ('Q1', 'Q2', 'Q3', 'Q4')
STATUS_CHOICES = ('on_track', 'watch', 'needs_attention', 'not_started')


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(db.String(120), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False, index=True)
    role: Mapped[str] = mapped_column(db.String(20), default='viewer', nullable=False)
    password_hash: Mapped[str] = mapped_column(db.String(255), nullable=False)
    is_active_user: Mapped[bool] = mapped_column(default=True, nullable=False)

    monthly_entries: Mapped[list['MonthlyEntry']] = relationship(back_populates='entered_by')
    kpi_updates: Mapped[list['KPIQuarterlyActual']] = relationship(back_populates='updated_by')

    @property
    def is_active(self) -> bool:
        return self.is_active_user

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def can_edit(self) -> bool:
        return self.role in {'admin', 'editor'}


class Branch(TimestampMixin, db.Model):
    __tablename__ = 'branches'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    region: Mapped[str | None] = mapped_column(db.String(120))
    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    monthly_entries: Mapped[list['MonthlyEntry']] = relationship(back_populates='branch')


class StrategicPriority(TimestampMixin, db.Model):
    __tablename__ = 'strategic_priorities'

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(db.String(200), unique=True, nullable=False)
    statement: Mapped[str] = mapped_column(db.Text, nullable=False)
    workbook_filename: Mapped[str | None] = mapped_column(db.String(255))

    goals: Mapped[list['StrategicGoal']] = relationship(back_populates='priority', cascade='all, delete-orphan')
    kpis: Mapped[list['KPIDefinition']] = relationship(back_populates='priority', cascade='all, delete-orphan')
    program_areas: Mapped[list['ProgramArea']] = relationship(back_populates='priority', cascade='all, delete-orphan')
    monthly_entries: Mapped[list['MonthlyEntry']] = relationship(back_populates='priority', cascade='all, delete-orphan')


class StrategicGoal(TimestampMixin, db.Model):
    __tablename__ = 'strategic_goals'

    id: Mapped[int] = mapped_column(primary_key=True)
    priority_id: Mapped[int] = mapped_column(ForeignKey('strategic_priorities.id'), nullable=False, index=True)
    code: Mapped[str] = mapped_column(db.String(20), nullable=False)
    title: Mapped[str] = mapped_column(db.String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(db.Text)

    priority: Mapped[StrategicPriority] = relationship(back_populates='goals')
    kpis: Mapped[list['KPIDefinition']] = relationship(back_populates='goal')
    monthly_entries: Mapped[list['MonthlyEntry']] = relationship(back_populates='goal')


class ProgramArea(TimestampMixin, db.Model):
    __tablename__ = 'program_areas'
    __table_args__ = (UniqueConstraint('priority_id', 'name', name='uq_program_area_priority_name'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    priority_id: Mapped[int] = mapped_column(ForeignKey('strategic_priorities.id'), nullable=False, index=True)
    name: Mapped[str] = mapped_column(db.String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(db.Text)

    priority: Mapped[StrategicPriority] = relationship(back_populates='program_areas')
    monthly_entries: Mapped[list['MonthlyEntry']] = relationship(back_populates='program_area')


class KPIDefinition(TimestampMixin, db.Model):
    __tablename__ = 'kpi_definitions'

    id: Mapped[int] = mapped_column(primary_key=True)
    priority_id: Mapped[int] = mapped_column(ForeignKey('strategic_priorities.id'), nullable=False, index=True)
    goal_id: Mapped[int | None] = mapped_column(ForeignKey('strategic_goals.id'))
    name: Mapped[str] = mapped_column(db.String(200), nullable=False)
    community_need: Mapped[str] = mapped_column(db.Text, nullable=False)
    definition: Mapped[str] = mapped_column(db.Text, nullable=False)
    measure_type: Mapped[str] = mapped_column(db.String(50), nullable=False)
    data_source: Mapped[str] = mapped_column(db.String(200), nullable=False)
    frequency: Mapped[str] = mapped_column(db.String(50), nullable=False)
    owner: Mapped[str] = mapped_column(db.String(120), nullable=False)
    target_approach: Mapped[str] = mapped_column(db.String(200), nullable=False)
    dashboard_level: Mapped[str] = mapped_column(db.String(50), nullable=False)
    is_board_metric: Mapped[bool] = mapped_column(default=False, nullable=False)
    baseline_value: Mapped[float | None] = mapped_column(db.Float)
    annual_target: Mapped[float | None] = mapped_column(db.Float)
    unit_label: Mapped[str | None] = mapped_column(db.String(50))
    sort_order: Mapped[int] = mapped_column(default=0, nullable=False)

    priority: Mapped[StrategicPriority] = relationship(back_populates='kpis')
    goal: Mapped[StrategicGoal | None] = relationship(back_populates='kpis')
    quarterly_actuals: Mapped[list['KPIQuarterlyActual']] = relationship(back_populates='kpi', cascade='all, delete-orphan')

    def annual_actual_for_year(self, year: int) -> float | None:
        values = [a.actual_value for a in self.quarterly_actuals if a.year == year and a.actual_value is not None]
        if not values:
            return None
        return round(sum(values), 2)


class KPIQuarterlyActual(TimestampMixin, db.Model):
    __tablename__ = 'kpi_quarterly_actuals'
    __table_args__ = (UniqueConstraint('kpi_id', 'year', 'quarter', name='uq_kpi_year_quarter'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    kpi_id: Mapped[int] = mapped_column(ForeignKey('kpi_definitions.id'), nullable=False, index=True)
    year: Mapped[int] = mapped_column(nullable=False, index=True)
    quarter: Mapped[str] = mapped_column(db.String(2), nullable=False)
    actual_value: Mapped[float | None] = mapped_column(db.Float)
    target_value: Mapped[float | None] = mapped_column(db.Float)
    status: Mapped[str] = mapped_column(db.String(30), default='not_started', nullable=False)
    notes: Mapped[str | None] = mapped_column(db.Text)
    updated_by_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))

    kpi: Mapped[KPIDefinition] = relationship(back_populates='quarterly_actuals')
    updated_by: Mapped[User | None] = relationship(back_populates='kpi_updates')

    def sync_status(self) -> None:
        self.status = determine_status(self.actual_value, self.target_value)


class MonthlyEntry(TimestampMixin, db.Model):
    __tablename__ = 'monthly_entries'

    id: Mapped[int] = mapped_column(primary_key=True)
    priority_id: Mapped[int] = mapped_column(ForeignKey('strategic_priorities.id'), nullable=False, index=True)
    entry_month: Mapped[date] = mapped_column(nullable=False, index=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'), nullable=False, index=True)
    goal_id: Mapped[int | None] = mapped_column(ForeignKey('strategic_goals.id'))
    program_area_id: Mapped[int | None] = mapped_column(ForeignKey('program_areas.id'))
    service_name: Mapped[str] = mapped_column(db.String(200), nullable=False)
    audience_group: Mapped[str | None] = mapped_column(db.String(120))
    partner_name: Mapped[str | None] = mapped_column(db.String(200))
    multilingual_support: Mapped[bool] = mapped_column(default=False, nullable=False)
    inclusive_design: Mapped[bool] = mapped_column(default=False, nullable=False)
    referral_support: Mapped[bool] = mapped_column(default=False, nullable=False)
    sessions_offered: Mapped[int] = mapped_column(default=0, nullable=False)
    attendance_or_uses: Mapped[int] = mapped_column(default=0, nullable=False)
    unique_users: Mapped[int] = mapped_column(default=0, nullable=False)
    completions: Mapped[int] = mapped_column(default=0, nullable=False)
    avg_satisfaction: Mapped[float | None] = mapped_column(db.Float)
    belonging_gain_pct: Mapped[float | None] = mapped_column(db.Float)
    ease_of_use_pct: Mapped[float | None] = mapped_column(db.Float)
    referrals_made: Mapped[int] = mapped_column(default=0, nullable=False)
    materials_or_resource_uses: Mapped[int] = mapped_column(default=0, nullable=False)
    notes: Mapped[str | None] = mapped_column(db.Text)
    entered_by_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))

    priority: Mapped[StrategicPriority] = relationship(back_populates='monthly_entries')
    branch: Mapped[Branch] = relationship(back_populates='monthly_entries')
    goal: Mapped[StrategicGoal | None] = relationship(back_populates='monthly_entries')
    program_area: Mapped[ProgramArea | None] = relationship(back_populates='monthly_entries')
    entered_by: Mapped[User | None] = relationship(back_populates='monthly_entries')


@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return db.session.get(User, int(user_id))


def determine_status(actual_value: float | None, target_value: float | None) -> str:
    if actual_value is None:
        return 'not_started'
    if target_value in (None, 0):
        return 'on_track' if actual_value > 0 else 'not_started'
    ratio = actual_value / target_value
    if ratio >= 1:
        return 'on_track'
    if ratio >= 0.85:
        return 'watch'
    return 'needs_attention'


def avg_metric(values: list[float | None]) -> float | None:
    clean = [float(v) for v in values if v is not None]
    if not clean:
        return None
    return round(mean(clean), 2)
