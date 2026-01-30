from agents.base_agent import BaseAgent

class ReportingAgent(BaseAgent):
    def __init__(self, client):
        super().__init__("Reporting", "Technical Project Manager", client)

    def run(self, raw_changes):
        system_prompt = """
You are the Reporting Agent. Summarize the changes made by the AI Assistant.
Include:
- High-level list of improvements.
- Risks and tradeoffs.
- Before vs. After comparison summary.
- Next steps suggestions.
"""
        user_prompt = f"Changes made:\n\n{raw_changes}"
        return self.client.get_completion(self.format_prompt(system_prompt, user_prompt))

    def run_stream(self, raw_changes):
        system_prompt = """
You are the Reporting Agent. Summarize the changes made by the AI Assistant.
Include:
- High-level list of improvements.
- Risks and tradeoffs.
- Before vs. After comparison summary.
- Next steps suggestions.
"""
        user_prompt = f"Changes made:\n\n{raw_changes}"
        return self.client.get_streaming_completion(self.format_prompt(system_prompt, user_prompt))
