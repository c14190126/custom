from odoo import models, fields, api, _


class buku(models.Model):  # inherit dari Model
    _name = 'perpus.buku'  # atribut dari class Model
    _description = 'class untuk berlatih ttg idea'
    # rec_name = 'name'
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # attribute field

    name = fields.Char('Nama Buku', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    id_buku = fields.Char('Id Buku', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    pengarang = fields.Char('Pengarang', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    penerbit = fields.Char('Penerbit', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    tahunterbit = fields.Char('Tahun Terbit', size=64, required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    copy = fields.Integer('Jumlah Buku', required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    harga = fields.Integer('Harga Peminjaman Buku', required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')
    detailpinjam_ids = fields.One2many('perpus.dpinjam', 'buku_id', string='Buku')

    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})

    _sql_constraints = [('id_unik', 'unique(id_buku)', _('ID Buku must be unique!')),
                        ('cek_harga', 'check (harga>0)', 'Harga tidak boleh negatif')]
    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

