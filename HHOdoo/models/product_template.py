from odoo import api, fields, models


class HhArticle(models.Model):
    _name = "hh.article"
    _description = "H&H Artikel / Text"
    _rec_name = "name"
    _order = "article_number, name"

    name = fields.Char(string="Bezeichnung", required=True, index=True)
    active = fields.Boolean(string="Archiv", default=True)
    article_number = fields.Char(string="Artikelnummer", required=True, copy=False, index=True)
    article_type = fields.Selection(
        [("article", "Artikel"), ("text", "Text")],
        string="Typ",
        default="article",
        required=True,
    )
    category_id = fields.Many2one(
        "hh.product.category",
        string="Warengruppe",
        index=True,
        ondelete="restrict",
    )
    is_favorite = fields.Boolean(string="Favorit")
    is_hidden = fields.Boolean(string="Verborgen")
    description = fields.Text(string="Beschreibung")
    long_description = fields.Html(string="Langtext")
    property_type = fields.Selection(
        [("select", "Selektartikel"), ("standard", "Standardartikel"), ("service", "Dienstleistung")],
        string="Eigenschaft",
        default="standard",
    )
    unit_name = fields.Char(string="Mengeneinheit", default="Stück")
    barcode = fields.Char(string="EAN")
    webshop = fields.Boolean(string="Im WebShop")
    report_visible = fields.Boolean(string="Im Report anzeigen", default=True)
    sale_price = fields.Monetary(string="Verkaufspreis (Netto)", currency_field="currency_id")
    purchase_price = fields.Monetary(string="Einkaufspreis (Netto)", currency_field="currency_id")
    sale_tax_rate = fields.Float(string="MwSt. Verkauf (%)", default=19.0)
    purchase_tax_rate = fields.Float(string="MwSt. Einkauf (%)", default=19.0)
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
    length = fields.Float(string="Länge")
    width = fields.Float(string="Breite")
    thickness = fields.Float(string="Dicke")
    volume = fields.Float(string="Volumen (m³)")
    weight = fields.Float(string="Gewicht (kg)")
    waste_allowance = fields.Float(string="Verschnitt / Zugabe (%)")
    image_1920 = fields.Binary(string="Bild", attachment=True)
    supplier_ids = fields.One2many("hh.article.supplier", "article_id", string="Lieferanten")
    stock_ids = fields.One2many("hh.article.stock", "article_id", string="Lagerbestand")
    time_ids = fields.One2many("hh.article.time", "article_id", string="Zeiten")
    stock_quantity = fields.Float(string="Lagerbestand", compute="_compute_totals")
    min_stock_quantity = fields.Float(string="Mindestlagerbestand", compute="_compute_totals")
    total_minutes = fields.Integer(string="Gesamtminuten", compute="_compute_totals")
    total_time_cost = fields.Monetary(string="Gesamtkosten Zeiten", compute="_compute_totals", currency_field="currency_id")
    project_count = fields.Integer(string="Projekte", default=0)
    document_count = fields.Integer(string="Dokumente", default=0)
    invoice_count = fields.Integer(string="Rechnungen", default=0)
    document_notes = fields.Text(string="Dokumenthinweise")

    _sql_constraints = [
        ("article_number_unique", "unique(article_number)", "Die Artikelnummer muss eindeutig sein."),
    ]

    @api.depends(
        "stock_ids.quantity",
        "stock_ids.minimum_quantity",
        "time_ids.minutes",
        "time_ids.cost",
    )
    def _compute_totals(self):
        for article in self:
            article.stock_quantity = sum(article.stock_ids.mapped("quantity"))
            article.min_stock_quantity = sum(article.stock_ids.mapped("minimum_quantity"))
            article.total_minutes = sum(article.time_ids.mapped("minutes"))
            article.total_time_cost = sum(article.time_ids.mapped("cost"))


class HhArticleSupplier(models.Model):
    _name = "hh.article.supplier"
    _description = "H&H Artikellieferant"
    _order = "is_primary desc, partner_id"

    article_id = fields.Many2one("hh.article", string="Artikel", required=True, ondelete="cascade")
    partner_id = fields.Many2one("res.partner", string="Lieferant", required=True)
    price = fields.Float(string="EK-Preis (Netto)")
    minimum_quantity = fields.Float(string="Min. Menge")
    packaging_unit = fields.Char(string="Verpackungseinheit")
    delivery_days = fields.Integer(string="Lieferzeit (Tage)")
    supplier_product_code = fields.Char(string="Bestellnummer")
    order_text = fields.Text(string="Bestelltext")
    note = fields.Text(string="Bemerkung")
    is_primary = fields.Boolean(string="Hauptlieferant")


class HhArticleStock(models.Model):
    _name = "hh.article.stock"
    _description = "H&H Artikelbestand"
    _order = "warehouse_name, location_name"

    article_id = fields.Many2one("hh.article", string="Artikel", required=True, ondelete="cascade")
    warehouse_name = fields.Char(string="Lager", required=True)
    location_name = fields.Char(string="Lagerstellplatz")
    quantity = fields.Float(string="Menge")
    minimum_quantity = fields.Float(string="Mindestlagerbestand")


class HhArticleTime(models.Model):
    _name = "hh.article.time"
    _description = "H&H Artikelzeit"
    _order = "sequence, id"

    article_id = fields.Many2one("hh.article", string="Artikel", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    minutes = fields.Integer(string="Minuten", required=True, default=0)
    work_type = fields.Char(string="Arbeitsart", required=True)
    cost = fields.Float(string="Kosten")