from addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo import http


class WebsiteSaleCustom(WebsiteSale):
    print(100)
    @http.route(['/shop'], type='http', auth="user", website=True, sitemap=True)
    def shop(self, page=0, category=None, search='', **post):
        print("hi")
        # result = WebsiteSale().shop(page=page, category=category, search=search, **post)
        result = super().shop(page=page, category=category, search=search, **post)

        user = request.env.user
        partner = user.partner_id

        domain = []
        if partner.product_ids:
            domain = [('id', 'in', partner.product_ids.ids)]
            print('hello')
        elif partner.product_category_ids:
            domain = [('product_category_ids', 'in', partner.product_category_ids.ids)]

        if domain:
            filtered_products = request.env['product.template'].search(domain)
            result.qcontext['products'] = filtered_products

        return result