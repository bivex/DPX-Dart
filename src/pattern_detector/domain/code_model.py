from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from .value_objects import SourceLocation


@dataclass
class DartConstructor:
    name: str
    is_factory: bool = False
    is_const: bool = False
    parameters: List[str] = field(default_factory=list)
    line_number: int = 1


@dataclass
class DartMethod:
    name: str
    return_type: str = "void"
    is_static: bool = False
    is_async: bool = False
    is_generator: bool = False
    parameters: List[str] = field(default_factory=list)
    body: str = ""
    line_number: int = 1
    lines_count: int = 1


@dataclass
class DartField:
    name: str
    type_annotation: str = "dynamic"
    is_final: bool = False
    is_const: bool = False
    is_late: bool = False
    default_value: Optional[str] = None
    line_number: int = 1


@dataclass
class DartClass:
    name: str
    is_abstract: bool = False
    is_sealed: bool = False
    is_base: bool = False
    is_interface: bool = False
    is_final: bool = False
    extends_class: Optional[str] = None
    with_mixins: List[str] = field(default_factory=list)
    implements_interfaces: List[str] = field(default_factory=list)
    constructors: List[DartConstructor] = field(default_factory=list)
    methods: List[DartMethod] = field(default_factory=list)
    fields: List[DartField] = field(default_factory=list)
    raw_body: str = ""
    line_number: int = 1

    @property
    def method_count(self) -> int:
        return len(self.methods)

    @property
    def is_widget(self) -> bool:
        ext = (self.extends_class or "").lower()
        return "statelesswidget" in ext or "statefulwidget" in ext or "inheritedwidget" in ext or "consumerwidget" in ext or "state<" in ext


@dataclass
class DartEnum:
    name: str
    values: List[str] = field(default_factory=list)
    fields: List[DartField] = field(default_factory=list)
    methods: List[DartMethod] = field(default_factory=list)
    line_number: int = 1

    @property
    def is_enhanced(self) -> bool:
        return len(self.fields) > 0 or len(self.methods) > 0


@dataclass
class DartMixin:
    name: str
    on_types: List[str] = field(default_factory=list)
    methods: List[DartMethod] = field(default_factory=list)
    fields: List[DartField] = field(default_factory=list)
    line_number: int = 1


@dataclass
class DartExtension:
    name: str
    on_type: str = "Object"
    is_extension_type: bool = False
    methods: List[DartMethod] = field(default_factory=list)
    line_number: int = 1


@dataclass
class DartFunction:
    name: str
    return_type: str = "void"
    is_async: bool = False
    is_generator: bool = False
    parameters: List[str] = field(default_factory=list)
    body: str = ""
    line_number: int = 1


@dataclass
class DartFile:
    file_path: str
    raw_content: str
    imports: List[str] = field(default_factory=list)
    classes: List[DartClass] = field(default_factory=list)
    enums: List[DartEnum] = field(default_factory=list)
    mixins: List[DartMixin] = field(default_factory=list)
    extensions: List[DartExtension] = field(default_factory=list)
    functions: List[DartFunction] = field(default_factory=list)


@dataclass
class CodeModel:
    files: List[DartFile] = field(default_factory=list)
    class_index: Dict[str, DartClass] = field(default_factory=dict)

    def add_file(self, file: DartFile) -> None:
        self.files.append(file)
        for cls in file.classes:
            self.class_index[cls.name.lower()] = cls

    def get_class(self, name: str) -> Optional[DartClass]:
        return self.class_index.get(name.lower())
