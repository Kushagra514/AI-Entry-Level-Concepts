# SOLID Principles

## 1. Definition
SOLID is an acronym for five design principles intended to make object-oriented designs more understandable, flexible, and maintainable. Coined by Robert C. Martin (Uncle Bob).

## 2. Intuition
Imagine a Swiss Army Knife that is also a phone and a flashlight. If the flashlight breaks, you have to send your phone to the shop. SOLID principles tell you to build separate, modular, easily swappable tools instead of a giant, fragile monolith.

## 3. Why it exists
As software grows, changes in one place tend to break unrelated features. Code becomes rigid (hard to change) and fragile (breaks easily). SOLID provides architectural rules to decouple code so changes remain localized and safe.

## 4. Mechanics (The 5 Principles)
- **S - Single Responsibility Principle (SRP):** A class should have one, and only one, reason to change.
- **O - Open/Closed Principle (OCP):** Software entities should be open for extension, but closed for modification. (Use interfaces/inheritance instead of `if/else`).
- **L - Liskov Substitution Principle (LSP):** Subtypes must be substitutable for their base types without breaking the program.
- **I - Interface Segregation Principle (ISP):** Clients should not be forced to depend on interfaces they do not use. (Many small interfaces > one fat interface).
- **D - Dependency Inversion Principle (DIP):** High-level modules should not depend on low-level modules. Both should depend on abstractions.

## 5. Complexity (Time & Space)
- Applying SOLID usually increases the number of classes/files (more boilerplate), which can increase the cognitive load for navigating the codebase initially, but drastically reduces maintenance complexity.

## 6. Tiny worked example (SRP)
*Violation:* `class User: def save_to_db(): ... def generate_report(): ...` (Changes to DB or Reports both force this class to change).
*Fix:* `class User: ...`, `class UserRepository: def save(user): ...`, `class UserReport: def generate(user): ...`.

## 7. Code (Python) - Dependency Inversion (DIP)
```python
from abc import ABC, abstractmethod

# Abstraction (Interface)
class DBConnection(ABC):
    @abstractmethod
    def save(self, data): pass

# Low-level module
class MySQLConnection(DBConnection):
    def save(self, data): print("Saving to MySQL")

# High-level module depends on ABSTRACTION, not MySQL implementation
class DataManager:
    def __init__(self, db: DBConnection):
        self.db = db
        
    def process_and_save(self, data):
        self.db.save(data)

# Inject dependency
mysql = MySQLConnection()
manager = DataManager(mysql)
```

## 8. Common mistakes
- **Over-engineering:** Applying SOLID to a 50-line script. SOLID is for large, evolving codebases. Abstracting everything prematurely leads to "Enterprise FizzBuzz" spaghetti.
- **Violating LSP:** Creating a `Square` class that inherits from `Rectangle`. If a function expects a `Rectangle` and sets width=5, height=10, a `Square` would break because its width and height must be equal.

## 9. 30-second interview answer
"SOLID is a set of five OOP design principles: Single Responsibility (one reason to change), Open/Closed (extend rather than modify), Liskov Substitution (subclasses must behave like parent classes), Interface Segregation (small, specific interfaces), and Dependency Inversion (depend on abstractions, not concretions). Together, they produce decoupled, maintainable code."

## 10. 2-minute interview answer
"SOLID principles are the foundation of scalable object-oriented design. First, the Single Responsibility Principle ensures a class only handles one domain, preventing giant 'God classes'. Second, the Open/Closed Principle dictates that we should be able to add new functionality (like a new payment method) by writing new code (a new class), rather than modifying existing, tested code (adding another `if/else` block). Third, Liskov Substitution guarantees that if a function accepts a `Vehicle`, passing a `Car` subclass won't crash it—the subclass must honor the parent's contract. Fourth, Interface Segregation warns against 'fat interfaces'; a `Printer` interface shouldn't force a basic printer to implement a `scan()` method. Finally, Dependency Inversion flips traditional dependencies: instead of a high-level `App` directly instantiating a low-level `MySQLDatabase`, both should depend on a `DatabaseInterface`. This allows us to inject a `PostgresDatabase` later without touching the `App` code. While they add initial boilerplate, these principles are non-negotiable for enterprise LLD."

## 11. Follow-ups
- "Give an example of violating OCP." (A class with a method `process_payment(type)` containing `if type == 'credit': ... elif type == 'paypal': ...`. Every new payment type requires modifying this function. Fix it using Polymorphism).

## 12. Deeper questions
- "How does Dependency Inversion relate to Dependency Injection?" (Dependency Inversion is the *principle*—depend on abstractions. Dependency Injection is the *technique* used to achieve it—passing the concrete implementation into the constructor rather than instantiating it inside).

## 13. Related concepts
- **Design Patterns**: Patterns are essentially practical applications of SOLID principles.
- **Mocking (Testing)**: DIP makes unit testing easy because you can inject a mock database.

## 14. When it breaks / Edge cases
- Extreme application of ISP can lead to interfaces with only one method, creating a fragmented, hard-to-read codebase.

## 15. Comparison with alternative approaches
- **YAGNI (You Aren't Gonna Need It) vs SOLID:** There is a natural tension. SOLID prepares you for change; YAGNI tells you not to prepare for changes you don't need yet. Good engineering is balancing the two.

---
*Where this shows up in ML:*
Building scalable ML pipelines. E.g., creating an `AbstractModel` and an `AbstractDataLoader` so you can swap architectures without rewriting the training loop (DIP).
