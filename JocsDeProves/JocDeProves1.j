NB. Comprovació funcionament basic

1                                   NB. Array Size 1
_1                                  NB. Array Size 1 negatiu
0 10 _23 40000                      NB. Array amb negatius

NB. Comprovació Funcionament Operands Aritmètics

12 _47 89 _34   +   5  76 _23 _91               NB. Suma            | Resultat: 17 29 66 -125
44 _18 67 _10   -   99 32 _45  2                NB. Resta           | Resultat: -55 -50 112 -12
73 _54 26 _80   *   11 68 _37  92               NB. Multiplicacio   | Resultat: 803 -3672 -962 -7360
39 _4  90  _7   %   13  2 _45 _23               NB. Divisio         | Resultat: 3 -2 -2 0
2 _10 23  _8    |   7  11 _20 _10               NB. Residu          | Resultat: 1 -9 3 -2
2  _4 _5 10     ^   3   2   3   3               NB. Potencia        | Resultat: 8 16 -125 1000

NB. Comprovació Funcionament Operands de Comparació

5 5 5 _5 _5 _5 >  _3 10 5 _10 2 _5              NB. GreaterThan     | Resultat: 1 0 0 1 0 0
5 5 5 _5 _5 _5 >= _3 10 5 _10 2 _5              NB. GreaterEqual    | Resultat: 1 0 1 1 0 1   
5 5 5 _5 _5 _5 <  _3 10 5 _10 2 _5              NB. LessThan        | Resultat: 0 1 0 0 1 0
5 5 5 _5 _5 _5 <= _3 10 5 _10 2 _5              NB. LessEqual       | Resultat: 0 1 1 0 1 1 
10 10 _4 _4 =  10 _10 _4 4                      NB. Equal           | Resultat: 1 0 1 0
10 10 _4 _4 <> 10 _10 _4 4                      NB. NotEqual        | Resultat: 0 1 0 1

NB. Comprovació Ordre d'Execucció i Prioritat d'Operands

100 -  10 * 2  + 5                              NB. Dreta a Esquerra    | Resultat: 30
100 - (10 * 2) + 5                              NB. Parentesis          | Resultat: 75
