from odoo import api, models, fields
from odoo.exceptions import ValidationError

class clinic_room_assignment(models.Model):
    _name = 'clinic_room_assignment'
    _description = 'Asignación de Habitación'
    _order = 'assignment_date desc'

    name = fields.Char(string='Código', required=True, readonly=True, copy=False,
                        default=lambda self: self.env['ir.sequence'].next_by_code('clinic_room_assignment'))

    patient_id = fields.Many2one('clinic_patient', string='Paciente', required=True)
    room_number = fields.Char(string='Número de Habitación', required=True)
    assignment_date = fields.Datetime(string='Fecha de asignación', required=True, default=fields.Datetime.now)
    release_date = fields.Datetime(string='Fecha de salida')
    is_active = fields.Boolean(string='Ocupada', compute='_compute_is_active', store=True)

    state = fields.Selection(selection=[
        ('assigned', 'Asignada'),
        ('released', 'Liberada'),
        ('cancelled', 'Cancelada')
    ], string='Estado', default='assigned')

    # Mira si la habitación sigue activa desde release_date
    @api.depends('release_date')
    def _compute_is_active(self):
        for record in self:
            record.is_active = not record.release_date

    def action_release(self):
        for record in self:
            record.state = 'released'
            record.release_date = fields.Datetime.now()

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'
            record.release_date = fields.Datetime.now()

    @api.constrains('assignment_date', 'release_date')
    def _check_dates(self):
        for record in self:
            if record.release_date and record.release_date < record.assignment_date:
                raise ValidationError("La fecha de salida no puede ser anterior a la fecha de asignación.")
