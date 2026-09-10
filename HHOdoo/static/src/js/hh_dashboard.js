/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class HHOdooDashboard extends Component {
    static template = "HHOdoo.Dashboard";

    setup() {
        this.actionService = useService("action");
        this.state = useState({
            activeModule: "Projektmanager",
            activeToolboxTab: "utilities",
            toolboxVisible: true,
            statusMessage: "Dieses Produkt ist lizenziert.",
        });
    }

    selectModule(moduleName) {
        this.state.activeModule = moduleName;
        this.state.statusMessage = `${moduleName} wurde ausgewahlt.`;
    }

    selectToolboxTab(tabName) {
        this.state.activeToolboxTab = tabName;
        this.state.statusMessage = `${tabName === "utilities" ? "Dienstprogramme" : "Einstellungen"} wurde ausgewahlt.`;
    }

    openProjects() {
        this.actionService.doAction("HHOdoo.action_hh_projects");
    }

    openEvents() {
        this.actionService.doAction("HHOdoo.action_hh_project_events");
    }

    openSettings() {
        this.actionService.doAction("base_setup.action_general_configuration");
    }

    selectTool(toolName) {
        this.state.statusMessage = `${toolName} wurde ausgewahlt.`;
    }

    closeToolbox() {
        this.state.toolboxVisible = false;
        this.state.statusMessage = "Toolbox wurde geschlossen.";
    }
}

registry.category("actions").add("hh_odoo.dashboard", HHOdooDashboard);
