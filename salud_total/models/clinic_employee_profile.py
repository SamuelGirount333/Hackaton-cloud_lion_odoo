from  odoo import api, fields, models 
from odoo.exceptions import ValidationError

class clinic_employee_profile(models.Model):
    _name = "clinic_employee_profile"
    _description = "Modulo de gestion de perfiles en la clinica"

    name = fields.Char(string="Nombre del empleado", required=True)
    identification = fields.Integer(string="Numero de indentificacion", required=True)
    
    clinic_rol_care = fields.Selection(selection=[
            ("nursing_assistant", "Auxiliar de enfermería"),
            ("practical_nurse", "Enfermero(a) profesional"),
            ("general_practitioner", "Médico general"),
            ("specialist", "Especialista"),
            ("surgeon", "Cirujano"),
            ("anesthesiologist", "Anestesiólogo")
        ],required=True, string="Rol Asistencial")
    
    clinic_rol_administrative = fields.Selection(selection=[
            ("receptionist", "Recepcionista"),
            ("counter", "Contador"),
            ("human_resources", "Recursos Humanos"),
            ("logistics_supplies", "Logistica insumos"),
        ], required=True, string="Rol Administrativo"
    )

    in_date = fields.Date(string="Fecha de ingreso")
    specialty = fields.Char(string="Especialidad del Medico")
    email = fields.Char(string="Correo Electronico")
    phone = fields.Char(string="Telefono de contacto")
    
    department = fields.Selection(selection=[
            ("care", "Cuerpo Asitencial"),
            ("administrative", "Cuerpo Administrativo")])
    
    is_doctor = fields.Boolean(string="¿Es Médico?", compute="_compute_is_doctor", store=True)

    @api.constrains("clinic_rol_care", "clinic_rol_administrative", "department", "specialty")
    def _check_roles_and_department(self):
        for record in self:
            
            if record.clinic_rol_care and record.clinic_rol_administrative:
                raise ValidationError("No puedes asignar un rol asistencial y uno administrativo al mismo tiempo.")
            
            if record.clinic_rol_care and record.department != "care":
                raise ValidationError("El rol asistencial solo puede usarse si el departamento es 'Cuerpo Asistencial'.")
            
            if record.clinic_rol_administrative and record.department != "administrative":
                raise ValidationError("El rol administrativo solo puede usarse si el departamento es 'Cuerpo Administrativo'.")
            
            medical_roles = ["general_practitioner", "specialist", "surgeon", "anesthesiologist"]
            if record.clinic_rol_care in medical_roles and not record.specialty:
                raise ValidationError("Los roles médicos requieren una especialidad registrada.")

    @api.depends('clinic_rol_care')
    def _compute_is_doctor(self):
        medical_roles = ["general_practitioner", "specialist", "surgeon", "anesthesiologist"]
        for record in self:
            record.is_doctor = record.clinic_rol_care in medical_roles
