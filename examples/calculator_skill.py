"""
Calculator Skill Extension
===========================
This example shows how to add a safe calculator skill to JARVIS.

Usage:
    - "Calculate 5 plus 3"
    - "What is 10 divided by 2"
    - "Calculate 2 to the power of 8"
"""

import ast
import operator

class CalculatorSkill:
    """Safe mathematical calculator skill"""
    
    # Allowed operators for safe evaluation
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos
    }
    
    # Word to operator mapping
    WORD_OPERATORS = {
        'plus': '+',
        'add': '+',
        'minus': '-',
        'subtract': '-',
        'times': '*',
        'multiplied by': '*',
        'multiply': '*',
        'divided by': '/',
        'divide': '/',
        'to the power of': '**',
        'power': '**',
        'squared': '**2',
        'cubed': '**3',
        'mod': '%',
        'modulo': '%'
    }
    
    def __init__(self, jarvis_instance):
        self.jarvis = jarvis_instance
    
    def can_handle(self, query):
        """Check if this skill can handle the query"""
        triggers = ['calculate', 'what is', 'compute', 'solve']
        return any(trigger in query for trigger in triggers)
    
    def handle(self, query):
        """Execute the calculator skill"""
        try:
            # Extract expression
            expression = self._extract_expression(query)
            
            if not expression:
                self.jarvis.speak("I need a mathematical expression to calculate")
                return
            
            # Convert words to operators
            expression = self._convert_words_to_operators(expression)
            
            # Calculate
            result = self._safe_eval(expression)
            
            if result is not None:
                self.jarvis.speak(f"The answer is {result}")
                print(f"Calculation: {expression} = {result}")
            else:
                self.jarvis.speak("I couldn't calculate that expression")
        
        except Exception as e:
            self.jarvis.speak("Sorry, I couldn't perform that calculation")
            print(f"Calculation error: {e}")
    
    def _extract_expression(self, query):
        """Extract mathematical expression from query"""
        # Remove trigger words
        for trigger in ['calculate', 'what is', 'compute', 'solve']:
            query = query.replace(trigger, '')
        
        return query.strip()
    
    def _convert_words_to_operators(self, expression):
        """Convert word operators to symbols"""
        for word, symbol in self.WORD_OPERATORS.items():
            expression = expression.replace(word, symbol)
        return expression
    
    def _safe_eval(self, expression):
        """Safely evaluate mathematical expression"""
        try:
            # Parse the expression
            node = ast.parse(expression, mode='eval')
            return self._eval_node(node.body)
        except:
            return None
    
    def _eval_node(self, node):
        """Recursively evaluate AST nodes"""
        if isinstance(node, ast.Num):
            # Number constant
            return node.n
        
        elif isinstance(node, ast.BinOp):
            # Binary operation (e.g., 2 + 3)
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op = self.OPERATORS.get(type(node.op))
            
            if op:
                return op(left, right)
            raise ValueError("Unsupported operator")
        
        elif isinstance(node, ast.UnaryOp):
            # Unary operation (e.g., -5)
            operand = self._eval_node(node.operand)
            op = self.OPERATORS.get(type(node.op))
            
            if op:
                return op(operand)
            raise ValueError("Unsupported operator")
        
        else:
            raise ValueError("Unsupported expression")


# Integration example
def add_calculator_to_jarvis():
    """Example of how to integrate this skill"""
    
    # In your Jarvis class __init__:
    # self.calculator = CalculatorSkill(self)
    
    # In your process_command method:
    # if self.calculator.can_handle(query):
    #     self.calculator.handle(query)
    #     return
    
    pass


if __name__ == "__main__":
    # Test the calculator
    class MockJarvis:
        def speak(self, text):
            print(f"JARVIS: {text}")
    
    jarvis = MockJarvis()
    calc = CalculatorSkill(jarvis)
    
    # Test calculations
    test_queries = [
        "calculate 5 plus 3",
        "what is 10 divided by 2",
        "calculate 2 to the power of 8",
        "what is 15 mod 4",
        "calculate 100 minus 37"
    ]
    
    for query in test_queries:
        print(f"\nUser: {query}")
        calc.handle(query)
