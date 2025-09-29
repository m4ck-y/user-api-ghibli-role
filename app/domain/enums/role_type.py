from enum import Enum


class RoleType(str, Enum):
    ADMIN = "admin"
    FILMS = "films"
    PEOPLE = "people"
    LOCATIONS = "locations"
    SPECIES = "species"
    VEHICLES = "vehicles"