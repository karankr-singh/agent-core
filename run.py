# run.py

from planner_agent import PlannerAgent
from executor_agent import ExecutorAgent
from critic import Critic
from evaluator import Evaluator
from rollback_manager import RollbackManager
from voter import Voter
from reputation import Reputation
from meta_goals import MetaGoals
from alignment import Alignment
from freeze import Freeze
from memory import Memory
from long_term_memory import LongTermMemory
from vector_memory import VectorMemory
from scheduler import Scheduler
from tool_registry import ToolRegistry
from code_sandbox import CodeSandbox
from message_bus import MessageBus
from tools import write_file, think
from web_tools import web_search
from llm import antigravity_llm, antigravity_embed
from loop import agent_loop

memory = Memory()
ltm = LongTermMemory()
vector_memory = VectorMemory(embed_fn=antigravity_embed)
bus = MessageBus()
reputation = Reputation()
alignment = Alignment()
meta_goals = MetaGoals(llm=antigravity_llm)

# 🔒 FREEZE MODE ON
freeze = Freeze(enabled=True)

planner_a = PlannerAgent(
    llm=antigravity_llm,
    memory=memory,
    long_term_memory=ltm,
    vector_memory=vector_memory,
    reputation=reputation,
    alignment=alignment,
    freeze=freeze,
    bus=bus,
    name="planner-A"
)

planner_b = PlannerAgent(
    llm=antigravity_llm,
    memory=memory,
    long_term_memory=ltm,
    vector_memory=vector_memory,
    reputation=reputation,
    alignment=alignment,
    freeze=freeze,
    bus=bus,
    name="planner-B"
)

voter = Voter(llm=antigravity_llm, reputation=reputation)

tool_registry = ToolRegistry()
tool_registry.register("think", "Internal reasoning", think)
tool_registry.register("write_file", "Write content to file", write_file)
tool_registry.register("web_search", "Search the web", web_search)

executor = ExecutorAgent(
    llm=antigravity_llm,
    tool_registry=tool_registry,
    memory=memory
)

critic = Critic(llm=antigravity_llm)
evaluator = Evaluator(llm=antigravity_llm)
rollback_manager = RollbackManager()

"""scheduler = Scheduler()
scheduler.add_task(
    goal="Run stable aligned agent",
    interval_seconds=86400"""

scheduler = Scheduler()
scheduler.add_task(
    goal="Run stable aligned agent",
    interval_seconds=86400
)

sandbox = CodeSandbox(
    allowed_files=[
        "planner_agent.py",
        "executor_agent.py"
    ]
)

agent_loop(
    planners=[planner_a, planner_b],
    voter=voter,
    executor=executor,
    critic=critic,
    tool_registry=tool_registry,
    code_sandbox=sandbox,
    evaluator=evaluator,
    rollback_manager=rollback_manager,
    bus=bus,
    reputation=reputation,
    meta_goals=meta_goals,
    alignment=alignment,
    freeze=freeze,
    scheduler=scheduler
)
