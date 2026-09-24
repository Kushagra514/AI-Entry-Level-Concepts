# OOP Fundamentals

## 1. Four Pillars
Encapsulation, Inheritance, Polymorphism, Abstraction.

## 2. Encapsulation
Bundle data and methods; hide internal state. Use `_` (protected) and `__` (private name-mangling) in Python.
```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance          # private
    def deposit(self, amount):
        if amount > 0: self.__balance += amount
    def get_balance(self): return self.__balance
```

## 3. Inheritance
Subclass inherits attributes/methods from superclass. Enables code reuse.
```python
class Animal:
    def __init__(self, name): self.name = name
    def speak(self): raise NotImplementedError
class Dog(Animal):
    def speak(self): return f"{self.name} says Woof"
class Cat(Animal):
    def speak(self): return f"{self.name} says Meow"
```

## 4. Polymorphism
Same interface, different behavior. Works via duck typing in Python.
```python
animals = [Dog("Rex"), Cat("Luna")]
for a in animals: print(a.speak())   # runtime dispatch
```

## 5. Abstraction
Hide complexity; expose only necessary interface. Use `abc.ABC` in Python.
```python
from abc import ABC, abstractmethod
class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return 3.14 * self.r ** 2
```

## 6. Composition vs Inheritance
Prefer composition ("has-a") over inheritance ("is-a") when behavior varies dynamically.
```python
class Engine:
    def start(self): return "Engine started"
class Car:
    def __init__(self): self.engine = Engine()   # composition
    def drive(self): return self.engine.start()
```

## 7. Method Resolution Order (MRO)
Python uses C3 linearization for multiple inheritance. Check via `ClassName.__mro__`.

## 8. super()
Calls parent class method without hardcoding parent name.
```python
class B(A):
    def __init__(self):
        super().__init__()   # calls A.__init__
```

## 9. Dunder Methods
```python
__init__, __str__, __repr__, __len__, __eq__, __lt__, __hash__
__enter__, __exit__    # context manager
__iter__, __next__     # iterator protocol
```

## 10. Class vs Static vs Instance Methods
```python
class MyClass:
    class_var = 0
    def instance_method(self): ...          # access self
    @classmethod
    def class_method(cls): ...              # access cls
    @staticmethod
    def static_method(): ...               # no self/cls
```

## 11. Properties
Control attribute access with getters/setters without changing API.
```python
class Circle:
    def __init__(self, r): self._r = r
    @property
    def radius(self): return self._r
    @radius.setter
    def radius(self, v):
        if v < 0: raise ValueError
        self._r = v
```

## 12. When to Use Each Pillar
- Encapsulation: always — protect invariants
- Inheritance: strong "is-a" relationships, shallow hierarchies
- Polymorphism: plugin architectures, strategy pattern
- Abstraction: define contracts in libraries/frameworks

## 13. Mixin Pattern
Add behavior without full inheritance hierarchy.
```python
class JSONMixin:
    def to_json(self): import json; return json.dumps(self.__dict__)
class User(JSONMixin, BaseModel): ...
```

## 14. Common Interview Questions
- Explain OOP with a real example.
- Composition vs inheritance tradeoffs.
- How does Python achieve polymorphism (duck typing vs interfaces)?

## 15. Python OOP Pitfalls
- Mutable default class variable shared across instances.
- Forgetting `self` in method signatures.
- Deep inheritance chains → fragile base class problem.
