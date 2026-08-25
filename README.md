# 🎯 DPX-Dart: Architectural Pattern & Static Analysis Engine for Dart 3.x & Flutter

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Architecture: Hexagonal DDD](https://img.shields.io/badge/Architecture-Hexagonal%20DDD-green.svg)](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software))
[![Patterns: 44 Rules](https://img.shields.io/badge/Patterns-44%20Rules-orange.svg)](#-supported-patterns--hazard-catalog)

**DPX-Dart** is a high-performance static analysis and architectural pattern detection engine for **Dart 3.x & Flutter** codebases.

Built with **Hexagonal Clean Architecture (DDD)**, DPX-Dart maps reactive UI trees, BLoC/Riverpod state machines, asynchronous streams, and GoF patterns to **44 architectural patterns and Flutter/Dart security & memory hazards**.

---

## 🏛️ Architecture & Design Philosophy

DPX-Dart follows Domain-Driven Design and Ports & Adapters (Hexagonal) architecture:

```
src/pattern_detector/
├── domain/                      # Core business logic & invariants (Zero external dependencies)
│   ├── code_model.py            # AST/Code Model (DartClass, DartEnum, DartMixin, DartExtension, DartFunction)
│   ├── detection.py             # Detection & DetectionReport aggregates
│   ├── pattern.py               # 44 Pattern catalog definitions & weights
│   ├── value_objects.py         # Confidence, SourceLocation, PatternCategory, PatternType
│   └── rules/                   # 44 Pattern Detection Rules
│       ├── idiomatic_rules.py   # Sealed Classes, Records, Pattern Matching, Extension Types, Mixins
│       ├── flutter_rules.py     # BLoC/Cubit, Riverpod, InheritedWidget, ValueNotifier, Clean UseCases
│       ├── concurrency_rules.py # Isolates, StreamTransformers, Async Streams, Yield
│       ├── creational_rules.py  # Factory Constructors, Widget Builders, CopyWith, Singletons, GetIt
│       ├── structural_rules.py  # Type Adapters, MethodChannels, Widget Composite Tree, Decorators
│       ├── behavioral_rules.py  # Middleware Interceptors, BLoC Events, Listenable Observers, Mementos
│       ├── security_rules.py    # Async Gap Context Use, Unclosed StreamControllers, Hardcoded Secrets
│       └── solid_principles_rules.py # Monolithic Widgets, God Services, Fat Abstract Interfaces
├── ports/                       # Interfaces defining domain boundaries
│   ├── inbound/                 # ParserPort, PatternDetectorPort
│   └── outbound/                # ExporterPort (HTML, JSON, Markdown, SARIF)
├── adapters/                    # Concrete technology implementations
│   ├── inbound/
│   │   ├── parsers/             # RegexDartParser (Single-pass Dart 3.x parser)
│   │   ├── detectors/           # DartPatternDetector engine
│   │   └── cli/                 # Typer & Rich interactive CLI
│   └── outbound/
│       └── exporters/           # Interactive HTML HUD, SARIF v2.1.0, JSON, Markdown
└── application/
    └── scan_service.py          # Orchestration service
```

---

## 🔍 Supported Patterns & Hazard Catalog (44 Rules)

| Category | Pattern Type | Target / Construct | Default Weight | Description |
|---|---|---|:---:|---|
| **Dart 3.x Modern** | `sealed_class_adt` | `sealed class Result<T>` | 95% | Exhaustive Algebraic Data Types and pattern matching |
| | `pattern_matching_switch` | `switch (state) { ... }` | 92% | Dart 3 pattern matching and destructuring |
| | `record_multiple_return` | `(int, String) getUser()` | 90% | Anonymous tuple records for type-safe multiple returns |
| | `extension_type_inlined` | `extension type Id(int)` | 92% | Zero-cost inlined type-safe wrapper |
| | `enhanced_enum_members` | `enum Status { ... }` | 90% | Enhanced enums with custom fields, getters, and constructors |
| | `mixin_behavior_composition`| `mixin Loggable on Service`| 92% | Reusable linear horizontal code composition |
| | `extension_method_sugar` | `extension StringExt on ...`| 90% | Ad-hoc retroactive API extension |
| **Flutter Reactive** | `bloc_cubit_state_machine` | `Bloc<Event, State>` | 95% | Unidirectional reactive state machine with emit() |
| | `riverpod_notifier_di` | `NotifierProvider / ref` | 92% | Compile-safe dependency injection & reactive scoping |
| | `inherited_widget_provider`| `InheritedWidget / of(ctx)`| 92% | Ambient widget-tree subtree data propagation |
| | `change_notifier_store` | `ChangeNotifier / notify` | 90% | Micro-reactive observable state store |
| | `clean_usecase_interactor`| `UseCase<Type, Params>` | 90% | Domain business logic interactors |
| **Concurrency & Async** | `isolate_worker_pool` | `Isolate.spawn / compute`| 92% | Off-main-thread heavy CPU computation worker |
| | `async_stream_pipeline` | `Stream<T> / async*` | 92% | Asynchronous event stream generation and transformation |
| **GoF Creational** | `factory_constructor` | `factory Class.fromMap()` | 92% | Factory pattern constructing subtype or cached instances |
| | `builder_widget_pattern` | `WidgetBuilder / builder:` | 90% | Builder pattern lazily instantiating contextual widgets |
| | `prototype_copy_with` | `copyWith(...)` | 92% | Prototype pattern cloning immutable objects with mutations |
| | `singleton_instance` | `ClassName._internal()` | 92% | Thread-safe single instance access via static getter |
| | `service_locator_di` | `GetIt.instance<T>()` | 90% | Global decoupled service locator registry |
| **GoF Structural** | `adapter_type_converter` | `TypeAdapter / toDomain` | 90% | Converting third-party/platform models to domain entities |
| | `bridge_platform_channel` | `MethodChannel / invoke` | 92% | Bridge pattern communicating across Dart/Native boundaries |
| | `composite_widget_tree` | `Widget build(ctx)` | 95% | Composite pattern structuring nested UI elements |
| | `decorator_wrapper_widget`| `Padding / DecoratedBox` | 90% | Decorator pattern dynamically augmenting widget presentation |
| | `facade_api_client` | `ApiClient / Repository` | 90% | Facade pattern providing unified interface over HTTP/Cache |
| | `flyweight_const_instance`| `const Constructor()` | 92% | Canonical memory sharing of compile-time constants |
| | `proxy_cached_repository` | `CachedRepo implements ...`| 90% | Proxy pattern intercepting calls with local caching |
| **GoF Behavioral** | `chain_middleware_interceptor` | `Interceptor / next` | 90% | Chain of Responsibility filtering HTTP requests/responses |
| | `command_intent_action` | `abstract class Event` | 92% | Command pattern encapsulating UI user actions |
| | `iterator_sync_generator` | `Iterable<T> sync*` | 90% | Lazy pull-based generator yielding elements |
| | `mediator_event_bus` | `EventBus.fire() / on<T>` | 92% | Decoupled cross-module event dispatching |
| | `memento_hydrated_snapshot`| `toJson() / fromJson()` | 92% | Memento pattern serializing and restoring state |
| | `observer_listenable_stream`| `StreamSubscription / watch`| 92% | Observer pattern subscribing to state changes |
| | `state_machine_hierarchy` | `sealed class OrderState` | 92% | Finite state machine modeling explicit transitions |
| | `strategy_algorithm_interface`| `PaymentStrategy` | 90% | Interchangeable domain algorithm strategies |
| | `template_method_lifecycle`| `initState() / dispose()` | 92% | Fixed lifecycle template method execution |
| | `visitor_widget_traversal`| `visitChildren(visitor)` | 90% | Visitor pattern traversing element trees |
| **Security & Memory Hazards** | `async_gap_context_use_hazard`| `await ... context.read` | 95% | Using BuildContext across async gaps without checking mounted |
| | `unclosed_stream_controller_hazard`| `StreamController` unclosed | 90% | Unclosed StreamController in State causing memory leak |
| | `hardcoded_api_key_secret_hazard`| `const apiKey = '...'` | 95% | Hardcoded secret keys or auth tokens in client code |
| | `unsafe_eval_js_injection_hazard`| `evaluateJavascript("$x")`| 92% | Unsanitized string interpolation into Webview JavaScript |
| | `setstate_during_build_hazard`| `setState()` in `build()` | 92% | Calling setState synchronously during widget build |
| | `late_initialization_race_hazard`| `late final x;` | 88% | Unchecked late field access risking LateInitializationError |
| **SOLID Principles** | `monolithic_widget_srp` | `build() > 100 lines` | 85% | Monolithic widget violating Single Responsibility |
| | `god_class_service_srp` | `Service > 15 methods` | 85% | God Class service handling multiple disparate domains |
| | `fat_abstract_interface_isp`| `Abstract class > 12 methods`| 85% | Fat interface violating Interface Segregation Principle |

---

## ⚡ Installation & CLI Usage

```bash
# Clone repository
git clone https://github.com/bivex/DPX-Dart.git
cd DPX-Dart

# Install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 🚀 Running Analysis

```bash
# 1. Quick scan on Dart / Flutter directory
dpx-dart scan lib/

# 2. Export Full Interactive HTML HUD + SARIF + JSON + Markdown
dpx-dart scan lib/ \
    -H reports/dpx_dart_hud.html \
    -J reports/dpx_dart_findings.json \
    -M reports/dpx_dart_report.md \
    -S reports/dpx_dart_report.sarif

# 3. View 44 supported pattern catalog
dpx-dart catalog
```

---

## 🌐 The DPX Multi-Language Static Analysis Family (28 Languages)

| # | Language | Repository | Ecosystem & Focus |
|:---:|---|---|---|
| 1 | **Clojure** | [`bivex/DPX`](https://github.com/bivex/DPX) | Lisp S-Expressions, Protocols, Multimethods |
| 2 | **C** | [`bivex/DPX-C`](https://github.com/bivex/DPX-C) | Memory Safety, Struct VTables, Idiomatic C11/C23 |
| 3 | **Cairo** | [`bivex/DPX-Cairo`](https://github.com/bivex/DPX-Cairo) | Starknet Smart Contracts, ZK-Rollup Invariants |
| 4 | **C++** | [`bivex/DPX-Cpp`](https://github.com/bivex/DPX-Cpp) | RAII, CRTP, Concepts, Modern C++20/23 |
| 5 | **C#** | [`bivex/DPX-CSharp`](https://github.com/bivex/DPX-CSharp) | .NET 9, Roslyn AST, Linq, Records |
| 6 | **Dart** | [`bivex/DPX-Dart`](https://github.com/bivex/DPX-Dart) | **Dart 3.x, Flutter, BLoC, Riverpod, Isolates** |
| 7 | **Elixir** | [`bivex/DPX-Elixir`](https://github.com/bivex/DPX-Elixir) | BEAM OTP, GenServer, Supervisors |
| 8 | **Erlang** | [`bivex/DPX-Erlang`](https://github.com/bivex/DPX-Erlang) | Fault Tolerance, Actor Model, OTP Behaviors |
| 9 | **Gleam** | [`bivex/DPX-Gleam`](https://github.com/bivex/DPX-Gleam) | Type-Safe BEAM, Actor Concurrency |
| 10 | **Go** | [`bivex/DPX-Go`](https://github.com/bivex/DPX-Go) | Goroutines, Channels, Composition, Interfaces |
| 11 | **Haskell** | [`bivex/DPX-Haskell`](https://github.com/bivex/DPX-Haskell) | Pure Functional, Monads, Typeclasses, Arrows |
| 12 | **Huff** | [`bivex/DPX-Huff`](https://github.com/bivex/DPX-Huff) | Low-Level EVM Bytecode & Opcodes |
| 13 | **Java** | [`bivex/DPX-Java`](https://github.com/bivex/DPX-Java) | Spring Boot, Enterprise Java, JVM Invariants |
| 14 | **Julia** | [`bivex/DPX-Julia`](https://github.com/bivex/DPX-Julia) | Multiple Dispatch, Scientific Computing |
| 15 | **Kotlin** | [`bivex/DPX-Kotlin`](https://github.com/bivex/DPX-Kotlin) | Coroutines, Multiplatform, Functional DSLs |
| 16 | **Lua** | [`bivex/DPX-Lua`](https://github.com/bivex/DPX-Lua) | Metatables, Coroutines, LuaJIT, Neovim |
| 17 | **Mojo** | [`bivex/DPX-Mojo`](https://github.com/bivex/DPX-Mojo) | SIMD Hardware, Memory Lifetimes, AI Systems |
| 18 | **Move** | [`bivex/DPX-Move`](https://github.com/bivex/DPX-Move) | Aptos & Sui Resource Safety, Linear Types |
| 19 | **OCaml** | [`bivex/DPX-OCaml`](https://github.com/bivex/DPX-OCaml) | Algebraic Data Types, Functors, Polymorphism |
| 20 | **PHP** | [`bivex/DPX-Php`](https://github.com/bivex/DPX-Php) | Modern PHP 8.4, Attributes, Traits, Laravel |
| 21 | **Python** | [`bivex/DPX-Py`](https://github.com/bivex/DPX-Py) | Metaprogramming, Protocols, Hexagonal DDD |
| 22 | **Rust** | [`bivex/DPX-Rust`](https://github.com/bivex/DPX-Rust) | Zero-Cost Abstractions, Borrow Checker, Traits |
| 23 | **Solidity** | [`bivex/DPX-Solidity`](https://github.com/bivex/DPX-Solidity) | DeFi Security, Reentrancy, EVM Yul/Assembly |
| 24 | **SQL** | [`bivex/DPX-SQL`](https://github.com/bivex/DPX-SQL) | PostgreSQL, MySQL, SQLite, T-SQL, PL/SQL |
| 25 | **Swift** | [`bivex/DPX-Swift`](https://github.com/bivex/DPX-Swift) | Protocol-Oriented Programming, Actors |
| 26 | **TypeScript** | [`bivex/DPX-TypeScript`](https://github.com/bivex/DPX-TypeScript) | Generics, Conditional Types, Clean Architecture |
| 27 | **Yul** | [`bivex/DPX-Yul`](https://github.com/bivex/DPX-Yul) | EVM Intermediate Representation Optimization |
| 28 | **Zig** | [`bivex/DPX-Zig`](https://github.com/bivex/DPX-Zig) | Comptime, Manual Memory Allocators, C ABI |

---

## 📄 License

MIT License © 2026 Bivex
