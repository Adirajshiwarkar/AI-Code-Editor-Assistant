import json
import re
import os
import threading
import queue
from utils.llm import LLMFactory
from tools.file_ops import read_file, write_file, list_files, write_file_safely
from tools.diff_generator import generate_unified_diff, get_change_summary
from tools.language_detector import detect_language, get_language_rules
from agents.planner import PlannerAgent
from agents.analysis import AnalysisAgent
from agents.refactor import RefactorAgent
from agents.qa import QAAgent
from agents.doc import DocAgent
from agents.test_gen import TestGenAgent
from agents.reporting import ReportingAgent
from agents.chat import ChatAgent
from agents.crew_config import CrewManager

class Coordinator:
    def __init__(self, backup_enabled=True):
        self.client = LLMFactory.create_llm()
        self.planner = PlannerAgent(self.client)
        self.analyzer = AnalysisAgent(self.client)
        self.refactorer = RefactorAgent(self.client)
        self.qa = QAAgent(self.client)
        self.doc_agent = DocAgent(self.client)
        self.test_gen = TestGenAgent(self.client)
        self.reporter = ReportingAgent(self.client)
        self.chat_agent = ChatAgent(self.client)
        self.crew_manager = CrewManager()
        self.backup_enabled = backup_enabled

    def execute_request(self, target_path, instruction, history=None):
        print(f"[*] Starting task: '{instruction}' on {target_path} (Using CrewAI)")
        
        # Determine if we should use simple chat or CrewAI
        if target_path == "" and len(instruction.split()) < 4:
             # Fast path for simple chat/greetings
             return self.chat_agent.run(instruction, history=history)

        try:
            # Execute via CrewAI
            result = self.crew_manager.run_coding_task(instruction, target_path, history=history)
            return str(result)
        except Exception as e:
            print(f"[!] CrewAI execution failed: {str(e)}. Falling back to legacy coordinator.")
            # Legacy logic starts here...
        files = []
        if target_path:
            if os.path.isfile(target_path):
                files = [target_path]
            elif os.path.isdir(target_path):
                files = list_files(target_path)
            # If target_path doesn't exist but looks like a file type, maybe it's new
            # For now, we only gather context if it exists
        
        # Detect language from first file if available
        language = "python"
        if files:
            language = detect_language(files[0])
        lang_rules = get_language_rules(language)
        print(f"[*] Detected language: {language}")
        
        context = ""
        if files:
            for f in files:
                if os.path.exists(f):
                    content = read_file(f)
                    context += f"--- {f} ---\n{content}\n\n"

        # 2. Plan
        print("[*] Planning...")
        plan_raw = self.planner.run(instruction, context)
        try:
            # Simple JSON extraction
            json_match = re.search(r'\[.*\]', plan_raw, re.DOTALL)
            plan = json.loads(json_match.group(0)) if json_match else []
        except:
            print("[!] Failed to parse plan. Falling back to default sequence.")
            plan = [
                {"agent": "Analysis", "description": "Analyze provided code."},
                {"agent": "Refactor", "description": "Apply refactorings."},
                {"agent": "QA", "description": "Review changes."},
                {"agent": "Doc", "description": "Generate documentation."},
                {"agent": "Reporting", "description": "Provide summary."}
            ]

        # 3. Step through plan
        results = []
        current_code_state = context
        original_code = context
        refactored_code = None
        
        for task in plan:
            agent_name = task.get("agent", "").lower()
            desc = task.get("description", "")
            print(f"[*] Executing task: {desc} (Agent: {agent_name})")
            
            if "analysis" in agent_name:
                res = self.analyzer.run(current_code_state)
                results.append(f"=== ANALYSIS ===\n{res}\n")
                
            elif "refactor" in agent_name:
                res = self.refactorer.run(current_code_state, desc, language)
                # Extract code from markdown
                code_match = re.search(r'```(?:python|javascript|typescript|java|cpp|go)?\n(.*?)\n```', res, re.DOTALL)
                if code_match:
                    refactored_code = code_match.group(1)
                    current_code_state = refactored_code
                    
                    # Generate diff
                    if original_code and refactored_code:
                        diff = generate_unified_diff(original_code, refactored_code, files[0] if files else "code")
                        summary = get_change_summary(original_code, refactored_code)
                        results.append(f"=== REFACTORING ===\n{res}\n\n=== DIFF ===\n{diff}\n\n=== SUMMARY ===\n{summary}\n")
                    else:
                        results.append(f"=== REFACTORING ===\n{res}\n")
                else:
                    results.append(f"=== REFACTORING ===\n{res}\n")
                    
            elif "qa" in agent_name:
                res = self.qa.run(original_code, current_code_state, language)
                results.append(f"=== QA REVIEW ===\n{res}\n")
                
            elif "testgen" in agent_name or "test" in agent_name:
                res = self.test_gen.run(current_code_state, language)
                results.append(f"=== TEST GENERATION ===\n{res}\n")
                
            elif "doc" in agent_name:
                # Determine doc type from description
                doc_type = "docstring"
                if "architecture" in desc.lower():
                    doc_type = "architecture"
                elif "readme" in desc.lower():
                    doc_type = "readme"
                elif "api" in desc.lower():
                    doc_type = "api"
                    
                res = self.doc_agent.run(current_code_state, doc_type, language)
                results.append(f"=== DOCUMENTATION ({doc_type}) ===\n{res}\n")
                
            elif "reporting" in agent_name:
                res = self.reporter.run("\n".join(results))
                results.append(f"=== REPORT ===\n{res}\n")
            elif "chat" in agent_name:
                res = self.chat_agent.run(instruction, current_code_state)
                results.append(f"{res}")
                
            else:
                res = f"Unknown agent: {agent_name}"
                results.append(res)

        # 4. Final Reporting
        # If it's just a single chat result, return it directly
        if len(plan) == 1 and plan[0].get("agent", "").lower() == "chat":
            return results[0]

        print("[*] Generating final report...")
        final_report = self.reporter.run("\n".join(results))
        
        # 5. Optionally write refactored code back
        if refactored_code and files:
            if self.backup_enabled:
                write_result = write_file_safely(files[0], refactored_code, create_backup_flag=True)
                print(f"[*] {write_result}")
    def execute_request_stream(self, target_path, instruction, history=None):
        print(f"[*] Starting streaming task: '{instruction}' on {target_path} (High Speed Mode)")
        
        # 1. ULTRA-FAST PATH: General chat or simple technical questions
        # Use simple chat if no files are involved or if it's a short query
        is_simple_query = (target_path == "") or (len(instruction.split()) < 15 and not target_path)
        
        if is_simple_query:
             yield "[START_REPORT]\n"
             for chunk in self.chat_agent.run_stream(instruction, history=history):
                 yield chunk
             return

        # 2. FAST-CODER PATH: Standard single-file refactoring
        # Bypasses the heavy CrewAI orchestration for common tasks
        if target_path and os.path.isfile(target_path):
            yield f"[STEP] Rapidly analyzing and refactoring {os.path.basename(target_path)}...\n"
            
            content = read_file(target_path)
            # Use the refactor agent directly to avoid the CrewAI coordination overhead
            yield "[START_REPORT]\n"
            
            # We'll use the refactorer agent's run_stream if it exists, otherwise use its run
            # For maximum speed, we directly stream the response
            full_response = ""
            for chunk in self.refactorer.run_stream(content, instruction, detect_language(target_path), history=history):
                full_response += chunk
                yield chunk
            
            # Extract code and provide final code signal
            code_match = re.search(r'```(?:python|javascript|typescript|java|cpp|go)?\n(.*?)\n```', full_response, re.DOTALL)
            if code_match:
                yield f"\n[FINAL_CODE]\n{code_match.group(1)}"
            return

        # 3. ADVANCED CREW PATH: Multi-file or complex projects (The "Full Crew")
        yield f"[STEP] Complex task detected. Assembling Expert Crew...\n"
        
        result_queue = queue.Queue()

        def crew_callback(output):
            if hasattr(output, 'agent'):
                result_queue.put(f"[STEP] {output.agent} is active...\n")
            elif hasattr(output, 'raw'):
                result_queue.put(f"[STEP] Phase complete.\n")

        def run_crew():
            try:
                result = self.crew_manager.run_coding_task(instruction, target_path, callback=crew_callback, history=history)
                result_queue.put(("[RESULT]", str(result)))
            except Exception as e:
                result_queue.put(("[ERROR]", str(e)))
            finally:
                result_queue.put(None)

        thread = threading.Thread(target=run_crew)
        thread.start()

        while True:
            item = result_queue.get()
            if item is None: break
            
            if isinstance(item, tuple):
                tag, val = item
                if tag == "[RESULT]":
                    yield "[START_REPORT]\n"
                    yield val
                    if target_path and os.path.exists(target_path) and os.path.isfile(target_path):
                        with open(target_path, 'r') as f:
                            final_code = f.read()
                        yield f"\n[FINAL_CODE]\n{final_code}"
                elif tag == "[ERROR]":
                    yield f"[STEP] Error: {val}\n"
                    yield "[START_REPORT]\n"
                    yield f"I encountered an error: {val}"
            else:
                yield item

        thread.join()
