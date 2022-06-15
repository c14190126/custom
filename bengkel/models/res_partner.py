from odoo import models, fields, api, _

class Partner(models.Model):
    _name = 'res.partner'
    _inherit= 'res.partner'
    poin = fields.Integer('Poin', tracking=True)

    poin_ids = fields.One2many('bengkel.transaksi', 'point_id', string='Poin')

    @api.depends('poin_ids', 'poin_ids.tpoin')
    def compute_poin(self):
        for partner in self:
            poin = 0
            for rec in partner.poin_ids:
                poin += rec.tpoin
                print(10)
            partner.update(
                {
                    'poin': poin,
                }
            )
