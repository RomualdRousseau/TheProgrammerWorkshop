import functools

axioms = [("a", "=>", "a")]

rules = [(("a", "+", "b"), "=>", ("b", "+", "a")), (("a", "+", "0"), "=>", "a")]


def is_variable(expr):
    return expr not in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")


def variables(expr, strict=True) -> list[str]:
    match expr:
        case (a, _, b):
            return variables(a, strict) + variables(b, strict)
        case _:
            return [expr] if not strict or is_variable(expr) else []


def substitute(expr, x_by_u):
    match expr:
        case (a, op, b):
            return (substitute(a, x_by_u), op, substitute(b, x_by_u))
        case _:
            return x_by_u[1] if expr == x_by_u[0] else expr


def alpha_convert(expr1, expr2):
    var1, var2 = list(dict.fromkeys(variables(expr1, False))), list(dict.fromkeys(variables(expr2, False)))
    var2_by_var1 = filter(lambda x: is_variable(x[0]), zip(var2, var1, strict=True))
    return functools.reduce(substitute, var2_by_var1, expr2)


def is_alpha_convertible(expr1, expr2):
    try:
        return expr1 == alpha_convert(expr1, expr2)
    except ValueError:
        return False


def beta_contract(expr1, expr2):
    if is_alpha_convertible(expr1, expr2[0]) or is_alpha_convertible(expr1, expr2):
        new_expr1 = alpha_convert(expr1, expr2)
        print("|-", expr2, new_expr1)
        return new_expr1[2]
    else:
        return expr1


def reduce(expr):
    match expr:
        case (_, _, _):
            new_expr = functools.reduce(beta_contract, rules, expr)
            return reduce(new_expr) if new_expr != expr else new_expr
        case _:
            return expr


def proof(expr):
    print("?-", expr)
    match expr:
        case (a, op, b):
            a, b = reduce(a), reduce(b)
            print((a, op, b))
            return (
                any(is_alpha_convertible((a, op, b), axiom) for axiom in axioms)
                if set(variables(a)) == set(variables(b))
                else False
            )
        case _:
            return False


def main():
    print(proof((("0", "+", "3"), "=>", (("3", "+", "0"), "=>", "3"))))
    print(proof((("y", "+", "0"), "=>", "y")))


if __name__ == "__main__":
    main()
