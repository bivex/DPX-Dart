# 🎯 DPX-Dart Analysis Report

- **Target Path**: `benchmarks/real_world/todos_overview_bloc.dart`
- **Scanned Files**: `4`
- **Execution Time**: `0.0017s`
- **Total Detections**: `27`

## 📊 Category Breakdown

| Category | Detections |
|---|:---:|
| `structural` | 19 |
| `flutter_reactive_architecture` | 5 |
| `dart_modern_idiomatic` | 1 |
| `creational` | 1 |
| `behavioral` | 1 |

## 🔍 Findings & Detections

| # | Category | Pattern Type | Target | Confidence | Location | Summary |
|---|---|---|---|:---:|---|---|
| 1 | `dart_modern_idiomatic` | `sealed_class_adt` | `TodosOverviewEvent` | **95%** [VERY_HIGH] | `todos_overview_event.dart:3` | Exhaustive Algebraic Data Types and pattern matching via Dart 3 sealed class hierarchies. |
| 2 | `flutter_reactive_architecture` | `bloc_cubit_state_machine` | `TodosOverviewBloc` | **95%** [VERY_HIGH] | `todos_overview_bloc.dart:9` | Unidirectional reactive state machine converting events into state streams using Bloc/Cubit. |
| 3 | `flutter_reactive_architecture` | `riverpod_notifier_di` | `Home` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:78` | Compile-time safe dependency injection and reactive state scoping via Riverpod Providers. |
| 4 | `flutter_reactive_architecture` | `riverpod_notifier_di` | `Toolbar` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:127` | Compile-time safe dependency injection and reactive state scoping via Riverpod Providers. |
| 5 | `flutter_reactive_architecture` | `riverpod_notifier_di` | `TodoItem` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:231` | Compile-time safe dependency injection and reactive state scoping via Riverpod Providers. |
| 6 | `flutter_reactive_architecture` | `riverpod_notifier_di` | `RiverpodProvider` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:1` | Compile-time safe dependency injection and reactive state scoping via Riverpod Providers. |
| 7 | `creational` | `prototype_copy_with` | `TodosOverviewBloc` | **92%** [VERY_HIGH] | `todos_overview_bloc.dart:9` | Prototype pattern cloning immutable models with selective field overwrites via copyWith(). |
| 8 | `structural` | `composite_widget_tree` | `MyApp` | **95%** [VERY_HIGH] | `riverpod_todos_app.dart:69` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 9 | `structural` | `composite_widget_tree` | `Home` | **95%** [VERY_HIGH] | `riverpod_todos_app.dart:78` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 10 | `structural` | `composite_widget_tree` | `Toolbar` | **95%** [VERY_HIGH] | `riverpod_todos_app.dart:127` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 11 | `structural` | `composite_widget_tree` | `Title` | **95%** [VERY_HIGH] | `riverpod_todos_app.dart:199` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 12 | `structural` | `composite_widget_tree` | `TodoItem` | **95%** [VERY_HIGH] | `riverpod_todos_app.dart:231` | Composite pattern structuring hierarchical UI elements where containers treat leaf widgets uniformly. |
| 13 | `structural` | `flyweight_const_instance` | `TodosOverviewEvent` | **92%** [VERY_HIGH] | `todos_overview_event.dart:3` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 14 | `structural` | `flyweight_const_instance` | `TodosOverviewSubscriptionRequested` | **92%** [VERY_HIGH] | `todos_overview_event.dart:10` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 15 | `structural` | `flyweight_const_instance` | `TodosOverviewTodoCompletionToggled` | **92%** [VERY_HIGH] | `todos_overview_event.dart:14` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 16 | `structural` | `flyweight_const_instance` | `TodosOverviewTodoDeleted` | **92%** [VERY_HIGH] | `todos_overview_event.dart:27` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 17 | `structural` | `flyweight_const_instance` | `TodosOverviewUndoDeletionRequested` | **92%** [VERY_HIGH] | `todos_overview_event.dart:36` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 18 | `structural` | `flyweight_const_instance` | `TodosOverviewFilterChanged` | **92%** [VERY_HIGH] | `todos_overview_event.dart:40` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 19 | `structural` | `flyweight_const_instance` | `TodosOverviewToggleAllRequested` | **92%** [VERY_HIGH] | `todos_overview_event.dart:49` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 20 | `structural` | `flyweight_const_instance` | `TodosOverviewClearCompletedRequested` | **92%** [VERY_HIGH] | `todos_overview_event.dart:53` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 21 | `structural` | `flyweight_const_instance` | `TodosOverviewState` | **92%** [VERY_HIGH] | `todos_overview_state.dart:5` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 22 | `structural` | `flyweight_const_instance` | `MyApp` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:69` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 23 | `structural` | `flyweight_const_instance` | `Home` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:78` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 24 | `structural` | `flyweight_const_instance` | `Toolbar` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:127` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 25 | `structural` | `flyweight_const_instance` | `Title` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:199` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 26 | `structural` | `flyweight_const_instance` | `TodoItem` | **92%** [VERY_HIGH] | `riverpod_todos_app.dart:231` | Flyweight pattern deduplicating identical immutable objects into canonical memory addresses via const constructor. |
| 27 | `behavioral` | `command_intent_action` | `TodosOverviewEvent` | **92%** [VERY_HIGH] | `todos_overview_event.dart:3` | Command pattern encapsulating user intents into standalone command objects (BLoC Events / Redux Actions). |
