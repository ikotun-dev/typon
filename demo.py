import inspect
from typing import Callable, Any, Dict

# Custom strict type annotations
class StrictType:
    def __init__(self, type_class: type):
        self.type_class = type_class

class Int(StrictType):
    def __init__(self):
        super().__init__(int)

class Str(StrictType):
    def __init__(self):
        super().__init__(str)

# Custom type checker
class StrictTypeChecker:
    def __init__(self):
        self.type_registry: Dict[str, type] = {
            'Int': int,
            'Str': str,
        }

    def check_type(self, value: Any, expected_type: StrictType) -> bool:
        if expected_type.type_class in self.type_registry.values():
            return isinstance(value, expected_type.type_class)
        return False

    def check_function(self, func: Callable) -> bool:
        signature = inspect.signature(func)
        for param_name, param in signature.parameters.items():
            if param_name in func.__annotations__:
                expected_type = func.__annotations__[param_name]
                if not self.check_type(param.default, expected_type):
                    return False
        if 'return' in func.__annotations__:
            expected_return_type = func.__annotations__['return']
            return self.check_type(func(), expected_return_type)
        return True

# Example usage
strict_type_checker = StrictTypeChecker()

@strict_type_checker.check_function
def add(a: Int, b: Int) -> Int:
    return a + b

@strict_type_checker.check_function
def concat(s1: Str, s2: Str) -> Str:
    return s1 + s2

@strict_type_checker.check_function
def invalid_function(a: Int, b: Str) -> Int:
    return a

# Test the functions
print(add(1, 2))  # Output: 3
print(concat("Hello, ", "world!"))  # Output: Hello, world!

# This will raise an error due to invalid function parameter type
print(invalid_function(1, "Hello"))  # Type mismatch error
