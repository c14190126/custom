from odoo import models, fields, api, _
from datetime import datetime


class dtransaksi(models.Model):  # inherit dari Model
    _name = 'bengkel.dtransaksi'  # atribut dari class Model
    _description = 'class untuk berlatih ttg idea'
    # rec_name = 'name'
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # attribute field
    # related
    harga_product = fields.Integer('Harga Produk', related='product_id.harga')

    harga = fields.Integer('Harga', compute='compute_harga', required=False, readonly=True)
    ket = fields.Char("Keterangan ", required=False, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    quantity = fields.Integer("Quantity ", required=False, index=True, readonly=True)
    diskon = fields.Integer("Diskon(%)", required=False, index=True, readonly=True)
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    transaksi_id = fields.Many2one('bengkel.transaksi', string="Transaksi", readonly=True, ondelete='cascade',
                                   states={'draft': [('readonly', False)]},
                                   domain="[('state', '=', 'confirmed')]")
    product_id = fields.Many2one('bengkel.product', string='Product', readonly=True, ondelete='cascade',
                                 states={'draft': [('readonly', False)]},
                                 domain="[('state', '=', 'confirmed')]")
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

    # @api.depends("harga_product", "quantity", "diskon")
    # def compute_harga(self):
    # for dtransaksi in self:
    #    harga = 0
    #    for rec in self:
    #        harga = rec.harga_product * rec.quantity - rec.harga_product * rec.quantity * rec.diskon/100
    #    dtransaksi.update(
    #        {
    #            'harga': harga,
    #        }
    #    )

    @api.depends("harga_product", "quantity", "diskon")
    def compute_harga(self):
        for dtransaksi in self:
            val = {
                "harga": 0,
            }
            for rec in self:
                val["harga"] = rec.harga_product * rec.quantity - rec.harga_product * rec.quantity * rec.diskon / 100
                print(val["harga"])
            dtransaksi.update(val)
