# Design Patterns Overview

## 1. Definition
Design Patterns are standard, reusable solutions to commonly occurring problems in software design. They are not code, but templates for how to solve an architectural issue.

## 2. Intuition
If you are building a house and need a way for people to move between floors, you don't invent a new mechanism; you use the "Stairs Pattern" or "Elevator Pattern." Design patterns are the stairs and elevators of software engineering.

## 3. Why it exists
They provide a shared vocabulary for developers (e.g., "Use a Singleton here" communicates intent instantly) and prevent reinventing the wheel with suboptimal, buggy solutions.

## 4. Mechanics
The Gang of Four (GoF) book categorizes 23 patterns into three types:
1. **Creational (Object Creation):** Singleton, Factory, Builder, Abstract Factory.
2. **Structural (Class/Object Composition):** Adapter, Decorator, Facade, Proxy.
3. **Behavioral (Communication between Objects):** Observer, Strategy, Command, State.

## 5. Complexity (Time & Space)
- Patterns often introduce extra classes and layers of indirection, increasing memory footprint and slightly impacting performance (due to dynamic dispatch/polymorphism), but vastly improving maintainability.

## 6. Tiny worked example (Strategy Pattern)
*Problem:* App needs to sort data using QuickSort or MergeSort depending on size.
*Solution:* Define a `SortStrategy` interface. Create `QuickSort` and `MergeSort` classes implementing it. The main app holds a reference to a `SortStrategy` and calls `.sort()`, oblivious to the underlying algorithm.

## 7. Code (Python) - Factory Pattern
```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self): pass

class Dog(Animal):
    def speak(self): return "Woof"

class Cat(Animal):
    def speak(self): return "Meow"

# Factory: Encapsulates creation logic
class AnimalFactory:
    @staticmethod
    def get_animal(animal_type: str) -> Animal:
        if animal_type == "dog": return Dog()
        if animal_type == "cat": return Cat()
        raise ValueError("Unknown animal")

# Client code doesn't instantiate Dog/Cat directly
pet = AnimalFactory.get_animal("dog")
print(pet.speak())
```

## 8. Common mistakes
- **Patternitis:** Trying to shoehorn a design pattern into every piece of code. Using a Factory to instantiate a class that will never have subclasses is unnecessary complexity.
- **Singleton Abuse:** Using Singletons as glorified global variables. They make unit testing difficult because they carry state across tests.

## 9. 30-second interview answer
"Design patterns are proven solutions to common software design problems, categorized into Creational, Structural, and Behavioral patterns. Creational patterns like Factory and Singleton handle object instantiation. Structural patterns like Adapter and Decorator handle object composition. Behavioral patterns like Observer and Strategy handle communication between objects. They provide a shared vocabulary and prevent architectural mistakes."

## 10. 2-minute interview answer
"Design patterns are the blueprints of Object-Oriented design, popularized by the Gang of Four. In Low-Level Design interviews, specific patterns appear constantly. For Creational patterns, the **Factory Pattern** is used to abstract away complex object instantiation, while the **Singleton Pattern** ensures only one instance of a class exists (useful for DB connections, though often an anti-pattern if abused). For Structural patterns, the **Adapter Pattern** wraps an incompatible interface so it works with a client (like an API wrapper), and the **Decorator Pattern** adds behavior to an object dynamically without modifying its base class. For Behavioral patterns, the **Observer Pattern** is heavily used in event-driven systems (Pub/Sub) where subjects notify observers of state changes, and the **Strategy Pattern** is used to encapsulate interchangeable algorithms, fulfilling the Open/Closed Principle. Knowing these patterns allows you to build scalable, decoupled systems."

## 11. Follow-ups
- "When would you use the Builder pattern?" (When creating an object requires a complex, multi-step initialization process with many optional parameters, avoiding a constructor with 15 arguments—an anti-pattern called telescoping constructors).

## 12. Deeper questions
- "How do you implement a thread-safe Singleton in Python?" (Using a metaclass or modifying the `__new__` method, combined with a `threading.Lock()` to ensure multiple threads don't initialize it simultaneously).

## 13. Related concepts
- **SOLID Principles**: Patterns are the practical implementation of SOLID.
- **Model-View-Controller (MVC)**: A higher-level architectural pattern that incorporates several GoF patterns (Observer, Strategy, Composite).

## 14. When it breaks / Edge cases
- Patterns designed for Java/C++ (like Visitor) are often completely unnecessary in Python due to dynamic typing and first-class functions.

## 15. Comparison with alternative approaches
- **OOP Patterns vs Functional Programming:** Many OOP patterns (like Command or Strategy) can be replaced in Python by simply passing a function as a parameter.

---
*Where this shows up in ML:*
PyTorch's `Dataset` is an implementation of the Strategy pattern. Keras callbacks use the Observer pattern.
