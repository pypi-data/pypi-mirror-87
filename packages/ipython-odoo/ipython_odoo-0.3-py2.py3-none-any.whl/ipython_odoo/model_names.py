CONVERT_ENV_KEYS = {
    # account
    'account.abstract.payment': 'abstract_payment',  # account.payment, pos.make.payment
    'account.account': 'account',                    # account.analytic.account, account.fiscal.position.account, hr_timesheet_sheet.sheet.account
    'account.account.tag': 'account_tag',
    'account.account.template': 'account_template',
    'account.account.type': 'account_type',
    'account.aged.trial.balance': 'aged_trial_balance',
    'account.balance.report': 'balance_report',
    'account.bank.accounts.wizard': 'bank_accounts_wizard',
    'account.bank.statement': 'bank_statement',      # pos.open.statement
    'account.bank.statement.cashbox': 'bank_statement_cashbox',
    'account.bank.statement.closebalance': 'bank_statement_closebalance',
    'account.bank.statement.line': 'bank_statement_line',
    'account.cashbox.line': 'cashbox_line',
    'account.chart.template': 'chart_template',
    'account.common.account.report': 'account_report',
    'account.common.journal.report': 'journal_report',
    'account.common.partner.report': 'partner_report',
    'account.common.report': 'common_report',
    'account.config.settings': 'account_config_settings',
    'account.financial.report': 'financial_report',
    'account.fiscal.position': 'fiscal_position',
    'account.fiscal.position.account': 'fiscal_position_account',  # account.account, account.analytic.account, hr_timesheet_sheet.sheet.account
    'account.fiscal.position.account.template': 'fiscal_position_account_template',
    'account.fiscal.position.tax': 'fiscal_position_tax',  # account.invoice.tax, account.tax
    'account.fiscal.position.tax.template': 'position_tax_template',
    'account.fiscal.position.template': 'position_template',
    'account.full.reconcile': 'full_reconcile',      # account.move.line.reconcile, account.partial.reconcile
    'account.invoice': 'invoice',                    # membership.invoice
    'account.invoice.cancel': 'invoice_cancel',      # mrp.repair.cancel
    'account.invoice.confirm': 'invoice_confirm',    # event.confirm
    'account.invoice.line': 'invoice_line',
    'account.invoice.refund': 'invoice_refund',
    'account.invoice.report': 'invoice_report',
    'account.invoice.tax': 'invoice_tax',            # account.fiscal.position.tax, account.tax
    'account.journal': 'journal',                    # account.print.journal
    'account.move': 'account_move',                  # stock.move, validate.account.move
    'account.move.line': 'move_line',
    'account.move.line.reconcile': 'move_line_reconcile',  # account.full.reconcile, account.partial.reconcile
    'account.move.line.reconcile.writeoff': 'move_line_reconcile_writeoff',
    'account.move.reversal': 'move_reversal',
    'account.partial.reconcile': 'partial_reconcile',  # account.full.reconcile, account.move.line.reconcile
    'account.payment': 'payment',                    # account.abstract.payment, pos.make.payment
    'account.payment.method': 'payment_method',
    'account.payment.term': 'payment_term',
    'account.payment.term.line': 'payment_term_line',
    'account.print.journal': 'print_journal',        # account.journal
    'account.reconcile.model': 'reconcile_model',    # ir.model
    'account.reconcile.model.template': 'model_template',
    'account.register.payments': 'register_payments',
    'account.report.general.ledger': 'report_general_ledger',  # account.report.partner.ledger
    'account.report.partner.ledger': 'report_partner_ledger',  # account.report.general.ledger
    'account.tax': 'tax',                            # account.fiscal.position.tax, account.invoice.tax
    'account.tax.group': 'tax_group',                # procurement.group, res.country.group
    'account.tax.template': 'account_tax_template',
    'account.unreconcile': 'unreconcile',
    'accounting.report': 'accounting_report',
    'cash.box.in': 'box_in',
    'cash.box.out': 'box_out',
    'report.account.report_agedpartnerbalance': 'account_report_agedpartnerbalance',
    'report.account.report_financial': 'account_report_financial',
    'report.account.report_generalledger': 'account_report_generalledger',
    'report.account.report_journal': 'account_report_journal',
    'report.account.report_overdue': 'account_report_overdue',
    'report.account.report_partnerledger': 'account_report_partnerledger',
    'report.account.report_trialbalance': 'account_report_trialbalance',
    'tax.adjustments.wizard': 'adjustments_wizard',
    'validate.account.move': 'validate_account_move',  # account.move, stock.move
    'wizard.multi.charts.accounts': 'multi_charts_accounts',

    # account_analytic_default
    'account.analytic.default': 'analytic_default',

    # account_asset
    'account.asset.asset': 'asset_asset',
    'account.asset.category': 'asset_category',
    'account.asset.depreciation.line': 'asset_depreciation_line',
    'asset.asset.report': 'asset_report',
    'asset.depreciation.confirmation.wizard': 'depreciation_confirmation_wizard',
    'asset.modify': 'modify',

    # account_bank_statement_import
    'account.bank.statement.import': 'bank_statement_import',  # base.language.import, base_import.import
    'account.bank.statement.import.journal.creation': 'bank_statement_import_journal_creation',

    # account_budget
    'account.budget.post': 'budget_post',            # blog.post, forum.post
    'crossovered.budget': 'budget',
    'crossovered.budget.lines': 'budget_lines',      # ir.server.object.lines, stock.landed.cost.lines, stock.valuation.adjustment.lines

    # account_check_printing
    'print.prenumbered.checks': 'prenumbered_checks',

    # account_voucher
    'account.voucher': 'voucher',
    'account.voucher.line': 'voucher_line',

    # analytic
    'account.analytic.account': 'analytic_account',  # account.account, account.fiscal.position.account, hr_timesheet_sheet.sheet.account
    'account.analytic.line': 'analytic_line',
    'account.analytic.tag': 'analytic_tag',

    # anonymization
    'ir.model.fields.anonymization': 'model_fields_anonymization',
    'ir.model.fields.anonymization.history': 'model_fields_anonymization_history',
    'ir.model.fields.anonymization.migration.fix': 'model_fields_anonymization_migration_fix',
    'ir.model.fields.anonymize.wizard': 'model_fields_anonymize_wizard',

    # auth_ldap
    'res.company.ldap': 'company_ldap',

    # auth_oauth
    'auth.oauth.provider': 'oauth_provider',

    # barcodes
    'barcode.nomenclature': 'nomenclature',
    'barcode.rule': 'barcode_rule',
    'barcodes.barcode_events_mixin': 'barcode_events_mixin',

    # base
    '_unknown': '_unknown',
    'base': 'base',
    'base.language.export': 'language_export',
    'base.language.import': 'language_import',       # account.bank.statement.import, base_import.import
    'base.language.install': 'language_install',
    'base.module.configuration': 'module_configuration',  # pos_mercury.configuration
    'base.module.update': 'module_update',
    'base.module.upgrade': 'module_upgrade',
    'base.update.translations': 'update_translations',  # base.gengo.translations
    'change.password.user': 'password_user',
    'change.password.wizard': 'password_wizard',
    'ir.actions.act_url': 'act_url',
    'ir.actions.act_window': 'act_window',
    'ir.actions.act_window.view': 'act_window_view',  # ir.ui.view
    'ir.actions.act_window_close': 'act_window_close',
    'ir.actions.actions': 'actions',
    'ir.actions.client': 'client',
    'ir.actions.report.xml': 'report_xml',
    'ir.actions.server': 'server',                   # fetchmail.server
    'ir.actions.todo': 'todo',
    'ir.attachment': 'attachment',
    'ir.autovacuum': 'autovacuum',
    'ir.config_parameter': 'config_parameter',
    'ir.cron': 'cron',
    'ir.exports': 'exports',
    'ir.exports.line': 'exports_line',
    'ir.fields.converter': 'fields_converter',
    'ir.filters': 'filters',
    'ir.http': 'http',
    'ir.logging': 'logging',
    'ir.mail_server': 'mail_server',
    'ir.model': 'model',                             # account.reconcile.model
    'ir.model.access': 'access',
    'ir.model.constraint': 'model_constraint',
    'ir.model.data': 'model_data',
    'ir.model.fields': 'fields',                     # subscription.document.fields
    'ir.model.relation': 'model_relation',
    'ir.module.category': 'module_category',
    'ir.module.module': 'module',                    # base.import.module
    'ir.module.module.dependency': 'module_dependency',
    'ir.needaction_mixin': 'needaction_mixin',
    'ir.property': 'prop',
    'ir.qweb': 'qweb',                               # ir.qweb.field.qweb
    'ir.qweb.field': 'qweb_field',
    'ir.qweb.field.contact': 'qweb_field_contact',   # mail.mass_mailing.contact
    'ir.qweb.field.date': 'qweb_field_date',         # report.stock.lines.date
    'ir.qweb.field.datetime': 'qweb_field_datetime',
    'ir.qweb.field.duration': 'qweb_field_duration',
    'ir.qweb.field.float': 'qweb_field_float',
    'ir.qweb.field.html': 'qweb_field_html',
    'ir.qweb.field.image': 'qweb_field_image',       # product.image
    'ir.qweb.field.integer': 'qweb_field_integer',
    'ir.qweb.field.many2one': 'qweb_field_many2one',
    'ir.qweb.field.monetary': 'qweb_field_monetary',
    'ir.qweb.field.qweb': 'qweb_field_qweb',         # ir.qweb
    'ir.qweb.field.relative': 'qweb_field_relative',
    'ir.qweb.field.selection': 'qweb_field_selection',
    'ir.qweb.field.text': 'qweb_field_text',
    'ir.rule': 'rule',
    'ir.sequence': 'sequence',
    'ir.sequence.date_range': 'sequence_date_range',
    'ir.server.object.lines': 'server_object_lines',  # crossovered.budget.lines, stock.landed.cost.lines, stock.valuation.adjustment.lines
    'ir.translation': 'translation',
    'ir.ui.menu': 'menu',                            # website.menu
    'ir.ui.view': 'view',                            # ir.actions.act_window.view
    'ir.ui.view.custom': 'view_custom',
    'ir.values': 'values',
    'report.base.report_irmodulereference': 'base_report_irmodulereference',
    'res.bank': 'bank',                              # res.partner.bank
    'res.company': 'company',
    'res.config': 'config',                          # google.drive.config, pos.config
    'res.config.installer': 'config_installer',
    'res.config.settings': 'config_settings',
    'res.country': 'country',
    'res.country.group': 'country_group',            # account.tax.group, procurement.group
    'res.country.state': 'country_state',
    'res.currency': 'currency',
    'res.currency.rate': 'currency_rate',
    'res.font': 'font',
    'res.groups': 'groups',
    'res.lang': 'lang',
    'res.partner': 'partner',                        # crm.lead.forward.to.partner, crm.lead2opportunity.partner, mail.channel.partner
    'res.partner.bank': 'partner_bank',              # res.bank
    'res.partner.category': 'partner_category',
    'res.partner.title': 'partner_title',
    'res.request.link': 'request_link',              # stock.move.operation.link
    'res.users': 'users',
    'res.users.log': 'users_log',                    # crm.activity.log
    'wizard.ir.model.menu.create': 'ir_model_menu_create',
    'workflow': 'workflow',
    'workflow.activity': 'workflow_activity',        # crm.activity, marketing.campaign.activity
    'workflow.instance': 'instance',
    'workflow.transition': 'transition',             # marketing.campaign.transition
    'workflow.triggers': 'triggers',
    'workflow.workitem': 'workitem',                 # marketing.campaign.workitem

    # base_action_rule
    'base.action.rule': 'action_rule',

    # base_gengo
    'base.gengo.translations': 'gengo_translations',  # base.update.translations

    # base_import
    'base_import.import': 'import',                  # account.bank.statement.import, base.language.import

    # base_import_module
    'base.import.module': 'import_module',           # ir.module.module

    # base_setup
    'base.config.settings': 'base_config_settings',

    # bus
    'bus.bus': 'bus',
    'bus.presence': 'presence',

    # calendar
    'calendar.alarm': 'alarm',
    'calendar.alarm_manager': 'alarm_manager',
    'calendar.attendee': 'attendee',
    'calendar.contacts': 'contacts',
    'calendar.event': 'calendar_event',              # event.event
    'calendar.event.type': 'event_type',

    # crm
    'base.partner.merge.automatic.wizard': 'partner_merge_automatic_wizard',
    'base.partner.merge.line': 'partner_merge_line',
    'crm.activity': 'crm_activity',                  # marketing.campaign.activity, workflow.activity
    'crm.activity.log': 'activity_log',              # res.users.log
    'crm.activity.report': 'activity_report',
    'crm.lead': 'lead',
    'crm.lead.lost': 'lead_lost',
    'crm.lead.tag': 'lead_tag',
    'crm.lead2opportunity.partner': 'lead2opportunity_partner',  # crm.lead.forward.to.partner, mail.channel.partner, res.partner
    'crm.lead2opportunity.partner.mass': 'lead2opportunity_partner_mass',
    'crm.lost.reason': 'lost_reason',                # forum.post.reason
    'crm.merge.opportunity': 'merge_opportunity',
    'crm.opportunity.report': 'opportunity_report',
    'crm.partner.binding': 'partner_binding',
    'crm.stage': 'crm_stage',

    # decimal_precision
    'decimal.precision': 'precision',

    # delivery
    'delivery.carrier': 'carrier',
    'delivery.price.rule': 'price_rule',

    # event
    'event.config.settings': 'event_config_settings',
    'event.confirm': 'confirm',                      # account.invoice.confirm
    'event.event': 'event',                          # calendar.event
    'event.mail': 'event_mail',                      # mail.mail
    'event.mail.registration': 'mail_registration',  # event.registration, report.event.registration
    'event.registration': 'registration',            # event.mail.registration, report.event.registration
    'event.type': 'type',
    'report.event.registration': 'event_registration',  # event.mail.registration, event.registration

    # event_sale
    'event.event.ticket': 'event_ticket',
    'registration.editor': 'editor',
    'registration.editor.line': 'editor_line',

    # fetchmail
    'fetchmail.server': 'fetchmail_server',          # ir.actions.server

    # gamification
    'gamification.badge': 'badge',
    'gamification.badge.user': 'badge_user',
    'gamification.badge.user.wizard': 'badge_user_wizard',
    'gamification.challenge': 'challenge',
    'gamification.challenge.line': 'challenge_line',
    'gamification.goal': 'goal',
    'gamification.goal.definition': 'goal_definition',
    'gamification.goal.wizard': 'goal_wizard',

    # google_account
    'google.service': 'service',

    # google_drive
    'google.drive.config': 'drive_config',           # pos.config, res.config

    # hr
    'hr.department': 'department',
    'hr.employee': 'employee',                       # hr.holidays.summary.employee
    'hr.employee.category': 'employee_category',
    'hr.job': 'job',

    # hr_attendance
    'hr.attendance': 'attendance',                   # resource.calendar.attendance

    # hr_contract
    'hr.contract': 'hr_contract',                    # publisher_warranty.contract
    'hr.contract.type': 'contract_type',

    # hr_expense
    'hr.expense': 'expense',
    'hr.expense.config.settings': 'expense_config_settings',
    'hr.expense.refuse.wizard': 'expense_refuse_wizard',
    'hr.expense.register.payment.wizard': 'expense_register_payment_wizard',
    'hr.expense.sheet': 'expense_sheet',             # hr_timesheet_sheet.sheet

    # hr_holidays
    'hr.holidays': 'holidays',
    'hr.holidays.remaining.leaves.user': 'holidays_remaining_leaves_user',
    'hr.holidays.status': 'holidays_status',
    'hr.holidays.summary.dept': 'holidays_summary_dept',
    'hr.holidays.summary.employee': 'holidays_summary_employee',  # hr.employee
    'report.hr_holidays.report_holidayssummary': 'hr_holidays_report_holidayssummary',

    # hr_payroll
    'hr.contribution.register': 'contribution_register',  # payslip.lines.contribution.register
    'hr.payroll.config.settings': 'payroll_config_settings',
    'hr.payroll.structure': 'payroll_structure',
    'hr.payslip': 'payslip',
    'hr.payslip.employees': 'payslip_employees',
    'hr.payslip.input': 'payslip_input',             # hr.rule.input
    'hr.payslip.line': 'payslip_line',
    'hr.payslip.run': 'payslip_run',
    'hr.payslip.worked_days': 'payslip_worked_days',
    'hr.rule.input': 'rule_input',                   # hr.payslip.input
    'hr.salary.rule': 'salary_rule',
    'hr.salary.rule.category': 'rule_category',
    'payslip.lines.contribution.register': 'lines_contribution_register',  # hr.contribution.register
    'report.hr_payroll.report_contributionregister': 'hr_payroll_report_contributionregister',
    'report.hr_payroll.report_payslipdetails': 'hr_payroll_report_payslipdetails',

    # hr_recruitment
    'hr.applicant': 'applicant',
    'hr.applicant.category': 'applicant_category',
    'hr.recruitment.config.settings': 'recruitment_config_settings',
    'hr.recruitment.degree': 'recruitment_degree',
    'hr.recruitment.report': 'recruitment_report',
    'hr.recruitment.source': 'recruitment_source',   # utm.source
    'hr.recruitment.stage': 'recruitment_stage',

    # hr_timesheet_attendance
    'hr.timesheet.attendance.report': 'attendance_report',
    'hr_timesheet_sheet.sheet.day': 'sheet_day',

    # hr_timesheet_sheet
    'hr.timesheet.current.open': 'timesheet_current_open',
    'hr_timesheet_sheet.sheet': 'sheet',             # hr.expense.sheet
    'hr_timesheet_sheet.sheet.account': 'sheet_account',  # account.account, account.analytic.account, account.fiscal.position.account

    # im_livechat
    'im_livechat.channel': 'im_livechat_channel',    # im_livechat.report.channel, mail.channel, slide.channel
    'im_livechat.channel.rule': 'channel_rule',
    'im_livechat.report.channel': 'report_channel',  # im_livechat.channel, mail.channel, slide.channel
    'im_livechat.report.operator': 'report_operator',

    # link_tracker
    'link.tracker': 'tracker',
    'link.tracker.click': 'tracker_click',
    'link.tracker.code': 'tracker_code',             # report.intrastat.code

    # lunch
    'lunch.alert': 'alert',
    'lunch.cashmove': 'cashmove',
    'lunch.order': 'lunch',
    'lunch.order.line': 'lunch_line',
    'lunch.order.line.lucky': 'lunch_line_lucky',
    'lunch.product': 'lunch_product',                # product.product
    'lunch.product.category': 'lunch_product_category',

    # mail
    'email_template.preview': 'preview',
    'mail.alias': 'alias',
    'mail.alias.mixin': 'alias_mixin',               # rating.mixin, utm.mixin, website.published.mixin
    'mail.channel': 'mail_channel',                  # im_livechat.channel, im_livechat.report.channel, slide.channel
    'mail.channel.partner': 'channel_partner',       # crm.lead.forward.to.partner, crm.lead2opportunity.partner, res.partner
    'mail.compose.message': 'mail_compose_message',  # mail.message, mrp.message, survey.mail.compose.message
    'mail.followers': 'followers',
    'mail.mail': 'mail',                             # event.mail
    'mail.message': 'mail_message',                  # mail.compose.message, mrp.message, survey.mail.compose.message
    'mail.message.subtype': 'message_subtype',
    'mail.notification': 'notification',
    'mail.shortcode': 'shortcode',
    'mail.template': 'mail_template',
    'mail.thread': 'thread',
    'mail.tracking.value': 'tracking_value',         # product.attribute.value
    'mail.wizard.invite': 'wizard_invite',
    'publisher_warranty.contract': 'publisher_warranty_contract',  # hr.contract

    # maintenance
    'maintenance.equipment': 'equipment',
    'maintenance.equipment.category': 'equipment_category',
    'maintenance.request': 'request',
    'maintenance.stage': 'maintenance_stage',
    'maintenance.team': 'maintenance_team',          # crm.team

    # marketing_campaign
    'campaign.analysis': 'analysis',
    'marketing.campaign': 'marketing_campaign',      # mail.mass_mailing.campaign, utm.campaign
    'marketing.campaign.activity': 'campaign_activity',  # crm.activity, workflow.activity
    'marketing.campaign.segment': 'campaign_segment',
    'marketing.campaign.transition': 'campaign_transition',  # workflow.transition
    'marketing.campaign.workitem': 'campaign_workitem',  # workflow.workitem

    # mass_mailing
    'mail.mail.statistics': 'mail_statistics',
    'mail.mass_mailing': 'mass_mailing',
    'mail.mass_mailing.campaign': 'mass_mailing_campaign',  # marketing.campaign, utm.campaign
    'mail.mass_mailing.contact': 'mass_mailing_contact',  # ir.qweb.field.contact
    'mail.mass_mailing.list': 'mass_mailing_list',
    'mail.mass_mailing.stage': 'mass_mailing_stage',
    'mail.mass_mailing.tag': 'mass_mailing_tag',
    'mail.statistics.report': 'statistics_report',
    'mass.mailing.config.settings': 'mailing_config_settings',

    # membership
    'membership.invoice': 'membership_invoice',      # account.invoice
    'membership.membership_line': 'membership_line',
    'report.membership': 'membership',

    # mrp
    'change.production.qty': 'production_qty',       # stock.change.product.qty
    'mrp.bom': 'bom',
    'mrp.bom.line': 'bom_line',
    'mrp.config.settings': 'mrp_config_settings',
    'mrp.message': 'mrp_message',                    # mail.compose.message, mail.message, survey.mail.compose.message
    'mrp.product.produce': 'product_produce',
    'mrp.production': 'production',
    'mrp.routing': 'routing',
    'mrp.routing.workcenter': 'routing_workcenter',  # mrp.workcenter
    'mrp.unbuild': 'unbuild',
    'mrp.workcenter': 'workcenter',                  # mrp.routing.workcenter
    'mrp.workcenter.productivity': 'workcenter_productivity',
    'mrp.workcenter.productivity.loss': 'workcenter_productivity_loss',
    'mrp.workorder': 'workorder',
    'report.mrp.report_mrpbomstructure': 'mrp_report_mrpbomstructure',
    'report.mrp_bom_cost': 'mrp_bom_cost',
    'stock.move.lots': 'move_lots',

    # mrp_byproduct
    'mrp.subproduct': 'subproduct',

    # mrp_repair
    'mrp.repair': 'repair',
    'mrp.repair.cancel': 'repair_cancel',            # account.invoice.cancel
    'mrp.repair.fee': 'repair_fee',
    'mrp.repair.line': 'repair_line',
    'mrp.repair.make_invoice': 'repair_make_invoice',

    # note
    'note.note': 'note',
    'note.stage': 'note_stage',
    'note.tag': 'note_tag',

    # pad
    'pad.common': 'common',

    # payment
    'payment.acquirer': 'acquirer',
    'payment.token': 'token',
    'payment.transaction': 'transaction',

    # point_of_sale
    'pos.category': 'pos_category',
    'pos.config': 'pos_config',                      # google.drive.config, res.config
    'pos.config.settings': 'pos_config_settings',
    'pos.details.wizard': 'details_wizard',
    'pos.discount': 'discount',
    'pos.make.payment': 'make_payment',              # account.abstract.payment, account.payment
    'pos.open.statement': 'open_statement',          # account.bank.statement
    'pos.order': 'pos_order',
    'pos.order.line': 'pos_order_line',
    'pos.pack.operation.lot': 'pos_pack_operation_lot',  # stock.pack.operation.lot, stock.production.lot
    'pos.session': 'session',
    'report.point_of_sale.report_invoice': 'point_of_sale_report_invoice',
    'report.point_of_sale.report_saledetails': 'point_of_sale_report_saledetails',
    'report.pos.order': 'report_pos_order',

    # portal
    'portal.wizard': 'wizard',
    'portal.wizard.user': 'wizard_user',

    # pos_cache
    'pos.cache': 'cache',

    # pos_mercury
    'pos_mercury.configuration': 'configuration',    # base.module.configuration
    'pos_mercury.mercury_transaction': 'mercury_transaction',

    # pos_restaurant
    'restaurant.floor': 'floor',
    'restaurant.printer': 'printer',
    'restaurant.table': 'table',

    # procurement
    'procurement.group': 'procurement_group',        # account.tax.group, res.country.group
    'procurement.order': 'procurement',
    # 'procurement.order.compute.all': 'order_compute_all',
    'procurement.rule': 'procurement_rule',

    # product
    'product.attribute': 'attribute',
    'product.attribute.line': 'attribute_line',
    'product.attribute.price': 'attribute_price',    # stock.change.standard.price
    'product.attribute.value': 'attribute_value',    # mail.tracking.value
    'product.category': 'product_category',
    'product.packaging': 'packaging',
    'product.price.history': 'price_history',
    'product.price_list': 'price_list',
    'product.pricelist': 'pricelist',
    'product.pricelist.item': 'pricelist_item',
    'product.product': 'product',                    # lunch.product
    'product.supplierinfo': 'supplierinfo',
    'product.template': 'product_template',
    'product.uom': 'uom',
    'product.uom.categ': 'uom_categ',
    'report.product.report_pricelist': 'product_report_pricelist',

    # product_margin
    'product.margin': 'margin',

    # project
    'project.config.settings': 'project_config_settings',
    'project.project': 'project',
    'project.tags': 'tags',
    'project.task': 'task',
    'project.task.type': 'task_type',
    'report.project.task.user': 'project_task_user',

    # project_issue
    'project.issue': 'issue',
    'project.issue.report': 'issue_report',

    # purchase
    'purchase.config.settings': 'purchase_config_settings',
    'purchase.order': 'purchase',
    'purchase.order.line': 'purchase_line',
    'purchase.report': 'purchase_report',

    # purchase_requisition
    'purchase.requisition': 'requisition',
    'purchase.requisition.line': 'requisition_line',
    'purchase.requisition.type': 'requisition_type',

    # rating
    'rating.mixin': 'rating_mixin',                  # mail.alias.mixin, utm.mixin, website.published.mixin
    'rating.rating': 'rating',

    # report
    'ir.qweb.field.barcode': 'qweb_field_barcode',
    'report': 'report',
    'report.abstract_report': 'abstract_report',
    'report.paperformat': 'paperformat',

    # report_intrastat
    'report.intrastat': 'intrastat',
    'report.intrastat.code': 'intrastat_code',       # link.tracker.code

    # resource
    'resource.calendar': 'calendar',
    'resource.calendar.attendance': 'calendar_attendance',  # hr.attendance
    'resource.calendar.leaves': 'calendar_leaves',
    'resource.resource': 'resource',

    # sale
    'sale.advance.payment.inv': 'advance_payment_inv',
    'sale.layout_category': 'layout_category',
    'sale.order': 'sale',
    'sale.order.line': 'sale_line',
    'sale.report': 'sale_report',

    # sales_team
    'crm.team': 'crm_team',                          # maintenance.team
    'sale.config.settings': 'sale_config_settings',

    # stock
    'make.procurement': 'make_procurement',
    'procurement.orderpoint.compute': 'orderpoint_compute',
    'product.putaway': 'putaway',
    'product.removal': 'removal',
    'report.stock.forecast': 'stock_forecast',
    'report.stock.lines.date': 'stock_lines_date',   # ir.qweb.field.date
    'stock.backorder.confirmation': 'backorder_confirmation',
    'stock.change.product.qty': 'change_product_qty',  # change.production.qty
    'stock.config.settings': 'stock_config_settings',
    'stock.fixed.putaway.strat': 'fixed_putaway_strat',
    'stock.immediate.transfer': 'immediate_transfer',
    'stock.incoterms': 'incoterms',
    'stock.inventory': 'inventory',
    'stock.inventory.line': 'inventory_line',
    'stock.location': 'location',                    # event.track.location
    'stock.location.path': 'path',
    'stock.location.route': 'route',
    'stock.move': 'stock_move',                      # account.move, validate.account.move
    'stock.move.operation.link': 'move_operation_link',  # res.request.link
    'stock.pack.operation': 'pack_operation',
    'stock.pack.operation.lot': 'stock_pack_operation_lot',  # pos.pack.operation.lot, stock.production.lot
    'stock.picking': 'picking',                      # stock.return.picking
    'stock.picking.type': 'picking_type',
    'stock.production.lot': 'production_lot',        # pos.pack.operation.lot, stock.pack.operation.lot
    'stock.quant': 'quant',
    'stock.quant.package': 'quant_package',
    'stock.return.picking': 'return_picking',        # stock.picking
    'stock.return.picking.line': 'return_picking_line',
    'stock.scrap': 'scrap',
    'stock.warehouse': 'warehouse',
    'stock.warehouse.orderpoint': 'warehouse_orderpoint',

    # stock_account
    'stock.change.standard.price': 'change_standard_price',  # product.attribute.price
    'stock.history': 'history',
    'wizard.valuation.history': 'valuation_history',

    # stock_landed_costs
    'stock.landed.cost': 'landed_cost',
    'stock.landed.cost.lines': 'landed_cost_lines',  # crossovered.budget.lines, ir.server.object.lines, stock.valuation.adjustment.lines
    'stock.valuation.adjustment.lines': 'valuation_adjustment_lines',  # crossovered.budget.lines, ir.server.object.lines, stock.landed.cost.lines

    # stock_picking_wave
    'stock.picking.to.wave': 'picking_to_wave',      # stock.picking.wave
    'stock.picking.wave': 'picking_wave',            # stock.picking.to.wave

    # subscription
    'subscription.document': 'document',
    'subscription.document.fields': 'document_fields',  # ir.model.fields
    'subscription.subscription': 'subscription',
    'subscription.subscription.history': 'subscription_history',

    # survey
    'survey.label': 'label',
    'survey.mail.compose.message': 'survey_mail_compose_message',  # mail.compose.message, mail.message, mrp.message
    'survey.page': 'page',
    'survey.question': 'survey_question',            # event.question
    'survey.stage': 'survey_stage',
    'survey.survey': 'survey',
    'survey.user_input': 'user_input',
    'survey.user_input_line': 'user_input_line',

    # utm
    'utm.campaign': 'utm_campaign',                  # mail.mass_mailing.campaign, marketing.campaign
    'utm.medium': 'medium',
    'utm.mixin': 'utm_mixin',                        # mail.alias.mixin, rating.mixin, website.published.mixin
    'utm.source': 'source',                          # hr.recruitment.source

    # web_planner
    'web.planner': 'planner',

    # web_tour
    'web_tour.tour': 'tour',

    # website
    'website': 'website',
    'website.config.settings': 'website_config_settings',
    'website.menu': 'website_menu',                  # ir.ui.menu
    'website.published.mixin': 'published_mixin',    # mail.alias.mixin, rating.mixin, utm.mixin
    'website.seo.metadata': 'seo_metadata',

    # website_blog
    'blog.blog': 'blog',
    'blog.post': 'blog_post',                        # account.budget.post, forum.post
    'blog.tag': 'blog_tag',

    # website_crm_partner_assign
    'crm.lead.assignation': 'lead_assignation',
    'crm.lead.forward.to.partner': 'lead_forward_to_partner',  # crm.lead2opportunity.partner, mail.channel.partner, res.partner
    'crm.lead.report.assign': 'lead_report_assign',  # crm.partner.report.assign
    'crm.partner.report.assign': 'partner_report_assign',  # crm.lead.report.assign
    'res.partner.activation': 'partner_activation',
    'res.partner.grade': 'partner_grade',

    # website_customer
    'res.partner.tag': 'partner_tag',

    # website_event_questions
    'event.answer': 'answer',                        # event.registration.answer
    'event.question': 'event_question',              # survey.question
    'event.question.report': 'question_report',
    'event.registration.answer': 'registration_answer',  # event.answer

    # website_event_track
    'event.sponsor': 'sponsor',
    'event.sponsor.type': 'sponsor_type',
    'event.track': 'track',
    'event.track.location': 'track_location',        # stock.location
    'event.track.tag': 'track_tag',

    # website_forum
    'forum.forum': 'forum',
    'forum.post': 'forum_post',                      # account.budget.post, blog.post
    'forum.post.reason': 'post_reason',              # crm.lost.reason
    'forum.post.vote': 'post_vote',
    'forum.tag': 'forum_tag',

    # website_forum_doc
    'forum.documentation.stage': 'documentation_stage',
    'forum.documentation.toc': 'documentation_toc',

    # website_quote
    'sale.order.option': 'order_option',             # sale.quote.option
    'sale.quote.line': 'quote_line',
    'sale.quote.option': 'quote_option',             # sale.order.option
    'sale.quote.template': 'quote_template',

    # website_sale
    'product.image': 'image',                        # ir.qweb.field.image
    'product.public.category': 'public_category',
    'product.style': 'style',

    # website_slides
    'slide.category': 'slide_category',
    'slide.channel': 'slide_channel',                # im_livechat.channel, im_livechat.report.channel, mail.channel
    'slide.embed': 'embed',
    'slide.slide': 'slide',
    'slide.tag': 'slide_tag',

    # website_twitter
    'website.twitter.tweet': 'twitter_tweet',

    # Legal Entity
    'sintez.legal.entity': 'legal_entity',
}
