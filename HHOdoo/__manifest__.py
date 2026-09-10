{
    "name": "HHOdoo",
    "summary": "H&H project management extensions",
    "version": "18.0.1.0.0",
    "category": "Services/Project",
    "author": "H&H Software",
    "license": "LGPL-3",
    "depends": ["project", "contacts", "base_setup"],
    "data": [
        "security/ir.model.access.csv",
        "views/hh_project_event_views.xml",
        "views/project_project_views.xml",
        "views/res_config_settings_views.xml",
        "views/hh_odoo_menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "HHOdoo/static/src/js/hh_dashboard.js",
            "HHOdoo/static/src/xml/hh_dashboard.xml",
            "HHOdoo/static/src/css/hh_dashboard.css",
        ],
    },
    "application": True,
    "installable": True,
}