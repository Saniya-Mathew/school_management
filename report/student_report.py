# -*- coding: utf-8 -*-
import xlsxwriter
import io
from odoo import api,models,_
from odoo.exceptions import UserError


class StudentReport(models.AbstractModel):
    _name = 'report.school.report_student_inform'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Prepare report data based on filters"""
        query = """SELECT f_name, date FROM student_registration s
                       INNER JOIN school_club_student_registration_rel rel
                       ON s.id = rel.student_registration_id"""
        where_clause = []

        if data.get('class_id'):
            where_clause.append("s.class_id = '%s'" % (data.get('class_id')))
        if data.get('dept_id'):
            where_clause.append("s.dept_id = '%s'" % (data.get('dept_id')))
        if data.get('club_id'):
            where_clause.append("rel.school_club_id ='%s'" % (data.get('club_id')))
        if where_clause:
            query += " WHERE " + " AND ".join(where_clause)

        print(query)
        self.env.cr.execute(query)
        docs = self.env.cr.dictfetchall()
        print(docs)
        if docs:
            return {
                'doc_ids': docids,
                'doc_model': 'student.registration',
                'docs': docs,
                'data': data,
            }
        else:
            raise UserError(_("""No Data\n"""))

    @api.model
    def get_xlsx_report(self, data, response):
        """Generate the xlsx report"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()

        cell_format = workbook.add_format({'font_size': '12px', 'align': 'center', 'bold': True})
        head_format = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        txt_format = workbook.add_format({'font_size': '10px', 'align': 'center'})
        wrap_format = workbook.add_format({'text_wrap': True, 'font_size': '6px', 'align': 'center','bold': True})

        sheet.merge_range('C2:E4', 'STUDENT REPORT', head_format)

        company = self.env.company
        company_info = f"""{company.name}
        {company.street or ''} {company.street2 or ''}
        {company.city or ''} {company.state_id.name or ''}
        {company.country_id.name or ''}"""
        sheet.merge_range('B2:B4', company_info, wrap_format)

        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 25)
        sheet.set_column(4, 4, 25)

        report_data = self._get_report_values([], data)
        docs = report_data.get('docs', [])
        sheet.write('C7', 'Student Name', cell_format)
        sheet.write('E7', 'Admission Date', cell_format)
        for i, student in enumerate(docs, start=9):
            sheet.write(f'C{i}', student.get('f_name'), txt_format)
            sheet.write(f'E{i}', student.get('date'), txt_format)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

