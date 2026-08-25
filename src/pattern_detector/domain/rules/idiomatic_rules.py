import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class SealedClassAdtRule(Rule):
    @property
    def name(self) -> str:
        return "SEALED_CLASS_ADT"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                if cls.is_sealed:
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="DART_SEALED_CLASS",
                        weight=0.95,
                        description=f"Class '{cls.name}' is declared as a sealed class for exhaustive pattern matching and ADT modeling",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.SEALED_CLASS_ADT,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class PatternMatchingSwitchRule(Rule):
    @property
    def name(self) -> str:
        return "PATTERN_MATCHING_SWITCH"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        switch_expr_pattern = re.compile(r'\bswitch\s*\([^)]*\)\s*\{[^}]*=>', re.DOTALL)
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if switch_expr_pattern.search(m.body) or "case (" in m.body or "case const" in m.body:
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="DART_PATTERN_MATCHING_SWITCH",
                            weight=0.92,
                            description=f"Method '{cls.name}.{m.name}' applies Dart 3 pattern matching / switch expressions",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.PATTERN_MATCHING_SWITCH,
                                target_name=f"{cls.name}.{m.name}",
                                location=loc,
                                confidence=Confidence(0.92),
                                evidence=[ev],
                            )
                        )
            for fn in file.functions:
                if switch_expr_pattern.search(fn.body) or "case (" in fn.body:
                    loc = SourceLocation(file_path=file.file_path, line_number=fn.line_number)
                    ev = EvidenceItem(
                        rule_name="DART_PATTERN_MATCHING_SWITCH",
                        weight=0.92,
                        description=f"Function '{fn.name}' applies Dart 3 pattern matching switch expression",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.PATTERN_MATCHING_SWITCH,
                            target_name=fn.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class RecordMultipleReturnRule(Rule):
    @property
    def name(self) -> str:
        return "RECORD_MULTIPLE_RETURN"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        record_pattern = re.compile(r'^\s*\([a-zA-Z0-9_<>,?\s]+\)\s*$')
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if record_pattern.match(m.return_type.strip()) or re.search(r'return\s*\([^,]+,[^)]+\);', m.body):
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="DART_RECORD_MULTIPLE_RETURN",
                            weight=0.90,
                            description=f"Method '{cls.name}.{m.name}' uses Dart 3 Record tuple return type '{m.return_type}'",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.RECORD_MULTIPLE_RETURN,
                                target_name=f"{cls.name}.{m.name}",
                                location=loc,
                                confidence=Confidence(0.90),
                                evidence=[ev],
                            )
                        )
        return detections


class ExtensionTypeInlinedRule(Rule):
    @property
    def name(self) -> str:
        return "EXTENSION_TYPE_INLINED"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for ext in file.extensions:
                if ext.is_extension_type:
                    loc = SourceLocation(file_path=file.file_path, line_number=ext.line_number)
                    ev = EvidenceItem(
                        rule_name="DART_EXTENSION_TYPE",
                        weight=0.92,
                        description=f"Extension type '{ext.name}' on '{ext.on_type}' provides zero-cost inlined type safety",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.EXTENSION_TYPE_INLINED,
                            target_name=ext.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class EnhancedEnumMembersRule(Rule):
    @property
    def name(self) -> str:
        return "ENHANCED_ENUM_MEMBERS"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for en in file.enums:
                if en.is_enhanced:
                    loc = SourceLocation(file_path=file.file_path, line_number=en.line_number)
                    ev = EvidenceItem(
                        rule_name="DART_ENHANCED_ENUM",
                        weight=0.90,
                        description=f"Enum '{en.name}' is an Enhanced Enum defining {len(en.fields)} fields and {len(en.methods)} methods",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.ENHANCED_ENUM_MEMBERS,
                            target_name=en.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class MixinBehaviorCompositionRule(Rule):
    @property
    def name(self) -> str:
        return "MIXIN_BEHAVIOR_COMPOSITION"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for mx in file.mixins:
                loc = SourceLocation(file_path=file.file_path, line_number=mx.line_number)
                on_str = f" on {', '.join(mx.on_types)}" if mx.on_types else ""
                ev = EvidenceItem(
                    rule_name="DART_MIXIN_COMPOSITION",
                    weight=0.92,
                    description=f"Mixin '{mx.name}'{on_str} defines reusable horizontal behavior composition",
                    location=loc,
                )
                detections.append(
                    Detection(
                        pattern_type=PatternType.MIXIN_BEHAVIOR_COMPOSITION,
                        target_name=mx.name,
                        location=loc,
                        confidence=Confidence(0.92),
                        evidence=[ev],
                    )
                )
        return detections


class ExtensionMethodSugarRule(Rule):
    @property
    def name(self) -> str:
        return "EXTENSION_METHOD_SUGAR"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for ext in file.extensions:
                if not ext.is_extension_type:
                    loc = SourceLocation(file_path=file.file_path, line_number=ext.line_number)
                    ev = EvidenceItem(
                        rule_name="DART_EXTENSION_METHOD",
                        weight=0.90,
                        description=f"Extension '{ext.name}' on '{ext.on_type}' retroactively augments API functionality",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.EXTENSION_METHOD_SUGAR,
                            target_name=ext.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections
