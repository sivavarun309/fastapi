def test(a=None, b=None, c=None, d=None):
    print(f"a={a} and b={b} and c={c} and d={d}")

dic = {"a":"value a", "b":"Value b", "c":"Value c", "d":"value d"}

test(**dic)

