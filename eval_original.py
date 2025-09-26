# eval_original.py
from antlr4 import InputStream, CommonTokenStream
from ExprOriginalLexer import ExprOriginalLexer
from ExprOriginalParser import ExprOriginalParser
from ExprOriginalVisitor import ExprOriginalVisitor

class EvalVisitor(ExprOriginalVisitor):
    def visitProg(self, ctx: ExprOriginalParser.ProgContext):
        return self.visit(ctx.expr())

    def visitExprBinarySum(self, ctx: ExprOriginalParser.ExprBinarySumContext):
        left = self.visit(ctx.expr())
        right = self.visit(ctx.term())
        op = ctx.opsuma().getText()
        if op == '+':
            return left + right
        else:
            return left - right

    def visitExprToTerm(self, ctx: ExprOriginalParser.ExprToTermContext):
        return self.visit(ctx.term())

    def visitTermBinaryMul(self, ctx: ExprOriginalParser.TermBinaryMulContext):
        left = self.visit(ctx.term())
        right = self.visit(ctx.factor())
        op = ctx.opmul().getText()
        if op == '*':
            return left * right
        else:
            return left / right

    def visitTermToFactor(self, ctx: ExprOriginalParser.TermToFactorContext):
        return self.visit(ctx.factor())

    def visitFactorNum(self, ctx: ExprOriginalParser.FactorNumContext):
        text = ctx.NUM().getText()
        if '.' in text:
            return float(text)
        else:
            return int(text)

    def visitFactorId(self, ctx: ExprOriginalParser.FactorIdContext):
        name = ctx.ID().getText()
        raise Exception(f"Variable '{name}' no está definida (implementa tabla de símbolos si la necesitas).")

    def visitFactorPar(self, ctx: ExprOriginalParser.FactorParContext):
        return self.visit(ctx.expr())

# helper to evaluate a string
def eval_string(s: str):
    input_stream = InputStream(s)
    lexer = ExprOriginalLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = ExprOriginalParser(tokens)
    tree = parser.prog()
    visitor = EvalVisitor()
    return visitor.visit(tree)

if __name__ == "__main__":
    tests = ["2+3*4", "20-5-3", "100/10/2", "2+3*(4-5)", "2*3+4"]
    for t in tests:
        print(t, "=", eval_string(t))
