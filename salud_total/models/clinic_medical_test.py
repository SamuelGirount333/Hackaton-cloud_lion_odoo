from odoo import api, models, fields 
from odoo.exceptions import ValidationError

class clinic_medical_test(models.Model):
    _name = 'clinic_medical_test'
    _description = 'Examen Médico'
    _order = 'request_date desc'

    name = fields.Char(string='Código', required=True, readonly=True, copy=False, 
                        default=lambda self: self.env['ir.sequence'].next_by_code('clinic_medical_test'))

    patient_id = fields.Many2one('clinic_patient', string='Paciente', required=True)
    doctor_id = fields.Many2one('clinic_employee_profile', string='Médico Solicitante', required=True, domain=[('is_doctor', '=', True)])
    
    test_type = fields.Selection(selection=[
        ('blood', 'Análisis de sangre'),
        ('urine', 'Análisis de orina'),
        ('xray', 'Radiografía'),
        ('mri', 'Resonancia magnética'),
        ('ecg', 'Electrocardiograma'),
        ('other', 'Otro'),
    ], string='Tipo de Examen', required=True)
    
    description = fields.Text(string='Descripción')
    request_date = fields.Date(string='Fecha de Solicitud', default=fields.Date.today, required=True)
    result_date = fields.Date(string='Fecha de Resultado')
    result = fields.Text(string='Resultado del Examen')

    state = fields.Selection(selection=[
        ('requested', 'Solicitado'),
        ('in_process', 'En proceso'),
        ('completed', 'Completado'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', default='requested')

    def action_process(self):
        for record in self:
            record.state = 'in_process'

    def action_complete(self):
        for record in self:
            record.state = 'completed'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    @api.constrains('result_date')
    def _check_result_date(self):
        for record in self:
            if record.result_date and record.result_date < record.request_date:
                raise ValidationError('La fecha de resultado no puede ser anterior a la fecha de solicitud.')
