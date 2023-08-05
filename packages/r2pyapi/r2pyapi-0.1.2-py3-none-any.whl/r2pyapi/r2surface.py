from typing import Optional

import r2pipe

from .r2types import R2Export, R2Function, R2Import, R2Section, R2Core, R2Bin, R2EntryPoint


class R2Surface:
    def __init__(self, r2: r2pipe.open_sync.open) -> None:
        self.r2 = r2
        self.core = R2Core(**self.r2.cmdj("ij")["core"])
        self.bin = R2Bin(self.r2.cmdj("ij")["bin"])
        self.entry_point = R2EntryPoint(**self.r2.cmdj("iej")[0])
        self.imports = [R2Import(entry) for entry in self.r2.cmdj("iij")]
        self.exports = [R2Export(**entry) for entry in self.r2.cmdj("iEj")]
        self.sections = [R2Section(**entry) for entry in self.r2.cmdj("iSj")]
        if self.r2.cmdj("aflj") is None:
            self.r2.cmd("aaa")
        self.functions = [R2Function(entry) for entry in self.r2.cmdj("aflj")]

    def find_function(self, function_name: str) -> Optional[R2Function]:
        for function in self.functions:
            if function.name == function_name:
                return function
        return None

    def find_section(self, section_name: str) -> Optional[R2Section]:
        for section in self.sections:
            if section.name == section_name:
                return section
        return None

    def find_export(self, export_name: str) -> Optional[R2Export]:
        for export in self.exports:
            if export.name == export_name:
                return export
        return None

    def find_export_loose(self, export_name: str) -> Optional[R2Export]:
        for export in self.exports:
            if export.name.endswith(export_name):
                return export
        return None

    def find_import(self, import_name: str) -> Optional[R2Import]:
        for import_ in self.imports:
            if import_.name == import_name:
                return import_
        return None
