# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "mfg_engine"
app_title = "Erpnext Manufacturing Workorder Jobcard Engine"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Manufacturing Workorder Jobcard Engine - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/mfg_engine/css/mfg_engine.bundle.css"
app_include_js = "/assets/mfg_engine/js/mfg_engine.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Erpnext Manufacturing Workorder Jobcard Engine Entry": {
        "validate": "mfg_engine.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "mfg_engine.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "mfg_engine.tasks.hourly_sync"
    ],
    "daily": [
        "mfg_engine.tasks.daily_reconciliation"
    ],
    "weekly": [
        "mfg_engine.tasks.weekly_digest"
    ]
}
