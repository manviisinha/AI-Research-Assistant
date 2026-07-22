"""Generate a PNG visualization of the LangGraph researcher workflow."""
import sys
sys.path.insert(0, ".")

from src.assistant.graph import researcher

# Generate PNG using Mermaid.ink API (no Docker needed)
graph = researcher.get_graph(xray=True)

try:
    # draw_mermaid_png() uses the mermaid.ink API to render
    png_data = graph.draw_mermaid_png()
    
    output_path = "agent_workflow.png"
    with open(output_path, "wb") as f:
        f.write(png_data)
    
    print(f"Saved workflow diagram to: {output_path}")
    
except Exception as e:
    print(f"Mermaid PNG failed: {e}")
    print("\nFalling back to ASCII representation...\n")
    print(graph.draw_mermaid())
