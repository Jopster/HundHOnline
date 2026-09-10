from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    hh_document_path = fields.Char(
        string="Dokumentenpfad",
        config_parameter="hh_odoo.document_path",
    )
    hh_maintenance_mode = fields.Boolean(
        string="Wartungsmodus",
        config_parameter="hh_odoo.maintenance_mode",
    )