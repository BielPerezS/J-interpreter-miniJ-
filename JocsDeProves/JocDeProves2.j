NB. Comprovació Funcionament Operands Complexos

1 2 , _8 9 10 _20                               NB. Concatencació ','   | Resultat: 1 2 -8 9 10 -20
_1 4 7 20 , 86 10 _21 9                         NB. Concatencació ','   | Resultat: -1 4 7 20 86 10 -21 9
3 2 1 0 { 10 _20 30 _40                         NB. Selecció '{'        | Resultat: -40 30 -20 10
] 1 2 3 4                                       NB. Identitat '['       | Resultat: 1 2 3 4 
# 1 2 3 4                                       NB. Size '#'            | Resultat: 4
1 0 1 0 # 1 2 5 9                               NB. Mask '#'            | Resultat: 1 5
i. 1                                            NB. Naturals 'i.'       | Resultat: 0
i. 11                                           NB. Naturals 'i.'       | Resultat: 0 1 2 3 4 5 6 7 8 9 10

+: _1 3 _8 2                                    NB. Twice '+:'          | Resultat: -2 6 -16 4
-: _1 3 _8 2                                    NB. Twice '-:'          | Resultat: 0 0 0 0
*: _1 3 _8 2                                    NB. Twice '*:'          | Resultat: 1 9 64 4
%: _1 3 _8 2                                    NB. Twice '%:'          | Resultat: 1 1 1 1 
|: _1 3 _8 2                                    NB. Twice '|:'          | Resultat: 0 0 0 0 
^:  1 3  8 2                                    NB. Twice '^:'          | Resultat: 1 27 16777216 4

+/ 10 _5 7 _4                                   NB. Fold '+:'           | Resultat: 8
-/ 10 _5 7 _4                                   NB. Fold '+:'           | Resultat: 12
*/ 10 _5 7 _4                                   NB. Fold '+:'           | Resultat: 1400
%/ 100 _2 7 _4                                  NB. Fold '+:'           | Resultat: 2
|/ 10 _5 7 _4                                   NB. Fold '+:'           | Resultat: 0
^/ 2  5 2  4                                    NB. Fold '+:'           | Resultat: 1099511627776 (si el numero resultant es massa gran donarà 0)

5 -~ 3                                          NB. Flip '-~'           | Resultat: -2
5 %~ 3                                          NB. Flip '%~'           | Resultat: 0
5 |~ 3                                          NB. Flip '|~'           | Resultat: 2
5 ^~ 3                                          NB. Flip '^~'           | Resultat: 243
