# OOP Fundamentals

## 1. Definition
Object-Oriented Programming (OOP) is a paradigm that organizes software design around data, or objects, rather than functions and logic. An object is a data field that has unique attributes and behavior.

## 2. Intuition
Instead of having scattered variables `car_color`, `car_speed` and functions `accelerate(speed)`, you bundle them into a `Car` blueprint. When you buy a specific car, you instantiate the blueprint into an object: `my_car = Car('red')`.

## 3. Why it exists
As procedural programs grow, tracking which functions modify which global variables becomes impossible (spaghetti code). OOP encapsulates data and the functions that modify it into single units, making large codebases modular, reusable, and easier to maintain.

## 4. Mechanics
The Four Pillars of OOP:
1. **Encapsulation:** Hiding internal state and requiring all interaction to be performed through an object's methods (getters/setters).
2. **Abstraction:** Hiding complex implementation details and showing only the essential features of the object (Interfaces/Abstract Classes).
3. **Inheritance:** Creating new classes (child) that derive attributes and methods from existing classes (parent), promoting code reuse.
4. **Polymorphism:** The ability of different classes to be treated as instances of the same class through a common interface (e.g., `Dog.speak()` and `Cat.speak()`).

## 5. Complexity (Time & Space)
- Virtual method dispatch (Polymorphism) adds a slight runtime overhead (vtable lookup) compared to direct function calls.
- Objects have memory overhead for headers/pointers.

## 6. Tiny worked example
```python
# Encapsulation
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance # Private attribute
        
    def deposit(self, amount):
        if amount > 0: self.__balance += amount
        
    def get_balance(self):
        return self.__balance
```

## 7. Code (Python)
```python
from abc import ABC, abstractmethod

# Abstraction
class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

# Inheritance
class Dog(Animal):
    def speak(self):
        return "Woof"

class Cat(Animal):
    def speak(self):
        return "Meow"

# Polymorphism
def make_animal_speak(animal: Animal):
    print(animal.speak())

make_animal_speak(Dog()) # Outputs: Woof
make_animal_speak(Cat()) # Outputs: Meow
```

## 8. Common mistakes
- **Deep Inheritance Trees:** Creating classes like `Animal -> Mammal -> Dog -> Poodle`. Prefer Composition over Inheritance (give the Poodle a `BarkBehavior` object rather than inheriting from `BarkingMammal`).
- **Breaking Encapsulation:** Making internal variables public (`self.balance`) instead of using properties or getters/setters, making future validation changes impossible without breaking the API.

## 9. 30-second interview answer
"OOP organizes code into modular objects combining data and behavior. It relies on four pillars: Encapsulation (hiding internal state), Abstraction (hiding implementation details behind interfaces), Inheritance (reusing code from parent classes), and Polymorphism (allowing different objects to respond to the same method call appropriately)."

## 10. 2-minute interview answer
"Object-Oriented Programming manages software complexity by modeling the world as interacting objects. The four pillars structure this paradigm. Encapsulation protects an object's internal state, ensuring it can only be modified through defined methods, which preserves data integrity. Abstraction simplifies the interface by hiding the underlying implementation—for example, a `save()` method might write to a DB or a file, but the caller doesn't need to know. Inheritance allows a child class to inherit attributes from a parent class, establishing an 'is-a' relationship (a Car is a Vehicle) to reuse code. Finally, Polymorphism allows us to program to an interface rather than an implementation; we can iterate through a list of `Vehicle` objects and call `.drive()` on each, and the runtime will execute the correct method whether the object is a Car or a Truck. In modern design, however, we often favor Composition ('has-a') over deep Inheritance ('is-a') to avoid brittle, tightly coupled code hierarchies."

## 11. Follow-ups
- "What is Composition over Inheritance?" (Composition means assembling objects from smaller components—a Car *has an* Engine. Inheritance means a Car *is a* Vehicle. Composition is more flexible because you can swap the Engine at runtime; you can't swap a parent class).

## 12. Deeper questions
- "How does Python handle private variables?" (It uses name mangling. `__var` is renamed to `_ClassName__var` internally. It's not strictly private like in Java, but a strong convention/mechanism to avoid accidental access).

## 13. Related concepts
- **SOLID Principles**: The rules for writing *good* OOP code.
- **Design Patterns**: Standard solutions to common OOP design problems.

## 14. When it breaks / Edge cases
- Diamond Problem in Multiple Inheritance (Class D inherits from B and C, which both inherit from A. If D calls a method from A, which path does it take?). Python solves this via Method Resolution Order (MRO) using the C3 linearization algorithm.

## 15. Comparison with alternative approaches
- **OOP vs Functional Programming (FP):** OOP groups data and methods; state is mutable. FP keeps data and functions separate; state is immutable. FP is often better for concurrent data processing, OOP for GUI and simulations.

---
*Where this shows up in ML:*
PyTorch's `nn.Module` (Inheritance), `forward()` methods (Polymorphism), Dataset/DataLoader abstractions.
