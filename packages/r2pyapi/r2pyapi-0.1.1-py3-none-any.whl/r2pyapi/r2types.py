from dataclasses import dataclass
from typing import Dict, List, Optional, Union, cast


@dataclass()
class R2Core:
    type: str
    file: str
    fd: int
    size: int
    humansz: str
    iorw: bool
    mode: str
    block: int
    format: str


@dataclass()
class R2EntryPoint:
    vaddr: int
    paddr: int
    baddr: int
    laddr: int
    haddr: int
    type: str


@dataclass(init=False)
class R2Bin:
    arch: str
    baddr: int
    binsz: int
    bintype: str
    bits: int
    canary: bool
    class_: str
    cmp_csum: Optional[str]
    compiled: str
    compiler: str
    crypto: bool
    dbg_file: str
    endian: str
    havecode: bool
    hdr_csum: Optional[str]
    guid: str
    intrp: str
    laddr: int
    lang: str
    linenum: bool
    lsyms: bool
    machine: str
    maxopsz: int
    minopsz: int
    nx: bool
    os: str
    overlay: Optional[bool]
    cc: str
    pcalign: int
    pic: bool
    relocs: bool
    retguard: Optional[bool]
    rpath: str
    sanitiz: bool
    signed: Optional[bool]
    static: bool
    stripped: bool
    subsys: str
    va: bool
    checksums: dict

    def __init__(self, raw: Dict[str, Union[str, int, bool]]) -> None:
        self.arch = cast(str, raw["arch"])
        self.baddr = cast(int, raw["baddr"])
        self.binsz = cast(int, raw["binsz"])
        self.bintype = cast(str, raw["bintype"])
        self.bits = cast(int, raw["bits"])
        self.canary = cast(bool, raw["canary"])
        self.class_ = cast(str, raw["class"])
        self.cmp_csum = cast(str, raw["cmp.csum"]) if "cmp.csum" in raw.keys() else None
        self.compiled = cast(str, raw["compiled"])
        self.compiler = cast(str, raw["compiler"])
        self.crypto = cast(bool, raw["crypto"])
        self.dbg_file = cast(str, raw["dbg_file"])
        self.endian = cast(str, raw["endian"])
        self.havecode = cast(bool, raw["havecode"])
        self.hdr_csum = cast(str, raw["hdr.csum"]) if "hdr.csum" in raw.keys() else None
        self.guid = cast(str, raw["guid"])
        self.intrp = cast(str, raw["intrp"])
        self.laddr = cast(int, raw["laddr"])
        self.lang = cast(str, raw["lang"])
        self.linenum = cast(bool, raw["linenum"])
        self.lsyms = cast(bool, raw["lsyms"])
        self.machine = cast(str, raw["machine"])
        self.maxopsz = cast(int, raw["maxopsz"])
        self.minopsz = cast(int, raw["minopsz"])
        self.nx = cast(bool, raw["nx"])
        self.os = cast(str, raw["os"])
        self.overlay = cast(bool, raw["overlay"]) if "overlay" in raw.keys() else None
        self.cc = cast(str, raw["cc"])
        self.pcalign = cast(int, raw["pcalign"])
        self.pic = cast(bool, raw["pic"])
        self.relocs = cast(bool, raw["relocs"])
        self.retguard = cast(bool, raw["retguard"]) if "retguard" in raw.keys() else None
        self.rpath = cast(str, raw["rpath"])
        self.sanitiz = cast(bool, raw["sanitiz"])
        self.signed = cast(bool, raw["signed"]) if "signed" in raw.keys() else None
        self.static = cast(bool, raw["static"])
        self.stripped = cast(bool, raw["stripped"])
        self.subsys = cast(str, raw["subsys"])
        self.va = cast(bool, raw["va"])
        self.checksums = cast(dict, raw["checksums"])


@dataclass()
class R2FileInfo:
    core: R2Core
    bin: R2Bin


@dataclass()
class R2Section:
    vaddr: int
    paddr: int
    size: int
    vsize: int
    name: str
    perm: str


@dataclass()
class R2Export:
    name: str
    flagname: str
    realname: str
    ordinal: int
    bind: str
    size: int
    type: str
    vaddr: int
    paddr: int
    is_imported: bool


