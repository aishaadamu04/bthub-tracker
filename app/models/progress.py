# app/models/progress.py
from dataclasses import dataclass
from datetime import datetime


# ── THE CURRICULUM DICTIONARY ──────────────────────────────
# Stored in code, not the DB. The DB only stores which level
# a child is on. This dict maps that number to what it means.

CURRICULUM_LEVELS = {
    1: {
        "week": "W1",
        "title": "Intro to Programming",
        "topics": ["What is code?", "Variables", "Print statements"],
        "pass_score": 60
    },
    2: {
        "week": "W2",
        "title": "Data Types & Input",
        "topics": ["Strings", "Integers", "User input"],
        "pass_score": 60
    },
    3: {
        "week": "W3",
        "title": "Conditionals",
        "topics": ["if/else", "Comparison operators", "Nested conditions"],
        "pass_score": 60
    },
    4: {
        "week": "W4",
        "title": "Loops",
        "topics": ["for loops", "while loops", "range()"],
        "pass_score": 60
    },
    5: {
        "week": "W5",
        "title": "Functions",
        "topics": ["Defining functions", "Parameters", "Return values"],
        "pass_score": 65
    },
    6: {
        "week": "W6",
        "title": "Lists & Dictionaries",
        "topics": ["Lists", "Dictionaries", "Looping over collections"],
        "pass_score": 65
    },
    7: {
        "week": "W7",
        "title": "Introduction to OOP",
        "topics": ["Classes", "Attributes", "Methods"],
        "pass_score": 70
    },
    8: {
        "week": "W8",
        "title": "Professional Project Setup",
        "topics": ["Project structure", "PyTest", "Documentation"],
        "pass_score": 70
    }
}


# ── PROGRESS DATACLASS ──────────────────────────────────────

@dataclass
class Progress:
    id: int
    child_id: int
    week_number: int
    lesson_title: str
    completed: bool = False
    score: int = None
    completed_at: str = None

    @staticmethod
    def from_row(row):
        return Progress(
            id=row['id'],
            child_id=row['child_id'],
            week_number=row['week_number'],
            lesson_title=row['lesson_title'],
            completed=bool(row['completed']),
            score=row['score'],
            completed_at=row['completed_at']
        )

    def get_level_info(self):
        """Returns the curriculum info for this progress entry's week."""
        return CURRICULUM_LEVELS.get(self.week_number)
    
    def get_level_info(self):
        return CURRICULUM_LEVELS.get(self.week_number)