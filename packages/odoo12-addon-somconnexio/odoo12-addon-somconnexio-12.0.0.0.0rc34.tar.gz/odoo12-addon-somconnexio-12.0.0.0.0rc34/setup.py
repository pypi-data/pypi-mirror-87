import setuptools

with open('odoo/addons/somconnexio/README.md') as f:
    long_description = f.read()

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    odoo_addon={
        'depends_override': {
            'account_asset_management': 'odoo12-addon-account-asset-management==12.0.2.3.0',
            'account_financial_report': 'odoo12-addon-account-financial-report==12.0.1.4.1',
            'account_payment_mode': 'odoo12-addon-account-payment-mode==12.0.1.0.1',
            'account_payment_order': 'odoo12-addon-account-payment-order==12.0.1.6.2',
            'account_payment_partner': 'odoo12-addon-account-payment-partner==12.0.1.0.2',
            'easy_my_coop_api': 'odoo12-addon-easy-my-coop-api==12.0.0.0.1.99.dev22',
            'easy_my_coop_es': 'odoo12-addon-easy-my-coop-es==12.0.0.0.14',
            'easy_my_coop_sponsorship': 'odoo12-addon-easy-my-coop-sponsorship==12.0.0.0.0rc1',
            'l10n_es_account_asset': 'odoo12-addon-l10n-es-account-asset==12.0.2.0.6',
            'contract': 'odoo12-addon-contract==12.0.7.3.4',
            'crm_lead_product': 'odoo12-addon-crm-lead-product==12.0.1.0.0.99.dev12',
            'mass_mailing_list_dynamic': 'odoo12-addon-mass-mailing-list-dynamic==12.0.1.0.3',
            'web_favicon': 'odoo12-addon-web-favicon==12.0.1.0.0.99.dev14',
            'web_responsive': 'odoo12-addon-web-responsive==12.0.2.3.2',
            'web_decimal_numpad_dot': 'odoo12-addon-web-decimal-numpad-dot==12.0.1.0.0.99.dev9',
            'web_no_bubble': 'odoo12-addon-web-no-bubble==12.0.1.0.0.99.dev8',
            'web_searchbar_full_width': 'odoo12-addon-web-searchbar-full-width==12.0.1.0.0.99.dev6',
            'partner_firstname': 'odoo12-addon-partner-firstname==12.0.1.1.0',
            'queue_job': 'odoo12-addon-queue-job==12.0.1.5.0',
            'component_event': 'odoo12-addon-component-event==12.0.1.0.0.99.dev11',
            'l10n_es_aeat_mod303': 'odoo12-addon-l10n-es-aeat-mod303==12.0.1.10.0',
            'l10n_es_aeat_mod390': 'odoo12-addon-l10n-es-aeat-mod390==12.0.2.5.0',
            'l10n_es_aeat_mod349': 'odoo12-addon-l10n-es-aeat-mod349==12.0.1.3.0',
            'l10n_es_aeat_mod111': 'odoo12-addon-l10n-es-aeat-mod111==12.0.1.3.1',
            'l10n_es_aeat_mod190': 'odoo12-addon-l10n-es-aeat-mod190==12.0.1.0.0.99.dev2',
            'l10n_es_partner': 'odoo12-addon-l10n-es-partner==12.0.1.0.2',
            'mis_builder': 'odoo12-addon-mis-builder==12.0.3.6.4',
            'mis_builder_budget': 'odoo12-addon-mis-builder-budget==12.0.3.5.0',
            'l10n_es_mis_report': 'odoo12-addon-l10n-es-mis-report==12.0.1.1.0',
            'l10n_es_account_bank_statement_import_n43': 'odoo12-addon-l10n-es-account-bank-statement-import-n43==12.0.1.0.6',
            'account_payment_return': 'odoo12-addon-account-payment-return==12.0.2.1.0',
            'account_banking_sepa_credit_transfer': 'odoo12-addon-account-banking-sepa-credit-transfer==12.0.1.0.0.99.dev11',
            'base_import_async': 'odoo12-addon-base-import-async==12.0.1.0.0.99.dev10',
            'mail_activity_board': 'odoo12-addon-mail-activity-board==12.0.1.0.1',
            'mail_activity_done': 'odoo12-addon-mail-activity-done==12.0.1.1.0',
        },
        'external_dependencies_override': {
            'python': {
                'factory': 'factory-boy'
            },
        },
    },
)
