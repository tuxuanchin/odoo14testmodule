from odoo import api, fields, models
from odoo.exceptions import ValidationError

# from odoo-14.0.addons.sale.models.sale import SaleOrder as OdooSaleOrder


class SaleCouponApplyCode(models.TransientModel):
    _inherit = "sale.coupon.apply.code"

    coupon_code = fields.Char(string="Code", required=True)

    # def apply_coupon(self, order, coupon_code):
    #     print(self)
    #     self.coupon_code = coupon_code
    #     print("Coupon_code:...", self.coupon_code)
    #     print("Order:...", order)
    #     if coupon_code:
    #         coupons = self.env['coupon.sale'].search(
    #              [('name', '=', coupon_code)])
    #         if coupons:
    #             if coupons.number_valid <= 0:
    #                 raise ValidationError("COUPON IS USED TO MUCH")
    #             else:
    #                 coupons.number_valid -= 1
    #                 percent_off = float(coupon_code[4:])
    #                 order.amount_discount = order.amount_untaxed / 100 * percent_off
    #                 order.amount_total = order.amount_untaxed - order.amount_discount + order.amount_tax,
    #
    #         else:
    #             raise ValidationError("INVALID CODE")



















































