# run_worker.py

from executor_agent import ExecutorAgent
from tool_registry import ToolRegistry
from worker_agent import WorkerAgent
from message_bus import MessageBus
from tools import write_file, think
from web_tools import web_search
from llm import antigravity_llm

bus = MessageBus()

tool_registry = ToolRegistry()
tool_registry.register("think", "Internal reasoning", think)
tool_registry.register("write_file", "Write content to file", write_file)
tool_registry.register("web_search", "Search the web", web_search)

executor = ExecutorAgent(
    llm=antigravity_llm,
    tool_registry=tool_registry,
    memory=None
)

worker = WorkerAgent(
    name="worker-1",
    executor=executor,
    bus=bus
)

worker.loop()
