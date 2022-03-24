from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Individual:
    name: str
    background: str
    profession: str
    gender: str
    age: str
    language: List[str]
    preferred_learning_style: List[str]

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(self.background) ^ hash(self.profession) ^ hash(self.gender) ^ hash(self.age)


@dataclass
class Course:
    name: str
    topic: str
    available_languages: List[str]
    appealing_learning_styles: List[str]
    course_rates: Dict[Individual, float] = field(default_factory=dict)

    def __hash__(self) -> int:
        return hash(self.name) ^ hash(self.topic)


@dataclass
class Provider:
    name: str
    available_courses: List[Course]
    past_participants: Dict[Course, List[Individual]]
