from odoo import models, fields, api, _


class merek(models.Model):  # inherit dari Model
    _name = 'bengkel.merek'  # atribut dari class Model
    _description = 'class untuk berlatih ttg idea'
    # rec_name = 'name'
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # attribute field

    name = fields.Char('Merek', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    id_merek = fields.Char('Id Merek', size=64, required=True, index=True, readonly=True, default='new')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    product_ids = fields.One2many('bengkel.product', 'kategori', string='Kategori')

    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "bengkel.merek")])
        if not seq:
            raise UserError(_("bengkel.transaksi sequence not found, please create bengkel.transaksi sequence"))
        for val in vals_list:
            val['id_merek'] = seq.next_by_id()
        return super(merek, self).create(vals_list)