from odoo import fields, models


class HhProductCategory(models.Model):
    _name = "hh.product.category"
    _description = "H&H Warengruppe"
    _parent_name = "parent_id"
    _parent_store = True
    _order = "parent_path, name"

    name = fields.Char(string="Warengruppe", required=True, index=True)
    parent_id = fields.Many2one(
        "hh.product.category",
        string="Übergeordnete Warengruppe",
        index=True,
        ondelete="restrict",
    )
    parent_path = fields.Char(index=True)
    child_ids = fields.One2many("hh.product.category", "parent_id", string="Untergruppen")
    active = fields.Boolean(default=True)
    product_tmpl_ids = fields.One2many("product.template", "hh_category_id", string="Artikel")
    product_count = fields.Integer(compute="_compute_product_count")

    def _compute_product_count(self):
        for category in self:
            category.product_count = self.env["product.template"].search_count(
                [("hh_category_id", "child_of", category.id)]
            )

    def action_view_products(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("HHOdoo.action_hh_articles")
        action["domain"] = [("hh_category_id", "child_of", self.id)]
        action["context"] = {"default_hh_category_id": self.id}
        return action