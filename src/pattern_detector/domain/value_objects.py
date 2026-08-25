from enum import Enum
from dataclasses import dataclass
from typing import Optional


class PatternCategory(str, Enum):
    DART_MODERN_IDIOMATIC = "dart_modern_idiomatic"
    FLUTTER_REACTIVE_ARCHITECTURE = "flutter_reactive_architecture"
    CONCURRENCY_ASYNC = "concurrency_async"
    CREATIONAL = "creational"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"
    DART_FLUTTER_SECURITY_HAZARDS = "dart_flutter_security_hazards"
    SOLID_PRINCIPLES = "solid_principles"


class PatternType(str, Enum):
    # Dart 3.x Modern Idiomatic
    SEALED_CLASS_ADT = "sealed_class_adt"
    PATTERN_MATCHING_SWITCH = "pattern_matching_switch"
    RECORD_MULTIPLE_RETURN = "record_multiple_return"
    EXTENSION_TYPE_INLINED = "extension_type_inlined"
    ENHANCED_ENUM_MEMBERS = "enhanced_enum_members"
    MIXIN_BEHAVIOR_COMPOSITION = "mixin_behavior_composition"
    EXTENSION_METHOD_SUGAR = "extension_method_sugar"

    # Flutter & Reactive Architecture
    BLOC_CUBIT_STATE_MACHINE = "bloc_cubit_state_machine"
    RIVERPOD_NOTIFIER_DI = "riverpod_notifier_di"
    INHERITED_WIDGET_PROVIDER = "inherited_widget_provider"
    CHANGE_NOTIFIER_STORE = "change_notifier_store"
    CLEAN_USECASE_INTERACTOR = "clean_usecase_interactor"

    # Concurrency & Async
    ISOLATE_WORKER_POOL = "isolate_worker_pool"
    ASYNC_STREAM_PIPELINE = "async_stream_pipeline"

    # GoF Creational in Dart
    FACTORY_CONSTRUCTOR = "factory_constructor"
    BUILDER_WIDGET_PATTERN = "builder_widget_pattern"
    PROTOTYPE_COPY_WITH = "prototype_copy_with"
    SINGLETON_INSTANCE = "singleton_instance"
    SERVICE_LOCATOR_DI = "service_locator_di"

    # GoF Structural in Dart
    ADAPTER_TYPE_CONVERTER = "adapter_type_converter"
    BRIDGE_PLATFORM_CHANNEL = "bridge_platform_channel"
    COMPOSITE_WIDGET_TREE = "composite_widget_tree"
    DECORATOR_WRAPPER_WIDGET = "decorator_wrapper_widget"
    FACADE_API_CLIENT = "facade_api_client"
    FLYWEIGHT_CONST_INSTANCE = "flyweight_const_instance"
    PROXY_CACHED_REPOSITORY = "proxy_cached_repository"

    # GoF Behavioral in Dart
    CHAIN_MIDDLEWARE_INTERCEPTOR = "chain_middleware_interceptor"
    COMMAND_INTENT_ACTION = "command_intent_action"
    ITERATOR_SYNC_GENERATOR = "iterator_sync_generator"
    MEDIATOR_EVENT_BUS = "mediator_event_bus"
    MEMENTO_HYDRATED_SNAPSHOT = "memento_hydrated_snapshot"
    OBSERVER_LISTENABLE_STREAM = "observer_listenable_stream"
    STATE_MACHINE_HIERARCHY = "state_machine_hierarchy"
    STRATEGY_ALGORITHM_INTERFACE = "strategy_algorithm_interface"
    TEMPLATE_METHOD_LIFECYCLE = "template_method_lifecycle"
    VISITOR_WIDGET_TRAVERSAL = "visitor_widget_traversal"

    # Security & Memory Hazards
    ASYNC_GAP_CONTEXT_USE_HAZARD = "async_gap_context_use_hazard"
    UNCLOSED_STREAM_CONTROLLER_HAZARD = "unclosed_stream_controller_hazard"
    HARDCODED_API_KEY_SECRET_HAZARD = "hardcoded_api_key_secret_hazard"
    UNSAFE_EVAL_JS_INJECTION_HAZARD = "unsafe_eval_js_injection_hazard"
    SETSTATE_DURING_BUILD_HAZARD = "setstate_during_build_hazard"
    LATE_INITIALIZATION_RACE_HAZARD = "late_initialization_race_hazard"

    # SOLID Principles
    MONOLITHIC_WIDGET_SRP = "monolithic_widget_srp"
    GOD_CLASS_SERVICE_SRP = "god_class_service_srp"
    FAT_ABSTRACT_INTERFACE_ISP = "fat_abstract_interface_isp"


class ConfidenceLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


@dataclass(frozen=True)
class SourceLocation:
    file_path: str
    line_number: int
    column_number: int = 1

    def __str__(self) -> str:
        return f"{self.file_path}:{self.line_number}:{self.column_number}"


@dataclass(frozen=True)
class EvidenceItem:
    rule_name: str
    weight: float
    description: str
    location: Optional[SourceLocation] = None


@dataclass
class Confidence:
    value: float  # 0.0 to 1.0

    @property
    def level(self) -> ConfidenceLevel:
        if self.value >= 0.85:
            return ConfidenceLevel.VERY_HIGH
        if self.value >= 0.70:
            return ConfidenceLevel.HIGH
        if self.value >= 0.50:
            return ConfidenceLevel.MEDIUM
        return ConfidenceLevel.LOW

    @property
    def percentage(self) -> int:
        return int(round(self.value * 100))
