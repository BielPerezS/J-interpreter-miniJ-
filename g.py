import sys
from antlr4 import *
from gLexer import gLexer
from gParser import gParser
from gVisitor import gVisitor
from curses.ascii import isdigit
from locale import atoi
import re 
import numpy as np
from numpy import *

binarikey = { 
    '+' : np.add,
    '-' : np.subtract,
    '*' : np.multiply,
    '%' : np.floor_divide,
    '|' : np.remainder,
    '^' : np.power,
    ',' : np.concatenate,
    #Sucre sintactic 
    '>' : lambda x, y: np.greater(x, y).astype(int),            
    '>=': lambda x, y: np.greater_equal(x, y).astype(int),
    '<' : lambda x, y: np.less(x, y).astype(int),
    '<=': lambda x, y: np.less_equal(x, y).astype(int),
    '=' : lambda x, y: np.equal(x, y).astype(int),
    '<>': lambda x, y: np.not_equal(x, y).astype(int)
}

binarySimple = {
    '+' ,
    '-' ,
    '*' ,
    '%' ,
    '|' ,
    '^' ,
    '>' ,
    '>=',
    '<' ,
    '<=',
    '=' ,
    '<>',
}

class EvalVisitor(gVisitor):
    def __init__(self):
        self.ts = {}
        
    def visitRoot(self, ctx):
        content = list(ctx.getChildren())
        if not content:
            return  
        [expressio] = content
        exptext = expressio.getText()
        
        if not re.search(r"=:", exptext):
            result = self.visit(expressio) 
            # Cas d'un únic eleemtn o Missatge d'error
            if isinstance(result, np.integer) or isinstance(result,str):  
                print(result)
            # Cas on es retorna una solució numèrica array
            else:   
                print(*result)
        else:
            self.visit(expressio)

    def visitPrio(self, ctx):
        [_,expr,_] = list(ctx.getChildren())
        return self.visit(expr)

    def visitAssig(self,ctx):
        [var,_,expressio] = list(ctx.getChildren())
        valor = self.visit(expressio)
        self.ts[var.getText()] = valor
    # Solucionar @: i nom de funcions en una funció
    def expand(self, tokens):
        expanded = []
        for token in tokens:
            if type(token) == type(np.array(1)):
                # Si es un np.array el posem i ja
                expanded.append(token)
            
            elif token in self.ts:
                # Si el token es una funció o variable l'hem de resoldre
                expanded.extend(self.expand(self.ts[token]))
                
            elif token == "@:":
                continue  # Ignorem @:
            else:
                expanded.append(token)
        return expanded
    # Donem format per a després poguer utilitzar les funcions facil-ment
    def visitFunction(self, ctx):
        content = list(ctx.getChildren())
        name = content[0].getText()
        elements = content[2:]  # Ignorem VAR and =:
        parsed_func = []

        for elem in elements:
            token = elem.getText()
            nums = self.visit(elem)
            # Verificar si nums procesable
            if nums is not None:
                # Cas numpy array
                if isinstance(nums, np.ndarray):
                    # Si es un array que conte subarrays o altres objectes
                    if nums.dtype == object:
                        for item in nums:
                            parsed_func.append(item)
                    else:
                        parsed_func.append(nums)
                
                # Cas lista
                elif isinstance(nums, list):
                    for item in nums:
                        parsed_func.append(item)

                # Cas simple número, string, etc.
                else:
                    parsed_func.append(nums)

            elif token in [':', '/', '~']:
                # Completar operands que són dos operands
                if parsed_func and isinstance(parsed_func[-1], str):
                    parsed_func[-1] += token
                else:
                    return(f"Error: Unexpected operator {token} before {token}")

            else:
                parsed_func.append(token)


        # Resolve all the @: cases and expand the function
        expanded_args = self.expand(parsed_func)
        self.ts[name] = expanded_args

    def visitAplicafuncio(self,ctx):
        [funcname,expr] = list(ctx.getChildren())
        #obtenim el nom de la funcio i string de les intruccions
        name = funcname.getText()
        operations = self.ts[name]
        stackOps = list(operations)
        #resolem expressio i obtenim el valor
        stackNums = [self.visit(expr)]

        #deaspilem el string d'instruccions
        while stackOps:
            elem = stackOps.pop()
            
            if (len(stackNums) <= 0):
                return (f"Error: Expected at least 1 parameter to be called by {elem} function")
            
            # Operadors de mida 2
            if (len(elem) == 2):
                # Naturals
                if (elem == 'i.'):   
                    stackNums.append(naturalsOperand(stackNums.pop()))
                # Twice
                elif (elem[1] == ':'):
                    if (elem[0] != '@'):
                        L = stackNums.pop()
                        try:
                            stackNums.append(binaryOperands(elem[0],L,L))          
                        except Exception as e:
                            return f"Error {elem[0]}: : Asegurat d'utilitzar un element vàlid"

                    # La funcio @: no fa res a efecte practica, nomes hem de permetre que tot segueixi
                    else:
                        continue
                # Fold
                elif (elem[1] == '/'):
                    L = stackNums.pop()
                    try:
                        stackNums.append(foldOperands(elem[0],L))
                    except Exception as e:
                        return f"Error {elem[0]}/ : Asegurat d'utilitzar un element vàlid"

                elif (elem[1] == '~'):
                    L1 = stackOps.pop()
                    L2 = stackNums.pop()
                    if (elem[1] == '|'):
                        stackNums.append(binaryOperands(elem[0],L2,L1))         
                    else:
                        stackNums.append(binaryOperands(elem[0],L1,L2))         

                elif (elem in binarySimple):
                    L1 = stackOps.pop()
                    L2 = stackNums.pop()
                    if (elem == '|'):
                        stackNums.append(binaryOperands(elem,L2,L1))  
                    else:
                        stackNums.append(binaryOperands(elem,L1,L2))  
                else:
                    return (f"Error:\n Operador desconegut {elem}")
                
            # Operadors que nomes requereixen elements en stackNums
            elif (elem == ']'):
                continue #stackNums.append(stackNums.pop())     
            
            # Operadors binaris trivials
            elif (elem in binarySimple):
                L1 = stackOps.pop()
                L2 = stackNums.pop()
                if (elem == '|'):
                    stackNums.append(binaryOperands(elem,L2,L1))          
                else:
                    stackNums.append(binaryOperands(elem,L1,L2))          
            
            elif (elem == ','):
                L1 = stackOps.pop()
                L2 = stackNums.pop()
                stackNums.append(concatenateOperands(L1,L2))
            
            elif (elem == '{'):
                L1 = stackOps.pop()
                L2 = stackNums.pop()
                stackNums.append(selectOperands(L1,L2))  
            
            elif (elem == '#'):
                L2 = stackNums.pop()

                # Si no tenim res mes a stackOps aleshores es unari  
                if (len(stackOps) == 0):
                    stackNums.append(sizeOperand(L2))
                else:
                    L1 = stackOps.pop()
                    # Si NO tenim algun numero just darrera aleshores es unari
                    if isinstance(L1, str):
                        stackNums.append(sizeOperand(L2))
                    # Si tenim un numero aleshores es binari
                    elif isinstance(L1, np.ndarray):
                        stackNums.append(maskfilterOperand(L1,L2))
                    else:
                        return(f"Error:\nTipus de dades no conegut en L1: {type(L1)}")

            else:
                return (f"Error:\nOperador desconegut: {elem}")
            
            
        #Al final del tot si no ha quedat Exactament un operand a stackNums alehsores error!
        if (len(stackNums) > 1):
            return (f"Error:\nMasses valor per a la funció {funcname.getText()}")
        
        if (len(stackNums) == 0):
            return (f"Error:\nS'esperen més valors per a la funció {funcname.getText()}")
        
        return stackNums.pop()
            
    def visitVar(self, ctx):
        [var] = list(ctx.getChildren())
        return self.ts[var.getText()]

    def visitExprllista(self, ctx):
        [elem] = list(ctx.getChildren())
        return self.visit(elem)

    def visitLlista(self, ctx):
        secuencia = list(ctx.getChildren())
        Llista = []
        for nums in secuencia:
            Llista.append(int(nums.getText().replace('_','-')))
        return np.array(Llista)

    def visitUn(self,ctx):
        content = list(ctx.getChildren())
        OP1 = content[0].getText()
        OP2 = content[1].getText()
        # Twice i Fold
        if (OP2 == ':' or OP2 == '/'):
            [_,_,expr] = list(ctx.getChildren())
            L = self.visit(expr)
            if OP2 == ':':
                try:
                    return binaryOperands(OP1,L,L)      
                except Exception as e:
                    return f"Error {OP2} : Asegura insertat utilitzar un element valid"

            if OP2 == '/':
                try:
                    return foldOperands(OP1,L)
                except Exception as e:
                    return f"Error {OP2} : Asegura insertat utilitzar un element valid"
                
        else:
            L = self.visit(content[1])
            if OP1 == ']' or  OP1 == '@:':
                return L
            if OP1 == 'i.':
                return naturalsOperand(L)
            if OP1 == '#':
                return sizeOperand(L)

    def visitBin(self,ctx):
        #print("Binari")
        content = list(ctx.getChildren())
        #print("getting text")
        flip = content[2].getText()
        #print (flip)

        #Cas Flip
        if (flip == '~'):
            #print("flipeando")
            [expr1, op,flipcase,expr2] = list(ctx.getChildren())
            L1 = self.visit(expr1)
            L2 = self.visit(expr2)
            op = op.getText()
            if (op == '|'):
                return  binaryOperands(op,L1,L2)        #binarikey[op](L1,L2)
            else:
                return  binaryOperands(op,L2,L1)        #binarikey[op](L2,L1)

        #No flip
        else:
            #print("normal")
            [expr1, op,expr2] = list(ctx.getChildren())
            L1 = self.visit(expr1)
            L2 = self.visit(expr2)
            function = op.getText()
            
            if function == '#':
                return maskfilterOperand(L1,L2)
            
            elif function == '{':
                return selectOperands(L1,L2)      # content[select]
            
            else: 
                if function == '|':
                    return binaryOperands(function,L2,L1)   #binarikey[function](L2,L1)
                elif function == ',':
                    return concatenateOperands(L1,L2)
                elif function == '@:':
                    return L1 + L2
                else:
                    return binaryOperands(function,L1,L2)   #binarikey[function](L1,L2)

