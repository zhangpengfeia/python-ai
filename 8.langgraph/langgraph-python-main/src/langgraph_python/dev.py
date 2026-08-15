from langgraph_python.graphs import core_agent_graph
from langgraph_python.graphs.demo import (
    demo_branch_graph,
    demo_loop_graph,
    demo_parallel_graph,
)

agent = core_agent_graph.build_graph().compile()
parallel_graph = demo_parallel_graph.build_graph().compile()
branch_graph = demo_branch_graph.build_graph().compile()
loop_graph = demo_loop_graph.build_graph().compile()
