from fractions import Fraction

class intcalc:
    def __init__(self):
        pass

    def parse_expression(self, expression):
        expression = expression.replace(' ', '')

        if '/' in expression and 'x' in expression:
            parts = expression.split('/')
            numerator = parts[0]
            denominator = parts[1]

            if numerator == '':
                coeff = 1
            elif numerator == '-':
                coeff = -1
            else:
                coeff = int(numerator)

            if '^' in denominator:
                var_part, exp_part = denominator.split('^')
                if var_part != 'x':
                    raise ValueError("Unsupported denominator format.")
                exponent = -int(exp_part)
            else:
                if denominator != 'x':
                    raise ValueError("Unsupported denominator format.")
                exponent = -1

            return {'coefficient': coeff, 'variable': 'x', 'exponent': exponent}

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

        else:
            return {'coefficient': int(expression), 'variable': None, 'exponent': 0}

    def split_terms(self, expression):
        expression = expression.replace(' ', '')
        terms = []
        current_term = ''

        for i, char in enumerate(expression):
            if char in '+-':
                if current_term:
                    terms.append(current_term)
                current_term = char
            else:
                current_term += char

        if current_term:
            terms.append(current_term)

        return terms

    def power_rule(self, parsed_expression):
        coeff = parsed_expression['coefficient']
        var = parsed_expression['variable']
        exponent = parsed_expression['exponent']

        if var is None:
            return f"{coeff}x"

        if exponent == -1:
            coeff_str = '' if coeff == 1 else '-' if coeff == -1 else str(coeff)
            return f"{coeff_str}ln|x|"

        else:
            new_exponent = exponent + 1
            new_coefficient = Fraction(coeff, new_exponent)

            coeff_str = '' if new_coefficient == 1 else '-' if new_coefficient == -1 else str(new_coefficient)
            exp_str = '' if new_exponent == 1 else f"^{new_exponent}"

            return f"{coeff_str}{var}{exp_str}"

    def integrate(self, expression):
        terms = self.split_terms(expression)
        integrated_terms = []

        for term in terms:
            parsed = self.parse_expression(term)
            integrated = self.power_rule(parsed)
            integrated_terms.append(integrated)

        return ' + '.join(integrated_terms) + " + C"

    def separate_outside_inside(self, expression):
        expression = expression.replace(' ', '')
        groups = []
        paren_tracker = []
        group_start = None

        for i, char in enumerate(expression):
            if char == '(':
                if not paren_tracker:
                    group_start = i
                paren_tracker.append('(')
            elif char == ')':
                paren_tracker.pop()
                if not paren_tracker:
                    groups.append(expression[group_start:i+1])

        if len(groups) != 2:
            raise ValueError("Expected two parenthesis groups for u-substitution.")

        outside_group = groups[0]
        inside_group = expression[expression.find(groups[1]):]

        outside = outside_group[1:-1]
        inside = inside_group

        return outside, inside

    def simple_derivative(self, expression):
        terms = self.split_terms(expression)
        derivative_terms = []

        for term in terms:
            parsed = self.parse_expression(term)
            if parsed['variable'] is None:
                continue
            new_coeff = parsed['coefficient'] * parsed['exponent']
            new_exp = parsed['exponent'] - 1

            if new_exp == 0:
                derivative_terms.append(str(new_coeff))
            elif new_exp == 1:
                derivative_terms.append(f"{new_coeff}x")
            else:
                derivative_terms.append(f"{new_coeff}x^{new_exp}")

        return ''.join(derivative_terms)

    def is_proportional(self, parsed_outside, parsed_derivative):
        if parsed_outside['variable'] != parsed_derivative['variable']:
            return None
        
        ratio = Fraction(parsed_outside['coefficient'], parsed_derivative['coefficient'])
        return ratio


    def extract_inside_base_exponent(self, inside):
        if ')^' in inside:
            paren_end = inside.find(')')
            base = inside[1:paren_end]
            exponent = int(inside[paren_end + 2:])
        else:
            base = inside[1:-1]
            exponent = 1 
        return base, exponent


    def integrate_u_power_rule(self, exponent):
        new_exponent = exponent + 1
        return f"u^{new_exponent}/{new_exponent}"


    def u_substitution(self, expression):
        outside, inside = self.separate_outside_inside(expression)
        parsed_outside = self.parse_expression(outside)

        inside_base, inside_exponent = self.extract_inside_base_exponent(inside)
        inside_derivative = self.simple_derivative(inside_base)
        parsed_inside_derivative = self.parse_expression(inside_derivative)

        ratio = self.is_proportional(parsed_outside, parsed_inside_derivative)
        if ratio is None:
            raise ValueError("Outside term is not proportional to derivative of inside base. U-substitution not possible.")

        integral_u = self.integrate_u_power_rule(inside_exponent)

        if ratio != 1:
            integral_u = f"{Fraction(ratio)}*{integral_u}"

        final_result = integral_u.replace('u', f'({inside_base})')

        return final_result + " + C"



calc = intcalc()
print(calc.u_substitution("(2x)(5x^2+4)^3"))

