class BaseAgent:
    def __init__(self, name, role, client):
        self.name = name
        self.role = role
        self.client = client

    def format_prompt(self, system_prompt, user_prompt, history=None):
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_prompt})
        return messages

    def run(self, user_prompt, context=None, history=None):
        raise NotImplementedError("Subclasses must implement run()")

    def run_stream(self, user_prompt, context=None, history=None):
        # Default implementation for streaming if supported by client
        if hasattr(self.client, 'get_streaming_completion'):
            system_prompt = getattr(self, "system_prompt", f"You are the {self.name} Agent.")
            return self.client.get_streaming_completion(self.format_prompt(system_prompt, user_prompt, history=history))
        else:
            # Fallback to non-streaming
            return [self.run(user_prompt, context, history=history)]
