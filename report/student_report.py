# -*- coding: utf-8 -*-
from odoo import models,api


class StudentReport(models.AbstractModel):
    _name = 'report.school.report_student_inform'

    @api.model
    def _get_report_values(self, docids,data):
        docs = self.env['student.registration'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'student.registration',
            'docs': docs,
            'data': data,
        }
