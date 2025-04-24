from odoo import http
from odoo.http import request

class WebsiteEvent(http.Controller):
    @http.route('/get_event_categories', auth="public", type='json', website=True,)
    def get_event_categories(self):
        print("hii san")
        """Get the website categories for the snippet."""
        events = request.env['school.event'].sudo().search_read(fields=['name', 'id'])
        values = {
            'event': events,
        }
        return values
