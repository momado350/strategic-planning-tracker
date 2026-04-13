from __future__ import annotations

from datetime import date

from .extensions import db
from .models import Branch, KPIQuarterlyActual, KPIDefinition, MonthlyEntry, ProgramArea, StrategicGoal, StrategicPriority, User


USERS = [
    ('Admin User', 'admin@example.com', 'admin'),
    ('Editor User', 'editor@example.com', 'editor'),
    ('Viewer User', 'viewer@example.com', 'viewer'),
]

BRANCHES = [
    ('Central', 'Urban Core'),
    ('Bluford', 'East'),
    ('Plaza', 'Midtown'),
    ('North-East', 'North'),
    ('Trails West', 'South'),
    ('Sugar Creek', 'East'),
]


PRIORITY_SEEDS = [
    {
        'slug': 'supporting-all-learners',
        'name': 'Supporting All Learners',
        'statement': 'Nurture a love of learning and build foundational skills that empower individuals at every stage of life.',
        'workbook_filename': 'library_supporting_all_learners_kpi_tracker.xlsx',
        'goals': [
            ('Goal 1', 'Support Individual Growth, Resilience, and Empowerment'),
            ('Goal 2', 'Cultivate a Culture of Coordinated, Joyful Learning'),
            ('Goal 3', 'Prioritize Foundational Skills and Networks for Learners'),
        ],
        'program_areas': [
            'Collections & Learning Materials', 'Early Literacy', 'Youth & Family Learning', 'Adult Lifelong Learning',
            'Skill Development & Enrichment', 'Literacy & Reading Engagement', 'Digital Learning, Access & Technology Skills', 'Services for Educators'
        ],
        'kpis': [
            dict(goal='Goal 1', name='Total learning participation', community_need='Access to learning opportunities for all ages, including experiences that are engaging, fun, and accessible', definition='Total attendance across all learner-focused programs and classes during the fiscal year.', measure_type='Output', data_source='Program attendance records', frequency='Quarterly', owner='Programming + data team', target_approach='Increase over baseline', dashboard_level='Board + Management', is_board_metric=True, baseline_value=18500, annual_target=21000, unit_label='participants', sort_order=1),
            dict(goal='Goal 1', name='Unique learners served', community_need='Access to learning opportunities for all ages, including experiences that are engaging, fun, and accessible', definition='Unduplicated count of people participating in learner-focused services during the fiscal year.', measure_type='Reach', data_source='Program registrations and attendance logs', frequency='Quarterly', owner='Data team', target_approach='Increase reach over baseline', dashboard_level='Board + Management', is_board_metric=True, baseline_value=6900, annual_target=7600, unit_label='learners', sort_order=2),
            dict(goal='Goal 3', name='Early literacy participation', community_need='Support for building foundational literacy, core skills, and digital skills', definition='Attendance in early literacy, storytime, and school-readiness programs.', measure_type='Output', data_source='Program attendance records', frequency='Quarterly', owner='Youth and family learning', target_approach='Maintain strong reach and improve access', dashboard_level='Board + Management', is_board_metric=True, baseline_value=4200, annual_target=4700, unit_label='participants', sort_order=3),
            dict(goal='Goal 3', name='Digital literacy participation', community_need='Support for building foundational literacy, core skills, and digital skills', definition='Attendance in digital skills classes, one-on-one tech help, and device learning sessions.', measure_type='Output', data_source='Digital learning logs', frequency='Quarterly', owner='Digital learning + data team', target_approach='Increase over baseline', dashboard_level='Board + Management', is_board_metric=True, baseline_value=1500, annual_target=1900, unit_label='participants', sort_order=4),
            dict(goal='Goal 1', name='Participation in college/career/workforce learning', community_need='Access to college, career, and workforce preparation, including job skills training', definition='Attendance in career, job readiness, mentoring, and college preparation activities.', measure_type='Output', data_source='Program attendance records', frequency='Quarterly', owner='Adult learning + teen services', target_approach='Increase over baseline', dashboard_level='Board + Management', is_board_metric=True, baseline_value=980, annual_target=1250, unit_label='participants', sort_order=5),
            dict(goal='Goal 2', name='Participant satisfaction / engagement', community_need='Access to learning opportunities for all ages, including experiences that are engaging, fun, and accessible', definition='Average participant satisfaction score for learner-focused experiences.', measure_type='Outcome', data_source='Post-program survey', frequency='Quarterly', owner='Programming + data team', target_approach='Maintain high performance', dashboard_level='Board + Management', is_board_metric=True, baseline_value=4.5, annual_target=4.7, unit_label='score', sort_order=6),
            dict(goal='Goal 3', name='Percentage reporting skill or confidence gains', community_need='Support for building foundational literacy, core skills, and digital skills', definition='Percent of surveyed participants who report stronger skills or confidence after participating.', measure_type='Outcome', data_source='Participant survey', frequency='Quarterly', owner='Data team', target_approach='Set baseline and improve', dashboard_level='Board + Management', is_board_metric=True, baseline_value=78, annual_target=85, unit_label='%', sort_order=7),
            dict(goal='Goal 2', name='Active learning partnerships', community_need='Access to diverse books, materials, and technology that support learning', definition='Count of active partner organizations engaged in learner-focused programming or referrals.', measure_type='Capacity', data_source='Partnership log', frequency='Quarterly', owner='Community engagement', target_approach='Maintain and strengthen network', dashboard_level='Board + Management', is_board_metric=True, baseline_value=18, annual_target=24, unit_label='partners', sort_order=8),
        ],
        'quarterly_actuals': {
            'Q1': [4950, 1760, 1110, 420, 280, 4.6, 80, 19],
            'Q2': [5200, 1875, 1160, 455, 302, 4.6, 82, 20],
            'Q3': [5380, 1940, 1205, 498, 325, 4.7, 83, 22],
        },
        'entries': [
            dict(entry_month=date(2026, 7, 1), branch='Central', goal='Goal 1', area='Adult Lifelong Learning', service_name='Career Launch Lab', audience_group='Young adults and job seekers', partner_name='Workforce partnership', multilingual_support=False, inclusive_design=True, referral_support=True, sessions_offered=4, attendance_or_uses=82, unique_users=61, completions=46, avg_satisfaction=4.6, belonging_gain_pct=80, ease_of_use_pct=88, referrals_made=19, materials_or_resource_uses=25, notes='Included resume reviews and mock interviews.'),
            dict(entry_month=date(2026, 8, 1), branch='Bluford', goal='Goal 2', area='Youth & Family Learning', service_name='Family STEM Night', audience_group='Families', partner_name='School district', multilingual_support=False, inclusive_design=True, referral_support=False, sessions_offered=2, attendance_or_uses=96, unique_users=74, completions=0, avg_satisfaction=4.7, belonging_gain_pct=84, ease_of_use_pct=87, referrals_made=2, materials_or_resource_uses=18, notes='Hands-on stations for all ages.'),
            dict(entry_month=date(2026, 9, 1), branch='Trails West', goal='Goal 3', area='Digital Learning, Access & Technology Skills', service_name='Digital Basics Bootcamp', audience_group='Adults', partner_name='Senior center', multilingual_support=True, inclusive_design=True, referral_support=True, sessions_offered=3, attendance_or_uses=58, unique_users=44, completions=37, avg_satisfaction=4.8, belonging_gain_pct=86, ease_of_use_pct=91, referrals_made=11, materials_or_resource_uses=12, notes='Spanish language support provided.'),
        ],
    },
    {
        'slug': 'fostering-community-pride',
        'name': 'Fostering Community Pride',
        'statement': 'Bring people together to celebrate local culture, share community stories, collaborate, and strengthen civic connection.',
        'workbook_filename': 'library_fostering_community_pride_kpi_tracker.xlsx',
        'goals': [
            ('Goal 1', 'Serve as a Trusted Civic Convener'),
            ('Goal 2', 'Celebrate and Preserve Local History and Culture'),
            ('Goal 3', 'Deepen Neighborhood Partnerships and Community Involvement'),
        ],
        'program_areas': [
            'Community Events', 'Exhibitions & Gatherings', 'Arts, Culture, & Civic Programs', 'Local History & Heritage',
            'Cultural Collections', 'Film & Media', 'Street Sheets'
        ],
        'kpis': [
            dict(goal='Goal 1', name='Civic/community dialogue participation', community_need='Access to opportunities for civic participation, community dialogue, and social connection', definition='Total participation in forums, dialogues, civic learning, and community discussion programs.', measure_type='Output', data_source='Program attendance records', frequency='Quarterly', owner='Community engagement', target_approach='Increase over baseline', dashboard_level='Board + Management', is_board_metric=True, baseline_value=2400, annual_target=2900, unit_label='participants', sort_order=1),
            dict(goal='Goal 1', name='Unique participants', community_need='Access to opportunities for civic participation, community dialogue, and social connection', definition='Unduplicated count of people participating in community pride programs.', measure_type='Reach', data_source='Attendance and sign-in records', frequency='Quarterly', owner='Data team', target_approach='Increase over baseline', dashboard_level='Board + Management', is_board_metric=True, baseline_value=1600, annual_target=1900, unit_label='participants', sort_order=2),
            dict(goal='Goal 2', name='Local history participation', community_need='Access to local history and cultural knowledge that reflects the community', definition='Participation in local history, oral history, and heritage-centered programs and exhibitions.', measure_type='Output', data_source='Program attendance + exhibit counts', frequency='Quarterly', owner='Local history team', target_approach='Increase over baseline', dashboard_level='Board + Management', is_board_metric=True, baseline_value=1800, annual_target=2200, unit_label='participants', sort_order=3),
            dict(goal='Goal 2', name='Local history/archive use', community_need='Access to local history and cultural knowledge that reflects the community', definition='Number of archive, local history, or cultural collection uses.', measure_type='Output / Reach', data_source='Archive logs and collection use reports', frequency='Quarterly', owner='Local history + data team', target_approach='Increase over baseline', dashboard_level='Board + Management', is_board_metric=True, baseline_value=1300, annual_target=1650, unit_label='uses', sort_order=4),
            dict(goal='Goal 2', name='Arts/culture/exhibition participation', community_need='Access to arts and cultural programs that amplify local voices', definition='Participation in arts, cultural, film, and exhibition programs that center local voices.', measure_type='Output', data_source='Program attendance records', frequency='Quarterly', owner='Programming + cultural affairs', target_approach='Increase over baseline', dashboard_level='Board + Management', is_board_metric=True, baseline_value=3500, annual_target=4100, unit_label='participants', sort_order=5),
            dict(goal='Goal 1', name='Respectful dialogue rating', community_need='Spaces that support respectful, inclusive dialogue', definition='Percent of surveyed participants who report feeling conversations were respectful and inclusive.', measure_type='Outcome', data_source='Participant survey', frequency='Quarterly', owner='Data team', target_approach='Maintain high performance', dashboard_level='Board + Management', is_board_metric=True, baseline_value=86, annual_target=91, unit_label='%', sort_order=6),
            dict(goal='Goal 2', name='Stronger community/cultural connection', community_need='Access to local history and cultural knowledge that reflects the community', definition='Percent of surveyed participants who report stronger connection to local culture, history, or neighborhood identity.', measure_type='Outcome', data_source='Participant survey', frequency='Quarterly', owner='Data team', target_approach='Set baseline and improve', dashboard_level='Board + Management', is_board_metric=True, baseline_value=74, annual_target=82, unit_label='%', sort_order=7),
            dict(goal='Goal 3', name='Active neighborhood/community partners', community_need='Strong, trusted partnerships to address shared challenges', definition='Count of active neighborhood, civic, and cultural partners engaged in planning or delivery.', measure_type='Capacity', data_source='Partnership log', frequency='Quarterly', owner='Community engagement', target_approach='Strengthen network and shared ownership', dashboard_level='Board + Management', is_board_metric=True, baseline_value=22, annual_target=28, unit_label='partners', sort_order=8),
        ],
        'quarterly_actuals': {
            'Q1': [680, 470, 520, 360, 980, 88, 76, 23],
            'Q2': [720, 510, 548, 398, 1030, 89, 78, 24],
            'Q3': [755, 530, 575, 421, 1095, 90, 79, 26],
        },
        'entries': [
            dict(entry_month=date(2026, 7, 1), branch='Central', goal='Goal 1', area='Community Events', service_name='Neighborhood Issues Forum', audience_group='Adults', partner_name='Civic coalition', multilingual_support=True, inclusive_design=True, referral_support=True, sessions_offered=1, attendance_or_uses=86, unique_users=79, completions=0, avg_satisfaction=4.5, belonging_gain_pct=77, ease_of_use_pct=89, referrals_made=14, materials_or_resource_uses=9, notes='Provided nonpartisan voter information.'),
            dict(entry_month=date(2026, 8, 1), branch='Sugar Creek', goal='Goal 2', area='Local History & Heritage', service_name='Oral History Scan Day', audience_group='All ages', partner_name='Neighborhood association', multilingual_support=True, inclusive_design=True, referral_support=False, sessions_offered=1, attendance_or_uses=63, unique_users=58, completions=24, avg_satisfaction=4.7, belonging_gain_pct=84, ease_of_use_pct=90, referrals_made=1, materials_or_resource_uses=33, notes='Collected family photographs and story submissions.'),
            dict(entry_month=date(2026, 9, 1), branch='Plaza', goal='Goal 3', area='Arts, Culture, & Civic Programs', service_name='Local Voices Film Night', audience_group='Adults and teens', partner_name='Local arts group', multilingual_support=False, inclusive_design=True, referral_support=False, sessions_offered=2, attendance_or_uses=118, unique_users=92, completions=0, avg_satisfaction=4.8, belonging_gain_pct=82, ease_of_use_pct=87, referrals_made=0, materials_or_resource_uses=12, notes='Panel discussion followed screening.'),
        ],
    },
    {
        'slug': 'facilitating-inclusive-experiences',
        'name': 'Facilitating Inclusive Experiences',
        'statement': 'Create community belonging through consistent services, programs, and collections that reflect community needs, interests, and aspirations.',
        'workbook_filename': 'library_facilitating_inclusive_experiences_kpi_tracker.xlsx',
        'goals': [
            ('Goal 1', 'Deliver Consistent, Community-Driven Services'),
            ('Goal 2', 'Create Experiences that are Safe, Welcoming, and Friendly'),
        ],
        'program_areas': [
            'Outreach & Community Access', 'RISE', 'Tap-In Center', 'Language Support', 'Health and Wellness Support',
            'Multilingual & Diverse Collections', 'Library Spaces', 'Technology Services'
        ],
        'kpis': [
            dict(goal='Goal 1', name='Branch compliance with service standards', community_need='Access to consistent, equitable services across all locations', definition='Percent of audited branches meeting core service standards.', measure_type='Quality / Compliance', data_source='Service standards audit', frequency='Quarterly', owner='Operations + branch leadership', target_approach='Reach and sustain target across all branches', dashboard_level='Board + Management', is_board_metric=True, baseline_value=78, annual_target=90, unit_label='%', sort_order=1),
            dict(goal='Goal 1', name='Multilingual communications availability', community_need='Language access and support for multilingual individuals and families', definition='Percentage of high-priority services and communications available in multiple languages.', measure_type='Capacity / Access', data_source='Communications inventory', frequency='Quarterly', owner='Communications + branch leadership', target_approach='Increase over baseline', dashboard_level='Board + Management', is_board_metric=True, baseline_value=42, annual_target=65, unit_label='%', sort_order=2),
            dict(goal='Goal 1', name='Ease of understanding and using services', community_need='Personalized support and guidance that meets people where they are', definition='Percent of surveyed users who say library services were easy to understand and use.', measure_type='Outcome', data_source='Service survey', frequency='Quarterly', owner='Data team', target_approach='Set baseline and improve', dashboard_level='Board + Management', is_board_metric=True, baseline_value=84, annual_target=90, unit_label='%', sort_order=3),
            dict(goal='Goal 2', name='Sense of belonging', community_need='Access to safe, welcoming spaces where everyone feels they belong', definition='Percent of surveyed users who report feeling welcome, respected, and like they belong.', measure_type='Outcome', data_source='Visitor survey', frequency='Quarterly', owner='Data team', target_approach='Set baseline and improve', dashboard_level='Board + Management', is_board_metric=True, baseline_value=81, annual_target=88, unit_label='%', sort_order=4),
            dict(goal='Goal 2', name='Feeling safe and welcome', community_need='Access to safe, welcoming spaces where everyone feels they belong', definition='Percent of surveyed users who report feeling safe and welcome in library spaces.', measure_type='Outcome', data_source='Visitor survey', frequency='Quarterly', owner='Operations + data team', target_approach='Maintain high performance', dashboard_level='Board + Management', is_board_metric=True, baseline_value=87, annual_target=92, unit_label='%', sort_order=5),
            dict(goal='Goal 2', name='Welcoming/accessibility space audit score', community_need='Flexible, accessible spaces that support a wide range of programs and materials', definition='Average score from branch space audits on welcoming design, accessibility, flexibility, and signage.', measure_type='Quality', data_source='Space audit tool', frequency='Quarterly', owner='Facilities + branch leadership', target_approach='Improve branch scores over time', dashboard_level='Board + Management', is_board_metric=True, baseline_value=3.8, annual_target=4.3, unit_label='score', sort_order=6),
            dict(goal='Goal 1', name='Use of multilingual and diverse collections', community_need='Programs, events, and spaces that reflect community interests and experiences', definition='Total checkouts or uses of multilingual and culturally relevant materials.', measure_type='Output / Reach', data_source='ILS and vendor reports', frequency='Quarterly', owner='Collections + data team', target_approach='Increase over baseline', dashboard_level='Board + Management', is_board_metric=True, baseline_value=4200, annual_target=5200, unit_label='uses', sort_order=7),
            dict(goal='Goal 2', name='Services and spaces reflect community aspirations', community_need='Programs, events, and spaces that reflect community interests and experiences', definition='Percent of surveyed users who say programs, collections, or spaces reflect their community interests and lived experiences.', measure_type='Outcome', data_source='Community feedback survey', frequency='Quarterly', owner='Community engagement + data team', target_approach='Set baseline and improve', dashboard_level='Board + Management', is_board_metric=True, baseline_value=73, annual_target=82, unit_label='%', sort_order=8),
        ],
        'quarterly_actuals': {
            'Q1': [82, 48, 86, 83, 89, 4.0, 1280, 76],
            'Q2': [84, 54, 88, 84, 90, 4.1, 1325, 78],
            'Q3': [86, 59, 89, 86, 91, 4.2, 1402, 80],
        },
        'entries': [
            dict(entry_month=date(2026, 7, 1), branch='Central', goal='Goal 1', area='RISE', service_name='RISE Welcome Orientation', audience_group='Refugee and immigrant families', partner_name='Community partner coalition', multilingual_support=True, inclusive_design=True, referral_support=True, sessions_offered=3, attendance_or_uses=61, unique_users=48, completions=45, avg_satisfaction=4.7, belonging_gain_pct=92, ease_of_use_pct=94, referrals_made=17, materials_or_resource_uses=21, notes='Arabic and Spanish interpretation available.'),
            dict(entry_month=date(2026, 8, 1), branch='Bluford', goal='Goal 2', area='Library Spaces', service_name='Calm Space Open House', audience_group='All ages', partner_name=None, multilingual_support=False, inclusive_design=True, referral_support=False, sessions_offered=2, attendance_or_uses=74, unique_users=67, completions=0, avg_satisfaction=4.6, belonging_gain_pct=88, ease_of_use_pct=86, referrals_made=3, materials_or_resource_uses=14, notes='Included sensory-friendly hours.'),
            dict(entry_month=date(2026, 9, 1), branch='Plaza', goal='Goal 1', area='Language Support', service_name='Multilingual Service Navigation Clinic', audience_group='Multilingual adults', partner_name='Health consortium', multilingual_support=True, inclusive_design=True, referral_support=True, sessions_offered=4, attendance_or_uses=53, unique_users=41, completions=38, avg_satisfaction=4.8, belonging_gain_pct=90, ease_of_use_pct=95, referrals_made=22, materials_or_resource_uses=11, notes='Provided printed translations and live support.'),
        ],
    },
]


