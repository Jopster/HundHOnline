from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    hh_article_number = fields.Char(string="Artikelnummer", copy=False, index=True)
    hh_category_id = fields.Many2one(
        "hh.product.category",
        string="Warengruppe",
        index=True,
        ondelete="restrict",
    )
    hh_is_article = fields.Boolean(string="Ist Artikel", default=True)
    hh_long_description = fields.Html(string="Langtext")
    hh_property = fields.Selection(
        [("select", "Selektartikel"), ("standard", "Standardartikel"), ("service", "Dienstleistung")],
        string="Eigenschaft",
        default="standard",
    )
    hh_webshop = fields.Boolean(string="Im WebShop")
    hh_report_visible = fields.Boolean(string="Im Report anzeigen", default=True)
    hh_length = fields.Float(string="Länge")
    hh_width = fields.Float(string="Breite")
    hh_thickness = fields.Float(string="Dicke")
    hh_volume = fields.Float(string="Volumen (m³)")
    hh_weight = fields.Float(string="Gewicht (kg)")
    hh_waste_allowance = fields.Float(string="Verschnitt / Zugabe (%)")
    hh_supplier_ids = fields.One2many("hh.product.supplier", "product_tmpl_id", string="Lieferanten")
    hh_stock_ids = fields.One2many("hh.product.stock", "product_tmpl_id", string="Lagerbestand")
    hh_time_ids = fields.One2many("hh.product.time", "product_tmpl_id", string="Zeiten")
    hh_stock_quantity = fields.Float(string="Lagerbestand", compute="_compute_hh_totals")
    hh_min_stock_quantity = fields.Float(string="Mindestlagerbestand", compute="_compute_hh_totals")
    hh_total_minutes = fields.Integer(string="Gesamtminuten", compute="_compute_hh_totals")
    hh_total_time_cost = fields.Float(string="Gesamtkosten Zeiten", compute="_compute_hh_totals")
    hh_project_count = fields.Integer(string="Projekte", default=0)
    hh_document_count = fields.Integer(string="Dokumente", default=0)
    hh_invoice_count = fields.Integer(string="Rechnungen", default=0)
    hh_document_notes = fields.Text(string="Dokumenthinweise")

    _sql_constraints = [
        ("hh_article_number_unique", "unique(hh_article_number)", "Die Artikelnummer muss eindeutig sein."),
    ]

    @api.depends(
        "hh_stock_ids.quantity",
        "hh_stock_ids.minimum_quantity",
        "hh_time_ids.minutes",
        "hh_time_ids.cost",
    )
    def _compute_hh_totals(self):
        for product in self:
            product.hh_stock_quantity = sum(product.hh_stock_ids.mapped("quantity"))
            product.hh_min_stock_quantity = sum(product.hh_stock_ids.mapped("minimum_quantity"))
            product.hh_total_minutes = sum(product.hh_time_ids.mapped("minutes"))
            product.hh_total_time_cost = sum(product.hh_time_ids.mapped("cost"))


class HhProductSupplier(models.Model):
    _name = "hh.product.supplier"
    _description = "H&H Artikellieferant"
    _order = "is_primary desc, partner_id"

    product_tmpl_id = fields.Many2one("product.template", string="Artikel", required=True, ondelete="cascade")
    partner_id = fields.Many2one("res.partner", string="Lieferant", required=True)
    price = fields.Float(string="EK-Preis (Netto)")
    minimum_quantity = fields.Float(string="Min. Menge")
    packaging_unit = fields.Char(string="Verpackungseinheit")
    delivery_days = fields.Integer(string="Lieferzeit (Tage)")
    supplier_product_code = fields.Char(string="Bestellnummer")
    order_text = fields.Text(string="Bestelltext")
    note = fields.Text(string="Bemerkung")
    is_primary = fields.Boolean(string="Hauptlieferant")


class HhProductStock(models.Model):
    _name = "hh.product.stock"
    _description = "H&H Artikelbestand"
    _order = "warehouse_name, location_name"

    product_tmpl_id = fields.Many2one("product.template", string="Artikel", required=True, ondelete="cascade")
    warehouse_name = fields.Char(string="Lager", required=True)
    location_name = fields.Char(string="Lagerstellplatz")
    quantity = fields.Float(string="Menge")
    minimum_quantity = fields.Float(string="Mindestlagerbestand")


class HhProductTime(models.Model):
    _name = "hh.product.time"
    _description = "H&H Artikelzeit"
    _order = "sequence, id"

    product_tmpl_id = fields.Many2one("product.template", string="Artikel", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    minutes = fields.Integer(string="Minuten", required=True, default=0)
    work_type = fields.Char(string="Arbeitsart", required=True)
    cost = fields.Float(string="Kosten")