from odoo import api, models, fields
from odoo.exceptions import ValidationError

class clinic_medical_consult(models.Model):
    _name = 'clinic_medical_consult'
    _description = 'Consulta Médica'
    _order = 'consultation_date desc'

    name = fields.Char(string='Código', required=True, copy=False)
    
    patient_id = fields.Many2one('clinic_patient', string='Paciente', required=True)    
    doctor_id = fields.Many2one('clinic_employee_profile', string='Doctor(a)',required=True, domain="[('is_doctor','=',True)]")    
    appointment_id = fields.Many2one('clinic_appointment', string='Cita médica', required=True)
    
    consultation_date = fields.Datetime(string='Fecha de consulta', default=fields.Datetime.now, required=True)
    symptoms = fields.Text(string='Síntomas')
    diagnosis = fields.Text(string='Diagnóstico')
    treatment = fields.Text(string='Tratamiento')
    observations = fields.Text(string='Observaciones')

    state = fields.Selection(selection=[
        ('draft', 'Borrador'),
        ('in_consultation', 'En Consulta'),
        ('done', 'Finalizada'),
        ('cancelled', 'Cancelada'),
    ], string='Estado', default='draft')

    @api.constrains('consultation_date')
    def _check_consultation_date(self):
        for record in self:
            if record.consultation_date and record.consultation_date > fields.Datetime.now():
                raise ValidationError("La fecha de consulta no puede ser en el futuro.")

    def action_start_consultation(self):
        for record in self:
            record.state = 'in_consultation'

    def action_done(self):
        for record in self:
            record.state = 'done'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'