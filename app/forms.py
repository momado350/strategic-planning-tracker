from __future__ import annotations

from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    FloatField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

from .models import QUARTER_CHOICES, ROLE_CHOICES


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign in')


class UserForm(FlaskForm):
    full_name = StringField('Full name', validators=[DataRequired(), Length(max=120)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=255)])
    role = SelectField('Role', validators=[DataRequired()], choices=[(r, r.title()) for r in ROLE_CHOICES])
    password = PasswordField('Password', validators=[Optional(), Length(min=8, max=128)])
    submit = SubmitField('Save user')


class KPIForm(FlaskForm):
    goal_id = SelectField('Goal', coerce=int, validators=[DataRequired()])
    name = StringField('KPI name', validators=[DataRequired(), Length(max=200)])
    community_need = TextAreaField('Community need', validators=[DataRequired()])
    definition = TextAreaField('Definition', validators=[DataRequired()])
    measure_type = StringField('Measure type', validators=[DataRequired(), Length(max=50)])
    data_source = StringField('Data source', validators=[DataRequired(), Length(max=200)])
    frequency = StringField('Frequency', validators=[DataRequired(), Length(max=50)])
    owner = StringField('Owner', validators=[DataRequired(), Length(max=120)])
    target_approach = StringField('Target approach', validators=[DataRequired(), Length(max=200)])
    dashboard_level = SelectField('Dashboard level', choices=[('Board + Management', 'Board + Management'), ('Board', 'Board'), ('Management', 'Management')], validators=[DataRequired()])
    is_board_metric = BooleanField('Board metric')
    baseline_value = FloatField('Baseline', validators=[Optional()])
    annual_target = FloatField('Annual target', validators=[Optional()])
    unit_label = StringField('Unit label', validators=[Optional(), Length(max=50)])
    sort_order = IntegerField('Sort order', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Save KPI')


class MonthlyEntryForm(FlaskForm):
    entry_month = DateField('Month', validators=[DataRequired()])
    branch_id = SelectField('Branch', coerce=int, validators=[DataRequired()])
    goal_id = SelectField('Goal', coerce=int, validators=[DataRequired()])
    program_area_id = SelectField('Program area', coerce=int, validators=[DataRequired()])
    service_name = StringField('Service / Program name', validators=[DataRequired(), Length(max=200)])
    audience_group = StringField('Audience group', validators=[Optional(), Length(max=120)])
    partner_name = StringField('Partner name', validators=[Optional(), Length(max=200)])
    multilingual_support = BooleanField('Multilingual support used')
    inclusive_design = BooleanField('Inclusive design / welcoming approach used')
    referral_support = BooleanField('Referral or navigation support provided')
    sessions_offered = IntegerField('Sessions offered', validators=[DataRequired(), NumberRange(min=0)])
    attendance_or_uses = IntegerField('Attendance / uses', validators=[DataRequired(), NumberRange(min=0)])
    unique_users = IntegerField('Unique users', validators=[DataRequired(), NumberRange(min=0)])
    completions = IntegerField('Completions', validators=[DataRequired(), NumberRange(min=0)])
    avg_satisfaction = FloatField('Average satisfaction', validators=[Optional(), NumberRange(min=0, max=5)])
    belonging_gain_pct = FloatField('Belonging gain %', validators=[Optional(), NumberRange(min=0, max=100)])
    ease_of_use_pct = FloatField('Ease-of-use %', validators=[Optional(), NumberRange(min=0, max=100)])
    referrals_made = IntegerField('Referrals made', validators=[DataRequired(), NumberRange(min=0)])
    materials_or_resource_uses = IntegerField('Materials/resource uses', validators=[DataRequired(), NumberRange(min=0)])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save entry')


class KPIActualForm(FlaskForm):
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=2020, max=2100)])
    quarter = SelectField('Quarter', choices=[(q, q) for q in QUARTER_CHOICES], validators=[DataRequired()])
    actual_value = FloatField('Actual value', validators=[Optional()])
    target_value = FloatField('Target value', validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional()])
    submit = SubmitField('Save quarterly update')
