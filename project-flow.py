"""
EduGenie - Google Gemini Powered Learning Assistant
PROJECT FLOW DIAGRAM Generator using Graphviz

Install dependency:
    pip install graphviz
You also need the Graphviz system package installed (provides the `dot` binary):
    - Windows : https://graphviz.org/download/  (add to PATH)
    - macOS   : brew install graphviz
    - Linux   : sudo apt-get install graphviz

Run:
    python edugenie_flow_diagram.py
Output:
    EduGenie_Flow_Diagram.png / .pdf in the same folder
"""

from graphviz import Digraph


# ---------------------------------------------------------------------------
# Style helpers — keep node shapes consistent with standard flowchart symbols
# ---------------------------------------------------------------------------
STYLES = {
    "terminator": dict(shape="ellipse", style="filled", fillcolor="#2E86C1",
                        fontcolor="white", fontname="Helvetica Bold"),
    "process":    dict(shape="box", style="filled,rounded", fillcolor="#D6EAF8",
                        fontname="Helvetica"),
    "decision":   dict(shape="diamond", style="filled", fillcolor="#FCF3CF",
                        fontname="Helvetica Bold"),
    "io":         dict(shape="parallelogram", style="filled", fillcolor="#D5F5E3",
                        fontname="Helvetica"),
    "gemini":     dict(shape="box", style="filled,rounded", fillcolor="#F9E79F",
                        fontname="Helvetica Bold", color="#B7950B", penwidth="2"),
    "datastore":  dict(shape="cylinder", style="filled", fillcolor="#EBDEF0",
                        fontname="Helvetica"),
}


def node(graph: Digraph, name: str, label: str, kind: str):
    graph.node(name, label, **STYLES[kind])


def build_edugenie_flow_diagram() -> Digraph:
    flow = Digraph("EduGenie_Flow_Diagram", format="png")
    flow.attr(rankdir="TB", splines="spline", nodesep="0.5", ranksep="0.7",
              fontname="Helvetica",
              label="EduGenie - Gemini Powered Learning Assistant\nProject / System Flow",
              labelloc="t", fontsize="20")
    flow.attr("node", fontname="Helvetica")
    flow.attr("edge", fontname="Helvetica", fontsize="10")

    # -----------------------------------------------------------------
    # START
    # -----------------------------------------------------------------
    node(flow, "start", "Start", "terminator")
    node(flow, "auth", "User Login / Sign Up", "process")
    node(flow, "auth_check", "Credentials\nValid?", "decision")
    node(flow, "auth_fail", "Show Error &\nRetry", "process")
    node(flow, "dashboard", "User Dashboard", "process")

    flow.edge("start", "auth")
    flow.edge("auth", "auth_check")
    flow.edge("auth_check", "auth_fail", label="No")
    flow.edge("auth_fail", "auth")
    flow.edge("auth_check", "dashboard", label="Yes")

    # -----------------------------------------------------------------
    # MAIN MENU CHOICE
    # -----------------------------------------------------------------
    node(flow, "menu", "Choose Activity", "decision")
    flow.edge("dashboard", "menu")

    # -----------------------------------------------------------------
    # BRANCH 1: BROWSE COURSES / LESSONS
    # -----------------------------------------------------------------
    node(flow, "browse_course", "Browse Courses\n& Lessons", "process")
    node(flow, "select_lesson", "Select / View\nLesson Content", "process")
    node(flow, "mark_complete", "Mark Lesson\nCompleted", "process")
    node(flow, "update_progress_1", "Update Progress\nTracker", "datastore")

    flow.edge("menu", "browse_course", label="Learn a Course")
    flow.edge("browse_course", "select_lesson")
    flow.edge("select_lesson", "mark_complete")
    flow.edge("mark_complete", "update_progress_1")
    flow.edge("update_progress_1", "menu")

    # -----------------------------------------------------------------
    # BRANCH 2: ASK GEMINI (AI DOUBT-SOLVING CHAT)
    # -----------------------------------------------------------------
    node(flow, "ask_query", "Type Question /\nDoubt in Chat", "io")
    node(flow, "send_gemini", "Send Prompt to\nGoogle Gemini API", "process")
    node(flow, "gemini_process", "Gemini Generates\nContextual Answer", "gemini")
    node(flow, "display_answer", "Display Answer\nto Student", "process")
    node(flow, "save_chat", "Save Q&A to\nChat History", "datastore")

    flow.edge("menu", "ask_query", label="Ask Doubt")
    flow.edge("ask_query", "send_gemini")
    flow.edge("send_gemini", "gemini_process")
    flow.edge("gemini_process", "display_answer")
    flow.edge("display_answer", "save_chat")
    flow.edge("save_chat", "menu")

    # -----------------------------------------------------------------
    # BRANCH 3: TAKE A QUIZ / ASSESSMENT (Gemini can auto-generate quiz)
    # -----------------------------------------------------------------
    node(flow, "select_quiz", "Select Topic for\nQuiz / Practice Test", "process")
    node(flow, "gen_quiz", "Gemini Generates\nQuiz Questions", "gemini")
    node(flow, "attempt_quiz", "Student Attempts\nQuiz", "process")
    node(flow, "submit_quiz", "Submit Answers", "io")
    node(flow, "evaluate", "Gemini Evaluates &\nScores Answers", "gemini")
    node(flow, "store_result", "Store Result &\nUpdate Progress", "datastore")
    node(flow, "show_result", "Show Score +\nAI Explanation", "process")

    flow.edge("menu", "select_quiz", label="Take Quiz")
    flow.edge("select_quiz", "gen_quiz")
    flow.edge("gen_quiz", "attempt_quiz")
    flow.edge("attempt_quiz", "submit_quiz")
    flow.edge("submit_quiz", "evaluate")
    flow.edge("evaluate", "store_result")
    flow.edge("store_result", "show_result")
    flow.edge("show_result", "menu")

    # -----------------------------------------------------------------
    # BRANCH 4: VIEW PROGRESS / ANALYTICS
    # -----------------------------------------------------------------
    node(flow, "view_progress", "View Progress\nDashboard & Analytics", "process")
    flow.edge("menu", "view_progress", label="Check Progress")
    flow.edge("view_progress", "menu")

    # -----------------------------------------------------------------
    # BRANCH 5: GIVE FEEDBACK
    # -----------------------------------------------------------------
    node(flow, "give_feedback", "Submit Feedback /\nRating", "io")
    node(flow, "save_feedback", "Store Feedback", "datastore")
    flow.edge("menu", "give_feedback", label="Give Feedback")
    flow.edge("give_feedback", "save_feedback")
    flow.edge("save_feedback", "menu")

    # -----------------------------------------------------------------
    # LOGOUT / END
    # -----------------------------------------------------------------
    node(flow, "logout", "Logout", "process")
    node(flow, "end", "End", "terminator")
    flow.edge("menu", "logout", label="Exit")
    flow.edge("logout", "end")

    return flow


if __name__ == "__main__":
    diagram = build_edugenie_flow_diagram()
    output_path = diagram.render("EduGenie_Flow_Diagram", cleanup=True)
    print(f"Flow diagram generated: {output_path}")