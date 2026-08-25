import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class AdapterTypeConverterRule(Rule):
    @property
    def name(self) -> str:
        return "ADAPTER_TYPE_CONVERTER"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                name_lower = cls.name.lower()
                has_adapter_method = any(m.name in ["toDomain", "toEntity", "fromDto", "adapt", "read", "write"] for m in cls.methods)
                if ("adapter" in name_lower or "converter" in name_lower or any("typeadapter" in i.lower() for i in cls.extends_class or "")) and (has_adapter_method or cls.method_count <= 4):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_ADAPTER_CONVERTER",
                        weight=0.90,
                        description=f"Class '{cls.name}' implements Adapter pattern converting between DTO and Domain entities",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.ADAPTER_TYPE_CONVERTER,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class BridgePlatformChannelRule(Rule):
    @property
    def name(self) -> str:
        return "BRIDGE_PLATFORM_CHANNEL"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        channel_pattern = re.compile(r'\bMethodChannel\s*\(|\bEventChannel\s*\(|\bBasicMessageChannel\s*\(', re.DOTALL)
        for file in model.files:
            for cls in file.classes:
                if channel_pattern.search(cls.raw_body):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_BRIDGE_PLATFORM_CHANNEL",
                        weight=0.92,
                        description=f"Class '{cls.name}' implements Bridge pattern communicating across Dart/Native boundaries via MethodChannel",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.BRIDGE_PLATFORM_CHANNEL,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class CompositeWidgetTreeRule(Rule):
    @property
    def name(self) -> str:
        return "COMPOSITE_WIDGET_TREE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.is_widget:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_COMPOSITE_WIDGET",
                        weight=0.95,
                        description=f"Widget '{cls.name}' ({cls.extends_class}) participates in Composite UI Element Tree",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.COMPOSITE_WIDGET_TREE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class DecoratorWrapperWidgetRule(Rule):
    @property
    def name(self) -> str:
        return "DECORATOR_WRAPPER_WIDGET"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_child = any(f.name == "child" and "widget" in f.type_annotation.lower() for f in cls.fields)
                if cls.is_widget and has_child and any(k in cls.name.lower() for k in ["wrapper", "decorator", "padding", "container", "themed", "styled"]):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_DECORATOR_WIDGET",
                        weight=0.90,
                        description=f"Widget '{cls.name}' decorates a child widget with additional visual or behavioral properties",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.DECORATOR_WRAPPER_WIDGET,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class FacadeApiClientRule(Rule):
    @property
    def name(self) -> str:
        return "FACADE_API_CLIENT"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                name_lower = cls.name.lower()
                if any(k in name_lower for k in ["apiclient", "networkclient", "facade", "repositoryimpl"]) and cls.method_count >= 3:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_FACADE_API_CLIENT",
                        weight=0.90,
                        description=f"Class '{cls.name}' provides unified Facade interface over multiple endpoints or data sources",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.FACADE_API_CLIENT,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class FlyweightConstInstanceRule(Rule):
    @property
    def name(self) -> str:
        return "FLYWEIGHT_CONST_INSTANCE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_const_ctor = any(c.is_const for c in cls.constructors) or "const " + cls.name + "(" in cls.raw_body
                if has_const_ctor:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_FLYWEIGHT_CONST_CTOR",
                        weight=0.92,
                        description=f"Class '{cls.name}' defines const constructor for canonical memory deduplication (Flyweight pattern)",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.FLYWEIGHT_CONST_INSTANCE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class ProxyCachedRepositoryRule(Rule):
    @property
    def name(self) -> str:
        return "PROXY_CACHED_REPOSITORY"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                name_lower = cls.name.lower()
                has_cache_field = any("cache" in f.name.lower() or "local" in f.name.lower() for f in cls.fields)
                if ("proxy" in name_lower or "cached" in name_lower) and has_cache_field:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="STRUCTURAL_PROXY_CACHED_REPO",
                        weight=0.90,
                        description=f"Class '{cls.name}' implements Proxy pattern intercepting calls with local caching before remote fetch",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.PROXY_CACHED_REPOSITORY,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections
