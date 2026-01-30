from agents.base_agent import BaseAgent

class DocAgent(BaseAgent):
    def __init__(self, client):
        super().__init__("Doc", "Technical Writer", client)

    def run(self, code_context, request_type="docstring", language="python"):
        system_prompt = f"""
You are the Doc Agent. Generate high-quality technical documentation.

Language: {language}
Request type: {request_type}

Documentation types supported:
- docstring: Function/class docstrings with parameters, returns, examples
- module: Module-level documentation explaining purpose and usage
- architecture: High-level system architecture and component relationships
- api: API documentation with endpoints, parameters, responses
- readme: Comprehensive README with setup, usage, examples

Guidelines:
- Be clear, concise, and professional
- Include code examples where helpful
- Explain the "why" not just the "what"
- Use proper formatting (Markdown, docstring conventions)
- Include type information and parameter descriptions
- Add usage examples for complex functionality

Output the documentation in the appropriate format for the request type.
"""
        user_prompt = f"Generate {request_type} documentation for:\n\n{code_context}"
        return self.client.get_completion(self.format_prompt(system_prompt, user_prompt))
