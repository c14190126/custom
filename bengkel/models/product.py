from odoo import models, fields, api, _


class product(models.Model):  # inherit dari Model
    _name = 'bengkel.product'  # atribut dari class Model
    _description = 'class untuk berlatih ttg idea'
    # rec_name = 'name'
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # attribute field

    name = fields.Char('Nama Product', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    id_product = fields.Char('Id Product', size=64, required=True, index=True, readonly=True, default='new')
    merk = fields.Many2one('bengkel.merek', string="Merek", readonly=True, ondelete='cascade',
                               states={'draft': [('readonly', False)]},
                               domain="[('state', '=', 'confirmed')]")
    kategori = fields.Many2one('bengkel.kategori', string="Kategori", readonly=True, ondelete='cascade',
                               states={'draft': [('readonly', False)]},
                               domain="[('state', '=', 'confirmed')]")
    jumlah = fields.Integer('Stock Awal', required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    temp = fields.Integer('Stock Sekarang', readonly='True',compute='compute_kurang')
    harga = fields.Integer('Harga', required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})

    detailtransaksi_ids = fields.One2many('bengkel.dtransaksi', 'product_id', string='Produk')

    _sql_constraints = [('cek_harga', 'check (harga>0)', 'Harga tidak boleh negatif'),
                        ('cek_jumlah', 'check (jumlah>0)', 'Jumlah tidak boleh negatif')]
    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "bengkel.product")])
        if not seq:
            raise UserError(_("bengkel.product sequence not found, please create bengkel.product sequence"))
        for val in vals_list:
            val['id_product'] = seq.next_by_id()
        return super(product, self).create(vals_list)

    @api.depends('detailtransaksi_ids', 'detailtransaksi_ids.quantity' )
    def compute_kurang(self):
        for product in self:
            val = { 'temp': product.jumlah }
            for rec in product.detailtransaksi_ids:
                val["temp"] -= rec.quantity
                product.jumlah = val['temp']
            product.update(val)