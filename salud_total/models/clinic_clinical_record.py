from  odoo import api, models, fields
from  odoo.exceptions import ValidationError


class clinic_clinical_record(models.Model):
    _name = "clinic_clinical_record"
    _description = "Informacion del ingreso del paciente"

    patient_id = fields.Many2one("clinic_patient", string="Relacion con paciente")
    employee_id = fields.Many2one("clinic_employee_profile", string="Responsable")
    
    record_date = fields.Date(string="Fecha de apertura", default=fields.Date.today, required=True)
    attention_type = fields.selection(
        selection=[
            ("consultation", "Consulta Externa"),
            ("surgery", "Cirugia"),
            ("emergency", "Urgencias")
        ], string="Tipo de Atencion medica", required=True)
    status = fields.selection(
        selection=[
            ("in_progess", "En Proceso"),
            ("finished", "Finalizada"),
            ("canceled", "Cancelada")
        ], string="Estado de la consulta", required=True)


    @api.constrains("status")
    def _check_open_history(self):
        for record in self:
            if record.status == "in_progess":
                registros= self.env['clinic_clinical_record'].search([
                ("patient_id", "=", record.patient_id.id),
                ("status", "=", "in_progress"),
                ("id", "!=", record.id)
                ])
                if registros:
                    raise ValidationError("El paciente ya cuenta con una Historia abierta.")

    @api.constrains("record_date")
    def _check_recor_date(self):
        for record in self:
            if record.record_date > fields.Date.today():
                raise ValidationError("La fecha de apertura no puede contener datos futuros ")