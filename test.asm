ORG 512
LDE 0
LDD 1
STO message
:Loop
ADE 1
PRNT
ADID
LOAD 0
SKE0 0
JMP Loop
HLT
:message
DSTR Hello, world! This is proof that this works!
