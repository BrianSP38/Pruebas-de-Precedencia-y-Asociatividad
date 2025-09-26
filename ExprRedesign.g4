grammar ExprRedesign;

prog: expr EOF ;

expr
    : sum (opmul expr)?   # ExprMulRight
    ;

sum
    : factor (opsuma sum)? # SumRight
    ;

factor
    : ID
    | NUM
    | PARI expr PARD
    ;

opsuma: '+' | '-' ;
opmul : '*' | '/' ;

ID   : [a-zA-Z_] [a-zA-Z_0-9]* ;
NUM  : [0-9]+ ('.' [0-9]+)? ;
PARI : '(' ;
PARD : ')' ;
WS   : [ \t\r\n]+ -> skip ;
