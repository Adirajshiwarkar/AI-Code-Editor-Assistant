from agents.base_agent import BaseAgent

class AnalysisAgent(BaseAgent):
    def __init__(self, client):
        super().__init__("Analysis", "Senior Code Reviewer", client)

    def run(self, files_content):
        system_prompt = """
You are the Code Analysis Agent. Analyze the provided code for:
- Structure and architecture.
- Logic flow and intent.
- Potential bottlenecks or complexity issues.
- Missing edge cases.
- Style and naming inconsistencies.

Provide a detailed technical report on the findings.
"""
        user_prompt = f"Code for analysis:\n\n{files_content}"
        return self.client.get_completion(self.format_prompt(system_prompt, user_prompt))
