from agents.base_agent import BaseAgent

class TestGenAgent(BaseAgent):
    def __init__(self, client):
        super().__init__("TestGen", "Test Engineer", client)

    def run(self, code_content, language="python", test_type="unit"):
        system_prompt = f"""
You are the Test Generation Agent. Generate comprehensive tests for the provided code.

Language: {language}
Test Type: {test_type}

Your responsibilities:
- Generate unit tests that validate functionality
- Cover edge cases and error conditions
- Use appropriate testing framework for the language
- Include setup and teardown if needed
- Add clear test descriptions and assertions
- Ensure tests are runnable and follow best practices

For Python: Use pytest
For JavaScript/TypeScript: Use Jest
For Java: Use JUnit
For Go: Use testing package

Output ONLY the test code within a markdown code block.
"""
        user_prompt = f"Generate {test_type} tests for this code:\n\n{code_content}"
        return self.client.get_completion(self.format_prompt(system_prompt, user_prompt))

    def generate_test_suite(self, code_content, language="python"):
        """Generate a complete test suite with multiple test cases."""
        system_prompt = f"""
You are the Test Generation Agent. Create a comprehensive test suite.

Language: {language}

Generate tests that include:
1. Happy path tests (normal expected usage)
2. Edge case tests (boundary conditions)
3. Error handling tests (invalid inputs, exceptions)
4. Integration tests (if applicable)

Organize tests logically and use descriptive test names.
Include comments explaining what each test validates.

Output ONLY the complete test file within a markdown code block.
"""
        user_prompt = f"Generate comprehensive test suite for:\n\n{code_content}"
        return self.client.get_completion(self.format_prompt(system_prompt, user_prompt))
