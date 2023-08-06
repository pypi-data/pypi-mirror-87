
def RiemanSum(f, a, b):
    """One dimensional function that returns the riemansum between two points;
    This implies that the function has the property of Rieman integrability."""
    if not callable(f):
        raise TypeError("[Rieman.py]: Function RiemanSum needs the input function f to be callabe")
     h = 0.0001 # Just a small number that can be differing. Will indicate the precission
     rie = []
     while a < b:
         rie.append(f(a)*h)
         a += h
    return sum(rie)
