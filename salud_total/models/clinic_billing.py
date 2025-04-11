from odoo import api, models, fields
from odoo.exceptions import ValidationError

class clinic_billing(models.Model):
    _name = 'clinic_billing'
    _description = 'Facturación Clínica'
    _order = 'billing_date desc'

    name = fields.Char(string='Factura N°', required=True, readonly=True, copy=False,
                        default=lambda self: self.env['ir.sequence'].next_by_code('clinic.billing'))
    """
<odoo>
    <data noupdate="1">
        <record id="seq_clinic_billing" model="ir.sequence">
            <field name="name">Factura Clínica</field>
            <field name="code">clinic.billing</field>
            <field name="prefix">BILL-</field>
            <field name="padding">5</field>
            <field name="number_next">1</field>
            <field name="number_increment">1</field>
        </record>
    </data>
</odoo>

    """

    patient_id = fields.Many2one('clinic_patient', string='Paciente', required=True)
    consultation_id = fields.Many2one('clinic_medical_consult', string='Consulta Médica', required=True)
    billing_date = fields.Date(string='Fecha de Facturación', default=fields.Date.today, required=True)
    amount = fields.Float(string='Total a Pagar', required=True)

    state = fields.Selection(selection=[
        ('draft', 'Borrador'),
        ('paid', 'Pagado'),
        ('cancelled', 'Cancelado')
    ], string='Estado', default='draft')

    def action_paid(self):
        for record in self:
            record.state = 'paid'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    @api.constrains('amount')
    def _check_amount_positive(self):
        for record in self:
            if record.amount <= 0:
                raise ValidationError("El monto de la factura debe ser mayor a cero.")
