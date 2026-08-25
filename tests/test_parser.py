import pytest
from pattern_detector.adapters.inbound.parsers.dart_parser import RegexDartParser


SAMPLE_DART_CODE = """
import 'package:flutter/material.dart';
import 'package:bloc/bloc.dart';

sealed class AuthState {}
class AuthInitial extends AuthState {}
class AuthSuccess extends AuthState {
  final String token;
  const AuthSuccess(this.token);
}

enum Priority {
  low, high;
  final String label;
  const Priority(this.label);
}

mixin DiagnosticLogger on BaseService {
  void logTrace(String msg) {}
}

extension type UserId(int id) {}

extension StringCasing on String {
  String toTitleCase() => this[0].toUpperCase() + substring(1);
}

class UserCardWidget extends StatelessWidget {
  final Widget child;
  const UserCardWidget({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    return Container(child: child);
  }
}

class OrderService {
  static final OrderService instance = OrderService._internal();
  OrderService._internal();

  factory OrderService.fromMap(Map<String, dynamic> map) => instance;

  Stream<int> pollUpdates() async* {
    yield 1;
  }

  (int, String) getUserTuple() {
    return (42, 'Alice');
  }
}
"""


def test_regex_dart_parser():
    parser = RegexDartParser()
    file_ast = parser.parse_file("lib/sample.dart", SAMPLE_DART_CODE)

    assert len(file_ast.imports) == 2
    assert "package:flutter/material.dart" in file_ast.imports

    # Classes
    class_names = [c.name for c in file_ast.classes]
    assert "AuthState" in class_names
    assert "AuthSuccess" in class_names
    assert "UserCardWidget" in class_names
    assert "OrderService" in class_names

    auth_state = next(c for c in file_ast.classes if c.name == "AuthState")
    assert auth_state.is_sealed is True

    widget_cls = next(c for c in file_ast.classes if c.name == "UserCardWidget")
    assert widget_cls.is_widget is True

    order_svc = next(c for c in file_ast.classes if c.name == "OrderService")
    ctor_names = [c.name for c in order_svc.constructors]
    assert any(c.is_factory for c in order_svc.constructors)
    assert any("pollUpdates" in m.name and m.is_generator for m in order_svc.methods)

    # Enum
    assert len(file_ast.enums) == 1
    assert file_ast.enums[0].name == "Priority"
    assert file_ast.enums[0].is_enhanced is True

    # Mixin
    assert len(file_ast.mixins) == 1
    assert file_ast.mixins[0].name == "DiagnosticLogger"
    assert "BaseService" in file_ast.mixins[0].on_types

    # Extensions
    assert len(file_ast.extensions) == 2
    ext_types = [e for e in file_ast.extensions if e.is_extension_type]
    assert len(ext_types) == 1
    assert ext_types[0].name == "UserId"
