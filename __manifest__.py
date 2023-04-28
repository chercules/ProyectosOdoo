# -*- coding: utf-8 -*-
{
    'name': "Activo Fijo SV",

    'summary': """
        Control de Activo Fijo para El Salvador""",

    'description': """
        Controla los activo de la empresa  conforme a la ley vigente en El Salvador Abril 2018
    """,

    'author': "Carlos Hercules",
    'website': "http://www.lamorazan.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Control de Activos',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizard/wizard_activo_reporte.xml',
        'reportes/rep_activos.xml',
        'reportes/comprobante.xml',
        'reportes/rep_all_activos.xml',
        'reportes/rep_all_activos_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
