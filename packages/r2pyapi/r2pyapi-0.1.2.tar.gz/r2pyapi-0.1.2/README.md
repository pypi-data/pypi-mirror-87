# r2pyapi

High level radare2 python API 

# Installation

```
$ pip install r2pyapi
```

You also need to install [radare2](https://github.com/radareorg/radare2).
radare2 can be easily installed by the instruction described [here](https://github.com/radareorg/radare2#install--update).

# Usage

``` python
import r2pipe
from r2pyapi import R2Surface, R2Seeker, R2Reader

r2 = r2pipe.open("test.exe")

# instruction search
with R2Seeker(r2) as seeker:
    results = seeker.seek_instructions("push ebp")
    print(next(result))
    # R2Instruction(offset=4288663, len=2, code='push ebp')

# read byte sequences
with R2Reader(r2) as reader:
    bytes_read = reader.read_bytes_at(0x0401000, 4)
    # [85, 139, 236, 131]

# get sections
r2_surf = R2Surface(r2)
print(r2_surf.sections)
# [R2Section(vaddr=4198400, paddr=1024, size=51200, vsize=53248, name='.text', perm='-r-x'), ... ]

# get import
print(r2_surf.find_import("MessageBoxA"))
# R2Import(ordinal=1, bind='NONE', type='FUNC', name='MessageBoxA', libname='USER32.dll', plt=4251916)
```
