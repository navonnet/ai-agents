from dataclasses import dataclass

@dataclass
class Customer:
    id: int
    firstName: str
    lastName: str
    email: str