@dataclass(init=False)
class R2Import:
    ordinal: int
    bind: str
    type: str
    name: str
    libname: Optional[str]
    plt: int

    def __init__(self, raw: Dict[str, Union[str, int]]) -> None:
        self.ordinal = cast(int, raw["ordinal"])
        self.bind = cast(str, raw["bind"])
        self.type = cast(str, raw["type"])
        self.name = cast(str, raw["name"])
        self.libname = cast(str, raw["libname"]) if "libname" in raw.keys() else None
        self.plt = cast(int, raw["plt"])


@dataclass()
class R2Ref:
    addr: int
    type: str
    at: int


@dataclass()
class R2LocalVarRef:
    base: str
    offset: int


@dataclass(init=False)
class R2LocalVar:
    name: str
    kind: str
    type: str
    ref: R2LocalVarRef

    def __init__(self, raw: dict) -> None:
        self.name = raw["name"]
        self.kind = raw["kind"]
        self.type = raw["type"]
        self.ref = R2LocalVarRef(raw["ref"]["base"], raw["ref"]["offset"])


@dataclass()
class R2RegVar:
    name: str
    kind: str
    type: str
    ref: str


@dataclass(init=False)
class R2Function:
    offset: int
    name: str
    size: int
    is_pure: bool
    realsz: int
    noreturn: bool
    stackframe: int
    calltype: str
    cost: int
    cc: int
    bits: int
    type: int
    nbbs: int
    edges: int
    ebbs: int
    signature: str
    minbound: int
    maxbound: int
    callrefs: Optional[List[R2Ref]]
    datarefs: List[int]
    codexrefs: Optional[List[R2Ref]]
    dataxrefs: List[int]
    indegree: int
    outdegree: int
    nlocals: int
    nargs: int
    bpvars: Optional[List[R2LocalVar]]
    spvars: Optional[List[R2LocalVar]]
    regvars: Optional[List[R2RegVar]]
    difftype: Optional[str]

    def __init__(self, raw: dict) -> None:
        self.offset = raw["offset"]
        self.name = raw["name"]
        self.size = raw["size"]
        self.is_pure = raw["is-pure"] == "true"
        self.realsz = raw["realsz"]
        self.noreturn = raw["noreturn"]
        self.stackframe = raw["stackframe"]
        self.calltype = raw["calltype"]
        self.cost = raw["cost"]
        self.cc = raw["cc"]
        self.bits = raw["bits"]
        self.type = raw["type"]
        self.nbbs = raw["nbbs"]
        self.edges = raw["edges"]
        self.ebbs = raw["ebbs"]
        self.signature = raw["signature"]
        self.minbound = raw["minbound"]
        self.maxbound = raw["maxbound"]
        if "callrefs" in raw.keys():
            self.callrefs = [R2Ref(**entry) for entry in raw["callrefs"]]
        else:
            self.callrefs = None
        self.datarefs = raw["datarefs"] if "datarefs" in raw.keys() else None
        if "codexrefs" in raw.keys():
            self.codexrefs: List[R2Ref] = [R2Ref(**entry) for entry in raw["codexrefs"]]
        else:
            self.codexrefs = None
        self.dataxrefs = raw["dataxrefs"] if "dataxrefs" in raw.keys() else None
        self.indegree = raw["indegree"]
        self.outdegree = raw["outdegree"]
        self.nlocals = raw["nlocals"] if "nlocals" in raw.keys() else None
        self.nargs = raw["nargs"] if "nargs" in raw.keys() else None
        if "bpvars" in raw.keys():
            self.bpvars = [R2LocalVar(entry) for entry in raw["bpvars"]]
        else:
            self.bpvars = None
        if "spvars" in raw.keys():
            self.spvars = [R2LocalVar(entry) for entry in raw["spvars"]]
        else:
            self.spvars = None
        if "regvars" in raw.keys():
            self.regvars = [R2RegVar(**entry) for entry in raw["regvars"]]
        else:
            self.regvars = None
        if "difftype" in raw.keys():
            self.difftype = raw["difftype"]
        else:
            self.difftype = None


@dataclass()
class R2Instruction:
    offset: int
    len: int
    code: str


@dataclass()
class R2ByteSearchResult:
    offset: int
    type: str
    data: str
