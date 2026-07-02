# test_functional.py
"""
Simple functional test script for EduGenie Learning Assistant.
Make sure the server is running first:
    uvicorn main:app --reload

Then run this script in another terminal:
    python test_functional.py
"""

import requests

BASE_URL = "http://127.0.0.1:8000"

def test_ask_question():
    print("\n--- Testing: Ask a Question ---")
    payload = {"student_name": "Asha", "question": "What is photosynthesis?"}
    res = requests.post(f"{BASE_URL}/ask", json=payload)
    print(res.json())

def test_explanation():
    print("\n--- Testing: Get an Explanation ---")
    payload = {"topic": "Machine Learning", "level": "beginner"}
    res = requests.post(f"{BASE_URL}/explain", json=payload)
    print(res.json())

def test_summarization():
    print("\n--- Testing: Summarize Content ---")
    payload = {
        "content": ("Machine learning is a subset of artificial intelligence. "
                     "It enables systems to learn from data without explicit programming. "
                     "It is widely used in recommendation systems, fraud detection, and more.")
    }
    res = requests.post(f"{BASE_URL}/summarize", json=payload)
    print(res.json())

def test_quiz_generation_and_check():
    print("\n--- Testing: Generate a Quiz ---")
    payload = {"topic": "Python Programming"}
    res = requests.post(f"{BASE_URL}/quiz/generate", json=payload)
    quiz_data = res.json()
    print(quiz_data)

    # Test answer checking using the first question
    first_q = quiz_data["questions"][0]
    print("\n--- Testing: Quiz Answer Check (Incorrect choice) ---")
    wrong_choice = next(opt for opt in first_q["options"] if opt != first_q["correct_answer"])
    check_payload = {
        "topic": "Python Programming",
        "question": first_q["question"],
        "selected_option": wrong_choice,
        "correct_answer": first_q["correct_answer"]
    }
    check_res = requests.post(f"{BASE_URL}/quiz/check", json=check_payload)
    print(check_res.json())

    print("\n--- Testing: Quiz Answer Check (Correct choice) ---")
    check_payload["selected_option"] = first_q["correct_answer"]
    check_res = requests.post(f"{BASE_URL}/quiz/check", json=check_payload)
    print(check_res.json())

def test_learning_plan():
    print("\n--- Testing: Personalized Learning Plan ---")
    payload = {"topic": "Data Science", "current_level": "beginner"}
    res = requests.post(f"{BASE_URL}/learning-plan", json=payload)
    print(res.json())


if __name__ == "__main__":
    test_ask_question()
    test_explanation()
    test_summarization()
    test_quiz_generation_and_check()
    test_learning_plan()