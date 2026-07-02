from .db import get_db, query_db, execute_db
from flask import current_app

QUIZ_QUESTIONS = [
    # Week 1 - Intro to Programming
    (1, "What is code?", "Instructions for a computer", "A type of food", "A video game", "A website", "a"),
    (1, "Which symbol usually ends a print statement in Python?", "; ", ")", "!", ":", "b"),


    # Week 2 - Data Types & Input
    (2, "Which of these is a whole number type?", "String", "Integer", "Boolean", "List", "b"),
    (2, "What function gets text input from a user in Python?", "input()", "get()", "read()", "ask()", "a"),


    # Week 3 - Conditionals
    (3, "Which keyword checks a condition in Python?", "loop", "if", "func", "class", "b"),
    (3, "What does '==' check?", "Assignment", "Equality", "Greater than", "Not equal", "b"),


    # Week 4 - Loops
    (4, "Which loop repeats a set number of times easily?", "if loop", "for loop", "print loop", "def loop", "b"),
    (4, "What does range(3) produce?", "0,1,2", "1,2,3", "0,1,2,3", "3", "a"),


    # Week 5 - Functions
    (5, "What keyword defines a function in Python?", "func", "def", "function", "method", "b"),
    (5, "What do we call information passed into a function?", "Outputs", "Variables", "Parameters", "Returns", "c"),


    # Week 6 - Lists & Dictionaries
    (6, "Which symbol creates a list in Python?", "{}", "()", "[]", "<>", "c"),
    (6, "How do you access a dictionary value by its key?", "dict[key]", "dict(key)", "dict.key()", "dict->key", "a"),


    # Week 7 - Intro to OOP
    (7, "What is a blueprint for creating objects called?", "Function", "Class", "Loop", "Module", "b"),
    (7, "What do we call variables that belong to an object?", "Methods", "Functions", "Attributes", "Parameters", "c"),


    # Week 8 - Professional Project Setup
    (8, "What tool is used to run automated tests in Python?", "PyTest", "PyRun", "TestPy", "AutoTest", "a"),
    (8, "Why is documentation important in a project?", "It makes code run faster", "It helps others understand the code", "It's required by Python", "It fixes bugs automatically", "b"),
]

def seed_quiz_questions(app):
    with app.app_context():
        count = query_db("SELECT COUNT(*) as c FROM quiz_questions", one=True)
        if count and count['c'] > 0:
            return  

        for week, question, a, b, c, d, correct in QUIZ_QUESTIONS:
            execute_db(
                """INSERT INTO quiz_questions
                   (week_number, question, option_a, option_b, option_c, option_d, correct_option)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                [week, question, a, b, c, d, correct]
            )