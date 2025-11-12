from dataclasses import dataclass, field
from typing import Dict, Tuple

from helpers.builder import BuilderMixin


@dataclass
class CityBuilder(BuilderMixin):
    """Sample city for tests. Use `.with_«attribute»` to modify its
    attributes."""

    name: str = "Rio de Janeiro"
    ibge_code: str = 3304557
    latitude: float = -22.902778
    longitude: float = -43.207778


@dataclass
class CoordinatesBuilder(BuilderMixin):
    """Sample coordinates for tests. Use `.with_«attribute»` to modify its
    attributes."""

    latitude: float = 0.0
    longitude: float = 0.0
    geohash: str = "7zzzzzzzzzzz"

    @property
    def coords(self) -> Tuple[float, float]:
        return self.latitude, self.longitude


@dataclass
class InvalidOtherContactsBuilder(BuilderMixin):
    """Sample lists of invalid other contacts for tests."""

    facebook: str = "pixinguinha.2"
    github: str = "pixinguinha_coder"


@dataclass
class NeighborhoodBuilder(BuilderMixin):
    """Sample neighborhood for tests. Use `.with_«attribute»` to modify its
    attributes."""

    name: str = "Olaria"
    latitude: float = -22.8466
    longitude: float = -43.2733


@dataclass
class PersonBuilder(BuilderMixin):
    """Sample person for tests. Use `.with_«attribute»` to modify its
    attributes."""

    name: str = "Alfredo da Rocha Vianna Filho"
    nickname: str = "Pixinguinha"
    mobile_phone: str = "1" * 16
    email_address: str = "pizindim@example.com"
    other_contacts: Dict[str, str] = field(default_factory=dict)
    contribution: str = "Ah, se tu soubesses como eu sou tão carinhoso."


@dataclass
class SectionBuilder(BuilderMixin):
    """Sample voter zone for tests. Use `.with_«attribute»` to modify its
    attributes."""

    number: int = 364


@dataclass
class StateBuilder(BuilderMixin):
    """Sample state for tests. Use `.with_«attribute»` to modify its
    attributes."""

    name: str = "Rio de Janeiro"
    short: str = "RJ"
    ibge_code: str = 33
    latitude: float = -22.9
    longitude: float = -43.2


@dataclass
class TerritoryBuilder(BuilderMixin):
    """Sample territory for tests. Use `.with_«attribute»` to modify its
    attributes."""

    name: str = "Escola Municipal Chile"
    description: str = ""
    category: str = "E"


@dataclass
class ValidOtherContactsBuilder(BuilderMixin):
    """Sample lists of valid other contacts for tests."""

    facebook: str = "pixinguinha.2"
    instagram: str = "pixin"


@dataclass
class ZoneBuilder(BuilderMixin):
    """Sample voter zone for tests. Use `.with_«attribute»` to modify its
    attributes."""

    number: int = 21
    zone_name: str = "Olaria"
