from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    coupon_ids = fields.Many2many('coupon.sale', 'partner_coupon_rel', 'partner_id', 'coupon_id_rec', string='Coupon')
    coupon = fields.Integer(string='Coupon')

    