def seed_demo_data(force: bool = False) -> None:
    if force:
        db.drop_all()
        db.create_all()

    users = ensure_users()
    admin = users['admin@example.com']
    editor = users['editor@example.com']

    branches = ensure_branches()

    if StrategicPriority.query.count() >= len(PRIORITY_SEEDS) and KPIDefinition.query.count() >= 24:
        return

    for spec in PRIORITY_SEEDS:
        if StrategicPriority.query.filter_by(slug=spec['slug']).first():
            continue
        seed_priority(spec, branches, admin, editor)

    db.session.commit()


def ensure_users() -> dict[str, User]:
    result: dict[str, User] = {}
    for full_name, email, role in USERS:
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(full_name=full_name, email=email, role=role)
            user.set_password('password123')
            db.session.add(user)
            db.session.flush()
        result[email] = user
    return result


def ensure_branches() -> dict[str, Branch]:
    result: dict[str, Branch] = {}
    for name, region in BRANCHES:
        branch = Branch.query.filter_by(name=name).first()
        if not branch:
            branch = Branch(name=name, region=region, active=True)
            db.session.add(branch)
            db.session.flush()
        result[name] = branch
    return result


def seed_priority(spec: dict, branches: dict[str, Branch], admin: User, editor: User) -> None:
    priority = StrategicPriority(
        slug=spec['slug'],
        name=spec['name'],
        statement=spec['statement'],
        workbook_filename=spec['workbook_filename'],
    )
    db.session.add(priority)
    db.session.flush()

    goals_by_code: dict[str, StrategicGoal] = {}
    for idx, (code, title) in enumerate(spec['goals'], start=1):
        goal = StrategicGoal(priority_id=priority.id, code=code, title=title, description=title)
        db.session.add(goal)
        db.session.flush()
        goals_by_code[code] = goal

    areas_by_name: dict[str, ProgramArea] = {}
    for area_name in spec['program_areas']:
        area = ProgramArea(priority_id=priority.id, name=area_name, description=area_name)
        db.session.add(area)
        db.session.flush()
        areas_by_name[area_name] = area

    kpis: list[KPIDefinition] = []
    for item in spec['kpis']:
        kpi = KPIDefinition(
            priority_id=priority.id,
            goal_id=goals_by_code[item['goal']].id,
            name=item['name'],
            community_need=item['community_need'],
            definition=item['definition'],
            measure_type=item['measure_type'],
            data_source=item['data_source'],
            frequency=item['frequency'],
            owner=item['owner'],
            target_approach=item['target_approach'],
            dashboard_level=item['dashboard_level'],
            is_board_metric=item['is_board_metric'],
            baseline_value=item['baseline_value'],
            annual_target=item['annual_target'],
            unit_label=item['unit_label'],
            sort_order=item['sort_order'],
        )
        db.session.add(kpi)
        db.session.flush()
        kpis.append(kpi)

    for quarter, values in spec['quarterly_actuals'].items():
        for idx, kpi in enumerate(kpis):
            actual = KPIQuarterlyActual(
                kpi_id=kpi.id,
                year=2026,
                quarter=quarter,
                actual_value=values[idx],
                target_value=kpi.annual_target,
                updated_by=admin,
            )
            actual.sync_status()
            db.session.add(actual)

    for item in spec['entries']:
        entry = MonthlyEntry(
            priority_id=priority.id,
            entry_month=item['entry_month'],
            branch=branches[item['branch']],
            goal=goals_by_code[item['goal']],
            program_area=areas_by_name[item['area']],
            service_name=item['service_name'],
            audience_group=item['audience_group'],
            partner_name=item['partner_name'],
            multilingual_support=item['multilingual_support'],
            inclusive_design=item['inclusive_design'],
            referral_support=item['referral_support'],
            sessions_offered=item['sessions_offered'],
            attendance_or_uses=item['attendance_or_uses'],
            unique_users=item['unique_users'],
            completions=item['completions'],
            avg_satisfaction=item['avg_satisfaction'],
            belonging_gain_pct=item['belonging_gain_pct'],
            ease_of_use_pct=item['ease_of_use_pct'],
            referrals_made=item['referrals_made'],
            materials_or_resource_uses=item['materials_or_resource_uses'],
            notes=item['notes'],
            entered_by=editor,
        )
        db.session.add(entry)
