import gradio as gr
from query import ask


def handle_query(question):
    """
    Gradio handler for user questions.
    """
    if not question or not question.strip():
        return "Please enter a question.", ""

    try:
        result = ask(question)

        answer = result["answer"]

        sources = "\n".join(f"• {source}" for source in result["sources"])

        debug_chunks = "\n\n".join(
            [
                f"Source: {chunk['source']} | Chunk: {chunk['chunk_index']} | Distance: {chunk['distance']:.4f}\n"
                f"{chunk['text']}"
                for chunk in result["retrieved_chunks"]
            ]
        )

        return answer, sources, debug_chunks

    except Exception as error:
        return f"Error: {error}", "", ""


with gr.Blocks(title="The Unofficial UIUC CS Guide") as demo:
    gr.Markdown("# The Unofficial UIUC CS Guide")
    gr.Markdown(
        "Ask questions about UIUC CS courses, professors, workload, difficulty, and student advice. "
        "Answers are generated only from the collected Reddit and Rate My Professors documents."
    )

    question = gr.Textbox(
        label="Your question",
        placeholder="Example: What do students say about CS 374 difficulty?",
        lines=2,
    )

    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=5)
    retrieved_chunks = gr.Textbox(label="Retrieved chunks for debugging", lines=12)

    ask_button.click(
        handle_query,
        inputs=question,
        outputs=[answer, sources, retrieved_chunks],
    )

    question.submit(
        handle_query,
        inputs=question,
        outputs=[answer, sources, retrieved_chunks],
    )


if __name__ == "__main__":
    demo.launch()
    