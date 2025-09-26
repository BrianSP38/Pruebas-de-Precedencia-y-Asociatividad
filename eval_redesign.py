# eval_redesign.py
from antlr4 import InputStream, CommonTokenStream
from ExprRedesignLexer import ExprRedesignLexer
from ExprRedesignParser import ExprRedesignParser
from ExprRedesignVisitor import ExprRedesignVisitor

class EvalVisitorRedesign(ExprRedesignVisitor):
    def visitProg(self, ctx: ExprRedesignParser.ProgContext):
        return self.visit(ctx.expr())

    def visitExprMulRight(self, ctx: ExprRedesignParser.ExprMulRightContext):
        # expr: sum (opmul expr)?
        left = self.visit(ctx.sum())
        if ctx.opmul() is not None:
            right = self.visit(ctx.expr())
            op = ctx.opmul().getText()
            if op == '*':
                return left * right
            else:
                return left / right
        else:
            return left

    def visitSumRight(self, ctx: ExprRedesignParser.SumRightContext):
        # sum: factor (opsuma sum)?
        left = self.visit(ctx.factor())
        if ctx.opsuma() is not None:
            right = self.visit(ctx.sum())
            op = ctx.opsuma().getText()
            if op == '+':
                return left + right
            else:
                return left - right
        else:
            return left

    def visitFactor(self, ctx: ExprRedesignParser.FactorContext):
        if ctx.NUM() is not None:
            text = ctx.NUM().getText()
            return float(text) if '.' in text else int(text)
        elif ctx.ID() is not None:
            raise Exception(f"Variable '{ctx.ID().getText()}' no definida.")
        else:
            return self.visit(ctx.expr())

def eval_string(s: str):
    input_stream = InputStream(s)
    lexer = ExprRedesignLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = ExprRedesignParser(tokens)
    tree = parser.prog()
    visitor = EvalVisitorRedesign()
    return visitor.visit(tree)

if __name__ == "__main__":
    tests = ["2+3*4", "20-5-3", "100/10/2", "2+3*(4-5)", "2*3+4"]
    for t in tests:
        print(t, "=>", eval_string(t))
