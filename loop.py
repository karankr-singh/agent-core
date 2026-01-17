# loop.py

def agent_loop(
    planners,
    voter,
    executor,
    critic,
    tool_registry,
    code_sandbox,
    evaluator,
    rollback_manager,
    bus,
    reputation,
    meta_goals,
    alignment,
    freeze,
    scheduler=None,
    max_steps=6
):
    if scheduler:
        tasks = scheduler.due_tasks()
        for task in tasks:
            if not alignment.validate_goal(task["goal"]):
                continue
            for p in planners:
                p.memory.set_goal(task["goal"])
            _run(
                planners,
                voter,
                executor,
                critic,
                tool_registry,
                code_sandbox,
                evaluator,
                rollback_manager,
                bus,
                reputation,
                meta_goals,
                alignment,
                freeze,
                scheduler,
                max_steps
            )
            scheduler.mark_ran(task)
    else:
        _run(
            planners,
            voter,
            executor,
            critic,
            tool_registry,
            code_sandbox,
            evaluator,
            rollback_manager,
            bus,
            reputation,
            meta_goals,
            alignment,
            freeze,
            scheduler,
            max_steps
        )


def _run(
    planners,
    voter,
    executor,
    critic,
    tool_registry,
    code_sandbox,
    evaluator,
    rollback_manager,
    bus,
    reputation,
    meta_goals,
    alignment,
    freeze,
    scheduler,
    max_steps
):
    for step in range(max_steps):
        proposals = [p.propose() for p in planners]
        chosen = voter.choose(
            planners[0].memory.data["goal"],
            proposals
        )

        author = chosen.get("planner", "unknown")
        goal = planners[0].memory.data["goal"]

        if chosen.get("type") == "broadcast":
            bus.publish(
                chosen["broadcast"]["topic"],
                chosen["broadcast"]["payload"]
            )
            continue

        # ---------- EXECUTION ----------
        if chosen.get("type") == "subtask":
            results = []
            for sub in chosen.get("subtasks", []):
                results.append(executor.execute(sub))
            final_result = " | ".join(results)
        else:
            final_result = executor.execute(
                chosen.get("instruction", "")
            )

        # ---------- CRITIC ----------
        critique = critic.review(
            goal=goal,
            result=str(final_result)
        )

        planners[0].memory.add("critic_feedback", critique)

        # ---------- SUCCESS ----------
        if "ACCEPT" in critique.upper():
            reputation.reward(author)

            # 🧠 VECTOR MEMORY — TAGGED RAW RESULT
            planners[0].vector_memory.add(
                f"[#goal:{goal}] [#execution] {final_result}"
            )

            # 🧠 VECTOR MEMORY — TAGGED INSIGHT
            planners[0].vector_memory.add(
                f"[#goal:{goal}] [#success] [#insight] {final_result}"
            )

            planners[0].long_term_memory.add_lesson(
                f"Successful completion of goal: {goal}"
            )

            # ---------- META GOALS ----------
            if not freeze.allow_meta_goals():
                break

            context = str(planners[0].memory.get_history())
            new_goals = meta_goals.generate(context)

            for g in new_goals:
                if alignment.validate_goal(g):
                    scheduler.add_task(
                        goal=g,
                        interval_seconds=86400
                    )
            break

        # ---------- FAILURE ----------
        else:
            reputation.penalize(author)

            # 🧠 VECTOR MEMORY — FAILURE PATTERN
            planners[0].vector_memory.add(
                f"[#goal:{goal}] [#failure] {final_result}"
            )

            for p in planners:
                p.update_policy(critique)
