import os

def wc(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content.strip() + "\n")
    os.system(f'git add "{path}" && git commit -m "Fill {os.path.basename(path)} (Batch E)"')

wc("19-dp-deep-dive/2d-dp.md", r"""# 2D Dynamic Programming

## 1. Definition
2D Dynamic Programming solves problems by maintaining a 2D state matrix, usually `dp[i][j]`. It is heavily used when the state depends on two variables: two strings (e.g., Edit Distance), a grid (e.g., Unique Paths), or an item index and a capacity (e.g., Knapsack).

## 2. Intuition
If you are navigating a grid from top-left to bottom-right, the number of ways to reach cell `(i, j)` depends entirely on the ways to reach the cell directly above `(i-1, j)` and directly to the left `(i, j-1)`. You sum them. By building a 2D table, you solve the maze step by step.

## 3. Why it exists
Many problems have optimal substructure defined by two independent axes. 1D DP cannot capture the relationship (e.g., comparing string A to string B requires tracking positions in both strings). 

## 4. Mechanics
- **Grid Traversal:** `dp[i][j] = dp[i-1][j] + dp[i][j-1]`.
- **String Matching:** `dp[i][j]` depends on `dp[i-1][j-1]` (if characters match) or `max(dp[i-1][j], dp[i][j-1])` (if they don't, e.g., Longest Common Subsequence).
- **0/1 Knapsack:** `dp[i][w]` depends on `dp[i-1][w]` (exclude item) and `dp[i-1][w-weight[i]] + value[i]` (include item).

## 5. Complexity (Time & Space)
- **Time:** $O(M \times N)$ to fill the $M \times N$ matrix.
- **Space:** $O(M \times N)$ naively. Can often be optimized to $O(\min(M, N))$ by noticing that row `i` only depends on row `i-1`.

## 6. Tiny worked example
Grid Paths. 2x2 Grid. Top-left is 1.
`dp = [[1, 1], [1, 0]]` (initialized row 0 and col 0 to 1).
`dp[1][1] = dp[0][1] + dp[1][0] = 1 + 1 = 2`.
2 paths to the bottom-right.

## 7. Code (Python)
```python
# Unique Paths with Obstacles
def uniquePathsWithObstacles(obstacleGrid):
    M, N = len(obstacleGrid), len(obstacleGrid[0])
    if obstacleGrid[0][0] == 1: return 0
    
    dp = [[0]*N for _ in range(M)]
    dp[0][0] = 1
    
    for i in range(M):
        for j in range(N):
            if obstacleGrid[i][j] == 1:
                dp[i][j] = 0
                continue
            if i > 0: dp[i][j] += dp[i-1][j]
            if j > 0: dp[i][j] += dp[i][j-1]
            
    return dp[M-1][N-1]
```

## 8. Common mistakes
- **Initialization errors:** Forgetting to properly initialize the first row and first column. E.g., in a grid with an obstacle in the first row, all cells *after* the obstacle in that row must be 0, not 1.
- **Index out of bounds:** Not handling `i-1` and `j-1` for the 0th row/col. Pad the array with an extra row/col of zeros to avoid `if` statements.

## 9. 30-second interview answer
"2D DP is used when a problem's state relies on two dimensions, such as tracking two strings in Edit Distance or navigating a grid. We construct an $O(M \times N)$ table where `dp[i][j]` is calculated using adjacent cells like `dp[i-1][j]` and `dp[i][j-1]`. Space complexity can usually be optimized to $O(N)$ by only storing the previous row."

## 10. 2-minute interview answer
"2D Dynamic Programming is a vast category encompassing grid traversal, string comparison, and 0/1 knapsack problems. The core concept is that the optimal solution requires tracking two independent variables. For example, in Longest Common Subsequence, `dp[i][j]` represents the LCS of string1 up to index `i` and string2 up to index `j`. If the characters match, the state transitions from `dp[i-1][j-1]`. If not, it transitions from the max of `dp[i-1][j]` or `dp[i][j-1]`. Because we fill an $M \times N$ matrix, the time complexity is strictly $O(M \times N)$. However, a crucial realization for system design and space-constrained environments is that row `i` almost always depends *only* on row `i-1`. By keeping only two 1D arrays (the 'current' row and 'previous' row) instead of the full matrix, we reduce space complexity from $O(M \times N)$ to $O(N)$. This space optimization is a standard interview follow-up."

## 11. Follow-ups
- "Can you optimize the space to $O(N)$?" (Yes, by realizing `dp[i][j]` only needs `dp[i-1][...]`. Maintain `prev_row` and `curr_row`).

## 12. Deeper questions
- "How do you recover the actual path/string (e.g., the exact LCS)?" (You cannot space-optimize to $O(N)$. You must keep the full $M \times N$ matrix and backtrack from `dp[M][N]`, moving to the cell that provided the optimal value at each step).

## 13. Related concepts
- **1D DP**: The simpler version.
- **Backtracking**: Finding the path after the DP table is filled.

## 14. When it breaks / Edge cases
- Grids with cycles (e.g., you can move up, down, left, right). You cannot use standard 2D DP; you must use Dijkstra's or BFS because the strict topological ordering of DP is broken.

## 15. Comparison with alternative approaches
- **Top-Down (Memoization) vs Bottom-Up (Tabulation):** Top-down is easier to write for complex string problems and computes only necessary states. Bottom-up is faster (no recursion overhead) and easier to space-optimize.

---
*Where this shows up in ML:*
Dynamic Time Warping (DTW) for speech recognition and time-series alignment is exactly a 2D DP algorithm on a grid.
""")

