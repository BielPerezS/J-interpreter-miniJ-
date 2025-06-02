NB. Comprovació d'alguns Errors

2  _4  ^   3  _3                NB. Error d'Ús              | Resultat: Error ^ : Integers to negative integer powers are not allowed.
2 8 + _2 10 3                   NB. Error d'Ús              | Resultat: Error + : S'espera que [2 8] i [-2 10  3] tinguin la mateixa mida
f =: 2 3 4 * 
f 1 2                           NB. Error d'Ús              | Resultat: Error * : S'espera que [2 3] i [1 2 3 4] tinguin la mateixa mida
0 10 2 { 1 2 3                  NB. Error d'Ús              | Resultat: Error Select : [ 0 10  2] no pot tenir elements mes grans que el size de L2: 3
1 0 1 1 # 1 2 3                 NB. Error d'Ús              | Resultat: Error # mask : S'espera que [1 0 1 1] i [1 2 3] tinguin la mateixa mida
i. 10 20                        NB. Error d'Ús              | Resultat: Error i. : S'espera un array de mida exctament 1 ==> Mida: 2
i. _5                           NB. Error d'Ús              | Resultat: Error i. : S'espera un numero estrictament positiu ==> Valor: -5