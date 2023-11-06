from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class Coupon(models.Model):
    _name = "coupon.sale"
    _description = "Coupon"

    name = fields.Char(string='Coupon Code', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    date_valid = fields.Date(string='Date Valid')
    number_valid = fields.Integer(string='Number Valid')

    percent_off = fields.Float(string='Percent Off', required=True)
    partner_ids = fields.Many2many('res.partner', 'partner_coupon_rel', 'coupon_id_rec', 'partner_id', string='Customer')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = 'VIP_' + str(vals['percent_off'])
        res = super(Coupon, self).create(vals)
        return res

    @api.constrains('percent_off')
    def check_name(self):
        if self.percent_off <= 0 or self.percent_off > 100:
            raise ValidationError("INVALID CODE")

