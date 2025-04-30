# -*- coding: utf-8 -*-
import xlsxwriter
from odoo import models, api, _
from odoo.exceptions import UserError
from datetime import date, timedelta
import io

class StudentReport(models.AbstractModel):
    _name = 'report.school.report_student'

    @api.model
    def _get_report_values(self, docids, data=None):
        """filtering conditions"""
        query = """SELECT s.f_name,class_id,reg_no,date_from,date_to,reason FROM school_leave l
                             INNER JOIN student_registration s ON l.student_id = s.id """
        where_clause = []
        if data.get('month'):
            where_clause.append("DATE_TRUNC('month', l.date_from) = DATE_TRUNC('month', CURRENT_DATE)")
        if data.get('week'):
            start_week = date.today() - timedelta(days=date.today().weekday())
            end_week = start_week + timedelta(days=6)
            where_clause.append("l.date_from BETWEEN '%s' AND '%s' " % (start_week, end_week))
        if data.get('day'):
            where_clause.append("l.date_from = CURRENT_DATE")
        if data.get('custom') and data.get('date_from') and data.get('date_to'):
            where_clause.append("l.date_from >= '%s' AND l.date_to <= '%s'" % (data.get('date_from'), data.get('date_to')))
        if data.get('student_ids'):
            where_clause.append("l.student_id in (%s)" % str(data.get('student_ids'))[1:-1])
        if data.get('class_id'):
            where_clause.append("s.class_id = '%s'" % (data.get('class_id')))

        if where_clause:
            query += " WHERE " + " AND ".join(where_clause)

        self.env.cr.execute(query)
        docs = self.env.cr.dictfetchall()
        if not docs:
            raise UserError(_("This report cannot be printed, There is no data!"))
        return {
            'doc_ids': docids,
            'doc_model': 'school.leave',
            'docs': docs,
            'data': data,
            # 'student name': ",".join(self.student_ids.mapped('f_name'))

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
        head2 = workbook.add_format(
            {'align': 'left', 'bold': True, 'font_size': '10px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        wrap_format = workbook.add_format({'text_wrap': True, 'font_size': '6px', 'align': 'center',
                                           'bold': True})
        sheet.merge_range('C2:F3', 'LEAVE REPORT', head)

        company = self.env.company
        company_info = f"""{company.name}
        {company.street or ''} {company.street2 or ''}
        {company.city or ''} {company.state_id.name or ''}
        {company.country_id.name or ''}"""
        sheet.merge_range('B2:B4', company_info, wrap_format)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 25)
        sheet.set_column(3, 3, 25)
        sheet.set_column(4, 4, 25)
        sheet.set_column(5, 5, 25)
        sheet.set_column(6, 6, 25)
        report_data = self._get_report_values([], data)
        docs = report_data.get('docs', [])

        if data.get('student name'):
            sheet.write('C5', f"Student Name: {data.get('student name')}", head2)
        if data.get('class_id'):
            sheet.write('C6', f"Class: {data.get('class_id')}", head2)
        if data.get('filter_by'):
            sheet.write('C7', f"Filter By: {data.get('filter_by')}", head2)
        column = 66
        if not data.get('student name'):
            sheet.write(f'{chr(column)}8', 'Student Name', cell_format)
            column += 1
        if not data.get('class_id'):
            sheet.write(f'{chr(column)}8', 'Class', cell_format)
            column += 1
        sheet.write(f'{chr(column)}8', 'Reg No', cell_format)
        column += 1
        sheet.write(f'{chr(column)}8', 'Date From', cell_format)
        column += 1
        sheet.write(f'{chr(column)}8', 'Date To', cell_format)
        column += 1
        sheet.write(f'{chr(column)}8', 'Reason', cell_format)

        for i, report in enumerate(docs, start=9):
            column = 66
            if not data.get('student name'):
                sheet.write(f'{chr(column)}{i}', report.get('f_name'), txt)
                column += 1
            if not data.get('class_id'):
                sheet.write(f'{chr(column)}{i}', report.get('class_id'), txt)
                column += 1
            sheet.write(f'{chr(column)}{i}', report.get('reg_no'), txt)
            column += 1
            sheet.write(f'{chr(column)}{i}', report.get('date_from'), txt)
            column += 1
            sheet.write(f'{chr(column)}{i}', report.get('date_to'), txt)
            column += 1
            sheet.write(f'{chr(column)}{i}', report.get('reason'), txt)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()




