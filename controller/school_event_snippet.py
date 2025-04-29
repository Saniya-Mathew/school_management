from odoo import http
from odoo.http import request

class WebsiteEvent(http.Controller):
    @http.route('/get_event_categories', auth="public", type='json', website=True,)
    def get_event_categories(self):
        """Get the website categories for the snippet."""
        events = request.env['school.event'].sudo().search_read(fields=['name','image','id'])
        values = {
            'event': events,
        }
        return values

    @http.route('/get_event_details/<int:student_id>', type='http', auth='public', website=True)
    def get_event_details(self, student_id):
        events = request.env['school.event'].sudo().browse(student_id)
        return request.render('school.get_event_details_template', {
            'event': events
        })