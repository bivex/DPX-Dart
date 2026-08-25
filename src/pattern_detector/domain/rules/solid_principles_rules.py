from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class MonolithicWidgetSrpRule(Rule):
    @property
    def name(self) -> str:
        return "MONOLITHIC_WIDGET_SRP"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.is_widget:
                    build_m = next((m for m in cls.methods if m.name == "build"), None)
                    if build_m and build_m.lines_count >= 80:
                        loc = SourceLocation(file_path=file.file_path, line_number=build_m.line_number)
                        ev = EvidenceItem(
                            rule_name="SOLID_SRP_MONOLITHIC_WIDGET",
                            weight=0.85,
                            description=f"Widget '{cls.name}.build()' spans {build_m.lines_count} lines (>80), violating SRP; decompose into sub-widgets",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.MONOLITHIC_WIDGET_SRP,
                                target_name=cls.name,
                                location=loc,
                                confidence=Confidence(0.85),
                                evidence=[ev],
                            )
                        )
        return detections


class GodClassServiceSrpRule(Rule):
    @property
    def name(self) -> str:
        return "GOD_CLASS_SERVICE_SRP"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if not cls.is_widget and cls.method_count >= 15:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="SOLID_SRP_GOD_CLASS_SERVICE",
                        weight=0.85,
                        description=f"Service class '{cls.name}' defines {cls.method_count} methods (>=15), violating Single Responsibility Principle",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.GOD_CLASS_SERVICE_SRP,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.85),
                            evidence=[ev],
                        )
                    )
        return detections


class FatAbstractInterfaceIspRule(Rule):
    @property
    def name(self) -> str:
        return "FAT_ABSTRACT_INTERFACE_ISP"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if (cls.is_abstract or cls.is_interface) and cls.method_count >= 12:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="SOLID_ISP_FAT_INTERFACE",
                        weight=0.85,
                        description=f"Abstract interface '{cls.name}' defines {cls.method_count} abstract methods (>=12), violating ISP",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.FAT_ABSTRACT_INTERFACE_ISP,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.85),
                            evidence=[ev],
                        )
                    )
        return detections
