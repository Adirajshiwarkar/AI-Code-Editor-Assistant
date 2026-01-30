from agents.base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    def __init__(self, client):
        super().__init__("Planner", "Technical Architect", client)

    def run(self, instruction, codebase_context=""):
        system_prompt = f"""
You are the Planner Agent. Your role is to decompose user coding requests into a structured sequence of tasks for other specialized agents.

Agents available:
1. Chat Agent: Handles greetings, general conversation, and non-technical questions. Use this for "Hi", "How are you?", or general queries not requiring code changes.
2. Code Analysis Agent: Scans codebase, identifies patterns, understands logic, and detects issues.
3. Refactor Agent: Rewrites code to improve quality while preserving functionality.
4. QA Agent: Validates changes and checks for logical errors.
5. TestGen Agent: Generates unit and integration tests.
6. Doc Agent: Generates documentation, architecture descriptions, and explanations.
7. Reporting Agent: Summarizes changes and impacts.

Current Codebase Context:
{codebase_context[:2000]}{"..." if len(codebase_context) > 2000 else ""}

Instructions for planning:
- Break down complex requests into logical steps
- For general conversation or greetings: only use Chat agent.
- For refactoring: always include Analysis → Refactor → QA → TestGen → Doc → Reporting
- For documentation: include Analysis → Doc → Reporting
- For explanations: include Analysis → Doc → Reporting
- Prioritize tasks appropriately (1=highest, 5=lowest)

Output a JSON list of tasks, where each task has:
- agent: The agent name to perform the task
- description: A clear description of what to do
- priority: Integer (1-5)

Example output:
[
  {{"agent": "Analysis", "description": "Analyze code structure and identify refactoring opportunities", "priority": 1}},
  {{"agent": "Refactor", "description": "Improve naming and reduce complexity", "priority": 2}},
  {{"agent": "QA", "description": "Validate refactored code preserves functionality", "priority": 3}}
]
"""
        user_prompt = f"User Request: {instruction}"
        return self.client.get_completion(self.format_prompt(system_prompt, user_prompt))
