from dataclasses import dataclass


@dataclass
class ResourceAmount:
    wood: int = 0
    clay: int = 0
    iron: int = 0
