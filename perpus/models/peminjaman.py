from odoo import models, fields, api, _


class peminjaman(models.Model):  # inherit dari Model
    _name = 'perpus.pinjam'  # atribut dari class Model
    _description = 'class untuk berlatih ttg idea'
    # rec_name = 'name'
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # attribute field

    name = fields.Char('Id Peminjaman', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    date = fields.Date('Tanggal Pinjam', default=fields.Date.context_today, readonly=True,
                       states={'draft': [('readonly', False)]})
    jumlah_buku  = fields.Integer('Jumlah Buku', compute="compute_count", required=True, index=True, readonly=True,
                      states={'draft': [('readonly', True)]})
    total = fields.Integer('Total',compute="compute_total", required=False, index=True, readonly=True,
                           states={'draft': [('readonly', True)]})
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    anggota_id = fields.Many2one('perpus.anggota', string="Nama Anggota", readonly=True, ondelete='cascade',
                                states={'draft': [('readonly', False)]},
                                domain="[('state', '=', 'confirmed')]")
    admin_id = fields.Many2one('res.users', 'Admin', readonly=True, default=lambda self: self.env.user)
    detailpinjam_ids = fields.One2many('perpus.dpinjam', 'pinjam_id', string='Pinjam')
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})

    _sql_constraints = [('name_unik', 'unique(name)', _('Id must be unique!'))]

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

    @api.depends('detailpinjam_ids', 'detailpinjam_ids.denda', 'detailpinjam_ids.biaya', 'detailpinjam_ids.dendat')

    def compute_total(self):
        for peminjaman in self:
            val = {
                "total": 0
            }
            for rec in peminjaman.detailpinjam_ids:
                val["total"] += rec.denda + rec.biaya + rec.dendat
            peminjaman.update(val)

    @api.depends('detailpinjam_ids.buku_id',)
    def compute_count(self):
        for peminjaman in self:
            val = {
                "jumlah_buku": 0
            }
            for rec in peminjaman.detailpinjam_ids:
                val["jumlah_buku"] += len(rec.buku_id)
            peminjaman.update(val)