/** @odoo-module **/

import { Component, onWillUnmount, useRef, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class HHOdooDashboard extends Component {
    static template = "HHOdoo.Dashboard";

    setup() {
        this.actionService = useService("action");
        this.workspaceRef = useRef("workspace");
        this.toolboxRef = useRef("toolbox");
        this.dragState = null;
        this.state = useState({
            activeModule: "Projektmanager",
            activeToolboxTab: "utilities",
            toolboxVisible: true,
            toolboxLeft: 7,
            toolboxTop: 7,
            statusMessage: "Dieses Produkt ist lizenziert.",
        });
        this.onPointerMove = this.onPointerMove.bind(this);
        this.onPointerUp = this.onPointerUp.bind(this);
        onWillUnmount(() => this.stopDragging());
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

    startDragging(event) {
        if (event.target.closest("button")) {
            return;
        }
        const toolboxRect = this.toolboxRef.el.getBoundingClientRect();
        this.dragState = {
            offsetX: event.clientX - toolboxRect.left,
            offsetY: event.clientY - toolboxRect.top,
        };
        event.currentTarget.setPointerCapture(event.pointerId);
        window.addEventListener("pointermove", this.onPointerMove);
        window.addEventListener("pointerup", this.onPointerUp, { once: true });
    }

    onPointerMove(event) {
        if (!this.dragState) {
            return;
        }
        const workspaceRect = this.workspaceRef.el.getBoundingClientRect();
        const toolboxRect = this.toolboxRef.el.getBoundingClientRect();
        const maxLeft = Math.max(0, workspaceRect.width - toolboxRect.width);
        const maxTop = Math.max(0, workspaceRect.height - toolboxRect.height);
        this.state.toolboxLeft = Math.min(maxLeft, Math.max(0, event.clientX - workspaceRect.left - this.dragState.offsetX));
        this.state.toolboxTop = Math.min(maxTop, Math.max(0, event.clientY - workspaceRect.top - this.dragState.offsetY));
    }

    onPointerUp() {
        this.stopDragging();
    }

    stopDragging() {
        this.dragState = null;
        window.removeEventListener("pointermove", this.onPointerMove);
        window.removeEventListener("pointerup", this.onPointerUp);
    }
}

registry.category("actions").add("hh_odoo.dashboard", HHOdooDashboard);
