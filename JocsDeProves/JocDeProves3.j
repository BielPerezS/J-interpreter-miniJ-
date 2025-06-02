NB. Assignacions Valors

x =: 10 20                                      NB. Assignació Bàsica
x                                               NB. Resultat: 10 20
x =: _10 20 30                                  NB. Assignació Sobreescritura
x                                               NB. Resultat: -10 20 30
y =: i.3                                        NB. Assignació
y                                               NB. 0 1 2 
y =: x + 4*y                                    NB. Asignació Composta?
y                                               NB. Resultat: -10 24 38
z =: # 1 2 3 4                                  NB. Assignació
z * y                                           NB. Resultat: -40 96 152 

NB. Funcions 

f =: i.                                         NB. Asignació d'una funció
f                                               NB. Resultat: i.
x =: 10
f x                                             NB. Resultat: 0 1 2 3 4 5 6 7 8 9
g =: *: @: f                                    NB. Composició                
g                                               NB. Resultat: *: i.
g x                                             NB. Resultat: 0 1 4 9 16 25 36 49 64 81

x =: 1 2 3 4 
reverse =: 3 2 1 0 {                            NB. Asignació d'una funció
reverse                                         NB. Resultat: [3 2 1 0] {
reverse x                                       NB. Resultat: 4 3 2 1
mod2 =: 2 |                                     NB. Asignació d'una funció        
mod2                                            NB. [2] |
mod2 1 2 3 4                                    NB. Resultat: 1 0 1 0
revmod2 =: mod2 @: reverse                      NB. Composició
revmod2 x                                       NB. 0 1 0 1
noeq0 =: 0 <>                                   NB. Asignació d'una funció
noeq0                                           NB. [0] <>        
noeq0 revmod2 x                                 NB. 1 0 1 0 
senars =: noeq0 @: revmod2                      NB. Composició
senars x                                        NB. 0 1 0 1

