from odoo import models, fields, api
from odoo.exceptions import ValidationError

class clinic_surgery_preparation(models.Model):
    _name = 'clinic_surgery_preparation'
    _description = 'Preparación para Cirugía'
    _order = 'scheduled_date desc'

    name = fields.Char(string='Código', required=True, readonly=True, copy=False,
        default=lambda self: self.env['ir.sequence'].next_by_code('clinic_surgery_preparation')
    )

    patient_id = fields.Many2one(
        'clinic_patient',
        string='Paciente',
        required=True
    )

    doctor_id = fields.Many2one(
        'clinic_employee_profile',
        string='Cirujano Responsable',
        required=True
    )

    scheduled_date = fields.Datetime(
        string='Fecha Programada',
        required=True
    )

    surgery_type = fields.Selection([
        ('cardiaca', 'Cirugía Cardíaca'),
        ('ortopedica', 'Cirugía Ortopédica'),
        ('neuro', 'Neurocirugía'),
        ('general', 'Cirugía General'),
        ('otra', 'Otra'),
    ], string='Tipo de Cirugía', required=True)
    
    fasting_required = fields.Boolean(string='Ayuno Requerido')
    fasting_hours = fields.Integer(string='Horas de Ayuno')
    allergies = fields.Text(string='Alergias')
    medications = fields.Text(string='Medicamentos Actuales')
    observations = fields.Text(string='Observaciones preoperatorias')
    
    consent_signed = fields.Boolean(string='Consentimiento Firmado', default=False)
    signature = fields.Binary(string='Firma de Consentimiento')
    
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('prepared', 'Preparado'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', default='draft')

    @api.constrains('scheduled_date')
    def _check_scheduled_date(self):
        for record in self:
            if record.scheduled_date and record.scheduled_date < fields.Datetime.now():
                raise ValidationError("No se puede programar una cirugía en el pasado.")

    def action_consent_(self):
        for record in self:
            if not record.consent_signed or not record.signature:
                raise ValidationError("Debe firmarse el consentimiento antes de preparar la cirugía.")
            record.state = 'prepared'

    def action_prepare(self):
        for record in self:
            record.state = 'prepared'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'