from agents.base_agent import BaseAgent

class QAAgent(BaseAgent):
    def __init__(self, client):
        super().__init__("QA", "Quality Assurance Lead", client)

    def run(self, original_code, refactored_code, language="python"):
        system_prompt = f"""
You are the QA Agent. Compare the original code with the refactored code.

Language: {language}

Your responsibilities:
- Check if functionality is preserved (critical!)
- Look for new bugs introduced
- Identify potential performance regressions
- Verify if the refactor actually improved the code
- Check for edge cases that might be affected
- Validate error handling improvements
- Assess code maintainability improvements

Provide a structured report with:
1. VERDICT: PASS or FAIL
2. Functionality Preservation: Detailed analysis
3. Bugs/Issues Found: List any problems
4. Improvements Validated: What got better
5. Recommendations: Any additional suggestions

Be thorough and critical. If functionality is not preserved, FAIL the review.
"""
        user_prompt = f"Original:\n{original_code}\n\nRefactored:\n{refactored_code}"
        return self.client.get_completion(self.format_prompt(system_prompt, user_prompt))
