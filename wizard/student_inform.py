# -*- coding: utf-8 -*-
import io
import json
import xlsxwriter
from odoo import fields, models,_
from odoo.tools import json_default


class StudentInform(models.TransientModel):
    _name = "student.inform"
    _description = "Student Report"

    class_id = fields.Many2one('class', string="Class")
    dept_id = fields.Many2one('department',string='Department')
    club_id = fields.Many2one('school.club',string='Club')

    def action_student_report(self):
        """printing student report based on some conditions"""
        # data=self.prepare_report_data()
        # return self.env.ref('school.action_report_student').report_action(self, data=data)
        data = {
            'class_id':self.class_id.id,
            'dept_id' : self.class_id.id,
            'club_id': self.club_id.id,
        }

    def action_student_exel_report(self):
        """Printing exel report"""
        data = self.prepare_report_data()
        return {
            'type': 'ir.actions.report',
            'data': {'model': "student.inform",
                     'options': json.dumps(data, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Student Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self, data, response):
        """xlsx report format"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        cell_format = workbook.add_format(
            {'font_size': '12px', 'align': 'center', 'bold': True, })
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '20px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        wrap_format = workbook.add_format({'text_wrap': True, 'font_size': '6px', 'align': 'center',
                                           'bold': True})
        sheet.merge_range('C2:E4', 'STUDENT REPORT', head)
        company = self.env.company
        company_info = f"""{company.name}
        {company.street or ''} {company.street2 or ''}
        {company.city or ''} {company.state_id.name or ''}
                {company.country_id.name or ''}"""
        sheet.merge_range('A2:B5', company_info, wrap_format)
        sheet.set_column(2, 2, 25)
        sheet.set_column(4, 4, 25)
        sheet.write('C7', 'Student Name', cell_format)
        sheet.write('E7', 'Admission Date', cell_format)

        for i, report in enumerate(data.get('report'), start=9):
            sheet.write(f'C{i}', report.get('f_name'), txt)
            sheet.write(f'E{i}', report.get('date'), txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

    def prepare_report_data(self):
        query = """SELECT f_name,date FROM student_registration s 
                         INNER JOIN school_club_student_registration_rel rel
                         ON s.id = rel.student_registration_id"""
        where_clause = []
        params = []
        if self.class_id:
            where_clause.append("class_id = %s")
            params.append(self.class_id.id)
        if self.dept_id:
            where_clause.append("dept_id = %s")
            params.append(self.dept_id.id)
        if self.club_id:
            where_clause.append('rel.school_club_id = %s')
            params.append(self.club_id.id)
        if where_clause:
            query += " WHERE " + " AND ".join(where_clause)

        self.env.cr.execute(query, params)
        report = self.env.cr.dictfetchall()
        data = {
            'report': report
        }
        return data


