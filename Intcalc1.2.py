from fractions import Fraction



class intcalc:

    def split_terms(self, expression):
        expression = expression.replace(' ', '')  # Remove spaces
        terms = []
        current_term = ''

        for i, char in enumerate(expression):
            if char in '+-':
                if current_term != '':
                    terms.append(current_term)
                current_term = char
            else:
                current_term += char
        if current_term:
            terms.append(current_term)
        
        return terms


    def seperate_outside_inside(self, expression):
        expression = expression.replace(' ', '')  # Remove spaces
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
                    groups.append(expression[group_start: i + 1])
        if len(groups) != 2:
            raise ValueError("Expects two sets of parentheses for U-subtitution")
        
        outside_group = groups[0]
        inside_group = groups[1]

        # Remove parentheses from groups 
        outside = outside_group[1,-1]
        inside = inside_group[1,-1]

        return outside, inside


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
            new_coefficient = Fraction(coeff, new_exponent)

            coeff_str = '' if new_coefficient == 1 else '-' if new_coefficient == -1 else str(new_coefficient)
            exp_str = '' if new_exponent == 1 else f"^{new_exponent}"

            return f"{coeff_str}{var}{exp_str}"
        

    #simple U-sub, medium and complex will come later with parts and trig
    def u_substitution(self, expression):

    # Split into outside multiplier and inside function
        outside, inside = self.separate_outside_inside(expression)
    
    # Parse the outside
        parsed_outside = self.parse_expression(outside)

    # Differentiate the inside (only the base, not including the outside exponent)
        inside_base, inside_exponent = self.extract_inside_base_exponent(inside)

        inside_derivative = self.simple_derivative(inside_base)

    # Parse the derivative
        parsed_inside_derivative = self.parse_expression(inside_derivative)

    # Compare proportionality
        ratio = self.is_proportional(parsed_outside, parsed_inside_derivative)
        if ratio is None:
            raise ValueError("Outside term is not proportional to derivative of inside base. U-substitution not possible.")

    # Now integrate u^n normally
        integral_u = self.integrate_u_power_rule(inside_exponent)

    # Adjust the integral by the proportional ratio
        if ratio != 1:
            integral_u = f"{Fraction(ratio)}*{integral_u}"

    # Substitute u back with the real inside base
        final_result = integral_u.replace('u', f'({inside_base})')

        return final_result + " + C"


    def is_proportional(self, outside, derivative):
        parsed_outside = self.parse_expression(outside)
        parsed_derivative = self.parse_expression(derivative)

        #Check for erranious Variables
        if parsed_outside['variable'] != parsed_derivative['variable']:
            return None  

        ratio = parsed_outside['coefficient'] / parsed_derivative['coefficient']
        return ratio

    def simple_derivative(self,expression):
        terms = self.split_terms(expression)
        derivative_terms = []

        for term in terms:
            parsed = self.parse_expression(term)
            if parsed['variable'] is None:
                continue
            new_coeff = parsed['coefficient'] * parsed['exponent']
            new_exp = parsed['exponent'] -1 

            if new_exp == 0:
                derivative_terms.append(str(new_coeff))
            elif new_exp == 1:
                derivative_terms.append(f'{new_coeff}x')
            else:
                derivative_terms.append(f"{new_coeff}x^{new_exp}")
        return ''.join(derivative_terms)

    def parse_expression_u(self,inside):
        if '^' in inside:
            base, exp = inside.split(')^')
            exp = int(exp)
        else:
            exp = 1

        return {'coefficient': 1, 'variable': u, 'exponent': exp}

    def integrate(self, expression):
        terms = self.split_terms(expression)
        integrated_terms = []

        for term in terms:
            parsed = self.parse_expression(term)
            integrated = self.power_rule(parsed)
            integrated_terms.append(integrated)
        
        return ' + '.join(integrated_terms) + " + C"






test_expression = ['4x^3 - 2x^2 + 5x - 7',
 '(2x)(5x^2+4)^3', 'x', '7', '2/x', '5/x^3']
calc = intcalc()

for expr in test_expression:
    try:
        result = calc.integrate(expr)
        print(f"∫ {expr} dx = {result}")
    except Exception as e:
        print(f"Error with {expr}: {str(e)}")
