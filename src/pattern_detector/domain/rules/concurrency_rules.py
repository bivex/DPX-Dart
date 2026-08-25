import re
from typing import List
from .base import Rule
from ..code_model import CodeModel
from ..detection import Detection
from ..value_objects import PatternType, Confidence, SourceLocation, EvidenceItem


class IsolateWorkerPoolRule(Rule):
    @property
    def name(self) -> str:
        return "ISOLATE_WORKER_POOL"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        isolate_pattern = re.compile(r'\bIsolate\.(spawn|run)\b|\bcompute\s*\(', re.DOTALL)
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if isolate_pattern.search(m.body):
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="DART_ISOLATE_CONCURRENCY",
                            weight=0.92,
                            description=f"Method '{cls.name}.{m.name}' spawns background Isolate task for off-main-thread computation",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.ISOLATE_WORKER_POOL,
                                target_name=f"{cls.name}.{m.name}",
                                location=loc,
                                confidence=Confidence(0.92),
                                evidence=[ev],
                            )
                        )
            for fn in file.functions:
                if isolate_pattern.search(fn.body):
                    loc = SourceLocation(file_path=file.file_path, line_number=fn.line_number)
                    ev = EvidenceItem(
                        rule_name="DART_ISOLATE_CONCURRENCY",
                        weight=0.92,
                        description=f"Function '{fn.name}' spawns background Isolate worker computation",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.ISOLATE_WORKER_POOL,
                            target_name=fn.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections


class AsyncStreamPipelineRule(Rule):
    @property
    def name(self) -> str:
        return "ASYNC_STREAM_PIPELINE"

    def evaluate(self, model: CodeModel) -> List[Detection]:
        detections: List[Detection] = []
        for file in model.files:
            for cls in file.classes:
                for m in cls.methods:
                    if "stream<" in m.return_type.lower() or (m.is_async and m.is_generator) or "yield*" in m.body:
                        loc = SourceLocation(file_path=file.file_path, line_number=m.line_number)
                        ev = EvidenceItem(
                            rule_name="DART_ASYNC_STREAM_PIPELINE",
                            weight=0.92,
                            description=f"Method '{cls.name}.{m.name}' generates or transforms asynchronous event Streams (async*/yield)",
                            location=loc,
                        )
                        detections.append(
                            Detection(
                                pattern_type=PatternType.ASYNC_STREAM_PIPELINE,
                                target_name=f"{cls.name}.{m.name}",
                                location=loc,
                                confidence=Confidence(0.92),
                                evidence=[ev],
                            )
                        )
            for fn in file.functions:
                if "stream<" in fn.return_type.lower() or (fn.is_async and fn.is_generator):
                    loc = SourceLocation(file_path=file.file_path, line_number=fn.line_number)
                    ev = EvidenceItem(
                        rule_name="DART_ASYNC_STREAM_PIPELINE",
                        weight=0.92,
                        description=f"Function '{fn.name}' yields asynchronous stream of events",
                        location=loc,
                    )
                    detections.append(
                        Detection(
                            pattern_type=PatternType.ASYNC_STREAM_PIPELINE,
                            target_name=fn.name,
                            location=loc,
                            confidence=Confidence(0.92),
                            evidence=[ev],
                        )
                    )
        return detections
