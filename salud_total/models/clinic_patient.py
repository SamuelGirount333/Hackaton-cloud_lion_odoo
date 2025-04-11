from odoo import api, models, fields

class clinic_patient(models.Model):
    _name =  "clinic_patient"
    _description = "Datos personales y de salud del cliente"

    history = fields.One2many("clinic_clinical_record", "patient_id", string="Historia clinica del paciente")

    name = fields.Char(string="Nombre completo del paciente", required=True)
    identificacion = fields.Integer(string="Identificacion del paciente", required=True)
    birth_date = fields.Date(string="Fecha de Nacimiento", required=True)
    age = fields.Integer(string="Edad", compute="_compute_age", required=True)
    
    sex = fields.Selection(selection=[
            ("male", "Masculino"),
            ("female", "Femenino"),])

    phone = fields.Char(string="Telefono de contacto", required=True)
    email = fields.Char(string="Correo electronico", required=True)
    address = fields.Text(string="Direccion Paciente", required=True)
    eps = fields.Char(string="E.P.S - Opcional")

    alergies = fields.Text(string="Alergias del paciente")
    previus_condition = fields.Text(string="Enfermedades del paciente")
    depend_medicine = fields.Boolean(string="Depende de algun medicameto", required=True)
    type_medicine = fields.Text(string="Cual medicamento depende?")

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                record.age = today.year - record.birth_date.year - (
                    (today.month, today.day) < (record.birth_date.month, record.birth_date.day)
                )
            else:
                record.age = 0
                