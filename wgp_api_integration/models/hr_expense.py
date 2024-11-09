from odoo import fields, models, api, _


class HrExpenseSheet(models.Model):
    _inherit = 'hr.expense.sheet'

    sync_statusCode = fields.Char('Status Code', copy=False, tracking=True)
    sync_message = fields.Char('Message', copy=False, tracking=True)
    sync_date = fields.Datetime('Sync Date', copy=False, tracking=True)

    def action_approve_expense_sheets(self):
        if not self.env.context.get('bypass'):
            self._check_can_approve()
        self._validate_analytic_distribution()
        duplicates = self.expense_line_ids.duplicate_expense_ids.filtered(lambda exp: exp.state in {'approved', 'done'})
        if duplicates:
            action = self.env["ir.actions.act_window"]._for_xml_id('hr_expense.hr_expense_approve_duplicate_action')
            action['context'] = {'default_sheet_ids': self.ids, 'default_expense_ids': duplicates.ids}
            return action
        self._do_approve()
