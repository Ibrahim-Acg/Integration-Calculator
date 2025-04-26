



class intcalc:
    def parse_expression(self, expression):
        expression = expression.replace(' ', '')  # Remove spaces

        # Handle fractions like 2/x or 1/x^3
        if '/' in expression and 'x' in expression:
            parts = expression.split('/')
            numerator = parts[0]
            denominator = parts[1]

            # Coefficient
            if numerator == '':
                coeff = 1
            elif numerator == '-':
                coeff = -1
            else:
                coeff = int(numerator)

            # Check if denominator has an exponent
            if '^' in denominator:
                var_part, exp_part = denominator.split('^')
                if var_part != 'x':
                    raise ValueError("Unsupported variable format.")
                exponent = -int(exp_part)  # NEGATIVE because it's in the denominator
            else:
                if denominator != 'x':
                    raise ValueError("Unsupported denominator format.")
                exponent = -1  # Default when it's just x

            return {'coefficient': coeff, 'variable': 'x', 'exponent': exponent}

        # Handle normal power rule like 3x^2
        if 'x' in expression:
            parts = expression.split('x')
            coeff_part = parts[0]
            exponent_part = parts[1] if len(parts) > 1 else ''

            if coeff_part == '':
                coeff = 1
            elif coeff_part == '-':
                coeff = -1
            else:
                coeff = int(coeff_part)

            if '^' in exponent_part:
                exponent = int(exponent_part.replace('^', ''))
            else:
                exponent = 1

            return {'coefficient': coeff, 'variable': 'x', 'exponent': exponent}

        # Handle constants
        else:
            return {'coefficient': int(expression), 'variable': None, 'exponent': 0}

    def power_rule(self, parsed_expression):
        coeff = parsed_expression['coefficient']
        var = parsed_expression['variable']
        exponent = parsed_expression['exponent']


    # ∫ constant dx = constant * x
        if var is None:
            return f"{coeff}x"

    # Special case: ∫ a/x dx = a * ln|x|
        if exponent == -1:
            coeff_str = '' if coeff == 1 else '-' if coeff == -1 else str(coeff)
            return f"{coeff_str}ln|x|"

    # Regular power rule
        else:
            new_exponent = exponent + 1
            new_coefficient = coeff / new_exponent

            coeff_str = '' if new_coefficient == 1 else '-' if new_coefficient == -1 else str(new_coefficient)
            exp_str = '' if new_exponent == 1 else f"^{new_exponent}"

            return f"{coeff_str}{var}{exp_str}"

    def integrate(self, expression):
        parsed = self.parse_expression(expression)
        result = self.power_rule(parsed)
        return result + " + C"





test_expression = ['3x^2', '5x', 'x', '7', '2/x', '5/x^3']
calc = intcalc()

for expr in test_expression:
    try:
        result = calc.integrate(expr)
        print(f"∫ {expr} dx = {result}")
    except Exception as e:
        print(f"Error with {expr}: {str(e)}")
