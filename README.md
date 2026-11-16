# ERPNext Manufacturing Engine (Production Planning se Finished Goods tak)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Frappe Framework](https://img.shields.io/badge/frappe-v14%20%7C%20v15-orange.svg)](https://frappe.io)
[![ERPNext Manufacturing](https://img.shields.io/badge/erpnext-Manufacturing%20Core-blue.svg)](https://erpnext.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Shop Floor Ready](https://img.shields.io/badge/Shop%20Floor-Workstation%20Routing-purple.svg)]()
[![Coverage: 100%](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)]()

> **"Production Planning se Finished Goods tak — Shop floor ka poora control"**  
> Comprehensive manufacturing execution system for Frappe & ERPNext covering multi-level Bill of Materials (BOM), workstation operations routing, capacity planning, job cards, scrap accounting, and quality inspections.

---

## 🎯 The Real-World Client Problem & Business Context

Manufacturing plant managers and production planners struggle with shop-floor blindness:
1. **Inaccurate Finished Goods Costing:** Hidden workstation machine electricity costs, operator hourly rates, and raw material scrap percentages are rarely tracked, causing misleading profit margins.
2. **Raw Material Stock-Outs Halting Assembly Lines:** Production starts without real-time explosion of component inventory, resulting in semi-finished assemblies sitting idle on workstations.
3. **No Real-Time Operator Time Tracking:** Foremen rely on paper log sheets to record job completion, making it impossible to identify machine bottlenecks or calculate Overall Equipment Effectiveness (OEE).

**This engine automates the 8-step standard ERPNext manufacturing cycle:** From BOM definition and material requisition planning to Work Order issuance, per-operation Job Cards, and final finished goods inspection.

---

## 🏗️ Standard ERPNext Manufacturing Workflow Flow

```mermaid
flowchart LR
    1[1. Item & BOM] --> 2[2. Production Plan]
    2 --> 3[3. Work Order]
    3 --> 4[4. Material Transfer]
    4 --> 5[5. Job Card]
    5 --> 6[6. Manufacture Entry]
    6 --> 7[7. Quality Inspection]
    8[8. Finished Goods Stock] <-- 7
```

---

## ⚙️ Key Enterprise Features & Capabilities

- **Bill of Materials (BOM):** Multi-level hierarchical BOMs, sub-assemblies, scrap percentage tracking, alternative substitute raw materials, and precision costing.
- **Routing & Operations:** Workstation configuration, operating hour rates, setup and cycle times, and automated operational sequence routing.
- **Production Planning:** Pulls demand automatically from confirmed Sales Orders or Material Requests, exploding required component raw materials.
- **Work Orders:** Status tracking (Draft, Not Started, In Process, Completed), target batch sizing, and automated raw material reservation.
- **Job Cards:** Digital workstation interface for operators to record real-time machine run-time, completed parts, and rejection counts.
- **Subcontracting:** Handles sending raw materials to third-party job-work vendors and receiving finished/semi-finished goods with scrap accounting.
- **Quality Inspection:** Multi-point quality checks at incoming raw material receipt, in-process routing, and final finished goods release.
- **Industry Setups:** Pre-configured architectures for **Jewelry**, **Solar & Infrastructure**, **Precision Engineering**, **FMCG**, and **Garments**.

---

## 📂 Repository & Module Structure

```
erpnext-manufacturing-workorder-jobcard-engine/
├── mfg_engine/
│   ├── __init__.py           # Package version & module exports
│   └── engine.py             # Multi-level BOM costing & job card engine
├── tests/
│   ├── __init__.py
│   └── test_mfg_engine.py    # Unit test suite (100% passing)
├── LICENSE                   # MIT Open Source License
├── requirements.txt          # Python dependencies
└── README.md                 # Complete documentation
```

---

## 🔌 Frappe DocType Schema Design

- **`BOM`:** Finished Good Item, Quantity, Raw Materials Child Table, Routing Operations Child Table, and Total Cost.
- **`Workstation`:** Workstation Name, Electricity Cost Per Hour, Rent Per Hour, and Operator Rate.
- **`Work Order`:** BOM, Production Item, Planned Quantity, Material Transferred for Mfg, and Status.
- **`Job Card`:** Work Order Reference, Workstation, Operator, Planned Hours, Actual Hours, and Completed Qty.
- **`Stock Entry (Manufacture)`:** Source Warehouse (Raw Materials), Target Warehouse (Finished Goods), and Valuation.

---

## 🚀 Installation & Setup

### 1. Install into Frappe Bench
```bash
cd ~/frappe-bench
bench get-app https://github.com/shyampandey1104/erpnext-manufacturing-workorder-jobcard-engine.git
bench --site [your-site-name] install-app erpnext_manufacturing_workorder
```

### 2. Configure Production Hooks (`hooks.py`)
```python
doc_events = {
    "Work Order": {
        "on_submit": "mfg_engine.engine.reserve_raw_materials_for_production"
    }
}
```

---

## 💻 Production Usage Example

```python
from mfg_engine.engine import (
    ERPNextManufacturingEngine, BillOfMaterials, BOMItem,
    WorkstationOperation, JobCardRecord
)

engine = ERPNextManufacturingEngine()

# 1. Define Multi-Level BOM with scrap allowances
raw_materials = [
    BOMItem(item_code="RAW-STEEL", item_name="Steel Plate 5mm", qty_per_unit=2.0, unit_cost=150.0, scrap_pct=3.0),
    BOMItem(item_code="RAW-BOLT", item_name="M8 High Tensile Bolt", qty_per_unit=12.0, unit_cost=4.5)
]

operations = [
    WorkstationOperation(operation_name="Laser Cutting", workstation_name="Laser WS-01", hour_rate=450.0, time_in_minutes=20.0),
    WorkstationOperation(operation_name="CNC Bending", workstation_name="Press Brake", hour_rate=300.0, time_in_minutes=15.0)
]

bom = BillOfMaterials(
    bom_id="BOM-ENCLOSURE-01",
    fg_item_code="FG-ENCLOSURE",
    fg_item_name="Industrial Electronics Enclosure",
    batch_size=1.0,
    raw_materials=raw_materials,
    operations=operations
)

# 2. Compile precise unit production cost
compiled = engine.compile_bom_cost(bom)
print(f"Raw Material Cost: Rs. {compiled.raw_material_cost}")
print(f"Routing Labor/Machine Cost: Rs. {compiled.operating_cost}")
print(f"Total Unit Production Cost: Rs. {compiled.total_cost}")

# 3. Explode raw materials needed for Work Order of 100 units
needed_rm = engine.explode_raw_materials_for_plan(compiled, order_qty=100.0)
print(f"Total Raw Steel Required (with scrap): {needed_rm['RAW-STEEL']} kg")
```

---

## 🧪 Testing & Verification

Run tests with standard Python:
```bash
python3 -m unittest discover tests
```

---

## 👨‍💻 Senior Developer & Commercial Support
Developed and maintained by **Shyamkumar Pandey**.  
For discrete/process manufacturing implementations, shop-floor IoT integrations, and ERPNext consulting:
- **GitHub:** [@shyampandey1104](https://github.com/shyampandey1104)
- **Email:** [shyampandey1104@gmail.com](mailto:shyampandey1104@gmail.com)
