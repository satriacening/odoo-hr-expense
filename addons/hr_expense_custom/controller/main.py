from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class TestController(http.Controller):

    @http.route("/test/", type='json', auth='user')
    def test_det(self):

        htm_result = """<html><body>
            <div class="bg-info text-center p-2">
                <b> Document: XMLID (Dynamic Document name and XMLID) </b>
                </div>
            </body>
            </html>
            """

        return {'html': htm_result}