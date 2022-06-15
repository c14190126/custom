from odoo import models, fields, api, _

class transaksi(models.Model):  # inherit dari Model
    _name = 'bengkel.transaksi'  # atribut dari class Model
    _description = 'class untuk berlatih ttg idea'
    # rec_name = 'name'
    # id = fields.Integer() #ini otomatis ada di odoo, akan jadi pk

    # attribute field

    name = fields.Char('Id Transaksi', size=64, required=True, index=True, readonly=True,default='new',
                       states={'draft': [('readonly', True)]})
    date = fields.Date('Tanggal Transaksi', default=fields.Date.context_today, readonly=True,
                       states={'draft': [('readonly', False)]})
    total = fields.Integer('Total',compute='compute_total', required=False, index=True, readonly=True,
                           states={'draft': [('readonly', True)]})
    customer = fields.Many2one('res.partner', 'Customer', index=True, readonly=True, states={'draft': [('readonly', False)]})
    tpoin = fields.Integer('Poin Didapat',  required=False, index=True, readonly=True, compute="compute_point",)

    state = fields.Selection(
        [('draft', 'Draft'),
         ('confirmed', 'Confirmed'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')
    # Description is read-only when not draft!
    description = fields.Text('Description', readonly=True, states={'draft': [('readonly', False)]})

    detailtransaksi_ids = fields.One2many('bengkel.dtransaksi', 'transaksi_id', string='Transaksi')

    mobil_id = fields.Many2one('bengkel.mobil', string="Nopol", readonly=True, ondelete='cascade', require=True,
                               states={'draft': [('readonly', False)]},
                               domain="[('state', '=', 'confirmed')]")
    point_id = fields.Many2one('res.partner', string="point", readonly=True, ondelete='cascade')
    employee = fields.Many2one('hr.employee', string="Service Advisor", readonly=True, ondelete='cascade', require=True,
                               states={'draft': [('readonly', False)]}, domain="[('department_id', '=', 'Service Consultant')]")

    poin = fields.Integer('Poin', related='point_id.poin', tracking=True)

    def action_canceled(self):
        self.state = 'canceled'

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "bengkel.transaksi")])
        if not seq:
            raise UserError(_("bengkel.transaksi sequence not found, please create bengkel.transaksi sequence"))
        for val in vals_list:
            val['name'] = seq.next_by_id(sequence_date=val['date'])
        return super(transaksi, self).create(vals_list)

    @api.depends('detailtransaksi_ids.harga')
    def compute_total(self):
        for transaksi in self:
            val = {
                "total": 0
            }
            for rec in transaksi.detailtransaksi_ids:
                val["total"] += rec.harga
            transaksi.update(val)

    def action_wiz_transaksi(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Nilai Kelas'),
            'res_model': 'wiz.bengkel.transaksi',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }

    def compute_point(self):
        for transaksi in self:
            val = {
                "tpoin": 0
            }
            for rec in self:
                val["tpoin"] += rec.total / 100000
            transaksi.update(val)

    @api.onchange(customer)
    def onchange_customer(self):
        if self.customer:
            if self.customer.poin:
                print(self.customer)
                # self.poin = self.customer.poin