from odoo import models, fields, api, _
from datetime import datetime


class dpinjam(models.Model):  # inherit dari Model
    _name = 'perpus.dpinjam'  # atribut dari class Model
    _description = 'class untuk berlatih ttg idea'
    # rec_name = 'name'
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # attribute field
    # related
    tgl_pinjam= fields.Date('Tanggal Pinjam', related='pinjam_id.date')
    harga_buku= fields.Integer('Harga Buku', related='buku_id.harga')

    tgl_balik = fields.Date('Tanggal Pengembalian', default=fields.Date.context_today, readonly=True,
                       states={'draft': [('readonly', False)]})
    denda = fields.Integer('Denda', required=False, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    dendat = fields.Integer('Denda Telat', compute='compute_denda', required=False, index=True, readonly=True,
                           states={'draft': [('readonly', True)]})
    biaya = fields.Integer('Biaya', compute='compute_biaya', required=False, index=True, readonly=True,
                           states={'draft': [('readonly', True)]})
    ket = fields.Char("Keterangan Denda", required=False, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    tmp_telat = fields.Integer('tmp telat')
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    pinjam_id = fields.Many2one('perpus.pinjam', string="Peminjaman Buku", readonly=True, ondelete='cascade',
                                states={'draft': [('readonly', False)]},
                                domain="[('state', '=', 'confirmed')]")
    buku_id = fields.Many2one('perpus.buku', string='Nama Buku', readonly=True, ondelete='cascade',
                              states={'draft': [('readonly', False)]},
                              domain="[('state', '=', 'confirmed')]")

    durasi = fields.Integer('Durasi', compute='compute_durasi', store="True")
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})

    _sql_constraints = [('cek_tanggal', 'check(durasi>0)', _('Return Date Must After Borrow Date!'))]

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('tgl_pinjam','tgl_balik')
    def compute_durasi(self):
        if self.tgl_pinjam and self.tgl_balik:
            for rec in self:
                durasi = int((self.tgl_balik - self.tgl_pinjam).days)
                rec.durasi= durasi

    @api.depends("durasi", "dendat","harga_buku")
    def compute_denda(self):
            for dpinjam in self:
                val = {
                    "dendat":0,
                    "tmp_telat":0
                }
                for rec in self:
                    if rec.durasi > 5:
                        val["tmp_telat"] = rec.durasi-5
                        val["dendat"] = 0.1 * rec.harga_buku * val["tmp_telat"]
                    else:
                        val["dendat"] += 0
                dpinjam.update(val)

    @api.depends("durasi", "biaya", "harga_buku" )
    def compute_biaya(self):
        for dpinjam in self:
            val = {
                "biaya": 0
            }
            for rec in self:
                    val["biaya"] = rec.durasi * rec.harga_buku
            dpinjam.update(val)



