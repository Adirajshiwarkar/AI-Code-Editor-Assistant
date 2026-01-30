from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from tools.crew_tools import read_file_tool, write_file_tool, list_files_tool
import os

class CrewManager:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        # Use gpt-4o-mini for maximum speed as requested by user
        self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=self.api_key)
        
        # Tools
        self.read_tool = read_file_tool
        self.write_tool = write_file_tool
        self.list_tool = list_files_tool

    def create_agents(self):
        # 1. Code Analyzer
        self.analyzer = Agent(
            role='Senior Code Analyst',
            goal='Execute rapid code analysis and provide immediate technical insights. No fluff.',
            backstory='You are a high-speed technical auditor. You provide direct, actionable analysis without preamble or asking for permission.',
            tools=[self.read_tool, self.list_tool],
            llm=self.llm,
            verbose=False,
            allow_delegation=False
        )

        # 2. Refactorer
        self.refactorer = Agent(
            role='Senior Software Engineer',
            goal='Immediately implement optimized and clean code changes. Always provide the full solution.',
            backstory='You are a pragmatist. You do not ask if the user wants to see the code; you simply write the best version of it immediately.',
            tools=[self.read_tool, self.write_tool],
            llm=self.llm,
            verbose=False,
            allow_delegation=False
        )

        # 3. QA Expert
        self.qa_specialist = Agent(
            role='Quality Assurance Engineer',
            goal='Verify logic and performance instantly. Ensure zero errors.',
            backstory='You are a precise validator. You confirm the quality of the work and suggest final optimizations without delay.',
            tools=[self.read_tool],
            llm=self.llm,
            verbose=False,
            allow_delegation=False
        )

        # 4. Technical Writer
        self.writer = Agent(
            role='Direct Technical Communicator',
            goal='Summarize findings and output final code/solutions directly to the user.',
            backstory='You are the bridge between the technical agents and the user. You never ask "would you like to see..."; you just show the complete result immediately.',
            llm=self.llm,
            verbose=False,
            allow_delegation=False
        )

    def run_coding_task(self, instruction, context_path, callback=None, history=None):
        self.create_agents()
        
        # Adjust descriptions for speed and directness
        path_desc = f"at {context_path}" if context_path else "provided"
        
        # Formatting history for CrewAI context
        history_context = ""
        if history:
            history_context = "\nCONVERSATION HISTORY:\n" + "\n".join([f"- {m['role'].upper()}: {m['content'][:200]}..." for m in history])

        # Define Task 1: Analysis & Refactor
        task1 = Task(
            description=f"{history_context}\n\nAnalyze and immediately refactor the code for: {instruction}. Use context {path_desc}. Provide the full optimized code and a summary of what you did.",
            expected_output="A technical summary followed by the full modified code in markdown.",
            agent=self.refactorer,
            callback=callback # Task callback
        )

        # Define Task 2: Review & Report
        task2 = Task(
            description="Verify the logic of the previous refactoring and generate the final comprehensive output for the user. Show all code and analysis directly.",
            expected_output="The final production-ready report including analysis and full code snippets.",
            agent=self.writer,
            context=[task1],
            callback=callback # Task callback
        )

        # Form a leaner Crew for faster execution
        crew = Crew(
            agents=[self.analyzer, self.refactorer, self.writer],
            tasks=[task1, task2],
            process=Process.sequential,
            verbose=False,
            step_callback=callback # Step callback for real-time thought streaming
        )

        return crew.kickoff()
