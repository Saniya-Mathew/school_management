# -*- coding: utf-8 -*-
import base64
from PIL import Image
from datetime import date, timedelta
import io
import json
import xlsxwriter
from docutils.nodes import header

from odoo import fields, models,api,_
from odoo.tools import json_default


class StudentLeaveInform(models.TransientModel):
    _name = "student.leave.inform"
    _description = "Student Report"

    student_ids = fields.Many2many('student.registration', string='Student',
                                 domain="[('class_id','=',class_id)]")
    class_id = fields.Many2one('class', string="Class")
    filter_by = fields.Selection(string='Filter by',
                              selection=[('month', 'Month'),
                                         ('week', 'Week'),
                                         ('day', 'Day'),
                                         ('custom','Custom')],)
    date_from = fields.Date(string='Start Date')
    date_to = fields.Date('End Date',)

    def action_print_report(self):
        """printing PDF report based on certain conditions"""
        data=self.prepare_report_data()
        return self.env.ref('school.action_report_student_leave').report_action(self,data=data)

    def action_print_exel_report(self):
        data = self.prepare_report_data()
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'student.leave.inform',
                     'options': json.dumps(data,default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Leave Excel Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center','bold': True,})
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        head2 = workbook.add_format(
            {'align': 'left', 'bold': True, 'font_size': '10px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        wrap_format = workbook.add_format({'text_wrap': True, 'font_size': '6px', 'align': 'center',
                                           'bold': True})
        sheet.merge_range('A2:K3', 'LEAVE REPORT', head)
        company = self.env.company
        company_info = f"""{company.name}
        {company.street or ''} {company.street2 or ''}
        {company.city or ''}, {company.state_id.name or ''} {company.zip or ''}
        {company.country_id.name or ''}"""

        sheet.merge_range('L2:N4', ' ', wrap_format)
        sheet.write('L2', company_info, wrap_format)
        if data.get('student name'):
            sheet.merge_range('B4:J4', f"Student Name: {data.get('student name')}", head2)
        if data.get('class_id'):
            sheet.merge_range('B5:J5', f"Class: {data.get('class_id')}", head2)
        if data.get('filter'):
            sheet.merge_range('B6:J6', f"Filter By: {data.get('filter')}", head2)
        letter = 66
        if not data.get('student name'):
            # sheet.merge_range('B8:C8','Student Name', cell_format)
            sheet.merge_range(f'{chr(letter)}8:{chr(letter+1)}8', 'Student Name:', cell_format)
            letter += 2
        if not data.get('class_id'):
            # sheet.merge_range('D8:E8', 'Class', cell_format)
            sheet.merge_range(f'{chr(letter)}8:{chr(letter+1)}8', 'Class', cell_format)
            letter += 2
        # sheet.merge_range('F8:G8', 'Reg No', cell_format)
        sheet.merge_range(f'{chr(letter)}8:{chr(letter + 1)}8', 'Reg No', cell_format)
        letter += 2
        # sheet.merge_range('H8:I8', 'Date From', cell_format)
        sheet.merge_range(f'{chr(letter)}8:{chr(letter + 1)}8',  'Date From', cell_format)
        letter += 2
        # sheet.merge_range('J8:K8', 'Date To', cell_format)
        sheet.merge_range(f'{chr(letter)}8:{chr(letter + 1)}8', 'Date To', cell_format)
        letter += 2
        # sheet.merge_range('L8:M8', 'Reason', cell_format)
        sheet.merge_range(f'{chr(letter)}8:{chr(letter + 1)}8',  'Reason', cell_format)
        letter += 2

        for i, report in enumerate(data.get('report'),start=10):
            letter = 66
            if not data.get('student name'):
                sheet.merge_range(f'{chr(letter)}{i}:{chr(letter + 1)}{i}',report.get('f_name'), txt)
                letter += 2
            if not data.get('class_id'):
                sheet.merge_range(f'{chr(letter)}{i}:{chr(letter + 1)}{i}',report.get('class_id'), txt)
                letter += 2
            sheet.merge_range(f'{chr(letter)}{i}:{chr(letter + 1)}{i}',report.get('reg_no'), txt)
            letter += 2
            sheet.merge_range(f'{chr(letter)}{i}:{chr(letter + 1)}{i}',report.get('date_from'), txt)
            letter += 2
            sheet.merge_range(f'{chr(letter)}{i}:{chr(letter + 1)}{i}',report.get('date_to'), txt)
            letter += 2
            sheet.merge_range(f'{chr(letter)}{i}:{chr(letter + 1)}{i}',report.get('reason'), txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    def prepare_report_data(self):
        query = """SELECT s.f_name,class_id,reg_no,date_from,date_to,reason FROM school_leave l
                     INNER JOIN student_registration s ON l.student_id = s.id """
        where_clause = []
        if self.filter_by == 'month':
            where_clause.append("DATE_TRUNC('month', l.date_from) = DATE_TRUNC('month', CURRENT_DATE)")
        if self.filter_by == 'week':
            start_week = date.today() - timedelta(days=date.today().weekday())
            end_week = start_week + timedelta(days=6)
            where_clause.append("l.date_from BETWEEN '%s' AND '%s' " % (start_week, end_week))
        if self.filter_by == 'day':
            where_clause.append("l.date_from = CURRENT_DATE")
        if self.filter_by == 'custom' and self.date_from and self.date_to:
            where_clause.append("l.date_from >= '%s' AND l.date_to <= '%s'" % (self.date_from, self.date_to))
        if self.student_ids:
            where_clause.append("l.student_id in (%s)" % str(self.student_ids.ids)[1:-1])
        if self.class_id:
            where_clause.append("s.class_id = '%s'" % (self.class_id.id))
        if where_clause:
            query += " WHERE " + " AND ".join(where_clause)

        self.env.cr.execute(query)
        report = self.env.cr.dictfetchall()
        data = {
            'student name': ",".join(self.student_ids.mapped('f_name')),
            'class_id': self.class_id.name,
            'filter': self.filter_by,
            'date from': self.date_from,
            'date to': self.date_to,
            'report': report
        }
        return data




