import unittest
from mfg_engine.engine import (
    ERPNextManufacturingEngine, BillOfMaterials, BOMItem, WorkstationOperation,
    WorkOrderRecord, JobCardRecord
)

class TestManufacturingEngine(unittest.TestCase):
    def test_bom_costing(self):
        engine = ERPNextManufacturingEngine()
        raw_materials = [
            BOMItem("RAW-STEEL", "Steel Sheet 2mm", 2.5, 120.0, scrap_pct=2.0),
            BOMItem("RAW-SCREW", "M6 Hex Bolt", 8.0, 5.0)
        ]
        operations = [
            WorkstationOperation("CNC Cutting", "CNC Workstation 1", 300.0, 15.0), # 0.25h * 300 = 75
            WorkstationOperation("Powder Coating", "Paint Booth", 200.0, 30.0)    # 0.5h * 200 = 100
        ]
        bom = BillOfMaterials("BOM-CABINET-01", "FG-CABINET", "Server Cabinet 42U", 1.0, raw_materials, operations)
        compiled = engine.compile_bom_cost(bom)
        self.assertGreater(compiled.raw_material_cost, 340.0)
        self.assertEqual(compiled.operating_cost, 175.0)
        self.assertGreater(compiled.total_cost, 500.0)

    def test_work_order_raw_material_explosion(self):
        engine = ERPNextManufacturingEngine()
        raw_materials = [BOMItem("RAW-COPPER", "Copper Wire", 0.5, 600.0)]
        bom = BillOfMaterials("BOM-MOTOR-01", "FG-MOTOR", "Electric Motor 1HP", 1.0, raw_materials, [])
        needed = engine.explode_raw_materials_for_plan(bom, order_qty=50.0)
        self.assertEqual(needed["RAW-COPPER"], 25.0)

if __name__ == "__main__":
    unittest.main()
