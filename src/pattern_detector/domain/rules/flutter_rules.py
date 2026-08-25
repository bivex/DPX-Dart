import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class BlocCubitStateMachineRule(Rule):
    @property
    def name(self) -> str:
        return "BLOC_CUBIT_STATE_MACHINE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                ext = (cls.extends_class or "").lower()
                if "bloc<" in ext or "cubit<" in ext or ext.endswith("bloc") or ext.endswith("cubit"):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="FLUTTER_BLOC_CUBIT",
                        weight=0.95,
                        description=f"Class '{cls.name}' implements BLoC/Cubit reactive state machine (extends {cls.extends_class})",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.BLOC_CUBIT_STATE_MACHINE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class RiverpodNotifierDiRule(Rule):
    @property
    def name(self) -> str:
        return "RIVERPOD_NOTIFIER_DI"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                ext = (cls.extends_class or "").lower()
                if "notifier" in ext or "asyncnotifier" in ext or "consumerwidget" in ext or "consumerstate" in ext:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="FLUTTER_RIVERPOD_NOTIFIER",
                        weight=0.92,
                        description=f"Class '{cls.name}' implements Riverpod Notifier / Consumer reactive scoping",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.RIVERPOD_NOTIFIER_DI,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
            # Check top-level providers e.g. final userProvider = Provider(...)
            if "stateprovider" in file.raw_content.lower() or "notifierprovider" in file.raw_content.lower() or "futureprovider" in file.raw_content.lower():
                loc = SourceLocation(file_path=file.file_path, line_number=1)
                ev = EvidenceItem(
                    rule_name="FLUTTER_RIVERPOD_PROVIDER_DECL",
                    weight=0.92,
                    description="File declares Riverpod Providers for dependency injection and state management",
                    location=loc,
                )
                detections.append(
                    Detection(
                        pattern_type=PatternType.RIVERPOD_NOTIFIER_DI,
                        target_name="RiverpodProvider",
                        location=loc,
                        confidence=Confidence(0.92),
                        evidence=[ev],
                    )
                )
        return detections


class InheritedWidgetProviderRule(Rule):
    @property
    def name(self) -> str:
        return "INHERITED_WIDGET_PROVIDER"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                ext = (cls.extends_class or "").lower()
                if "inheritedwidget" in ext or "inheritedmodel" in ext:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="FLUTTER_INHERITED_WIDGET",
                        weight=0.92,
                        description=f"Class '{cls.name}' extends InheritedWidget for ambient subtree data propagation",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.INHERITED_WIDGET_PROVIDER,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class ChangeNotifierStoreRule(Rule):
    @property
    def name(self) -> str:
        return "CHANGE_NOTIFIER_STORE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                ext = (cls.extends_class or "").lower()
                mixins = [m.lower() for m in cls.with_mixins]
                if "changenotifier" in ext or "valuenotifier" in ext or "changenotifier" in mixins:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="FLUTTER_CHANGE_NOTIFIER",
                        weight=0.90,
                        description=f"Class '{cls.name}' uses ChangeNotifier / ValueNotifier for observable state notifications",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.CHANGE_NOTIFIER_STORE,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class CleanUsecaseInteractorRule(Rule):
    @property
    def name(self) -> str:
        return "CLEAN_USECASE_INTERACTOR"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                name_lower = cls.name.lower()
                has_call = any(m.name == "call" for m in cls.methods)
                if ("usecase" in name_lower or "interactor" in name_lower or any("usecase" in i.lower() for i in cls.implements_interfaces)) and (has_call or cls.method_count <= 3):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="CLEAN_USECASE_INTERACTOR",
                        weight=0.90,
                        description=f"Class '{cls.name}' implements Clean Architecture UseCase / Interactor pattern",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.CLEAN_USECASE_INTERACTOR,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections
