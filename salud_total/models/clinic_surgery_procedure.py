from odoo import api, models, fields 
from odoo.exceptions import ValidationError

class clinic_surgery_procedure(models.Model):
    _name = 'clinic_surgery_procedure'
    _description = 'Procedimiento Quirúrgico'
    _order = 'surgery_date desc'

    name = fields.Char(string='Código de Procedimiento', required=True, copy=False)

    patient_id = fields.Many2one('clinic_patient', string='Paciente', required=True)
    doctor_id = fields.Many2one('clinic_employee_profile', string='Cirujano(a)', required=True, domain=[('is_doctor', '=', True)])
    surgery_preparation_id = fields.Many2one('clinic_surgery_preparation', string='Preparación Quirúrgica Relacionada', required=True)
    surgery_date = fields.Datetime(string='Fecha de la Cirugía', default=fields.Datetime.now, required=True)

    description = fields.Text(string='Descripción del procedimiento')

    result = fields.Text(string='Resultado')

    state = fields.Selection(selection=[
        ('draft', 'Borrador'),
        ('in_progress', 'En Proceso'),
        ('done', 'Finalizado'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', default='draft')

    @api.constrains('surgery_date')
    def _check_surgery_date(self):
        for record in self:
            if record.surgery_date and record.surgery_date > fields.Datetime.now():
                raise ValidationError("La fecha de la cirugía no puede estar en el futuro.")

    def action_start(self):
        for record in self:
            record.state = 'in_progress'

    def action_done(self):
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'
