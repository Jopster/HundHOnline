from odoo import fields, models


class HhProjectEvent(models.Model):
    _name = "hh.project.event"
    _description = "H&H Projekttermin"
    _order = "date_start desc, id desc"

    name = fields.Char(string="Bezeichnung", required=True)
    project_id = fields.Many2one(
        "project.project",
        string="Projekt",
        required=True,
        ondelete="cascade",
        index=True,
    )
    date_start = fields.Datetime(string="Termin", required=True, default=fields.Datetime.now)
    date_end = fields.Datetime(string="Ende")
    event_type = fields.Selection(
        [
            ("appointment", "Termin"),
            ("milestone", "Meilenstein"),
            ("note", "Notiz"),
        ],
        string="Typ",
        default="appointment",
        required=True,
    )
    responsible_id = fields.Many2one(
        "res.users",
        string="Verantwortlich",
        default=lambda self: self.env.user,
    )
    description = fields.Html(string="Beschreibung")
    active = fields.Boolean(default=True)