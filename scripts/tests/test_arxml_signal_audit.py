"""Small regression tests for the read-only ARXML audit helper."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import arxml_signal_audit as audit_tool


SAMPLE = """<?xml version="1.0" encoding="UTF-8"?>
<AUTOSAR xmlns="http://autosar.org/schema/r4.0">
  <AR-PACKAGES>
    <AR-PACKAGE>
      <SHORT-NAME>Demo</SHORT-NAME>
      <ELEMENTS>
        <I-SIGNAL>
          <SHORT-NAME>VehicleSpeed</SHORT-NAME>
          <LENGTH>16</LENGTH>
        </I-SIGNAL>
        <I-SIGNAL-I-PDU>
          <SHORT-NAME>VehicleStatusPdu</SHORT-NAME>
          <I-SIGNAL-TO-I-PDU-MAPPINGS>
            <I-SIGNAL-TO-I-PDU-MAPPING>
              <SHORT-NAME>VehicleSpeedMapping</SHORT-NAME>
              <I-SIGNAL-REF DEST="I-SIGNAL">/Demo/VehicleSpeed</I-SIGNAL-REF>
              <START-POSITION>0</START-POSITION>
              <PACKING-BYTE-ORDER> MOST-SIGNIFICANT-BYTE-LAST </PACKING-BYTE-ORDER>
            </I-SIGNAL-TO-I-PDU-MAPPING>
          </I-SIGNAL-TO-I-PDU-MAPPINGS>
        </I-SIGNAL-I-PDU>
      </ELEMENTS>
    </AR-PACKAGE>
  </AR-PACKAGES>
</AUTOSAR>
"""


class ArxmlAuditTests(unittest.TestCase):
    def test_namespaced_signal_and_mapping_are_indexed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "sample.arxml"
            source.write_text(SAMPLE, encoding="utf-8")
            objects, refs, index = audit_tool.parse_inputs([source])
            names = {item["short_name"] for item in objects}
            self.assertIn("VehicleSpeed", names)
            self.assertIn("VehicleStatusPdu", names)
            self.assertIn("VehicleSpeedMapping", names)
            self.assertIn("/Demo/VehicleSpeed", index)
            self.assertEqual(len(index["/Demo/VehicleSpeed"]), 1)
            mapping = next(item for item in objects if item["object_type"] == "I-SIGNAL-TO-I-PDU-MAPPING")
            self.assertEqual(mapping["parent_path"], "/Demo/VehicleStatusPdu")
            self.assertEqual(mapping["start_position"], "0")
            self.assertEqual(len([r for r in refs if r["reference"] == "/Demo/VehicleSpeed"]), 1)
            findings = audit_tool.audit(objects, refs, index)
            self.assertFalse([f for f in findings if f["rule"] == "UNRESOLVED_REFERENCE"])

    def test_missing_absolute_reference_is_reported(self):
        refs = [{
            "source_file": "sample.arxml",
            "object_path": "VehicleSpeedMapping",
            "reference_type": "I-SIGNAL-REF",
            "reference": "/Missing/Signal",
        }]
        findings = audit_tool.audit([], refs, {})
        self.assertEqual(findings[0]["rule"], "UNRESOLVED_REFERENCE")
        self.assertEqual(findings[0]["severity"], "WARN")


if __name__ == "__main__":
    unittest.main()
