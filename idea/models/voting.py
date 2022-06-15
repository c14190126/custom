from odoo import models, fields, api, _


class idea(models.Model):  # inherit dari Model
    _name = 'idea.voting'  # atribut dari class Model
    _description = 'class untuk berlatih ttg idea'
    # rec_name = 'name'
    _order = 'date desc'  # defaultnya adalah id, pengaruhnya saat list view
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # membuat attribute field
    name = fields.Char('Name', size=64, required=True, index=True, readonly=True, default='new',
                       states={})

    date = fields.Date('Date Voting', default=fields.Date.context_today, readonly=True,
                       states={'draft': [('readonly', False)]})

    state = fields.Selection(
        [('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('voted', 'Voted'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states
    vote = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No'),
         ('abstain', 'Abstain')], 'Vote', required=True, readonly=True, states={'draft': [('readonly', False)]})
    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, default=lambda self: self.env.user)
    idea_id = fields.Many2one('idea.idea', string='Idea', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done'),('active', '=', 'true')]")
    idea_date = fields.Date("Idea date", related='idea_id.date')
    active = fields.Boolean('Active', default=True, readonly=True, states={'draft': [('readonly', False)]})
    def action_voted(self):
        self.state = 'voted'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "idea.voting")])
        if not seq:
            raise UserError(_("idea.voting sequence not found, please create idea.voting sequence"))
        for val in vals_list:
            val['name'] = seq.next_by_id()
        return super(idea, self).create(vals_list)