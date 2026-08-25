# 🎯 DPX-Dart Analysis Report

- **Target Path**: `benchmarks/fintech_crypto_flutter_app.dart`
- **Scanned Files**: `5`
- **Execution Time**: `0.0022s`
- **Total Detections**: `61`

## 📊 Category Breakdown

| Category | Detections |
|---|:---:|
| `structural` | 30 |
| `dart_modern_idiomatic` | 7 |
| `flutter_reactive_architecture` | 7 |
| `creational` | 5 |
| `behavioral` | 5 |
| `concurrency_async` | 4 |
| `dart_flutter_security_hazards` | 3 |

## 🔍 Findings & Detections

| # | Category | Pattern Type | Target | Confidence | Location | Summary |
|---|---|---|---|:---:|---|---|
| 1 | `dart_modern_idiomatic` | `sealed_class_adt` | `WalletState` | **95%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:11` | Exhaustive Algebraic Data Types and pattern matching via Dart 3 sealed class hierarchies. |
| 2 | `dart_modern_idiomatic` | `sealed_class_adt` | `TodosOverviewEvent` | **95%** [VERY_HIGH] | `todos_overview_event.dart:3` | Exhaustive Algebraic Data Types and pattern matching via Dart 3 sealed class hierarchies. |
| 3 | `dart_modern_idiomatic` | `pattern_matching_switch` | `describeWalletState` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:60` | Dart 3 pattern matching, switch expressions, and structural record destructuring. |
| 4 | `dart_modern_idiomatic` | `extension_type_inlined` | `CryptoId` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:55` | Zero-cost compile-time type-safe inline wrappers via Dart 3 extension type. |
| 5 | `dart_modern_idiomatic` | `enhanced_enum_members` | `BlockchainNetwork` | **90%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:72` | Enhanced enum declaring explicit fields, getters, constructors, and interface implementations. |
| 6 | `dart_modern_idiomatic` | `mixin_behavior_composition` | `DiagnosticLogger` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:85` | Reusable horizontal behavior composition and constrained mixins via 'mixin ... on ...'. |
| 7 | `dart_modern_idiomatic` | `extension_method_sugar` | `StringCryptoFormatting` | **90%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:92` | Retroactive API extension augmenting third-party or core classes without subclassing. |
| 8 | `flutter_reactive_architecture` | `bloc_cubit_state_machine` | `TodosOverviewBloc` | **95%** [VERY_HIGH] | `todos_overview_bloc.dart:9` | Unidirectional reactive state machine converting events into state streams using Bloc/Cubit. |
| 9 | `flutter_reactive_architecture` | `riverpod_notifier_di` | `Home` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:78` | Compile-time safe dependency injection and reactive state scoping via Riverpod Providers. |
| 10 | `flutter_reactive_architecture` | `riverpod_notifier_di` | `Toolbar` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:127` | Compile-time safe dependency injection and reactive state scoping via Riverpod Providers. |
| 11 | `flutter_reactive_architecture` | `riverpod_notifier_di` | `TodoItem` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:231` | Compile-time safe dependency injection and reactive state scoping via Riverpod Providers. |
| 12 | `flutter_reactive_architecture` | `riverpod_notifier_di` | `RiverpodProvider` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:1` | Compile-time safe dependency injection and reactive state scoping via Riverpod Providers. |
| 13 | `flutter_reactive_architecture` | `clean_usecase_interactor` | `TransferFundsUseCase` | **90%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:100` | Single-purpose domain business interactor encapsulating transactional application logic. |
| 14 | `flutter_reactive_architecture` | `clean_usecase_interactor` | `TransferFundsUseCaseImpl` | **90%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:104` | Single-purpose domain business interactor encapsulating transactional application logic. |
| 15 | `concurrency_async` | `isolate_worker_pool` | `CryptoHashWorker.computeSha256Parallel` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:142` | Heavy CPU background task execution on isolated memory threads via Isolate.spawn() or compute(). |
| 16 | `concurrency_async` | `isolate_worker_pool` | `computeSha256Parallel` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:142` | Heavy CPU background task execution on isolated memory threads via Isolate.spawn() or compute(). |
| 17 | `concurrency_async` | `async_stream_pipeline` | `CryptoHashWorker.streamBlockConfirmations` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:150` | Asynchronous event streaming and reactive transformations via Stream<T>, async*, and yield. |
| 18 | `concurrency_async` | `async_stream_pipeline` | `streamBlockConfirmations` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:149` | Asynchronous event streaming and reactive transformations via Stream<T>, async*, and yield. |
| 19 | `creational` | `factory_constructor` | `WalletSuccess.WalletSuccess.fromJson` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:36` | Factory pattern implementing customized instance instantiation or cached return via factory keyword. |
| 20 | `creational` | `factory_constructor` | `SystemEnvironmentConfig.SystemEnvironmentConfig.fromMap` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:170` | Factory pattern implementing customized instance instantiation or cached return via factory keyword. |
| 21 | `creational` | `builder_widget_pattern` | `CryptoWalletCardWidget.build` | **90%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:178` | Builder pattern lazily constructing contextual widget subtrees via (BuildContext, ...) callback builders. |
| 22 | `creational` | `prototype_copy_with` | `WalletSuccess` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:23` | Prototype pattern cloning immutable models with selective field overwrites via copyWith(). |
| 23 | `creational` | `prototype_copy_with` | `TodosOverviewBloc` | **92%** [VERY_HIGH] | `todos_overview_bloc.dart:9` | Prototype pattern cloning immutable models with selective field overwrites via copyWith(). |
| 24 | `structural` | `composite_widget_tree` | `CryptoWalletCardWidget` | **95%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:174` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 25 | `structural` | `composite_widget_tree` | `DangerousWalletScreen` | **95%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:199` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 26 | `structural` | `composite_widget_tree` | `_DangerousWalletScreenState` | **95%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:206` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 27 | `structural` | `composite_widget_tree` | `MyApp` | **95%** [VERY_HIGH] | `riverpod_todos_app.dart:69` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 28 | `structural` | `composite_widget_tree` | `Home` | **95%** [VERY_HIGH] | `riverpod_todos_app.dart:78` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 29 | `structural` | `composite_widget_tree` | `Toolbar` | **95%** [VERY_HIGH] | `riverpod_todos_app.dart:127` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 30 | `structural` | `composite_widget_tree` | `Title` | **95%** [VERY_HIGH] | `riverpod_todos_app.dart:199` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 31 | `structural` | `composite_widget_tree` | `TodoItem` | **95%** [VERY_HIGH] | `riverpod_todos_app.dart:231` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 32 | `structural` | `flyweight_const_instance` | `WalletState` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:11` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 33 | `structural` | `flyweight_const_instance` | `WalletInitial` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:15` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 34 | `structural` | `flyweight_const_instance` | `WalletLoading` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:19` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 35 | `structural` | `flyweight_const_instance` | `WalletSuccess` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:23` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 36 | `structural` | `flyweight_const_instance` | `WalletFailure` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:40` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 37 | `structural` | `flyweight_const_instance` | `CryptoWalletCardWidget` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:174` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 38 | `structural` | `flyweight_const_instance` | `DangerousWalletScreen` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:199` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 39 | `structural` | `flyweight_const_instance` | `TodosOverviewEvent` | **92%** [VERY_HIGH] | `todos_overview_event.dart:3` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 40 | `structural` | `flyweight_const_instance` | `TodosOverviewSubscriptionRequested` | **92%** [VERY_HIGH] | `todos_overview_event.dart:10` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 41 | `structural` | `flyweight_const_instance` | `TodosOverviewTodoCompletionToggled` | **92%** [VERY_HIGH] | `todos_overview_event.dart:14` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 42 | `structural` | `flyweight_const_instance` | `TodosOverviewTodoDeleted` | **92%** [VERY_HIGH] | `todos_overview_event.dart:27` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 43 | `structural` | `flyweight_const_instance` | `TodosOverviewUndoDeletionRequested` | **92%** [VERY_HIGH] | `todos_overview_event.dart:36` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 44 | `structural` | `flyweight_const_instance` | `TodosOverviewFilterChanged` | **92%** [VERY_HIGH] | `todos_overview_event.dart:40` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 45 | `structural` | `flyweight_const_instance` | `TodosOverviewToggleAllRequested` | **92%** [VERY_HIGH] | `todos_overview_event.dart:49` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 46 | `structural` | `flyweight_const_instance` | `TodosOverviewClearCompletedRequested` | **92%** [VERY_HIGH] | `todos_overview_event.dart:53` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 47 | `structural` | `flyweight_const_instance` | `TodosOverviewState` | **92%** [VERY_HIGH] | `todos_overview_state.dart:5` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 48 | `structural` | `flyweight_const_instance` | `MyApp` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:69` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 49 | `structural` | `flyweight_const_instance` | `Home` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:78` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 50 | `structural` | `flyweight_const_instance` | `Toolbar` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:127` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 51 | `structural` | `flyweight_const_instance` | `Title` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:199` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 52 | `structural` | `flyweight_const_instance` | `TodoItem` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:231` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 53 | `structural` | `proxy_cached_repository` | `CryptoRepositoryProxy` | **90%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:120` | Proxy pattern intercepting data requests to transparently serve local cache before remote network fetch. |
| 54 | `behavioral` | `command_intent_action` | `WalletEvent` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:46` | Command pattern encapsulating user intents into standalone command objects (BLoC Events / Redux Actions). |
| 55 | `behavioral` | `command_intent_action` | `TodosOverviewEvent` | **92%** [VERY_HIGH] | `todos_overview_event.dart:3` | Command pattern encapsulating user intents into standalone command objects (BLoC Events / Redux Actions). |
| 56 | `behavioral` | `iterator_sync_generator` | `CryptoHashWorker.generateNonceSequence` | **90%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:157` | Iterator pattern generating lazily computed sequences on demand via sync* and yield. |
| 57 | `behavioral` | `iterator_sync_generator` | `generateNonceSequence` | **90%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:156` | Iterator pattern generating lazily computed sequences on demand via sync* and yield. |
| 58 | `behavioral` | `state_machine_hierarchy` | `WalletState` | **92%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:11` | State pattern representing distinct lifecycle states as polymorphic subtype instances (Initial, Loading, Success, Failure). |
| 59 | `dart_flutter_security_hazards` | `async_gap_context_use_hazard` | `_DangerousWalletScreenState.submitTransferDangerous` | **95%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:210` | Using BuildContext after an 'await' point without checking 'if (!context.mounted) return', risking crashes on unmounted widgets. |
| 60 | `dart_flutter_security_hazards` | `unclosed_stream_controller_hazard` | `_DangerousWalletScreenState` | **90%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:206` | StreamController instantiated in StatefulWidget or Service without corresponding close() in dispose(), leaking memory. |
| 61 | `dart_flutter_security_hazards` | `late_initialization_race_hazard` | `_DangerousWalletScreenState.uninitializedWalletKey` | **88%** [VERY_HIGH] | `fintech_crypto_flutter_app.dart:208` | Late field accessed without guaranteed preceding assignment, risking runtime LateInitializationError. |
