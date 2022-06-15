from odoo import models, fields, api, _

class Employee(models.Model):
    _inherit= 'hr.employee'
    bonus = fields.Integer(string='Bonus', store=True)
    bonus_ids = fields.One2many('bengkel.transaksi', 'employee', string='Bonus')

    @api.depends('bonus_ids', 'bonus_ids.total')
    def compute_poin(self):
        for employee in self:
            bonus = 0
            for rec in employee.poin_ids:
                bonus += rec.total* 0.05
                print(10)
            employee.update(
                {
                   "bonus" : bonus
                }
            )