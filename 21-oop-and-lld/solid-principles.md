# SOLID Principles

## 1. Overview
S — Single Responsibility, O — Open/Closed, L — Liskov Substitution,
I — Interface Segregation, D — Dependency Inversion.

## 2. Single Responsibility Principle (SRP)
A class should have only ONE reason to change.
```python
# Violation: Invoice handles both data and printing
class Invoice:
    def calculate_total(self): ...
    def print_invoice(self): ...   # unrelated concern
    def save_to_db(self): ...      # another concern

# Fix: separate classes
class Invoice: ...
class InvoicePrinter:
    def print(self, invoice): ...
class InvoiceRepository:
    def save(self, invoice): ...
```

## 3. Open/Closed Principle (OCP)
Open for extension, closed for modification.
```python
# Violation: must edit class to add new discount
class Discount:
    def apply(self, customer, price):
        if customer == 'VIP': return price * 0.8
        if customer == 'Regular': return price * 0.9  # keep adding if/else

# Fix: extend via subclasses
class Discount(ABC):
    @abstractmethod
    def apply(self, price): ...
class VIPDiscount(Discount):
    def apply(self, price): return price * 0.8
```

## 4. Liskov Substitution Principle (LSP)
Subclass instances must be substitutable for superclass without breaking correctness.
```python
# Violation
class Rectangle:
    def set_width(self, w): self.w = w
    def set_height(self, h): self.h = h
    def area(self): return self.w * self.h

class Square(Rectangle):         # Breaks LSP!
    def set_width(self, w): self.w = self.h = w   # unexpected side-effect
```
Fix: don't force Square to inherit from Rectangle. Use separate hierarchy.

## 5. Interface Segregation Principle (ISP)
Clients should not depend on methods they don't use. Split fat interfaces.
```python
# Violation
class Worker(ABC):
    @abstractmethod
    def work(self): ...
    @abstractmethod
    def eat(self): ...    # Robot can't eat!

# Fix
class Workable(ABC):
    @abstractmethod
    def work(self): ...
class Eatable(ABC):
    @abstractmethod
    def eat(self): ...

class Human(Workable, Eatable): ...
class Robot(Workable): ...
```

## 6. Dependency Inversion Principle (DIP)
High-level modules should not depend on low-level modules. Both depend on abstractions.
```python
# Violation: high-level class hardcodes low-level detail
class EmailService:
    def send(self, msg): ...
class Notification:
    def __init__(self): self.service = EmailService()  # concrete dependency

# Fix: inject abstraction
class MessageService(ABC):
    @abstractmethod
    def send(self, msg): ...
class EmailService(MessageService):
    def send(self, msg): ...
class Notification:
    def __init__(self, service: MessageService):
        self.service = service
```

## 7. SRP in Practice
Keep classes small. If describing a class requires "and", split it.

## 8. OCP and Strategy Pattern
OCP naturally leads to Strategy/Template Method patterns.

## 9. LSP Formal Definition
If S is a subtype of T, then objects of type T may be replaced with objects of type S without altering correctness.
Behavioral subtypes: preconditions ≤ parent, postconditions ≥ parent, invariants preserved.

## 10. ISP and Python Protocols
Python's `typing.Protocol` enables structural subtyping — class matches protocol if it has required methods, no explicit inheritance needed.

## 11. DIP and Dependency Injection
```python
# DI container / manual injection
notification = Notification(service=SMSService())
```
Frameworks like FastAPI use DI extensively.

## 12. Recognizing Violations in Interviews
- Giant class doing everything → SRP
- Long if/elif chains on type → OCP
- Overriding method to do nothing or raise → LSP
- Empty interface method implementations → ISP
- `new ConcreteClass()` inside business logic → DIP

## 13. SOLID and Testing
DIP makes unit testing easier: inject mocks via constructor.
SRP means each class has focused, testable behavior.

## 14. Common Interview Q
"Design X following SOLID." Start: define abstractions → inject dependencies → split responsibilities.

## 15. Quick Reference
| Principle | Key Question |
|-----------|-------------|
| SRP | Does this class have one reason to change? |
| OCP | Can I add feature without editing existing code? |
| LSP | Can I swap subclass without breaking callers? |
| ISP | Do all clients use all interface methods? |
| DIP | Does high-level code depend on abstractions? |
