import pytest
from pattern_detector.domain.value_objects import (
    PatternCategory,
    PatternType,
    Confidence,
    ConfidenceLevel,
    SourceLocation,
    EvidenceItem,
)
from pattern_detector.domain.pattern import PATTERN_CATALOG
from pattern_detector.domain.code_model import (
    DartClass,
    DartMethod,
    DartField,
    DartEnum,
    DartMixin,
    DartExtension,
    DartFile,
    CodeModel,
)
from pattern_detector.domain.detection import Detection, DetectionReport


def test_confidence_calculation():
    c1 = Confidence(0.95)
    assert c1.level == ConfidenceLevel.VERY_HIGH
    assert c1.percentage == 95

    c2 = Confidence(0.75)
    assert c2.level == ConfidenceLevel.HIGH

    c3 = Confidence(0.60)
    assert c3.level == ConfidenceLevel.MEDIUM

    c4 = Confidence(0.30)
    assert c4.level == ConfidenceLevel.LOW


def test_pattern_catalog_completeness():
    assert len(PATTERN_CATALOG) == 45
    for p_type in PatternType:
        assert p_type in PATTERN_CATALOG
        meta = PATTERN_CATALOG[p_type]
        assert meta.default_weight > 0.5
        assert len(meta.description) > 10


def test_code_model_indexing():
    model = CodeModel()
    cls1 = DartClass(name="OrderBloc", extends_class="Bloc<OrderEvent, OrderState>", line_number=10)
    cls2 = DartClass(name="OrderRepository", is_abstract=True, line_number=20)
    file1 = DartFile(file_path="order_bloc.dart", raw_content="", classes=[cls1, cls2])
    model.add_file(file1)

    assert model.get_class("OrderBloc") == cls1
    assert model.get_class("orderrepository") == cls2
    assert model.get_class("NonExistent") is None


def test_detection_report_serialization():
    loc = SourceLocation("lib/app.dart", 15, 1)
    ev = EvidenceItem("RULE_TEST", 0.95, "Test description", loc)
    d = Detection(
        pattern_type=PatternType.SEALED_CLASS_ADT,
        target_name="Result",
        location=loc,
        confidence=Confidence(0.95),
        evidence=[ev],
    )

    report = DetectionReport(
        target_path="lib/",
        scanned_files_count=1,
        execution_time_seconds=0.012,
        detections=[d],
    )

    assert report.total_detections == 1
    assert report.category_counts[PatternCategory.DART_MODERN_IDIOMATIC.value] == 1
    d_dict = d.to_dict()
    assert d_dict["pattern_type"] == "sealed_class_adt"
    assert d_dict["confidence"]["percentage"] == 95
