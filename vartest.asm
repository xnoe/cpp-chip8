ORG 512

LDD 1

STO msg1
CAL print
STO msg2
CAL print
HLT

:print
PRNT
LOAD 0
ADID
SKE0 0
JMP print
JMP print_ret

:print_ret
RET

:msg1
DSTR Hello!
ORG 1

:msg2
DSTR World!
ORG 1
