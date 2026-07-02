"""
EduGenie - Google Gemini Powered Learning Assistant
ER Diagram Generator (Chen Notation) using Graphviz

Install dependency:
    pip install graphviz
You also need the Graphviz system package installed (provides the `dot` binary):
    - Windows : https://graphviz.org/download/  (add to PATH)
    - macOS   : brew install graphviz
    - Linux   : sudo apt-get install graphviz

Run:
    python edugenie_er_diagram.py
Output:
    EduGenie_ER_Diagram.png / .pdf in the same folder
"""

from graphviz import Digraph


def underline(text: str) -> str:
    """Return an HTML-like label with the text underlined (used for primary keys)."""
    return f"<<U>{text}</U>>"


def add_entity(graph: Digraph, name: str, attributes: list, key_attrs: list):
    """
    Add an Entity (rectangle) node plus its Attribute (ellipse) nodes,
    connecting each attribute to the entity. Primary key attributes are underlined.
    """
    graph.node(name, name.replace("_", " "), shape="rectangle",
               style="filled", fillcolor="#D6EAF8", fontname="Helvetica Bold")

    for attr in attributes:
        attr_node_id = f"{name}_{attr}"
        label = underline(attr.replace("_", " ")) if attr in key_attrs else attr.replace("_", " ")
        graph.node(attr_node_id, label, shape="ellipse",
                   style="filled", fillcolor="#FCF3CF", fontname="Helvetica")
        graph.edge(name, attr_node_id, arrowhead="none")


def add_relationship(graph: Digraph, name: str, attributes: list = None):
    """Add a Relationship (diamond) node plus optional attribute (ellipse) nodes."""
    graph.node(name, name.replace("_", " "), shape="diamond",
               style="filled", fillcolor="#D5F5E3", fontname="Helvetica Bold")

    if attributes:
        for attr in attributes:
            attr_node_id = f"{name}_{attr}"
            graph.node(attr_node_id, attr.replace("_", " "), shape="ellipse",
                       style="filled", fillcolor="#FCF3CF", fontname="Helvetica")
            graph.edge(name, attr_node_id, arrowhead="none")


def connect(graph: Digraph, entity: str, relationship: str, cardinality: str):
    """Connect an Entity to a Relationship and label the edge with its cardinality."""
    graph.edge(entity, relationship, label=cardinality, fontname="Helvetica", fontsize="11")


def build_edugenie_er_diagram() -> Digraph:
    er = Digraph("EduGenie_ER_Diagram", format="png")
    er.attr(rankdir="TB", splines="line", nodesep="0.6", ranksep="0.9",
            fontname="Helvetica", label="EduGenie - Gemini Powered Learning Assistant\nEntity Relationship Diagram",
            labelloc="t", fontsize="20")
    er.attr("node", fontname="Helvetica")
    er.attr("edge", fontname="Helvetica")

    # ---------------------------------------------------------------
    # ENTITIES + ATTRIBUTES
    # ---------------------------------------------------------------
    add_entity(er, "USER",
               ["UserID", "Name", "Email", "Password", "Role", "JoinDate"],
               key_attrs=["UserID"])

    add_entity(er, "COURSE",
               ["CourseID", "Title", "Subject", "Level", "Description"],
               key_attrs=["CourseID"])

    add_entity(er, "LESSON",
               ["LessonID", "Title", "Content", "SequenceNo"],
               key_attrs=["LessonID"])

    add_entity(er, "CHAT_SESSION",
               ["SessionID", "StartTime", "EndTime", "Topic"],
               key_attrs=["SessionID"])

    add_entity(er, "GEMINI_QUERY",
               ["QueryID", "QueryText", "ResponseText", "Timestamp"],
               key_attrs=["QueryID"])

    add_entity(er, "QUIZ",
               ["QuizID", "Title", "TotalMarks", "DueDate"],
               key_attrs=["QuizID"])

    add_entity(er, "QUESTION",
               ["QuestionID", "QuestionText", "CorrectAnswer", "Marks"],
               key_attrs=["QuestionID"])

    add_entity(er, "FEEDBACK",
               ["FeedbackID", "Content", "Rating", "SubmittedDate"],
               key_attrs=["FeedbackID"])

    # ---------------------------------------------------------------
    # RELATIONSHIPS (with their own attributes where relevant)
    # ---------------------------------------------------------------
    add_relationship(er, "ENROLLS_IN", ["EnrollDate", "Status"])
    add_relationship(er, "CONTAINS")
    add_relationship(er, "INITIATES")
    add_relationship(er, "INCLUDES")
    add_relationship(er, "HAS_QUIZ")
    add_relationship(er, "CONSISTS_OF")
    add_relationship(er, "ATTEMPTS", ["Score", "AttemptDate"])
    add_relationship(er, "HAS_PROGRESS_IN", ["CompletionPercent", "LastAccessed"])
    add_relationship(er, "SUBMITS")

    # ---------------------------------------------------------------
    # ENTITY <-> RELATIONSHIP CONNECTIONS (with cardinalities)
    # ---------------------------------------------------------------
    connect(er, "USER", "ENROLLS_IN", "M")
    connect(er, "ENROLLS_IN", "COURSE", "N")

    connect(er, "COURSE", "CONTAINS", "1")
    connect(er, "CONTAINS", "LESSON", "N")

    connect(er, "USER", "INITIATES", "1")
    connect(er, "INITIATES", "CHAT_SESSION", "N")

    connect(er, "CHAT_SESSION", "INCLUDES", "1")
    connect(er, "INCLUDES", "GEMINI_QUERY", "N")

    connect(er, "LESSON", "HAS_QUIZ", "1")
    connect(er, "HAS_QUIZ", "QUIZ", "1")

    connect(er, "QUIZ", "CONSISTS_OF", "1")
    connect(er, "CONSISTS_OF", "QUESTION", "N")

    connect(er, "USER", "ATTEMPTS", "M")
    connect(er, "ATTEMPTS", "QUIZ", "N")

    connect(er, "USER", "HAS_PROGRESS_IN", "1")
    connect(er, "HAS_PROGRESS_IN", "COURSE", "N")

    connect(er, "USER", "SUBMITS", "1")
    connect(er, "SUBMITS", "FEEDBACK", "N")

    return er


if __name__ == "__main__":
    diagram = build_edugenie_er_diagram()
    output_path = diagram.render("EduGenie_ER_Diagram", cleanup=True)
    print(f"ER diagram generated: {output_path}")