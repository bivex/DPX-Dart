import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class ChainMiddlewareInterceptorRule(Rule):
    @property
    def name(self) -> str:
        return "CHAIN_MIDDLEWARE_INTERCEPTOR"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                name_lower = cls.name.lower()
                ext = (cls.extends_class or "").lower()
                if "interceptor" in ext or "middleware" in ext or "interceptor" in name_lower or "middleware" in name_lower:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_CHAIN_INTERCEPTOR",
                        weight=0.90,
                        description=f"Class '{cls.name}' implements Chain of Responsibility middleware / interceptor pipeline",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.CHAIN_MIDDLEWARE_INTERCEPTOR,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class CommandIntentActionRule(Rule):
    @property
    def name(self) -> str:
        return "COMMAND_INTENT_ACTION"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                name_lower = cls.name.lower()
                ext = (cls.extends_class or "").lower()
                if (cls.is_sealed or cls.is_abstract) and (name_lower.endswith("event") or name_lower.endswith("action") or name_lower.endswith("intent") or ext.endswith("event")):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_COMMAND_INTENT",
                        weight=0.92,
                        description=f"Class '{cls.name}' encapsulates user intent into Command object (BLoC Event / Redux Action)",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.COMMAND_INTENT_ACTION,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class IteratorSyncGeneratorRule(Rule):
    @property
    def name(self) -> str:
        return "ITERATOR_SYNC_GENERATOR"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if "iterable<" in m.return_type.lower() and m.is_generator and not m.is_async:
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="BEHAVIORAL_ITERATOR_SYNC_GENERATOR",
                            weight=0.90,
                            description=f"Method '{cls.name}.{m.name}' lazily yields sequence elements using sync* and yield",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.ITERATOR_SYNC_GENERATOR,
                                target_name=f"{cls.name}.{m.name}",
                                location=loc,
                                confidence=Confidence(0.90),
                                evidence=[ev],
                            )
                        )
            for fn in file.functions:
                if "iterable<" in fn.return_type.lower() and fn.is_generator and not fn.is_async:
                    loc = SourceLocation(file_path=file.file_path, line_number=fn.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_ITERATOR_SYNC_GENERATOR",
                        weight=0.90,
                        description=f"Function '{fn.name}' lazily yields items via sync* iterator generator",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.ITERATOR_SYNC_GENERATOR,
                            target_name=fn.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class MediatorEventBusRule(Rule):
    @property
    def name(self) -> str:
        return "MEDIATOR_EVENT_BUS"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        event_bus_pattern = re.compile(r'\bEventBus\b|\b_eventBus\.fire\b|\beventBus\.on<', re.IGNORECASE)
        for file in model.files:
            for cls in file.classes:
                if event_bus_pattern.search(cls.raw_body):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_MEDIATOR_EVENT_BUS",
                        weight=0.92,
                        description=f"Class '{cls.name}' interacts with central EventBus Mediator for decoupled module messaging",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.MEDIATOR_EVENT_BUS,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class MementoHydratedSnapshotRule(Rule):
    @property
    def name(self) -> str:
        return "MEMENTO_HYDRATED_SNAPSHOT"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_to_json = any(m.name == "toJson" or m.name == "toMap" for m in cls.methods)
                has_from_json = any(c.name in ["fromJson", "fromMap"] for c in cls.constructors)
                ext = (cls.extends_class or "").lower()
                if "hydratedbloc" in ext or "hydratedcubit" in ext or (has_to_json and has_from_json and any(k in cls.name.lower() for k in ["state", "snapshot", "memento"])):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_MEMENTO_SNAPSHOT",
                        weight=0.92,
                        description=f"Class '{cls.name}' captures and restores state snapshots via Memento serialization (toJson/fromJson)",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.MEMENTO_HYDRATED_SNAPSHOT,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class ObserverListenableStreamRule(Rule):
    @property
    def name(self) -> str:
        return "OBSERVER_LISTENABLE_STREAM"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        stream_listen_pattern = re.compile(r'\.listen\s*\(|\bStreamBuilder\b|\bListenableBuilder\b|\bValueListenableBuilder\b|\bAnimatedBuilder\b')
        for file in model.files:
            for cls in file.classes:
                if stream_listen_pattern.search(cls.raw_body):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_OBSERVER_STREAM_LISTENABLE",
                        weight=0.92,
                        description=f"Class '{cls.name}' acts as an Observer binding to observable Streams or Listenables",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.OBSERVER_LISTENABLE_STREAM,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class StateMachineHierarchyRule(Rule):
    @property
    def name(self) -> str:
        return "STATE_MACHINE_HIERARCHY"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                name_lower = cls.name.lower()
                if (cls.is_sealed or cls.is_abstract) and (name_lower.endswith("state") or name_lower.endswith("status")):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_STATE_PATTERN_HIERARCHY",
                        weight=0.92,
                        description=f"Class '{cls.name}' forms the root of a polymorphic finite State Machine hierarchy",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.STATE_MACHINE_HIERARCHY,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class StrategyAlgorithmInterfaceRule(Rule):
    @property
    def name(self) -> str:
        return "STRATEGY_ALGORITHM_INTERFACE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                name_lower = cls.name.lower()
                if (cls.is_abstract or cls.is_interface) and any(k in name_lower for k in ["strategy", "policy", "algorithm", "formatter", "validator"]) and cls.method_count <= 4:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_STRATEGY_INTERFACE",
                        weight=0.90,
                        description=f"Abstract class/interface '{cls.name}' defines an interchangeable Strategy contract",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.STRATEGY_ALGORITHM_INTERFACE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class TemplateMethodLifecycleRule(Rule):
    @property
    def name(self) -> str:
        return "TEMPLATE_METHOD_LIFECYCLE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                method_names = {m.name for m in cls.methods}
                if ("initState" in method_names and "build" in method_names) or ("onInit" in method_names and "onClose" in method_names):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="BEHAVIORAL_TEMPLATE_METHOD_LIFECYCLE",
                        weight=0.92,
                        description=f"Class '{cls.name}' participates in framework Template Method lifecycle workflow (initState -> build -> dispose)",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.TEMPLATE_METHOD_LIFECYCLE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class VisitorWidgetTraversalRule(Rule):
    @property
    def name(self) -> str:
        return "VISITOR_WIDGET_TRAVERSAL"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        visitor_pattern = re.compile(r'\b(visitChildren|visitAncestorElements|accept|visitElement)\b')
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if visitor_pattern.search(m.body):
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="BEHAVIORAL_VISITOR_TRAVERSAL",
                            weight=0.90,
                            description=f"Method '{cls.name}.{m.name}' applies Visitor pattern traversing widget element nodes",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.VISITOR_WIDGET_TRAVERSAL,
                                target_name=f"{cls.name}.{m.name}",
                                location=loc,
                                confidence=Confidence(0.90),
                                evidence=[ev],
                            )
                        )
        return detections
