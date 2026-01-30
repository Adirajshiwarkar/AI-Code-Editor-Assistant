from agents.base_agent import BaseAgent

class RefactorAgent(BaseAgent):
    def __init__(self, client):
        super().__init__("Refactor", "Expert Software Engineer", client)

    def run(self, file_content, instruction, language="python", history=None):
        user_prompt = f"Original Code:\n\n{file_content}\n\nInstruction: {instruction}"
        system_prompt = self.get_system_prompt(language)
        return self.client.get_completion(self.format_prompt(system_prompt, user_prompt, history=history))

    def get_system_prompt(self, language="python"):
        return f"""
You are the Refactor Agent. Your goal is to improve code according to the instruction while strictly preserving existing functionality.
Language: {language}

Guidelines:
- ALWAYS preserve the original functionality.
- IMPROVE naming, modularity, and readability.
- Output ONLY the refactored code within a markdown code block.
- Be extremely direct and fast.
"""

    def run_stream(self, file_content, instruction, language="python", history=None):
        user_prompt = f"Original Code:\n\n{file_content}\n\nInstruction: {instruction}"
        self.system_prompt = self.get_system_prompt(language)
        return super().run_stream(user_prompt, history=history)
