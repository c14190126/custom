from odoo import models, fields, api, _


class wiztransaksi(models.TransientModel):
    _name = 'wiz.bengkel.transaksi'
    _description = 'class untuk menyimpan data transaksi dan bengkel'

    transaksi_id = fields.Many2one('bengkel.transaksi', String='Transaksi', readonly=True)

    line_ids = fields.One2many('wiz.bengkel.transaksi.lines', 'wiz_header_id', string='bengkel')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')
    @api.model
    def default_get(self,
        fields_list):  # ini adalah common method, semacam constructor, akan dijalankan saat create object. Ini akan meng-overwrite default_get dari parent
        res = super(wiztransaksi, self).default_get(fields_list)
        # res  merupakan dictionary beserta value yang akan diisi, yang sudah diproses di super class (untuk create record baru)
        res['transaksi_id'] = self.env.context['active_id']
        return res

    @api.onchange('transaksi_id')
    def onchange_transaksi_id(self, product_id=None):
        if not self.transaksi_id:
            return
        vals = []
        line_ids = self.env['wiz.bengkel.transaksi.lines']
        for rec in self.transaksi_id. detailtransaksi_ids:
            line_ids += self.env['wiz.bengkel.transaksi.lines'].new({
                'wiz_header_id': self.id,
                'ref_transaksi_lines_id': rec.id,
                'product_id': rec.product_id.id,
            })

    def action_confirm(self):
    # looping re=line_ids
    # cari bengkel.transaksi.
        for rec in self.line_ids:
            rec.ref_transaksi_lines_id.diskon = rec.diskon
            rec.ref_transaksi_lines_id.quantity = rec.quantity

    class transaksi_lines_wiz(models.TransientModel):
        _name = 'wiz.bengkel.transaksi.lines'
        _description = 'class untuk menyimpan data bengkel suatu transaksi'

        wiz_header_id = fields.Many2one('wiz.bengkel.transaksi', string='transaksi')
        product_id = fields.Many2one('bengkel.product', string='Product', ondelete="restrict")

        ref_transaksi_lines_id = fields.Many2one('bengkel.dtransaksi')
        harga_product = fields.Integer('Harga Produk', related='product_id.harga')
        quantity = fields.Integer("Quantity ", required=True, index=True, readonly=True,
                                  states={'draft': [('readonly', False)]})
        diskon = fields.Integer("Diskon(%)", required=False, index=True, readonly=True,
                                states={'draft': [('readonly', False)]})
        state = fields.Selection(
            [('draft', 'Draft'),
             ('confirmed', 'Confirmed'),
             ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
            default='draft')