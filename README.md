# Practica LP mini J

## Descripció 
Aquest programa permet l'execucció d'un interpret reduit de G que anomenarem ``mini j`` mitjançant l'execucció de ``g.py`` i la gramaticà definida a ``g.g4``.<br>
## Decisions Preses

Al llarg de la creació d’aquest intèrpret vaig haver de prendre una decisió molt important:  
**Com implemento tot el sistema de funcions?**

La decisió presa per al tractament de funcions ha estat la següent:

### 1. Guardat de Funcions

Una funció, al cap i a la fi, no és res més que un conjunt d’operands, és a dir, una sèrie d’instruccions que cal aplicar a un input.  
He decidit orientar-ho de manera que, quan es guarda una funció, s’emmagatzema en una llista en forma de *stack* aquesta "recepta". Veiem un exemple:

```
    f =: 1 2 3 + 4 5 6 *            
    f = [[1 2 3], +, [4 5 6], *]   
    Tenim cada instrucció a executar guardada     
```
Tenim, doncs, cada instrucció a executar correctament guardada.

#### Què passa si una funció es defineix mitjançant l’ús d’una altra?

En aquest cas, tenia dues opcions a considerar:

1. Resoldre-ho en el moment en què s’utilitzi la funció  
2. Resoldre-ho en el moment de la **definició** de la funció

He optat per la **opció 2**, ja que a la llarga és més eficient i m’ha semblat més senzilla d’implementar.  
Ara bé, cal tenir en compte una limitació:

> Si es redefineix una funció que és utilitzada per una altra, **aquesta última no es veurà actualitzada**.

### 2. Aplicació de Funcions

Tenint clar que una funció conté la sèrie de passos que s’han d’executar sobre un input, l’aplicació d’una funció es veu prou simplificada.

L’únic que cal fer és mantenir **2 stacks**:

- `stackOps`: Guarda les operacions que s'han d'executar (incloent-hi les definides a la funció)
- `stackNums`: Guarda els nombres sobre els quals s’apliquen les operacions

De forma simplificada, el treball que es fa en aplicar una funció consisteix simplement a **recollir els elements necessaris** de `stackOps` i `stackNums`, i aplicar l’element extret de `stackOps`.

#### Exemple:

Si treiem un **operador aritmètic** de `stackOps`, llavors:

1. Extraiem un altre element de `stackOps` (hauria de ser una llista d’operands)
2. Extraiem un element de `stackNums`
3. Apliquem l’operació corresponent
4. El resultat es torna a col·locar a `stackNums`


## Execucció

**(Si fa falta) Instalar llibreries**
```bash
    pip3 install antlr4-tools
    antlr4
    pip3 install antlr4-python3-runtime==4.13
    pip3 install numpy
```

**Compilar-ho Tot**
```bash
    make
```
**Ús de l'interpret**
```bash
    python3 g.py
```
**Provar un Joc de Proves i Rederigir la sortida**
```bash
    python3 g.py JocDeProves/JocDeProves.j >> outputname.out
```

**Si no funciona, recomano crear un entorn virtual (venv):**

```bash
python3 -m venv setup
# Linux / macOS
source setup/bin/activate
# Windows
setup\Scripts\activate
```
    
### Fixters

`g.py`: Conté l'execucció de l'interpret<br>
`g.g4`: Conté la gramàtica de l'interpret<br>
`/JocDeProves`: Conté els jocs de proves i el seu exepcted result<br>
`Makefile`: Makefile


