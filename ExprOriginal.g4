grammar ExprOriginal;

prog: expr EOF ;

expr
    : expr opsuma term    # ExprBinarySum
    | term                # ExprToTerm
    ;

term
    : term opmul factor   # TermBinaryMul
    | factor              # TermToFactor
    ;

factor
    : ID                  # FactorId
    | NUM                 # FactorNum
    | PARI expr PARD      # FactorPar
    ;

// parser helpers (tokens as parser rules like in la imagen)
opsuma: '+' | '-' ;
opmul : '*' | '/' ;

// tokens
ID   : [a-zA-Z_] [a-zA-Z_0-9]* ;
NUM  : [0-9]+ ('.' [0-9]+)? ;
PARI : '(' ;
PARD : ')' ;
WS   : [ \t\r\n]+ -> skip ;