def binaryOperands(op,L1,L2):
    #Check de erros segons operand
    s1 = size(L1)
    s2 = size(L2)
    if s1 > 1 and s2 > 1 and s1 != s2:
        return f"Error {op} : S'espera que {L1} i {L2} tinguin la mateixa mida"
    try:
        return binarikey[op](L1, L2)
    #Errors varis
    except Exception as e:
        return f"Error {op} : {e}"

def OutOfBounds(L1,L2):
    L2size = np.size(L2) - 1
    for elem in L1:
        if elem > L2size:
            return True
    return False

def selectOperands(L1,L2):
    select = L1
    L2size = np.size(L2)
    content = L2
    if (OutOfBounds(L1,L2) == False):
        try:
            return content[select]
        except Exception as e:
            return f"Error Select : {e}"
    else:
        return f"Error Select : {L1} no pot tenir elements mes grans que el size de L2: {L2size}"

def concatenateOperands(L1,L2):
    try:
        return np.concatenate((L1,L2))
    except Exception as e:
        return f"Error , : {e}"

def foldOperands(op,L):
    result = L[0]
    for elements in L[1:]:
        result = binarikey[op](result, elements)
    return np.array([result])

def maskfilterOperand(L1,L2):
    mask = L1
    content = L2
    if (size(mask) != size(content)):
        return f"Error # mask : S'espera que {L1} i {L2} tinguin la mateixa mida"
    try:
        return content[mask.astype(bool)]
    except Exception as e:
        return f"Error # mask: {e}"
    
def naturalsOperand(L):
    if (size(L) != 1):
        return f"Error i. : S'espera un array de mida exctament 1 ==> Mida: {size(L)}\n"
    num = L.item()
    if (num < 0):
        return f"Error i. : S'espera un numero estrictament positiu ==> Valor: {num}\n"
    return np.array(range(num))

def sizeOperand(L):
    return np.array([np.size(L)])

def main():
    if len(sys.argv) == 2:
        input_file = sys.argv[1]
        visitor = EvalVisitor()

        with open(input_file, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue  

                input_stream = InputStream(line)
                lexer = gLexer(input_stream)
                token_stream = CommonTokenStream(lexer)
                parser = gParser(token_stream)
                tree = parser.root()
                result = visitor.visit(tree)
                if result is not None:
                    print(result)

    elif len(sys.argv) == 1:
        visitor = EvalVisitor()
        while (True):
            input_stream = InputStream(input(''))
            lexer = gLexer(input_stream)
            lexer.removeErrorListeners()
            token_stream = CommonTokenStream(lexer)
            parser = gParser(token_stream)
            parser.removeErrorListeners()
            tree = parser.root()
            visitor.visit(tree)

    else:
        print("Ús: python3 g.py OPCIONAL(<fitxer.j>)", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
