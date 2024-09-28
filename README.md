# Some console UI coding in Python
## Done in Wing editor
### Of no interest other than historical to this profile

some console color codes used with colorama module
```python
WHITE   = '\x1b[37;1m';   SILVER   = '\x1b[37;2m';   SILVER_   = '\x1b[47m'
YELLOW  = '\x1b[33;1m';   OLIVE    = '\x1b[33;2m';   OLIVE_    = '\x1b[43m'
GREEN   = '\x1b[32;1m';   LAUREL   = '\x1b[32;2m';   LAUREL_   = '\x1b[42m'
CYAN    = '\x1b[36;1m';   TEAL     = '\x1b[36;2m';   TEAL_     = '\x1b[46m'
BLUE    = '\x1b[34;1m';   NAVY     = '\x1b[34;2m';   NAVY_     = '\x1b[44m'
MAGENTA = '\x1b[35;1m';   EGGPLANT = '\x1b[35;2m';   EGGPLANT_ = '\x1b[45m'
RED     = '\x1b[31;1m';   MAROON   = '\x1b[31;2m';   MAROON_   = '\x1b[41m'
GREY    = '\x1b[30;1m';   BLACK    = '\x1b[30;2m';   BLACK_    = '\x1b[40m'
WT = WHITE  ;  SV = SILVER  ;  SV_ = SILVER_
YL = YELLOW ;  OL = OLIVE   ;  OL_ = OLIVE_
GN = GREEN  ;  LR = LAUREL  ;  LR_ = LAUREL_
CN = CYAN   ;  TL = TEAL    ;  TL_ = TEAL_
BL = BLUE   ;  NV = NAVY    ;  NV_ = NAVY_
MG = MAGENTA;  EG = EGGPLANT;  EG_ = EGGPLANT_
RD = RED    ;  MR = MAROON  ;  MR_ = MAROON_
GR = GREY   ;  BK = BLACK   ;  BK_ = BLACK_

color_dic = {
'\x1b[37;1m' : 'WHITE',  '\x1b[37;2m' : 'SILVER',  '\x1b[47m' : 'SILVER_',
'\x1b[33;1m' : 'YELLOW', '\x1b[33;2m' : 'OLIVE',   '\x1b[43m' : 'OLIVE_',
'\x1b[32;1m' : 'GREEN',  '\x1b[32;2m' : 'LAUREL',  '\x1b[42m' : 'LAUREL_',
'\x1b[36;1m' : 'CYAN',   '\x1b[36;2m' : 'TEAL',    '\x1b[46m' : 'TEAL_',
'\x1b[34;1m' : 'BLUE',   '\x1b[34;2m' : 'NAVY',    '\x1b[44m' : 'NAVY_',
'\x1b[35;1m' : 'MAGENTA','\x1b[35;2m' : 'EGGPLANT','\x1b[45m' : 'EGGPLANT_',
'\x1b[31;1m' : 'RED',    '\x1b[31;2m' : 'MAROON',  '\x1b[41m' : 'MAROON_',
'\x1b[30;1m' : 'GREY',   '\x1b[30;2m' : 'BLACK',   '\x1b[40m' : 'BLACK_'   }
```
