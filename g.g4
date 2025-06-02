grammar g;

root : stat* ;

stat 
     : VAR '=:' expr                                                            #assig
     | expr                                                                     #exprsupp
     | VAR '=:' (list | expr | '#' | '~' |OPB | OPU | OPE | VAR | AT)+          #function
     ;

expr : '(' expr ')'                                                             #prio
     | <assoc = right> expr (OPB | OPB '~' | '#') expr                          #bin
     | (OPB OPE | OPU | '#') expr                                               #un
     | VAR expr                                                                 #aplicafuncio
     | list                                                                     #exprllista
     | VAR                                                                      #var
     ;

list : NUM+                                                                     #llista
     ;

AT : '@:' ;
OPU : (']' | 'i.') ;
OPB : ('+' | '-'  | '*' | '%' | '|' |'^'| ',' | '{' | '>' | '>=' | '<' | '<=' | '=' | '<>') ;
OPE : ('/' | ':' ) ;

VAR : [a-z][a-z0-9]* ;
NUM : '_'? [0-9]+ ;
WS  : [ \t\r\n]+ -> skip ;
COMENT : 'NB.' ~[\r\n]* -> skip ;
LEXICAL_ERROR : . ;

