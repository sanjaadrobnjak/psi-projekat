import re

class EvaluatorError(Exception):
    pass

def evaluate(expr: str, nums: list[int]) -> int:
    tokens = _tokenize(expr)
    nums = nums.copy()
    for token in tokens:
        if token.isnumeric():
            try:
                nums.remove(int(token))
            except ValueError:
                raise EvaluatorError
        elif token not in '+-*/()':
            raise EvaluatorError
    try:
        return eval("".join(tokens))
    except (SyntaxError, ZeroDivisionError):
        raise EvaluatorError

def _tokenize(expr: str) -> list[str]:
    pattern = "(?:\\d+)|\(|\)|\+|-|\*|/"
    return re.findall(pattern, expr)
