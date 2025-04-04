# -*- coding: utf-8 -*-
from odoo import models,api


class StudentReport(models.AbstractModel):
    _name = 'report.school.report_student'
    @api.model
    def _get_report_values(self, docids,data):
        docs = self.env['school.leave'].browse(docids)
        print(data)
        return {
            'doc_ids': docids,
            'doc_model': 'school.leave',
            'docs': docs,
            'data': data,
        }
