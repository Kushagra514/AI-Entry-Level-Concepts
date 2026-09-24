# Low-Level Design (LLD) Interview Questions

## 1. What Interviewers Look For
- Identify entities and their relationships
- Apply OOP + SOLID principles
- Handle edge cases and concurrency
- Extensible, clean class design

## 2. General Approach (5 Steps)
1. Clarify requirements & constraints
2. Identify core entities (nouns → classes)
3. Define relationships (has-a, is-a)
4. Define methods and interactions
5. Handle edge cases, threading, storage

## 3. Parking Lot — Entities
```
ParkingLot (floors, entry/exit points)
ParkingFloor (spots[])
ParkingSpot (type: compact/large/handicapped, isOccupied)
Vehicle (licensePlate, type)
Ticket (entryTime, spot)
ParkingAttendant
```

## 4. Parking Lot — Key Methods
```python
class ParkingLot:
    def park(self, vehicle) -> Ticket: ...
    def unpark(self, ticket) -> float: ...  # return fee
    def find_spot(self, vehicle_type) -> ParkingSpot: ...
```

## 5. Library System — Entities
```
Library, Book (ISBN, copies), BookItem (physical copy), Member, Librarian
BookReservation, BookLending, Fine
Catalog (search by title/author/subject)
```

## 6. Library System — Key Interactions
- Member searches catalog → reserves book → librarian checks out → return → fine calculation.

## 7. Elevator System — Entities
```
ElevatorSystem, Elevator (currentFloor, state, direction)
ElevatorButton, HallButton (floor, direction)
ElevatorPanel (buttons inside elevator)
Request (floor, direction)
Dispatcher (scheduling algorithm: SCAN/LOOK)
```

## 8. Hotel Booking System — Entities
Room, RoomType, Booking, Guest, Hotel, Payment, Invoice.
Key: room availability check with date ranges.

## 9. Chess Game — Entities
Board (8×8), Piece (subclasses: King, Queen, Rook, Bishop, Knight, Pawn),
Player, Move, GameController.
```python
class Piece(ABC):
    @abstractmethod
    def get_valid_moves(self, board) -> list[Move]: ...
```

## 10. ATM — Entities
ATM, Card, Account, Transaction, CashDispenser, ReceiptPrinter,
Keypad, Screen, BankServer.
State machine: idle → card inserted → pin entered → transaction → eject.

## 11. Class Diagram Tips
- Use UML notation: `+` public, `-` private, `#` protected
- Arrows: inheritance (△), composition (◆), aggregation (◇), association (→)
- Show multiplicities: 1..*, 0..1

## 12. Handling Concurrency
- Parking Lot: lock spot before assigning to avoid double booking.
- Use optimistic locking (version field) for DB-backed designs.
- Python: `threading.Lock()` or database transactions.

## 13. Extensibility Hooks
- Use Strategy pattern for variable parts (pricing strategy, scheduling algorithm).
- Use Factory for object creation (VehicleFactory, SpotFactory).

## 14. Common Interview Mistakes
- Jumping to code without clarifying requirements.
- Missing edge cases: vehicle type mismatch, full lot, expired reservation.
- Making everything static/global.

## 15. Practice Problems Ranked by Frequency
1. Parking Lot ★★★★★
2. LRU Cache ★★★★★
3. Library System ★★★★
4. Elevator ★★★★
5. Chess/Snake&Ladder ★★★
6. ATM ★★★
7. Hotel Booking ★★★
