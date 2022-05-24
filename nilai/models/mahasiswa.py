from odoo import models, fields, api, _


class nilai(models.Model):  # inherit dari Model
    _name = 'nilai.mahasiswa'  # atribut dari class Model
    _description = 'class untuk berlatih ttg idea'
    # rec_name = 'name'
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # membuat attribute field

    name = fields.Char('Name', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    nrp = fields.Char('Nrp', size=64, required=True, index=True, readonly=True,
                      states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('confirmed', 'Confirmed'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    status = fields.Selection(
        [('aktif', 'Aktif'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('lulus', 'Lulus'),
         ('cuti', 'Cuti'),
         ('do', 'Do')], 'Status', required=True, readonly=False,  # krn required, sebaiknya dikasi default
        default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})

    # sponsor_ids = fields.Many2many('res.partner', 'idea_idea_res_partner_rel', 'idea_idea_id', 'res_partner_id', 'Sponsors')
    _sql_constraints = [('name_unik', 'unique(name)', _('Ideas must be unique!'))]


    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

