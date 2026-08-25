import os
import re
from typing import List, Dict, Optional
from ....domain.code_model import (
    DartConstructor,
    DartMethod,
    DartField,
    DartClass,
    DartEnum,
    DartMixin,
    DartExtension,
    DartFunction,
    DartFile,
    CodeModel,
)
from ....ports.inbound.parser_port import DartParserPort


class RegexDartParser(DartParserPort):
    """
    Robust, single-pass Dart 3.x and Flutter source code parser.
    """

    def parse_file(self, file_path: str, content: str) -> DartFile:
        dart_file = DartFile(file_path=file_path, raw_content=content)

        # 1. Parse imports
        self._parse_imports(content, dart_file)

        # 2. Parse classes
        self._parse_classes(content, dart_file)

        # 3. Parse enums
        self._parse_enums(content, dart_file)

        # 4. Parse mixins
        self._parse_mixins(content, dart_file)

        # 5. Parse extensions & extension types
        self._parse_extensions(content, dart_file)

        # 6. Parse top-level functions
        self._parse_functions(content, dart_file)

        return dart_file

    def parse_code_model(self, paths: List[str]) -> CodeModel:
        model = CodeModel()
        for path in paths:
            if os.path.isfile(path) and path.endswith(".dart"):
                try:
                    with open(path, "r", encoding="utf-8", errors="replace") as f:
                        content = f.read()
                    dart_file = self.parse_file(path, content)
                    model.add_file(dart_file)
                except Exception:
                    pass
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    for file in files:
                        if file.endswith(".dart"):
                            full_path = os.path.join(root, file)
                            try:
                                with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                                    content = f.read()
                                dart_file = self.parse_file(full_path, content)
                                model.add_file(dart_file)
                            except Exception:
                                pass
        return model

    def _get_line_number(self, content: str, match_start: int) -> int:
        return content.count("\n", 0, match_start) + 1

    def _parse_imports(self, content: str, dart_file: DartFile) -> None:
        pattern = re.compile(r'\bimport\s+[\'"]([^\'"]+)[\'"]', re.MULTILINE)
        for m in pattern.finditer(content):
            dart_file.imports.append(m.group(1))

    def _extract_balanced_block(self, content: str, start_pos: int) -> Optional[str]:
        brace_pos = content.find("{", start_pos)
        if brace_pos == -1:
            return None
        depth = 1
        idx = brace_pos + 1
        while idx < len(content) and depth > 0:
            if content[idx] == "{":
                depth += 1
            elif content[idx] == "}":
                depth -= 1
                if depth == 0:
                    return content[brace_pos + 1 : idx]
            idx += 1
        return None

    def _parse_classes(self, content: str, dart_file: DartFile) -> None:
        class_header_pattern = re.compile(
            r'\b(?:(sealed|abstract|base|interface|final)\s+)*class\s+([a-zA-Z0-9_]+)(?:<[^>]+>)?(?:\s+extends\s+([a-zA-Z0-9_<>,?\s]+?))?(?:\s+with\s+([a-zA-Z0-9_<>,?\s]+?))?(?:\s+implements\s+([a-zA-Z0-9_<>,?\s]+?))?\s*\{',
            re.MULTILINE,
        )

        for match in class_header_pattern.finditer(content):
            full_header = match.group(0)
            class_name = match.group(2)
            extends_class = match.group(3).strip() if match.group(3) else None
            with_mixins_raw = match.group(4)
            implements_raw = match.group(5)
            line_num = self._get_line_number(content, match.start())

            is_sealed = "sealed" in full_header
            is_abstract = "abstract" in full_header
            is_base = "base" in full_header
            is_interface = "interface" in full_header
            is_final = "final" in full_header

            with_mixins = [m.strip() for m in with_mixins_raw.split(",")] if with_mixins_raw else []
            implements_interfaces = [i.strip() for i in implements_raw.split(",")] if implements_raw else []

            body = self._extract_balanced_block(content, match.start()) or ""

            cls = DartClass(
                name=class_name,
                is_abstract=is_abstract,
                is_sealed=is_sealed,
                is_base=is_base,
                is_interface=is_interface,
                is_final=is_final,
                extends_class=extends_class,
                with_mixins=with_mixins,
                implements_interfaces=implements_interfaces,
                raw_body=body,
                line_number=line_num,
            )

            # Parse methods, constructors, and fields within class body
            self._parse_class_members(body, cls, line_num)
            dart_file.classes.append(cls)

    def _parse_class_members(self, body: str, cls: DartClass, class_line: int) -> None:
        # 1. Parse Constructors: [const|factory] ClassName[._name](...)
        ctor_pattern = re.compile(
            rf'\b(?:(const|factory)\s+)?{cls.name}(?:\.([a-zA-Z0-9_]+))?\s*\(([^)]*)\)',
            re.MULTILINE,
        )
        for m in ctor_pattern.finditer(body):
            modifier = m.group(1) or ""
            ctor_subname = m.group(2) or ""
            params_raw = m.group(3) or ""
            line_num = class_line + body.count("\n", 0, m.start())

            full_ctor_name = f"{cls.name}.{ctor_subname}" if ctor_subname else cls.name
            params = [p.strip() for p in params_raw.split(",") if p.strip()]

            ctor = DartConstructor(
                name=full_ctor_name,
                is_factory="factory" in modifier.lower(),
                is_const="const" in modifier.lower(),
                parameters=params,
                line_number=line_num,
            )
            cls.constructors.append(ctor)

        # 2. Parse Methods: [static] [ReturnType] methodName(...) [async|sync*|async*] { ... } or => ...;
        method_pattern = re.compile(
            r'\b(?:(static)\s+)?(?:([a-zA-Z0-9_<>,?\s]+)\s+)?([a-zA-Z0-9_]+)\s*\(([^)]*)\)\s*(async\*|sync\*|async)?\s*(?:\{|=>)',
            re.MULTILINE,
        )
        for m in method_pattern.finditer(body):
            is_static = bool(m.group(1))
            ret_type = (m.group(2) or "void").strip()
            method_name = m.group(3)
            params_raw = m.group(4) or ""
            async_modifier = m.group(5) or ""

            # Avoid matching constructor as a method
            if method_name == cls.name or method_name.startswith(cls.name + "."):
                continue

            line_num = class_line + body.count("\n", 0, m.start())
            method_body = self._extract_balanced_block(body, m.start()) or ""
            lines_count = len(method_body.splitlines()) if method_body else 1

            method = DartMethod(
                name=method_name,
                return_type=ret_type,
                is_static=is_static,
                is_async="async" in async_modifier,
                is_generator="*" in async_modifier,
                parameters=[p.strip() for p in params_raw.split(",") if p.strip()],
                body=method_body,
                line_number=line_num,
                lines_count=lines_count,
            )
            cls.methods.append(method)

        # 3. Parse Fields: [static] [late] [final|const] [Type] fieldName [= defaultVal];
        field_pattern = re.compile(
            r'\b(?:(static)\s+)?(?:(late)\s+)?(?:(final|const)\s+)?(?:([a-zA-Z0-9_<>,?]+)\s+)?([a-zA-Z0-9_]+)\s*(?:=\s*([^;]+))?;',
            re.MULTILINE,
        )
        for m in field_pattern.finditer(body):
            is_static = bool(m.group(1))
            is_late = bool(m.group(2))
            is_final = bool(m.group(3) and "final" in m.group(3))
            is_const = bool(m.group(3) and "const" in m.group(3))
            type_ann = (m.group(4) or "dynamic").strip()
            field_name = m.group(5)
            default_val = m.group(6).strip() if m.group(6) else None
            line_num = class_line + body.count("\n", 0, m.start())

            if field_name in ["return", "throw", "import", "class"]:
                continue

            fld = DartField(
                name=field_name,
                type_annotation=type_ann,
                is_final=is_final,
                is_const=is_const,
                is_late=is_late,
                default_value=default_val,
                line_number=line_num,
            )
            cls.fields.append(fld)

    def _parse_enums(self, content: str, dart_file: DartFile) -> None:
        enum_pattern = re.compile(r'\benum\s+([a-zA-Z0-9_]+)\s*\{', re.MULTILINE)
        for match in enum_pattern.finditer(content):
            enum_name = match.group(1)
            line_num = self._get_line_number(content, match.start())
            body = self._extract_balanced_block(content, match.start()) or ""

            en = DartEnum(name=enum_name, line_number=line_num)
            # Check for fields and methods in enhanced enum
            if ";" in body:
                values_part, members_part = body.split(";", 1)
                en.values = [v.strip() for v in values_part.split(",") if v.strip()]
                # Check for fields/methods in members_part
                if re.search(r'\b(final|String|int|double|bool)\s+\w+', members_part):
                    en.fields.append(DartField(name="enhanced_field", type_annotation="dynamic", line_number=line_num))
            else:
                en.values = [v.strip() for v in body.split(",") if v.strip()]

            dart_file.enums.append(en)

    def _parse_mixins(self, content: str, dart_file: DartFile) -> None:
        mixin_pattern = re.compile(r'\bmixin\s+([a-zA-Z0-9_]+)(?:\s+on\s+([a-zA-Z0-9_<>,?\s]+))?\s*\{', re.MULTILINE)
        for match in mixin_pattern.finditer(content):
            mixin_name = match.group(1)
            on_raw = match.group(2)
            line_num = self._get_line_number(content, match.start())
            on_types = [o.strip() for o in on_raw.split(",")] if on_raw else []

            mx = DartMixin(name=mixin_name, on_types=on_types, line_number=line_num)
            dart_file.mixins.append(mx)

    def _parse_extensions(self, content: str, dart_file: DartFile) -> None:
        # extension type or standard extension
        ext_pattern = re.compile(
            r'\bextension\s+(type\s+)?([a-zA-Z0-9_]+)(?:\([^)]*\))?\s*(?:on\s+([a-zA-Z0-9_<>]+))?\s*\{',
            re.MULTILINE,
        )
        for match in ext_pattern.finditer(content):
            is_ext_type = bool(match.group(1))
            ext_name = match.group(2)
            on_type = match.group(3) or "Object"
            line_num = self._get_line_number(content, match.start())

            ext = DartExtension(
                name=ext_name,
                on_type=on_type,
                is_extension_type=is_ext_type,
                line_number=line_num,
            )
            dart_file.extensions.append(ext)

    def _parse_functions(self, content: str, dart_file: DartFile) -> None:
        func_pattern = re.compile(
            r'^(?:([a-zA-Z0-9_<>,?\s]+)\s+)?([a-zA-Z0-9_]+)\s*\(([^)]*)\)\s*(async\*|sync\*|async)?\s*(?:\{|=>)',
            re.MULTILINE,
        )
        for match in func_pattern.finditer(content):
            ret_type = (match.group(1) or "void").strip()
            fn_name = match.group(2)
            params_raw = match.group(3) or ""
            async_mod = match.group(4) or ""
            line_num = self._get_line_number(content, match.start())

            if fn_name in ["if", "for", "while", "switch", "catch", "import", "class", "mixin", "enum", "extension"]:
                continue

            body = self._extract_balanced_block(content, match.start()) or ""

            fn = DartFunction(
                name=fn_name,
                return_type=ret_type,
                is_async="async" in async_mod,
                is_generator="*" in async_mod,
                parameters=[p.strip() for p in params_raw.split(",") if p.strip()],
                body=body,
                line_number=line_num,
            )
            dart_file.functions.append(fn)
