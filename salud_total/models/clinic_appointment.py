from  odoo import api, models, fields
from  odoo.exceptions import ValidationError

class clinic_appointment(models.Model):
    _name = 'clinic_appointment'
    _description = 'Citas médicas'
    _order = 'appointment_date desc'
    
    name = fields.Char(string='Referencia', required=True, copy=False, readonly=True,
    default=lambda self: self.env['ir.sequence'].next_by_code('clinic_appointment'))
    patient_id = fields.Many2one('clinic_patient', string='Paciente', required=True, ondelete='restrict')
    doctor_id = fields.Many2one('clinic_employee_profile', string='Médico', required=True, domain="[('is_doctor','=',True)]")
    appointment_date = fields.Datetime(string='Fecha y hora de la cita', required=True)
    notes = fields.Text(string='Notas')
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('scheduled', 'Programada'),
        ('done', 'Realizada'),
        ('cancelled', 'Cancelada')
    ], string='Estado', default='draft', tracking=True)

    duration = fields.Float(string='Duración estimada (horas)', default=1.0)
    priority = fields.Selection([
        ('0', 'Baja'),
        ('1', 'Normal'),
        ('2', 'Alta'),
        ('3', 'Urgente')
    ], string='Prioridad', default='1')
    
    @api.constrains('appointment_date')
    def _check_appointment_date(self):
        for record in self:
            if record.appointment_date and record.appointment_date < fields.Datetime.now(): 
                raise ValidationError('No se puede programar una cita en el pasado.')

    def action_schedule(self):
        for record in self:
            record.state = 'scheduled'

    def action_done(self):
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'