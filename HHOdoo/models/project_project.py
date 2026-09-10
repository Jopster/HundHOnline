from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    hh_reference = fields.Char(string="H&H Referenz", copy=False, index=True)
    hh_contact_id = fields.Many2one(
        "res.partner",
        string="Ansprechpartner",
        tracking=True,
    )
    hh_target_date = fields.Date(string="Zieltermin", tracking=True)
    hh_status = fields.Selection(
        [
            ("draft", "Entwurf"),
            ("active", "In Bearbeitung"),
            ("waiting", "Wartend"),
            ("done", "Abgeschlossen"),
        ],
        string="H&H Status",
        default="draft",
        required=True,
        tracking=True,
    )
    hh_event_ids = fields.One2many(
        "hh.project.event",
        "project_id",
        string="Termine",
    )
    hh_event_count = fields.Integer(compute="_compute_hh_event_count")

    def _compute_hh_event_count(self):
        for project in self:
            project.hh_event_count = len(project.hh_event_ids)

    def action_view_hh_events(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id(
            "HHOdoo.action_hh_project_events"
        )
        action["domain"] = [("project_id", "=", self.id)]
        action["context"] = {"default_project_id": self.id}
        return action