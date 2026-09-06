# 🤖 Agent-Core

> A modular autonomous-agent research prototype focused on planning, tool execution, memory, self-critique, reputation, alignment, and observability.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/Status-Research%20Prototype-orange?style=for-the-badge)](#project-status)

**Live dashboard:** https://agent-core-g9i9cydg48fozkz6zw2zjg.streamlit.app/

<img width="1364" height="599" alt="Agent-Core dashboard" src="https://github.com/user-attachments/assets/50415f40-9982-4a02-a475-585abdb2ac05" />

---

## 🎯 Why Agent-Core?

Many agent demos stop at a prompt → response loop. Agent-Core explores what happens when an agent is treated more like a **system**: it maintains state, uses tools, evaluates outcomes, records lessons, and makes later decisions using accumulated context.

The project is intentionally experimental rather than a claim of AGI or a production autonomous system.

### What it explores

- **Planning** — generate actionable next steps from a goal and context
- **Multi-planner selection** — multiple planners propose actions and a voter selects a candidate
- **Tool execution** — execute selected instructions through a tool registry
- **Critique** — evaluate execution results against the current goal
- **Memory** — maintain run history, long-term lessons, and semantic/vector memory
- **Reputation** — reward or penalize planners based on outcomes
- **Alignment** — validate goals before execution and before creating follow-up goals
- **Freeze control** — gate meta-goal generation
- **Scheduling** — optionally run due tasks and schedule generated goals
- **Observability** — expose the system state through a live dashboard

---

## 🧠 System Overview

```text
                         ┌──────────────────────┐
                         │       Goal / Task     │
                         └──────────┬───────────┘
                                    │
                                    ▼
                    ┌─────────────────────────────┐
                    │       Planner Agents        │
                    │  proposals + policy update  │
                    └──────────────┬──────────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │  Voter / Selector │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     Executor     │
                         │  tools / sandbox │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │      Critic       │
                         └────────┬─────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                 ACCEPT                      FAILURE
                    │                           │
                    ▼                           ▼
             Reward planner              Penalize planner
                    │                           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                   ┌─────────────────────────────┐
                   │ Memory + Reputation + Logs  │
                   └──────────────┬──────────────┘
                                  │
                                  ▼
                         Dashboard / Observability
```

The main execution loop coordinates planners, voting, execution, critique, reputation updates, memory writes, alignment checks, and optional scheduled/meta-goal handling.

---

## 🔄 Execution Cycle

For each agent run, the system broadly follows:

1. **Receive a goal** or scheduled task.
2. **Validate the goal** against alignment rules.
3. **Generate proposals** from the available planners.
4. **Select a proposal** using the voter.
5. **Execute** the selected instruction or subtasks.
6. **Critique the result** against the original goal.
7. If accepted, **reward the planner** and persist successful execution patterns.
8. If rejected, **penalize the planner**, store the failure pattern, and update planner policy.
9. When enabled, generate and validate **follow-up/meta-goals** for later execution.

The implementation currently caps the normal run loop at a configurable maximum number of steps (default: 6).

---

## 🧩 Core Components

| Component | Responsibility |
|---|---|
| `agent.py` | Planning, tool selection, execution, and reflection for the core agent abstraction |
| `loop.py` | Orchestrates the multi-agent execution cycle |
| `critic.py` | Reviews execution outcomes |
| `evaluator.py` | Evaluation logic used by the system |
| `executor_agent.py` | Executes selected instructions |
| `alignment.py` | Goal validation / alignment rules |
| `freeze.py` | Controls whether meta-goals may be generated |
| `llm.py` | LLM/embedding integration boundary |
| `long_term_memory.py` | Persistent lesson storage |
| `code_sandbox.py` | Code-execution sandbox component |
| `scheduler.py` | Optional scheduled task handling |
| `vector_memory.py` | Semantic memory storage/retrieval |

The repository also contains persisted memory/state files used by the prototype.

---

## 🧠 Memory Architecture

Agent-Core separates memory by purpose:

### Run memory
Stores the current goal, history, plans, actions, and critic feedback for the active run.

### Long-term memory
Stores lessons from successful and unsuccessful executions so future planning can use previous experience.

### Vector memory
Stores semantic representations of useful execution patterns and insights, allowing future plans to retrieve related context.

This gives the system a simple feedback loop:

```text
Experience → Critique → Lesson / Semantic Memory → Future Planning
```

---

## 🛡️ Alignment & Safety Controls

The prototype includes explicit control points rather than treating autonomy as unrestricted:

- Goal validation before scheduled execution
- Goal validation before generated meta-goals are accepted
- A global freeze mechanism controlling meta-goal generation
- Restricted tool selection through a tool registry
- A separate code-sandbox component for code execution

These mechanisms are **prototype safeguards**, not a claim that the system is safe for unrestricted autonomous deployment.

---

## 👀 Observability

The Streamlit dashboard is designed to make internal system state easier to inspect, including information such as:

- Current goal and run state
- Planner/reputation information
- Execution history
- Critic feedback
- Memory growth and stored knowledge
- Semantic-memory activity

<img width="1358" height="594" alt="Agent-Core dashboard view" src="https://github.com/user-attachments/assets/65f40330-160c-4314-a5f6-7b9a03798258" />

<img width="1361" height="630" alt="Agent-Core system view" src="https://github.com/user-attachments/assets/7fa6f5ed-786b-4c6b-973c-5a07c47ac157" />

<img width="1320" height="597" alt="Agent-Core memory view" src="https://github.com/user-attachments/assets/ae21619a-9888-493f-af40-e142247c2f52" />

---

## ⚙️ LLM Integration

`llm.py` is intentionally structured as an integration boundary for an external LLM/embedding provider. The current repository contains placeholder/fallback behavior rather than a complete provider integration.

That means the project should be treated as an **agent architecture prototype**, not as a turnkey autonomous-agent package.

---

## 🚀 Running the Project

The repository is currently an experimental codebase and does not ship with a populated `requirements.txt`. For local development, install the dependencies required by the modules you intend to run, then start the Streamlit dashboard using the repository's dashboard entry point.

The hosted dashboard is available here:

https://agent-core-g9i9cydg48fozkz6zw2zjg.streamlit.app/

> **Note:** Because the LLM layer currently contains placeholder behavior, a full autonomous run may require wiring `llm.py` to the intended model provider first.

---

## 📸 Project Screenshots

### Live system dashboard

<img width="1364" height="599" alt="Agent-Core live dashboard" src="https://github.com/user-attachments/assets/50415f40-9982-4a02-a475-585abdb2ac05" />

### Agent state and execution

<img width="1358" height="594" alt="Agent-Core execution dashboard" src="https://github.com/user-attachments/assets/65f40330-160c-4314-a5f6-7b9a03798258" />

---

## 📌 Project Status

**Research / experimental prototype**

Implemented concepts include planning, proposal selection, execution, critique, reputation updates, persistent lessons, semantic-memory hooks, alignment checks, freeze control, scheduling hooks, and dashboard-oriented observability.

Areas that still need production-level work include provider integration, dependency management, automated tests, stronger sandbox isolation, persistent database-backed storage, authentication, and robust failure handling.

---

## 🔭 Future Directions

- [ ] Production-ready LLM provider adapters
- [ ] Proper dependency locking and reproducible setup
- [ ] Automated unit/integration tests
- [ ] Stronger isolated code execution
- [ ] Database-backed memory and event storage
- [ ] Better evaluation benchmarks for agent performance
- [ ] Richer tool ecosystem with explicit permissions
- [ ] Improved dashboard metrics and run replay

---

## 💡 What This Project Demonstrates

From a software-engineering perspective, Agent-Core demonstrates work across:

- Agent orchestration and control flow
- State and memory management
- Multi-agent coordination
- Evaluation and feedback loops
- Tool interfaces
- Safety and policy gates
- Semantic retrieval concepts
- Observability for autonomous workflows

It is best viewed as a **systems-oriented AI research project** rather than a chatbot wrapper.

---

## 👤 Author

**Karan Kumar Singh** — Developer & Researcher

Built as an exploration of autonomous AI architectures, memory systems, feedback loops, and controllable agent behavior.
