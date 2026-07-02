"""
learning_path.py
-----------------
EduGenie - Personalized Learning Recommendations Module

Uses Google Gemini 1.5 Pro to generate a personalized, structured learning
path for any given topic. The model is instructed to suggest concepts from
beginner to advanced, organized by difficulty, and supported with useful
resource types (videos, articles, books), adapted to the learner's level.

Install:
    pip install google-generativeai

Setup:
    export GEMINI_API_KEY="your_api_key_here"
"""

import os

import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-1.5-pro"

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

_model = genai.GenerativeModel(MODEL_NAME)


def _build_prompt(topic: str, level: str) -> str:
    return f"""Create a personalized, structured learning path for the topic: "{topic}".

Instructions:
- Organize the path from beginner to advanced concepts, in logical order.
- Group concepts under clear headings: Beginner, Intermediate, and Advanced.
- For each concept, briefly explain why it matters and what to focus on.
- Recommend useful resource types for each stage (e.g. videos, articles,
  books, practice exercises) without inventing fake links or titles.
- Adapt the depth, pacing, and starting point of the path to a learner who
  is currently at the "{level}" level.
- Present the result in a clear, well-structured format using headings and
  bullet points so it is easy to scan.
"""


def get_learning_recommendations(topic: str, level: str = "beginner") -> str:
    """
    Generate a personalized, structured learning path for a topic using
    Gemini 1.5 Pro.

    Args:
        topic: The subject/topic the learner wants a learning path for.
        level: The learner's current level (e.g. "beginner", "intermediate",
            "advanced"). Defaults to "beginner".

    Returns:
        The generated learning path as formatted text, or a descriptive
        error message if the request fails or the response is invalid.
    """
    if not topic or not topic.strip():
        return "Please provide a valid topic to generate a learning path."

    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY is not set. Please configure your API key."

    prompt = _build_prompt(topic.strip(), level.strip() if level else "beginner")

    try:
        response = _model.generate_content(prompt)
        if response and getattr(response, "text", None):
            return response.text.strip()
        return "Sorry, a learning path could not be generated for this topic."
    except Exception as e:
        return f"Error while generating learning recommendations: {str(e)}"


if __name__ == "__main__":
    sample_topic = "Machine Learning"
    print(f"Topic: {sample_topic}\n")
    print(get_learning_recommendations(sample_topic, level="beginner"))