import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class FactoryConstructorRule(Rule):
    @property
    def name(self) -> str:
        return "FACTORY_CONSTRUCTOR"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                for ctor in cls.constructors:
                    if ctor.is_factory:
                        loc = SourceLocation(file_path=file.file_path, line_number=ctor.line_number)
                        ev = EvidenceItem(
                            rule_name="CREATIONAL_FACTORY_CONSTRUCTOR",
                            weight=0.92,
                            description=f"Class '{cls.name}' defines factory constructor '{ctor.name}' for custom instantiation or caching",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.FACTORY_CONSTRUCTOR,
                                target_name=f"{cls.name}.{ctor.name}",
                                location=loc,
                                confidence=Confidence(0.92),
                                evidence=[ev],
                            )
                        )
        return detections


class BuilderWidgetPatternRule(Rule):
    @property
    def name(self) -> str:
        return "BUILDER_WIDGET_PATTERN"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        builder_cb_pattern = re.compile(r'\b(builder|itemBuilder|pageBuilder|separatorBuilder)\s*:\s*\(\s*BuildContext\b|\bWidgetBuilder\b')
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if builder_cb_pattern.search(m.body) or "builder:" in m.body:
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="CREATIONAL_BUILDER_WIDGET",
                            weight=0.90,
                            description=f"Method '{cls.name}.{m.name}' utilizes Builder pattern for lazy contextual widget construction",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.BUILDER_WIDGET_PATTERN,
                                target_name=f"{cls.name}.{m.name}",
                                location=loc,
                                confidence=Confidence(0.90),
                                evidence=[ev],
                            )
                        )
        return detections


class PrototypeCopyWithRule(Rule):
    @property
    def name(self) -> str:
        return "PROTOTYPE_COPY_WITH"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_copy_with = any(m.name == "copyWith" for m in cls.methods)
                if has_copy_with:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_PROTOTYPE_COPY_WITH",
                        weight=0.92,
                        description=f"Class '{cls.name}' implements Prototype copyWith() pattern for immutable record cloning with field updates",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.PROTOTYPE_COPY_WITH,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class SingletonInstanceRule(Rule):
    @property
    def name(self) -> str:
        return "SINGLETON_INSTANCE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_private_ctor = any(c.name.startswith("_") for c in cls.constructors) or (f"{cls.name}._" in cls.raw_body)
                has_static_instance = any(
                    (f.is_static and f.type_annotation.lower() == cls.name.lower()) or
                    (m.is_static and m.return_type.lower() == cls.name.lower() and m.name in ["instance", "get", "shared"])
                    for f in cls.fields
                    for m in cls.methods
                )
                if (has_private_ctor and has_static_instance) or ("static final " + cls.name + " instance" in cls.raw_body.lower()) or ("static final _instance = " + cls.name + "._" in cls.raw_body.lower()):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="CREATIONAL_SINGLETON",
                        weight=0.92,
                        description=f"Class '{cls.name}' implements Singleton pattern with private constructor and static shared accessor",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.SINGLETON_INSTANCE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class ServiceLocatorDiRule(Rule):
    @property
    def name(self) -> str:
        return "SERVICE_LOCATOR_DI"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        get_it_pattern = re.compile(r'\bGetIt\.(instance|I)\b|\bsl<|\bgetIt<', re.IGNORECASE)
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if get_it_pattern.search(m.body):
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="CREATIONAL_SERVICE_LOCATOR_GETIT",
                            weight=0.90,
                            description=f"Method '{cls.name}.{m.name}' resolves dependencies via GetIt Service Locator",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.SERVICE_LOCATOR_DI,
                                target_name=f"{cls.name}.{m.name}",
                                location=loc,
                                confidence=Confidence(0.90),
                                evidence=[ev],
                            )
                        )
        return detections
