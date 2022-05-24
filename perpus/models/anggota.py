from odoo import models, fields, api, _


class anggota(models.Model):  # inherit dari Model
    _name = 'perpus.anggota'  # atribut dari class Model
    _description = 'class untuk berlatih ttg idea'
    # rec_name = 'name'
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # attribute field

    name = fields.Char('Nama Anggota', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    id_anggota = fields.Char('Id Anggota', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    email = fields.Char('E-mail', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    telp = fields.Char('Telepon', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})

    _sql_constraints = [('id_unik', 'unique(id_anggota)', _('Id must be unique!'))]

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

