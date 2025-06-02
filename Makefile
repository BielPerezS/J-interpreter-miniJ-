ANTLR = antlr4
GRAMMAR = g.g4
TARGETS = gLexer.py gParser.py gVisitor.py gListener.py
REMOVE = gLexer.tokens gLexer.interp gParser.tokens gParser.interp g.tokens g.interp 

all: $(TARGETS)

$(TARGETS): $(GRAMMAR)
	$(ANTLR) -Dlanguage=Python3 -visitor $(GRAMMAR)

.PHONY: clean

clean:
	rm -f $(TARGETS) $(REMOVE)
	rm -rf __pycache__

