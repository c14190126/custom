from odoo import models, fields, api, _

class mobil(models.Model):  # inherit dari Model
    _name = 'bengkel.mobil'  # atribut dari class Model
    _description = 'class untuk berlatih ttg idea'
    # rec_name = 'name'
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # attribute field

    name = fields.Char('Nomor Polisi', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    no_rangka = fields.Char('Nomor Rangka', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    nama_mobil = fields.Char('Nama Mobil', size=64, required=True, index=True, readonly=True,
                            states={'draft': [('readonly', False)]})
    warna = fields.Char('Warna', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    bbm = fields.Selection(
        [('bensin', 'Bensin'),
         ('diesel', 'Diesel')], 'Bahan Bakar', required=True, readonly=True, states={'draft': [('readonly', False)]})
    tahun = fields.Char('Tahun', size=64, required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    km = fields.Integer('Kilometer', required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')

    _sql_constraints = [('cek_km', 'check (km>0)', 'KM tidak boleh negatif'),
                        ('cek_tahun', 'check (tahun>0)', 'Tahun tidak boleh negatif'),
                        ('norangka_unik', 'unique(no_rangka)', _('no_rangka must be unique!'))
                        ]

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

