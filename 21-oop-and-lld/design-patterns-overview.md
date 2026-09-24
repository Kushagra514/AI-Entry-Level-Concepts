# Design Patterns Overview

## 1. Categories
- **Creational**: object creation mechanisms
- **Structural**: class/object composition
- **Behavioral**: algorithms and object interaction

## 2. Singleton (Creational)
Ensure only one instance exists.
```python
class Singleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
# Thread-safe version uses threading.Lock
```
Use when: DB connection pool, config manager, logger.

## 3. Factory Method (Creational)
Delegate object creation to subclass/method.
```python
class Notification:
    @staticmethod
    def create(kind):
        if kind == 'email': return EmailNotification()
        if kind == 'sms':   return SMSNotification()
        raise ValueError
```
Use when: object type determined at runtime, hide creation logic.

## 4. Abstract Factory (Creational)
Family of related factories. GUI toolkit (Windows/Mac buttons + checkboxes).

## 5. Builder (Creational)
Step-by-step construction of complex objects.
```python
class QueryBuilder:
    def __init__(self): self._parts = []
    def select(self, cols): self._parts.append(f"SELECT {cols}"); return self
    def from_(self, tbl): self._parts.append(f"FROM {tbl}"); return self
    def build(self): return ' '.join(self._parts)
# Usage: QueryBuilder().select('*').from_('users').build()
```

## 6. Adapter (Structural)
Convert one interface to another.
```python
class OldPayment:
    def do_pay(self, amount): ...
class PaymentAdapter:
    def __init__(self, old): self.old = old
    def pay(self, amount): return self.old.do_pay(amount)
```

## 7. Decorator (Structural)
Add behavior without modifying class. Python `@` syntax is a native decorator.
```python
class Coffee:
    def cost(self): return 5
class MilkDecorator:
    def __init__(self, coffee): self._coffee = coffee
    def cost(self): return self._coffee.cost() + 2
```

## 8. Facade (Structural)
Simplified interface to a subsystem.
```python
class HomeTheaterFacade:
    def __init__(self, amp, dvd, proj): ...
    def watch_movie(self): # calls amp.on(), dvd.play(), proj.on()
```

## 9. Observer (Behavioral)
Subject notifies observers on state change. Event-driven systems.
```python
class EventEmitter:
    def __init__(self): self._listeners = {}
    def on(self, event, fn): self._listeners.setdefault(event, []).append(fn)
    def emit(self, event, *args):
        for fn in self._listeners.get(event, []): fn(*args)
```

## 10. Strategy (Behavioral)
Encapsulate interchangeable algorithms.
```python
class Sorter:
    def __init__(self, strategy): self.strategy = strategy
    def sort(self, data): return self.strategy(data)
sorter = Sorter(sorted)
```

## 11. Command (Behavioral)
Encapsulate a request as an object — supports undo/redo.
```python
class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...
```

## 12. Template Method (Behavioral)
Define skeleton of algorithm in base class; subclasses fill in steps.
```python
class DataProcessor(ABC):
    def process(self):
        self.read(); self.transform(); self.write()
    @abstractmethod
    def transform(self): ...
```

## 13. Proxy (Structural)
Control access to another object: lazy init, access control, logging.

## 14. When to Use Which
| Pattern | Signal |
|---------|--------|
| Singleton | "only one instance" |
| Factory | "create based on type" |
| Observer | "notify on change" |
| Strategy | "swap algorithms" |
| Decorator | "add behavior dynamically" |
| Command | "queue/undo operations" |

## 15. Anti-Patterns to Avoid
- Over-engineering with patterns where simple code suffices.
- God Object (violates SRP).
- Singleton abuse (hidden global state, hard to test).
