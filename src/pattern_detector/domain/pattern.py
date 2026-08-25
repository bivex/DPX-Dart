from dataclasses import dataclass
from typing import Dict
from .value_objects import PatternCategory, PatternType


@dataclass(frozen=True)
class PatternMetadata:
    pattern_type: PatternType
    name: str
    category: PatternCategory
    description: str
    default_weight: float


PATTERN_CATALOG: Dict[PatternType, PatternMetadata] = {
    # Dart 3.x Modern Idiomatic
    PatternType.SEALED_CLASS_ADT: PatternMetadata(
        pattern_type=PatternType.SEALED_CLASS_ADT,
        name="Sealed Class ADT",
        category=PatternCategory.DART_MODERN_IDIOMATIC,
        description="Exhaustive Algebraic Data Types and pattern matching via Dart 3 sealed class hierarchies.",
        default_weight=0.95,
    ),
    PatternType.PATTERN_MATCHING_SWITCH: PatternMetadata(
        pattern_type=PatternType.PATTERN_MATCHING_SWITCH,
        name="Pattern Matching Switch",
        category=PatternCategory.DART_MODERN_IDIOMATIC,
        description="Dart 3 pattern matching, switch expressions, and structural record destructuring.",
        default_weight=0.92,
    ),
    PatternType.RECORD_MULTIPLE_RETURN: PatternMetadata(
        pattern_type=PatternType.RECORD_MULTIPLE_RETURN,
        name="Record Multiple Return",
        category=PatternCategory.DART_MODERN_IDIOMATIC,
        description="Anonymous type-safe tuple records enabling multiple return values without boilerplate classes.",
        default_weight=0.90,
    ),
    PatternType.EXTENSION_TYPE_INLINED: PatternMetadata(
        pattern_type=PatternType.EXTENSION_TYPE_INLINED,
        name="Extension Type Inlined",
        category=PatternCategory.DART_MODERN_IDIOMATIC,
        description="Zero-cost compile-time type-safe inline wrappers via Dart 3 extension type.",
        default_weight=0.92,
    ),
    PatternType.ENHANCED_ENUM_MEMBERS: PatternMetadata(
        pattern_type=PatternType.ENHANCED_ENUM_MEMBERS,
        name="Enhanced Enum Members",
        category=PatternCategory.DART_MODERN_IDIOMATIC,
        description="Enhanced enum declaring explicit fields, getters, constructors, and interface implementations.",
        default_weight=0.90,
    ),
    PatternType.MIXIN_BEHAVIOR_COMPOSITION: PatternMetadata(
        pattern_type=PatternType.MIXIN_BEHAVIOR_COMPOSITION,
        name="Mixin Behavior Composition",
        category=PatternCategory.DART_MODERN_IDIOMATIC,
        description="Reusable horizontal behavior composition and constrained mixins via 'mixin ... on ...'.",
        default_weight=0.92,
    ),
    PatternType.EXTENSION_METHOD_SUGAR: PatternMetadata(
        pattern_type=PatternType.EXTENSION_METHOD_SUGAR,
        name="Extension Method Sugar",
        category=PatternCategory.DART_MODERN_IDIOMATIC,
        description="Retroactive API extension augmenting third-party or core classes without subclassing.",
        default_weight=0.90,
    ),

    # Flutter & Reactive Architecture
    PatternType.BLOC_CUBIT_STATE_MACHINE: PatternMetadata(
        pattern_type=PatternType.BLOC_CUBIT_STATE_MACHINE,
        name="BLoC/Cubit Reactive State Machine",
        category=PatternCategory.FLUTTER_REACTIVE_ARCHITECTURE,
        description="Unidirectional reactive state machine converting events into state streams using Bloc/Cubit.",
        default_weight=0.95,
    ),
    PatternType.RIVERPOD_NOTIFIER_DI: PatternMetadata(
        pattern_type=PatternType.RIVERPOD_NOTIFIER_DI,
        name="Riverpod Notifier & DI",
        category=PatternCategory.FLUTTER_REACTIVE_ARCHITECTURE,
        description="Compile-time safe dependency injection and reactive state scoping via Riverpod Providers.",
        default_weight=0.92,
    ),
    PatternType.INHERITED_WIDGET_PROVIDER: PatternMetadata(
        pattern_type=PatternType.INHERITED_WIDGET_PROVIDER,
        name="InheritedWidget Provider",
        category=PatternCategory.FLUTTER_REACTIVE_ARCHITECTURE,
        description="Ambient subtree data propagation down the element tree via InheritedWidget.dependOnInheritedWidgetOfExactType.",
        default_weight=0.92,
    ),
    PatternType.CHANGE_NOTIFIER_STORE: PatternMetadata(
        pattern_type=PatternType.CHANGE_NOTIFIER_STORE,
        name="ChangeNotifier Store",
        category=PatternCategory.FLUTTER_REACTIVE_ARCHITECTURE,
        description="Observable state container broadcasting change notifications to UI listeners via notifyListeners().",
        default_weight=0.90,
    ),
    PatternType.CLEAN_USECASE_INTERACTOR: PatternMetadata(
        pattern_type=PatternType.CLEAN_USECASE_INTERACTOR,
        name="Clean Architecture UseCase Interactor",
        category=PatternCategory.FLUTTER_REACTIVE_ARCHITECTURE,
        description="Single-purpose domain business interactor encapsulating transactional application logic.",
        default_weight=0.90,
    ),

    # Concurrency & Async
    PatternType.ISOLATE_WORKER_POOL: PatternMetadata(
        pattern_type=PatternType.ISOLATE_WORKER_POOL,
        name="Isolate Worker Pool",
        category=PatternCategory.CONCURRENCY_ASYNC,
        description="Heavy CPU background task execution on isolated memory threads via Isolate.spawn() or compute().",
        default_weight=0.92,
    ),
    PatternType.ASYNC_STREAM_PIPELINE: PatternMetadata(
        pattern_type=PatternType.ASYNC_STREAM_PIPELINE,
        name="Async Stream Pipeline",
        category=PatternCategory.CONCURRENCY_ASYNC,
        description="Asynchronous event streaming and reactive transformations via Stream<T>, async*, and yield.",
        default_weight=0.92,
    ),

    # GoF Creational in Dart
    PatternType.FACTORY_CONSTRUCTOR: PatternMetadata(
        pattern_type=PatternType.FACTORY_CONSTRUCTOR,
        name="Factory Constructor",
        category=PatternCategory.CREATIONAL,
        description="Factory pattern implementing customized instance instantiation or cached return via factory keyword.",
        default_weight=0.92,
    ),
    PatternType.BUILDER_WIDGET_PATTERN: PatternMetadata(
        pattern_type=PatternType.BUILDER_WIDGET_PATTERN,
        name="Builder Widget Pattern",
        category=PatternCategory.CREATIONAL,
        description="Builder pattern lazily constructing contextual widget subtrees via (BuildContext, ...) callback builders.",
        default_weight=0.90,
    ),
    PatternType.PROTOTYPE_COPY_WITH: PatternMetadata(
        pattern_type=PatternType.PROTOTYPE_COPY_WITH,
        name="Prototype CopyWith Cloner",
        category=PatternCategory.CREATIONAL,
        description="Prototype pattern cloning immutable models with selective field overwrites via copyWith().",
        default_weight=0.92,
    ),
    PatternType.SINGLETON_INSTANCE: PatternMetadata(
        pattern_type=PatternType.SINGLETON_INSTANCE,
        name="Singleton Instance",
        category=PatternCategory.CREATIONAL,
        description="Singleton pattern restricting class instantiation to a single shared instance via private constructor.",
        default_weight=0.92,
    ),
    PatternType.SERVICE_LOCATOR_DI: PatternMetadata(
        pattern_type=PatternType.SERVICE_LOCATOR_DI,
        name="Service Locator DI (GetIt)",
        category=PatternCategory.CREATIONAL,
        description="Service Locator pattern managing dependency resolution via central registry (GetIt / Kiwi).",
        default_weight=0.90,
    ),

    # GoF Structural in Dart
    PatternType.ADAPTER_TYPE_CONVERTER: PatternMetadata(
        pattern_type=PatternType.ADAPTER_TYPE_CONVERTER,
        name="Adapter Type Converter",
        category=PatternCategory.STRUCTURAL,
        description="Adapter pattern converting DTOs or platform responses to domain entity models (TypeAdapter / toDomain).",
        default_weight=0.90,
    ),
    PatternType.BRIDGE_PLATFORM_CHANNEL: PatternMetadata(
        pattern_type=PatternType.BRIDGE_PLATFORM_CHANNEL,
        name="Bridge Platform Channel",
        category=PatternCategory.STRUCTURAL,
        description="Bridge pattern decoupling Dart abstractions from native iOS/Android platform implementations via MethodChannel.",
        default_weight=0.92,
    ),
    PatternType.COMPOSITE_WIDGET_TREE: PatternMetadata(
        pattern_type=PatternType.COMPOSITE_WIDGET_TREE,
        name="Composite Widget Tree",
        category=PatternCategory.STRUCTURAL,
        description="Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly.",
        default_weight=0.95,
    ),
    PatternType.DECORATOR_WRAPPER_WIDGET: PatternMetadata(
        pattern_type=PatternType.DECORATOR_WRAPPER_WIDGET,
        name="Decorator Wrapper Widget",
        category=PatternCategory.STRUCTURAL,
        description="Decorator pattern augmenting widget appearance or behavior dynamically without modifying base widget.",
        default_weight=0.90,
    ),
    PatternType.FACADE_API_CLIENT: PatternMetadata(
        pattern_type=PatternType.FACADE_API_CLIENT,
        name="Facade API Client",
        category=PatternCategory.STRUCTURAL,
        description="Facade pattern providing unified simplified interface over complex multi-endpoint networking and caching.",
        default_weight=0.90,
    ),
    PatternType.FLYWEIGHT_CONST_INSTANCE: PatternMetadata(
        pattern_type=PatternType.FLYWEIGHT_CONST_INSTANCE,
        name="Flyweight Const Canonical Instance",
        category=PatternCategory.STRUCTURAL,
        description="Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor.",
        default_weight=0.92,
    ),
    PatternType.PROXY_CACHED_REPOSITORY: PatternMetadata(
        pattern_type=PatternType.PROXY_CACHED_REPOSITORY,
        name="Proxy Cached Repository",
        category=PatternCategory.STRUCTURAL,
        description="Proxy pattern intercepting data requests to transparently serve local cache before remote network fetch.",
        default_weight=0.90,
    ),

    # GoF Behavioral in Dart
    PatternType.CHAIN_MIDDLEWARE_INTERCEPTOR: PatternMetadata(
        pattern_type=PatternType.CHAIN_MIDDLEWARE_INTERCEPTOR,
        name="Chain of Responsibility Interceptor",
        category=PatternCategory.BEHAVIORAL,
        description="Chain of Responsibility pipeline processing HTTP requests, auth tokens, and errors sequentially.",
        default_weight=0.90,
    ),
    PatternType.COMMAND_INTENT_ACTION: PatternMetadata(
        pattern_type=PatternType.COMMAND_INTENT_ACTION,
        name="Command Intent Action",
        category=PatternCategory.BEHAVIORAL,
        description="Command pattern encapsulating user intents into standalone command objects (BLoC Events / Redux Actions).",
        default_weight=0.92,
    ),
    PatternType.ITERATOR_SYNC_GENERATOR: PatternMetadata(
        pattern_type=PatternType.ITERATOR_SYNC_GENERATOR,
        name="Iterator Sync Generator",
        category=PatternCategory.BEHAVIORAL,
        description="Iterator pattern generating lazily computed sequences on demand via sync* and yield.",
        default_weight=0.90,
    ),
    PatternType.MEDIATOR_EVENT_BUS: PatternMetadata(
        pattern_type=PatternType.MEDIATOR_EVENT_BUS,
        name="Mediator Event Bus",
        category=PatternCategory.BEHAVIORAL,
        description="Mediator pattern facilitating decoupled publish-subscribe communication across distinct modules.",
        default_weight=0.92,
    ),
    PatternType.MEMENTO_HYDRATED_SNAPSHOT: PatternMetadata(
        pattern_type=PatternType.MEMENTO_HYDRATED_SNAPSHOT,
        name="Memento Hydrated State Snapshot",
        category=PatternCategory.BEHAVIORAL,
        description="Memento pattern capturing and restoring immutable state snapshots (HydratedBloc / toJson / fromJson).",
        default_weight=0.92,
    ),
    PatternType.OBSERVER_LISTENABLE_STREAM: PatternMetadata(
        pattern_type=PatternType.OBSERVER_LISTENABLE_STREAM,
        name="Observer Listenable Stream",
        category=PatternCategory.BEHAVIORAL,
        description="Observer pattern binding reactive UI components to observable streams or Listenable sources.",
        default_weight=0.92,
    ),
    PatternType.STATE_MACHINE_HIERARCHY: PatternMetadata(
        pattern_type=PatternType.STATE_MACHINE_HIERARCHY,
        name="State Pattern Hierarchy",
        category=PatternCategory.BEHAVIORAL,
        description="State pattern representing distinct lifecycle states as polymorphic subtype instances (Initial, Loading, Success, Failure).",
        default_weight=0.92,
    ),
    PatternType.STRATEGY_ALGORITHM_INTERFACE: PatternMetadata(
        pattern_type=PatternType.STRATEGY_ALGORITHM_INTERFACE,
        name="Strategy Algorithm Interface",
        category=PatternCategory.BEHAVIORAL,
        description="Strategy pattern encapsulating interchangeable algorithms behind a common interface.",
        default_weight=0.90,
    ),
    PatternType.TEMPLATE_METHOD_LIFECYCLE: PatternMetadata(
        pattern_type=PatternType.TEMPLATE_METHOD_LIFECYCLE,
        name="Template Method Lifecycle",
        category=PatternCategory.BEHAVIORAL,
        description="Template Method pattern executing fixed framework hooks (initState -> didChangeDependencies -> build -> dispose).",
        default_weight=0.92,
    ),
    PatternType.VISITOR_WIDGET_TRAVERSAL: PatternMetadata(
        pattern_type=PatternType.VISITOR_WIDGET_TRAVERSAL,
        name="Visitor Widget Traversal",
        category=PatternCategory.BEHAVIORAL,
        description="Visitor pattern recursively traversing element trees or AST nodes without altering node classes.",
        default_weight=0.90,
    ),

    # Security & Memory Hazards
    PatternType.ASYNC_GAP_CONTEXT_USE_HAZARD: PatternMetadata(
        pattern_type=PatternType.ASYNC_GAP_CONTEXT_USE_HAZARD,
        name="Async Gap BuildContext Hazard",
        category=PatternCategory.DART_FLUTTER_SECURITY_HAZARDS,
        description="Using BuildContext after an 'await' point without checking 'if (!context.mounted) return', risking crashes on unmounted widgets.",
        default_weight=0.95,
    ),
    PatternType.UNCLOSED_STREAM_CONTROLLER_HAZARD: PatternMetadata(
        pattern_type=PatternType.UNCLOSED_STREAM_CONTROLLER_HAZARD,
        name="Unclosed StreamController Leak Hazard",
        category=PatternCategory.DART_FLUTTER_SECURITY_HAZARDS,
        description="StreamController instantiated in StatefulWidget or Service without corresponding close() in dispose(), leaking memory.",
        default_weight=0.90,
    ),
    PatternType.HARDCODED_API_KEY_SECRET_HAZARD: PatternMetadata(
        pattern_type=PatternType.HARDCODED_API_KEY_SECRET_HAZARD,
        name="Hardcoded API Key / Secret Hazard",
        category=PatternCategory.DART_FLUTTER_SECURITY_HAZARDS,
        description="Hardcoded private API keys, bearer tokens, or secret credentials embedded directly in client source code.",
        default_weight=0.95,
    ),
    PatternType.UNSAFE_EVAL_JS_INJECTION_HAZARD: PatternMetadata(
        pattern_type=PatternType.UNSAFE_EVAL_JS_INJECTION_HAZARD,
        name="Unsafe evaluateJavascript Injection Hazard",
        category=PatternCategory.DART_FLUTTER_SECURITY_HAZARDS,
        description="Direct string interpolation into Webview evaluateJavascript without escaping, risking Cross-Site Scripting (XSS).",
        default_weight=0.92,
    ),
    PatternType.SETSTATE_DURING_BUILD_HAZARD: PatternMetadata(
        pattern_type=PatternType.SETSTATE_DURING_BUILD_HAZARD,
        name="setState() Called During build() Hazard",
        category=PatternCategory.DART_FLUTTER_SECURITY_HAZARDS,
        description="Synchronous setState() invocation inside the build() method triggering infinite rebuild loops and framework crashes.",
        default_weight=0.92,
    ),
    PatternType.LATE_INITIALIZATION_RACE_HAZARD: PatternMetadata(
        pattern_type=PatternType.LATE_INITIALIZATION_RACE_HAZARD,
        name="Unchecked Late Initialization Race Hazard",
        category=PatternCategory.DART_FLUTTER_SECURITY_HAZARDS,
        description="Late field accessed without guaranteed preceding assignment, risking runtime LateInitializationError.",
        default_weight=0.88,
    ),

    # SOLID Principles
    PatternType.MONOLITHIC_WIDGET_SRP: PatternMetadata(
        pattern_type=PatternType.MONOLITHIC_WIDGET_SRP,
        name="Monolithic Widget (SRP Violation)",
        category=PatternCategory.SOLID_PRINCIPLES,
        description="Excessively large Widget with build() method > 100 lines or declaring excessive state fields.",
        default_weight=0.85,
    ),
    PatternType.GOD_CLASS_SERVICE_SRP: PatternMetadata(
        pattern_type=PatternType.GOD_CLASS_SERVICE_SRP,
        name="God Class Service (SRP Violation)",
        category=PatternCategory.SOLID_PRINCIPLES,
        description="Service class defining excessive public methods (>15), indicating violation of Single Responsibility Principle.",
        default_weight=0.85,
    ),
    PatternType.FAT_ABSTRACT_INTERFACE_ISP: PatternMetadata(
        pattern_type=PatternType.FAT_ABSTRACT_INTERFACE_ISP,
        name="Fat Abstract Interface (ISP Violation)",
        category=PatternCategory.SOLID_PRINCIPLES,
        description="Abstract interface class declaring excessive methods (>12), violating Interface Segregation Principle.",
        default_weight=0.85,
    ),
}
