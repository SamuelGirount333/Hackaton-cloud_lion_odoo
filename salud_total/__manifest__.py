# -*- coding: utf-8 -*-
{
    'name': "salud_total",

    'summary': "Clinica",

    'description': """
    Hackatón
    """,

    'author': "Santiago, Samuel, Christian",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Healthcare',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
        'data': [
        'security/clinic_security.xml',
        'security/ir.model.access.csv',
        'views/clinic_appointment_view.xml',
        'views/clinic_billing_views.xml',
        'views/clinic_clinical_record_views.xml',
        'views/clinic_employee_profile_views.xml',
        'views/clinic_inventory_views.xml',
        'views/clinic_medical_consult_views.xml',
        'views/clinic_medical_test_views.xml',
        'views/clinic_nursing_filter_views.xml',
        'views/clinic_room_assignment_views.xml',
        'views/clinic_surgery_preparation_view.xml',
        'views/clinic_surgery_procedure_view.xml',
        'views/clinic_patient_view.xml',
        'views/clinic_menus.xml'
        ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
