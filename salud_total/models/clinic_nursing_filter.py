from odoo import api, fields, models
from odoo.exceptions import ValidationError

class clinic_nursing_filter(models.Model):
    _name = 'clinic_nursing_filter'
    _description = 'Filtro de Enfermería'
    _order = 'appointment_id'

    appointment_id = fields.Many2one('clinic_appointment', string='Cita médica',required=True)
    
    blood_pressure = fields.Char(string='Presión arterial') 
    heart_rate = fields.Integer(string='Frecuencia cardíaca (lpm)')
    respiratory_rate = fields.Integer(string='Frecuencia respiratoria (rpm)')
    temperature = fields.Float(string='Temperatura (°C)')
    weight = fields.Float(string='Peso (kg)')
    height = fields.Float(string='Estatura (cm)')
    bmi = fields.Float(string='IMC', compute='_compute_bmi', store=True) 
    notes = fields.Text(string='Observaciones')

    @api.depends('weight', 'height')    
    def _compute_bmi(self):
        for record in self:
            if record.weight and record.height:
                height_m = record.height / 100 
                record.bmi = round(record.weight / (height_m ** 2), 2)
            else:
                record.bmi = 0.0

    @api.constrains('temperature')
    def _check_temperature(self):
        for record in self:
            if record.temperature < 30 or record.temperature > 45:
                raise ValidationError("La temperatura ingresada no es válida.")