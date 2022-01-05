{
    'name': 'TechbotErp Sports Management System ',
    'version': '15.0.1.0.4',
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
    'depends': ['base', 'stock', 'hr', 'account', 'crm', 'sale_management', 'account_accountant'],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        # 'views/crm_lead_views.xml',
        # 'views/sports_management_views.xml',
        'views/employee_views.xml',
        'views/product_views.xml',
        'views/sale_order_views.xml',

        'views/student_details_view.xml',
        'views/res_partner_view.xml',
        'views/techboterp_menu_views.xml',

        # 'views/faculty_details_views.xml',
        # 'views/sports_management_action_views.xml',

        # 'views/students_class_view.xml',
        # 'views/sports_location_view.xml',
        # 'views/sports_session_view.xml',
        # 'views/sports_session_attendance_view.xml',

    ],
    # 'demo': ['demo/school_demo.xml'],
    'installable': True,
    'auto_install': False,
    'application': True,
}
