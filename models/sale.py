from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
# from addons.sale.models.sale import SaleOrder as VCSaleOrder


class SaleOrder(models.Model):
    _inherit = "sale.order"

    coupon = fields.Char(string='Coupon Code')
    percent_off = fields.Float(string='Percent Off')
    amount_discount = fields.Float(string='Discount')

    @api.constrains('coupon')
    def check_name(self):
        for rec in self:
            if self.coupon:
                coupons = self.env['coupon.sale'].search(
                    [('name', '=', self.coupon), ('partner_ids', '=', self.partner_id.id)])
                if coupons:
                    if self.create_date.date() > coupons.date_valid:
                        raise ValidationError("COUPON EXPIRED")
                    elif coupons.number_valid <= 0:
                        raise ValidationError("COUPON IS USED TO MUCH")
                    else:
                        coupons.number_valid -= 1
                        self.percent_off = float(self.coupon[4:])
                        self.amount_discount = self.amount_untaxed / 100 * self.percent_off
                        self.update({
                            'amount_total': self.amount_untaxed - self.amount_discount + self.amount_tax,
                        })
                else:
                    raise ValidationError("INVALID CODE")

    