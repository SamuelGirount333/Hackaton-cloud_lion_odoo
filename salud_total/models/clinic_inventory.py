from odoo import api, models, fields
from odoo.exceptions import ValidationError

class clinic_inventory(models.Model):
    _name = 'clinic_inventory'
    _description = 'Inventario Médico'

    name = fields.Char(string='Nombre del Producto', required=True)
    
    product_type = fields.Selection(selection=[
        ('medicine', 'Medicina'),
        ('equipment', 'Equipo Médico'),
        ('supply', 'Insumo Médico')
    ], string='Tipo de Producto', required=True)

    quantity = fields.Integer(string='Cantidad Disponible', default=0)
    unit = fields.Char(string='Unidad de Medida', default='unidades')
    expiration_date = fields.Date(string='Fecha de Vencimiento')
    is_expired = fields.Boolean(string='¿Vencido?', compute='_compute_is_expired', store=True)
    
    responsible_id = fields.Many2one('clinic_employee_profile', string='Responsable del Producto')

    @api.depends('expiration_date')
    def _compute_is_expired(self):
        today = fields.Date.today()
        for record in self:
            if record.expiration_date:
                record.is_expired = record.expiration_date < today
            else:
                record.is_expired = False

    @api.constrains('quantity')
    def _check_quantity(self):
        for record in self:
            if record.quantity < 0:
                raise ValidationError("La cantidad no puede ser negativa.")

