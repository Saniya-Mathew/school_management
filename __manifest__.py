{
    'name': "School Management",
    'version': '1.0',
    'depends': ['base','mail','sale', 'web'],
    'author': "San",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/school_user_groups.xml',
        'security/school_security.xml',
        'security/ir.model.access.csv',
        'data/school_department_data.xml',
        'data/school_class_data.xml',
        'data/school_subject_data.xml',
        'data/ir_sequence_data.xml',
        'data/mail_tempalate_data.xml',
        'data/ir_cron_data.xml',
        'data/ir_action_data.xml',
        'views/sale_order_view.xml',
        'views/registration_view.xml',
        'views/department_view.xml',
        'views/class_view.xml',
        'views/subject_view.xml',
        'views/academic_year_view.xml',
        'views/club_view.xml',
        'views/event_view.xml',
        'views/school_teacher_view.xml',
        'views/school_leave_views.xml',
        'views/school_exam_view.xml',
        'report/ir_actions_report.xml',
        'report/leave_report_template.xml',
        'report/student_report_template.xml',
        'wizard/student_inform.xml',
        'wizard/student_leave.xml',
        'views/school_management_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'school/static/src/js/action_manager.js'
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 1,

}
