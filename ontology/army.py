from dataclasses import dataclass

@dataclass
class Army:
    name: str
    strength: float
    energy: float
    morale: float
    resources: float
    intelligence: float
    momentum: float
    
    def overall(self) -> float:
        return round(
            self.strength * 0.35 + (self.energy / 10) * 0.25 +
            self.morale * 0.2 + (self.resources / 10) * 0.1 +
            self.intelligence * 0.1, 1
        )