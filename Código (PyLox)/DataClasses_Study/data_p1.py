# Dataclasses
import random
import string
from dataclasses import dataclass, field

def generate_id() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=12))

@dataclass(slots=True)
class Person:
    name: str
    address: str
    active: bool = True
    email_addresses: list[str] = field(default_factory=list)
    id: str = field(default_factory=generate_id)
    _search_string: str = field(init=False)

    def __post_init__(self) -> None:
        self._search_string = f"{self.name}{self.address}"

def main() -> None:
    person = Person(name="Jhon", address="123 Main St")
    person.name = "Arjan"
    print(person)


if __name__ == "__main__":
    main()


        
