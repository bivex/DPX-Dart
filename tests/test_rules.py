import pytest
from pattern_detector.domain.value_objects import PatternType
from pattern_detector.domain.code_model import CodeModel
from pattern_detector.adapters.inbound.parsers.dart_parser import RegexDartParser
from pattern_detector.adapters.inbound.detectors.dart_detector import DartPatternDetector


COMPREHENSIVE_DART_CODE = """
import 'package:flutter/material.dart';
import 'package:bloc/bloc.dart';

sealed class AppState {}
class AppLoading extends AppState {}
class AppLoaded extends AppState {
  final String data;
  const AppLoaded(this.data);
  AppLoaded copyWith({String? data}) => AppLoaded(data ?? this.data);
}

class CounterBloc extends Bloc<CounterEvent, AppState> {
  CounterBloc() : super(AppLoading());
}

abstract class CounterEvent {}

class UserNotifier extends ChangeNotifier {
  void updateUser() {
    notifyListeners();
  }
}

abstract class GetUserUseCase {
  Future<String> call();
}

class ThreadWorker {
  void runComputation() {
    compute((int x) => x * 2, 21);
  }
}

class AuthTokenInterceptor {
  void intercept() {}
}

class NetworkClient {
  void fetchUsers() {}
  void fetchPosts() {}
  void fetchComments() {}
}

class DangerousAsyncWidget extends StatefulWidget {
  @override
  _DangerousAsyncWidgetState createState() => _DangerousAsyncWidgetState();
}

class _DangerousAsyncWidgetState extends State<DangerousAsyncWidget> {
  late String uninitializedLate;

  Future<void> triggerAsyncAction(BuildContext context) async {
    await Future.delayed(const Duration(seconds: 1));
    Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    return Container();
  }
}

const apiKey = "dpx_mock_secret_token_1234567890abcdef";
"""


def test_rule_evaluations():
    parser = RegexDartParser()
    file_ast = parser.parse_file("lib/main.dart", COMPREHENSIVE_DART_CODE)

    model = CodeModel()
    model.add_file(file_ast)

    detector = DartPatternDetector()
    report = detector.detect(model)

    detected_types = {d.pattern_type for d in report.detections}

    # Verify Idiomatic & Flutter Reactive Detections
    assert PatternType.SEALED_CLASS_ADT in detected_types
    assert PatternType.BLOC_CUBIT_STATE_MACHINE in detected_types
    assert PatternType.CHANGE_NOTIFIER_STORE in detected_types
    assert PatternType.CLEAN_USECASE_INTERACTOR in detected_types
    assert PatternType.ISOLATE_WORKER_POOL in detected_types
    assert PatternType.PROTOTYPE_COPY_WITH in detected_types
    assert PatternType.FLYWEIGHT_CONST_INSTANCE in detected_types
    assert PatternType.CHAIN_MIDDLEWARE_INTERCEPTOR in detected_types
    assert PatternType.COMMAND_INTENT_ACTION in detected_types
    assert PatternType.STATE_MACHINE_HIERARCHY in detected_types
    assert PatternType.FACADE_API_CLIENT in detected_types

    # Verify Security & Memory Hazards
    assert PatternType.ASYNC_GAP_CONTEXT_USE_HAZARD in detected_types
    assert PatternType.HARDCODED_API_KEY_SECRET_HAZARD in detected_types
    assert PatternType.LATE_INITIALIZATION_RACE_HAZARD in detected_types
