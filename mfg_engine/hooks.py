# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "mfg_engine"
app_title = "Erpnext Manufacturing Workorder Jobcard Engine"
app_publisher = "Shyamkumar Pandey"
app_description = "Erpnext Manufacturing Workorder Jobcard Engine for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/mfg_engine/css/mfg_engine.bundle.css"
app_include_js = "/assets/mfg_engine/js/mfg_engine.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "mfg_engine.engine.on_document_submit",
        "on_cancel": "mfg_engine.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "mfg_engine.engine.daily_scheduled_sync"
    ]
}
