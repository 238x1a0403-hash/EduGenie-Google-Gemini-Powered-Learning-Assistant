"""
EduGenie - Google Gemini Powered Learning Assistant
"SELECT AI MODELS" ACTIVITY DIAGRAM Generator using Graphviz

Depicts:
  1. The two AI models chosen (Google Gemini 1.5 Pro - cloud, and
     LaMini-Flan-T5-783M - local lightweight) and which functionality
     each one powers.
  2. The modular project architecture: Frontend, Backend (FastAPI),
     individual feature modules, AI model layer, and dependency file.

Install dependency:
    pip install graphviz
You also need the Graphviz system package installed (provides the `dot` binary):
    - Windows : https://graphviz.org/download/  (add to PATH)
    - macOS   : brew install graphviz
    - Linux   : sudo apt-get install graphviz

Run:
    python edugenie_ai_model_architecture.py
Output:
    EduGenie_AI_Model_Architecture.png / .pdf in the same folder
"""

from graphviz import Digraph


STYLES = {
    "frontend":  dict(shape="box", style="filled,rounded", fillcolor="#D6EAF8",
                       fontname="Helvetica"),
    "backend":   dict(shape="box", style="filled,rounded", fillcolor="#AED6F1",
                       fontname="Helvetica Bold"),
    "module":    dict(shape="box", style="filled,rounded", fillcolor="#D1F2EB",
                       fontname="Helvetica"),
    "cloud_ai":  dict(shape="box3d", style="filled", fillcolor="#F9E79F",
                       fontname="Helvetica Bold", color="#B7950B", penwidth="2"),
    "local_ai":  dict(shape="box3d", style="filled", fillcolor="#F5CBA7",
                       fontname="Helvetica Bold", color="#A04000", penwidth="2"),
    "deps":      dict(shape="note", style="filled", fillcolor="#EBDEF0",
                       fontname="Helvetica"),
}


def node(graph: Digraph, name: str, label: str, kind: str):
    graph.node(name, label, **STYLES[kind])


def build_architecture_diagram() -> Digraph:
    g = Digraph("EduGenie_AI_Model_Architecture", format="png")
    g.attr(rankdir="TB", splines="spline", nodesep="0.55", ranksep="0.75",
           fontname="Helvetica",
           label="EduGenie - AI Model Selection & Modular Architecture",
           labelloc="t", fontsize="20")
    g.attr("node", fontname="Helvetica")
    g.attr("edge", fontname="Helvetica", fontsize="10")

    # -----------------------------------------------------------------
    # FRONTEND LAYER
    # -----------------------------------------------------------------
    with g.subgraph(name="cluster_frontend") as c:
        c.attr(label="Frontend (templates / static)", style="rounded,filled",
               fillcolor="#EBF5FB", fontname="Helvetica Bold")
        node(c, "index_html", "templates/\nindex.html", "frontend")
        node(c, "style_css", "static/\nstyle.css", "frontend")

    # -----------------------------------------------------------------
    # BACKEND LAYER (FastAPI app + feature modules)
    # -----------------------------------------------------------------
    with g.subgraph(name="cluster_backend") as c:
        c.attr(label="Backend - FastAPI Application", style="rounded,filled",
               fillcolor="#EAF2F8", fontname="Helvetica Bold")
        node(c, "main_py", "main.py\n(Central FastAPI App /\nRouting & Integration)", "backend")
        node(c, "qna_py", "qna.py\n(Question Answering)", "module")
        node(c, "summary_py", "summary_module.py\n(Summarization)", "module")
        node(c, "quiz_py", "quiz_module.py\n(Quiz Generation)", "module")
        node(c, "learning_path_py", "learning_path.py\n(Personalized Learning\nRecommendations)", "module")
        node(c, "explanation_py", "explanation_module.py\n(Concept Explanation)", "module")

    # -----------------------------------------------------------------
    # AI MODEL LAYER
    # -----------------------------------------------------------------
    with g.subgraph(name="cluster_ai") as c:
        c.attr(label="AI Model Layer", style="rounded,filled",
               fillcolor="#FEF9E7", fontname="Helvetica Bold")
        node(c, "gemini", "Google Gemini 1.5 Pro\n(Cloud API)\nReasoning, Context Understanding,\nStructured Response Generation",
             "cloud_ai")
        node(c, "lamini", "LaMini-Flan-T5-783M\n(Local Lightweight Model)\nInstruction-Tuned, CPU-Compatible",
             "local_ai")

    # -----------------------------------------------------------------
    # DEPENDENCY MANAGEMENT
    # -----------------------------------------------------------------
    node(g, "requirements_txt", "requirements.txt\n(Python Dependencies)", "deps")

    # -----------------------------------------------------------------
    # FRONTEND <-> BACKEND
    # -----------------------------------------------------------------
    g.edge("index_html", "main_py", label="HTTP Request /\nUser Interaction")
    g.edge("main_py", "index_html", label="Rendered Response")
    g.edge("style_css", "index_html", label="styles", style="dashed", dir="none")

    # -----------------------------------------------------------------
    # BACKEND ROUTING -> FEATURE MODULES
    # -----------------------------------------------------------------
    for module in ["qna_py", "summary_py", "quiz_py", "learning_path_py", "explanation_py"]:
        g.edge("main_py", module, label="routes to")

    # -----------------------------------------------------------------
    # FEATURE MODULES -> AI MODELS
    # -----------------------------------------------------------------
    g.edge("qna_py", "gemini", color="#B7950B")
    g.edge("summary_py", "gemini", color="#B7950B")
    g.edge("quiz_py", "gemini", color="#B7950B")
    g.edge("learning_path_py", "gemini", color="#B7950B")
    g.edge("explanation_py", "lamini", color="#A04000")

    # -----------------------------------------------------------------
    # DEPENDENCY MANAGEMENT -> SUPPORTS BACKEND + AI LAYER
    # -----------------------------------------------------------------
    g.edge("requirements_txt", "main_py", style="dashed", label="installs deps for", dir="none")
    g.edge("requirements_txt", "lamini", style="dashed", dir="none")

    return g


if __name__ == "__main__":
    diagram = build_architecture_diagram()
    output_path = diagram.render("EduGenie_AI_Model_Architecture", cleanup=True)
    print(f"Architecture diagram generated: {output_path}")