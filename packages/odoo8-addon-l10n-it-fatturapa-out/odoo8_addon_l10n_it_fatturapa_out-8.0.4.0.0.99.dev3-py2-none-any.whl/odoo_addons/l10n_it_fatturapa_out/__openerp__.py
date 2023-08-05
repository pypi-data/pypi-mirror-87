# -*- coding: utf-8 -*-
# Copyright 2014 Davide Corio
# Copyright 2015-2016 Lorenzo Battistini - Agile Business Group
# Copyright 2018 Gianmarco Conte, Marco Calcagni - Dinamiche Aziendali srl
# Copyright 2018-2019 Sergio Corato
# Copyright 2018 Sergio Zanchetta (Associazione PNLUG - Gruppo Odoo)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Italian Localization - Fattura elettronica - Emissione',
    'version': '8.0.4.0.0',
    'category': 'Localization/Italy',
    'summary': 'Electronic invoices emission',
    'author': 'Davide Corio, Agile Business Group, Innoviu,'
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/l10n-italy/tree/8.0/'
               'l10n_it_fatturapa_out',
    'license': 'LGPL-3',
    "depends": [
        'l10n_it_account',
        'l10n_it_fatturapa',
        'l10n_it_split_payment',
        ],
    "data": [
        'wizard/wizard_export_fatturapa_view.xml',
        'views/attachment_view.xml',
        'views/account_view.xml',
        'security/ir.model.access.csv',
        'security/rules.xml',
        'data/l10n_it_fatturapa_out_data.xml'
    ],
    'installable': True,
    'external_dependencies': {
        'python': ['unidecode'],
    }
}
