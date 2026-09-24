# Low-Level Design (LLD) Questions

## 1. Definition
Low-Level Design (LLD) interviews assess your ability to take a system requirement (e.g., "Design a Parking Lot") and translate it into Object-Oriented code, focusing on class diagrams, relationships, SOLID principles, and design patterns.

## 2. Intuition
High-Level Design (System Design) is about drawing boxes for databases and load balancers. Low-Level Design is about what goes *inside* the backend box: what classes exist, what data they hold, and how they call each other.

## 3. Why it exists
Writing code that works for a script is easy. Writing code that can be maintained by 50 developers over 5 years requires strict adherence to OOP principles. LLD interviews test if you write scalable, modular code.

## 4. Mechanics (The 4-Step Framework)
1. **Requirements Gathering:** Clarify exact features. (E.g., for Parking Lot: Are there multiple floors? Different vehicle sizes? Hourly pricing?)
2. **Identify Core Entities:** Nouns become classes. (ParkingLot, ParkingSpot, Vehicle, Ticket).
3. **Identify Relationships:** Has-A (Composition), Is-A (Inheritance).
4. **Define APIs/Methods:** Verbs become methods. (`parkVehicle()`, `calculateFare()`). Apply design patterns.

## 5. Complexity (Time & Space)
- LLD focuses on code organization and maintainability (Clean Code) rather than algorithmic time/space complexity, though efficient data structures (e.g., using a MinHeap for the nearest available parking spot) are a bonus.

## 6. Tiny worked example (Library Management System)
*Entities:* `Library`, `Book`, `Member`, `Loan`.
*Inheritance:* `BookItem` inherits from `Book` (adds barcode, status).
*Relationships:* `Library` has many `BookItems`. `Member` has many `Loans`.
*Methods:* `Library.search(title)`, `Member.checkout(book_item)`.

## 7. Code (Python) - Parking Lot Core Entities
```python
from enum import Enum
from abc import ABC

class VehicleSize(Enum):
    MOTORCYCLE = 1
    COMPACT = 2
    LARGE = 3

class Vehicle(ABC):
    def __init__(self, license_plate, size):
        self.license_plate = license_plate
        self.size = size

class Car(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate, VehicleSize.COMPACT)

class ParkingSpot:
    def __init__(self, spot_id, size):
        self.spot_id = spot_id
        self.size = size
        self.vehicle = None
        
    def is_free(self):
        return self.vehicle is None
        
    def park(self, vehicle):
        if self.is_free() and vehicle.size.value <= self.size.value:
            self.vehicle = vehicle
            return True
        return False
```

## 8. Common mistakes
- **Writing God Classes:** Putting all logic into one `ParkingLot` class instead of delegating (e.g., pricing logic should be in a `PricingStrategy` class, not `ParkingLot.calculate_fare()`).
- **Ignoring Concurrency:** Not mentioning how the code behaves if two users try to book the last movie ticket at the exact same millisecond. (Mention locks/mutexes or DB transaction isolation).

## 9. 30-second interview answer
"In an LLD interview, I follow a structured approach: clarify requirements, identify core entities (classes), map their relationships (composition/inheritance), and define their public APIs. I prioritize SOLID principles—for instance, extracting pricing logic into a Strategy pattern to satisfy the Open/Closed principle—and ensure the code is modular and testable."

## 10. 2-minute interview answer
"Approaching an LLD problem like designing a Parking Lot requires breaking the problem down into entities and behaviors. First, I define the models: `Vehicle` (abstract base class), `Car`, `Truck`, `ParkingSpot`, `Ticket`, and `Level`. A `ParkingLot` is composed of multiple `Level`s, and a `Level` is composed of `ParkingSpot`s. This composition allows for easy scaling. The core logic involves finding a free spot and calculating fares. To find a free spot efficiently, I wouldn't iterate through an array of spots; I'd use a queue or a hash map of available spots. For fare calculation, requirements change often (weekend rates, VIP rates), so I would use the Strategy Pattern. I'd create a `PricingStrategy` interface, allowing the system to swap in an `HourlyPricingStrategy` or `FlatRateStrategy` at runtime without modifying the core `Ticket` class. Finally, I'd address concurrency: since multiple gates are assigning spots simultaneously, the `assign_spot()` method must be thread-safe using a Mutex lock to prevent double-booking."

## 11. Follow-ups
- "How do you handle multiple parking gates simultaneously trying to assign the nearest spot?" (Use a Thread Lock/Mutex on the data structure holding the available spots, or use an atomic operation like `pop()` on a thread-safe Queue).

## 12. Deeper questions
- "Design an Elevator System. What pattern handles the scheduling?" (The State Pattern for the elevator's current status (MovingUp, MovingDown, Idle), and the Strategy Pattern for the dispatch algorithm (FCFS vs SCAN/Elevator algorithm)).

## 13. Related concepts
- **High-Level Design (HLD)**: The macro view of what LLD implements in the micro view.
- **UML Diagrams**: Class and Sequence diagrams used to visualize LLD.

## 14. When it breaks / Edge cases
- Designing a tightly coupled system where changing the payment gateway requires rewriting the User class (violation of Dependency Inversion).

## 15. Comparison with alternative approaches
- **Top-down vs Bottom-up LLD:** Top-down starts with the Main system (`ParkingLot`) and drills down. Bottom-up starts with primitives (`ParkingSpot`) and builds up. Bottom-up is usually safer to code in an interview.

---
*Where this shows up in ML:*
Designing a modular ML training pipeline (e.g., scikit-learn's `BaseEstimator` and `TransformerMixin` design).
