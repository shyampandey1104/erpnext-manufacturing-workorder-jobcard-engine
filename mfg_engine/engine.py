"""Complete ERPNext Manufacturing Engine (Production Planning se Finished Goods tak - Shop floor ka poora control)."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class BOMItem:
    item_code: str
    item_name: str
    qty_per_unit: float
    unit_cost: float
    scrap_pct: float = 0.0


@dataclass
class WorkstationOperation:
    operation_name: str
    workstation_name: str
    hour_rate: float
    time_in_minutes: float


@dataclass
class BillOfMaterials:
    bom_id: str
    fg_item_code: str
    fg_item_name: str
    batch_size: float
    raw_materials: List[BOMItem]
    operations: List[WorkstationOperation]
    operating_cost: float = 0.0
    raw_material_cost: float = 0.0
    total_cost: float = 0.0


@dataclass
class WorkOrderRecord:
    work_order_id: str
    bom_id: str
    fg_item_code: str
    planned_qty: float
    produced_qty: float = 0.0
    status: str = "DRAFT"  # DRAFT, NOT_STARTED, IN_PROCESS, COMPLETED, STOPPED


@dataclass
class JobCardRecord:
    job_card_id: str
    work_order_id: str
    operation_name: str
    workstation_name: str
    planned_qty: float
    completed_qty: float
    total_time_mins: float
    operator_name: str
    status: str = "OPEN"  # OPEN, WORK_IN_PROGRESS, COMPLETED


class ERPNextManufacturingEngine:
    """Production Planning, Multi-level BOM Costing & Job Card Execution Engine."""

    def compile_bom_cost(self, bom: BillOfMaterials) -> BillOfMaterials:
        """Calculates exact Raw Material Cost, Operating Routing Cost, and Total Unit Production Cost."""
        rm_total = 0.0
        for item in bom.raw_materials:
            effective_qty = item.qty_per_unit * (1.0 + (item.scrap_pct / 100.0))
            rm_total += effective_qty * item.unit_cost

        op_total = 0.0
        for op in bom.operations:
            op_cost = (op.time_in_minutes / 60.0) * op.hour_rate
            op_total += op_cost

        bom.raw_material_cost = round(rm_total, 2)
        bom.operating_cost = round(op_total, 2)
        bom.total_cost = round((rm_total + op_total) * bom.batch_size, 2)
        return bom

    def explode_raw_materials_for_plan(self, bom: BillOfMaterials, order_qty: float) -> Dict[str, float]:
        """Explodes required raw materials for a given Work Order quantity."""
        requirements: Dict[str, float] = {}
        for rm in bom.raw_materials:
            effective_qty = rm.qty_per_unit * (1.0 + (rm.scrap_pct / 100.0)) * order_qty
            requirements[rm.item_code] = round(effective_qty, 3)
        return requirements

    def complete_job_card(self, job_card: JobCardRecord, produced_qty: float, actual_mins: float) -> JobCardRecord:
        """Records workstation time and completed pieces on the shop-floor Job Card."""
        job_card.completed_qty = produced_qty
        job_card.total_time_mins = actual_mins
        job_card.status = "COMPLETED" if job_card.completed_qty >= job_card.planned_qty else "WORK_IN_PROGRESS"
        return job_card
