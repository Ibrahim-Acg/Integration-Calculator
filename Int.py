import math
from scipy import integrate
from fractions import Fraction


question = str(input())
if "^" in question:
    variable, exponent = question.split('^')
else:
    exponent = 1
    variable = question

# integrand = 2x
# We took 2 out of 2x
# We divided 2/2 = 1 
# Integrand still has the old coeff
# Remove the old coeff from integrand 

def integral(integrand, exponent):
    n = int(exponent) + 1 
    coeff , x = variable.split("x")
    if int(coeff) % n == 0:
        f = Fraction(int(coeff), n)
        ratio = f.as_integer_ratio()
        if ratio[0] == 1 and ratio[1] == 1:
            return f"x^{n}"
        elif ratio[0] == 1:
            return f"x^{n}/{ratio[1]}"
        elif ratio[1] == 1:
            return f"{ratio[0]}x^{n} "
        else:
            return f"{ratio[0]}x^{n}/{ratio[1]}"
    else:
        return f'{integrand}^{n}/{n}'

print(integral(variable, exponent))

#if coefficient//n == 0, then divide the coeff by n and return the new value 