{
    'name': 'Sports Management System V15',
    'version': '15.0.1.0.1',
    'summary': 'A module for Manage Complete Sports Activities  ',
    'description': 'Sports  Management System Enterprise version15',
    'category': 'Tools',
    'author': 'TecbotERp',
    'website': "https://techboterp.com",
    'company': 'TechbotErp',
    'license': 'LGPL-3',
    'complexity': 'easy',
    'sequence': '-100',
    'images': [],
    # 'static/description/EMS.jpg'
    'depends': ['base', 'hr', 'crm', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        # 'report/fleet_report.xml',
        # 'report/fleet_report_templates.xml',
        # 'data/fleet_mail_template_data.xml',
        # 'data/ir_sequence_data.xml',
        # 'report/job_card.xml',
        # 'report/job_card_template.xml',
        'views/sports_management_views.xml',
        'views/student_details_view.xml',
        'views/res_partner_view.xml',
        'views/faculty_details_views.xml',
        'views/sports_management_action_views.xml',
        'views/sports_management_menu_views.xml',
        'views/sports_location_view.xml',
        'views/sports_session_view.xml'

        # 'views/fleet_view.xml',

        # 'security/workshop_security.xml',

    ],
    # 'demo': ['demo/school_demo.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