wc("21-oop-and-lld/oop-fundamentals.md", r"""# OOP Fundamentals

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
""")

wc("21-oop-and-lld/solid-principles.md", r"""# SOLID Principles

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
""")

wc("21-oop-and-lld/design-patterns-overview.md", r"""# Design Patterns Overview

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
""")

wc("21-oop-and-lld/low-level-design-questions.md", r"""# Low-Level Design (LLD) Questions

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
""")

wc("21-oop-and-lld/common-lld-problems.md", r"""# Common LLD Problems

## 1. Definition
This covers the implementations of the most frequently asked Low-Level Design interview questions: LRU Cache, Rate Limiter, and a generic Pub/Sub (Observer) system.

## 2. Intuition
These problems test specific intersections of Object-Oriented principles and Data Structures. You must know the optimal algorithmic data structures (e.g., Hash Map + Doubly Linked List for LRU) while encapsulating them in clean, modular class structures.

## 3. LRU Cache (Least Recently Used)
**Requirement:** Get and Put in $O(1)$ time. Evict the least recently used item when capacity is reached.
**Architecture:** `HashMap` (maps key to node) + `DoublyLinkedList` (maintains recency order).
- **Read:** Look up in map. Move node to head of DLL.
- **Write:** If exists, update value and move to head. If new, add to head. If over capacity, remove tail of DLL and delete from map.

```python
class Node:
    def __init__(self, k, v):
        self.key, self.val = k, v
        self.prev = self.next = None

class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.cache = {}
        self.head, self.tail = Node(0, 0), Node(0, 0)
        self.head.next, self.tail.prev = self.tail, self.head # Dummy nodes
        
    def _remove(self, node):
        node.prev.next, node.next.prev = node.next, node.prev
        
    def _add(self, node):
        p = self.head.next
        self.head.next, node.prev = node, self.head
        node.next, p.prev = p, node
        
    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add(node)
            return node.val
        return -1
        
    def put(self, key, value):
        if key in self.cache: self._remove(self.cache[key])
        node = Node(key, value)
        self._add(node)
        self.cache[key] = node
        if len(self.cache) > self.cap:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]
```

## 4. Token Bucket Rate Limiter
**Requirement:** Allow a maximum of $N$ requests per timeframe. Allow bursts up to bucket capacity.
**Architecture:** Store `tokens` and `last_refill_time`. Upon request, refill tokens based on time elapsed, then consume one if available. Thread-safety (Locks) is critical here.

```python
import time, threading

class TokenBucket:
    def __init__(self, capacity, refill_rate_per_sec):
        self.capacity = capacity
        self.tokens = capacity
        self.refill_rate = refill_rate_per_sec
        self.last_refill = time.time()
        self.lock = threading.Lock()
        
    def allow_request(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.last_refill
            
            # Refill tokens
            new_tokens = elapsed * self.refill_rate
            self.tokens = min(self.capacity, self.tokens + new_tokens)
            self.last_refill = now
            
            if self.tokens >= 1:
                self.tokens -= 1
                return True
            return False
```

## 5. Pub/Sub (Observer Pattern)
**Requirement:** Let multiple subscribers listen to events published by a broker.
**Architecture:** `Publisher`, `Subscriber` (interface), `Topic`.

```python
class Topic:
    def __init__(self, name):
        self.name = name
        self.subscribers = []
        
    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)
        
    def publish(self, message):
        for sub in self.subscribers:
            sub.receive(self.name, message)

class Subscriber:
    def receive(self, topic_name, message):
        print(f"Received on {topic_name}: {message}")
```

## 6. Common mistakes
- **LRU Cache:** Forgetting to update the map when the tail node is evicted. You must delete `cache[lru_node.key]`, which is why the `Node` must store both `key` and `value`.
- **Rate Limiter:** Using a background thread to refill tokens every second. This is inefficient at scale. Always compute the refill lazily upon the incoming request using timestamps.
- **Not mentioning concurrency:** All three of these problems require mutex locks in production.

## 7. 30-second interview answer
"Common LLD problems merge data structures with OOP. The LRU Cache requires an O(1) combination of a Hash Map and a Doubly Linked List. The Rate Limiter is best implemented via the Token Bucket algorithm, utilizing lazy timestamp-based refills and mutex locks for thread safety. Pub/Sub systems rely entirely on the Observer design pattern to decouple publishers from subscribers."
""")

print("Batch E Part 2 complete")
