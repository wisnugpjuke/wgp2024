# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request
import json
import requests
from datetime import datetime


class HrExpense(http.Controller):
    @http.route('/get/hr-expense', type='http', auth='public', methods=['GET'], csrf=False)
    def get_hr_expense(self, **kw):
        try:
            if 'reportId' in kw:
                expense_report_ids = request.env['hr.expense.sheet'].sudo().search([('id', '=', kw['reportId'])])
            else:
                expense_report_ids = request.env['hr.expense.sheet'].sudo().search([])

            data_received = []
            if expense_report_ids:
                statusCode = "200"
                message = "OK"
                expense_line = []
                for exp in expense_report_ids:
                    for line in exp.expense_line_ids:
                        expense_line.append({
                            "expenseId": line.id,
                            "name": line.name,
                            "date": str(line.date.strftime("%d-%m-%Y")),
                            "description": line.description if line.description else '-',
                            "subTotal": line.total_amount
                        })
                    data_received.append({
                        "reportId": exp.id,
                        "name": exp.name,
                        "state": dict(exp._fields['state'].selection).get(exp.state),
                        "expenseLines": expense_line,
                    })
            else:
                statusCode = "404"
                message = "No Data!"

            if data_received:
                response = {
                    "statusCode": statusCode,
                    "message": message,
                    "data_received": data_received
                }
            else:
                response = {
                    "statusCode": statusCode,
                    "message": message,
                }
            return json.dumps(response)
        except:
            return "<h3>Something went wrong!</h3>"

    @http.route('/post/hr-expense', type='http', auth='public', methods=['POST'], csrf=False)
    def post_hr_expense(self, **kw):
        try:
            data = json.loads(request.httprequest.data)
            data_received = False
            if not data['reportId'] or not data['state']:
                statusCode = "400"
                message = "Report Id or State must be Filled!"
            elif data['state'] not in ['approve', 'cancel']:
                statusCode = "404"
                message = "State not Found!"
            else:
                expense_report_id = request.env['hr.expense.sheet'].sudo().search([('id', '=', data['reportId'])])
                if expense_report_id:
                    if expense_report_id.state != 'submit':
                        statusCode = "400"
                        message = "State must be in Submitted!"
                        data_received = {
                            "reportId": expense_report_id.id,
                            "state": dict(expense_report_id._fields['state'].selection).get(expense_report_id.state)
                        }
                    else:
                        if data['state'] == 'approve':
                            expense_report_id.with_context(bypass=True).action_approve_expense_sheets()
                        elif data['state'] == 'cancel':
                            expense_report_id._do_refuse('Refuse from API')

                        statusCode = "200"
                        message = "OK"
                        data_received = {
                            "reportId": expense_report_id.id,
                            "state": dict(expense_report_id._fields['state'].selection).get(expense_report_id.state)
                        }
                        expense_report_id.sync_statusCode = statusCode
                        expense_report_id.sync_message = message
                        expense_report_id.sync_date = fields.Datetime.now()
                else:
                    statusCode = "404"
                    message = "Report Id not Found!"
                    data_received = {
                        "reportId": data['reportId']
                    }

            if data_received:
                response = {
                    "statusCode": statusCode,
                    "message": message,
                    "data_received": data_received
                }
            else:
                response = {
                    "statusCode": statusCode,
                    "message": message,
                }
            return json.dumps(response)
        except:
            return "<h3>Something went wrong!</h3>"