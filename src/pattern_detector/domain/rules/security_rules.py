import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class AsyncGapContextUseHazardRule(Rule):
    @property
    def name(self) -> str:
        return "ASYNC_GAP_CONTEXT_USE_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if m.is_async and "await " in m.body:
                        # Check if context is used after await without mounted check
                        parts = m.body.split("await ")
                        for post_await in parts[1:]:
                            if re.search(r'\b(Navigator\.of|context\.(read|watch|select)|ScaffoldMessenger\.of|Theme\.of|showDialog)\b', post_await):
                                if "if (!mounted)" not in post_await and "if (!context.mounted)" not in post_await:
                                    loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                                    ev = EvidenceItem(
                                        rule_name="HAZARD_ASYNC_GAP_CONTEXT",
                                        weight=0.95,
                                        description=f"Method '{cls.name}.{m.name}' uses BuildContext after an 'await' point without checking 'if (!context.mounted) return'",
                                        location=loc,
                                    )
                                    detections.append(
                                        Detection(
                                            pattern_type=PatternType.ASYNC_GAP_CONTEXT_USE_HAZARD,
                                            target_name=f"{cls.name}.{m.name}",
                                            location=loc,
                                            confidence=Confidence(0.95),
                                            evidence=[ev],
                                        )
                                    )
                                    break
        return detections


class UnclosedStreamControllerHazardRule(Rule):
    @property
    def name(self) -> str:
        return "UNCLOSED_STREAM_CONTROLLER_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                has_stream_ctrl = any("streamcontroller" in f.type_annotation.lower() or "streamcontroller" in (f.default_value or "").lower() for f in cls.fields)
                has_dispose = any(m.name == "dispose" or m.name == "close" for m in cls.methods)
                has_ctrl_close = any(".close()" in m.body for m in cls.methods)
                if has_stream_ctrl and (not has_dispose or not has_ctrl_close):
                    loc = SourceLocation(file_path=file.file_path, line_number=cls.line_number)
                    ev = EvidenceItem(
                        rule_name="HAZARD_UNCLOSED_STREAM_CONTROLLER",
                        weight=0.90,
                        description=f"Class '{cls.name}' instantiates StreamController but does not guarantee close() in dispose(), risking memory leak",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.UNCLOSED_STREAM_CONTROLLER_HAZARD,
                            target_name=cls.name,
                            location=loc,
                            confidence=Confidence(0.90),
                            evidence=[ev],
                        )
                    )
        return detections


class HardcodedApiKeySecretHazardRule(Rule):
    @property
    def name(self) -> str:
        return "HARDCODED_API_KEY_SECRET_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        secret_pattern = re.compile(
            r'\b(?:api_key|apiKey|secret_key|secretKey|private_key|bearer_token|auth_token)\s*=\s*[\'"][A-Za-z0-9_\-]{16,}[\'"]',
            re.IGNORECASE,
        )
        for file in model.files:
            for line_idx, line in enumerate(file.raw_content.splitlines(), start=1):
                if secret_pattern.search(line):
                    loc = SourceLocation(file_path=file.file_path, line_number=line_idx)
                    ev = EvidenceItem(
                        rule_name="HAZARD_HARDCODED_SECRET",
                        weight=0.95,
                        description="Hardcoded private API key or secret token detected in Dart source code",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.HARDCODED_API_KEY_SECRET_HAZARD,
                            target_name="SecretKey",
                            location=loc,
                            confidence=Confidence(0.95),
                            evidence=[ev],
                        )
                    )
        return detections


class UnsafeEvalJsInjectionHazardRule(Rule):
    @property
    def name(self) -> str:
        return "UNSAFE_EVAL_JS_INJECTION_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        unsafe_js_pattern = re.compile(r'\bevaluateJavascript\s*\(\s*[\'"].*?\$[a-zA-Z0-9_]+', re.DOTALL)
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if unsafe_js_pattern.search(m.body):
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="HAZARD_UNSAFE_JS_INJECTION",
                            weight=0.92,
                            description=f"Method '{cls.name}.{m.name}' performs unescaped string interpolation inside evaluateJavascript(), risking XSS",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.UNSAFE_EVAL_JS_INJECTION_HAZARD,
                                target_name=f"{cls.name}.{m.name}",
                                location=loc,
                                confidence=Confidence(0.92),
                                evidence=[ev],
                            )
                        )
        return detections


class SetstateDuringBuildHazardRule(Rule):
    @property
    def name(self) -> str:
        return "SETSTATE_DURING_BUILD_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if m.name == "build" and "setState(" in m.body and "onPressed:" not in m.body and "onTap:" not in m.body:
                        # Check direct synchronous setState call in build
                        if re.search(r'^\s*setState\s*\(', m.body, re.MULTILINE):
                            loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                            ev = EvidenceItem(
                                rule_name="HAZARD_SETSTATE_IN_BUILD",
                                weight=0.92,
                                description=f"Widget '{cls.name}' calls setState() synchronously inside build(), triggering infinite re-render loop",
                                location=loc,
                            )
                            detections.append(
                                Detection(
                                    pattern_type=PatternType.SETSTATE_DURING_BUILD_HAZARD,
                                    target_name=f"{cls.name}.build",
                                    location=loc,
                                    confidence=Confidence(0.92),
                                    evidence=[ev],
                                )
                            )
        return detections


class LateInitializationRaceHazardRule(Rule):
    @property
    def name(self) -> str:
        return "LATE_INITIALIZATION_RACE_HAZARD"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                for f in cls.fields:
                    if f.is_late and not f.default_value:
                        loc = SourceLocation(file_path=file.file_path, line_number=f.line_number)
                        ev = EvidenceItem(
                            rule_name="HAZARD_UNINITIALIZED_LATE_FIELD",
                            weight=0.88,
                            description=f"Field '{cls.name}.{f.name}' is declared 'late' without default value, risking LateInitializationError",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.LATE_INITIALIZATION_RACE_HAZARD,
                                target_name=f"{cls.name}.{f.name}",
                                location=loc,
                                confidence=Confidence(0.88),
                                evidence=[ev],
                            )
                        )
        return detections
