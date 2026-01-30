import argparse
import sys
import os
from coordinator import Coordinator

def main():
    parser = argparse.ArgumentParser(
        description="AI Autonomous Coding & Refactoring Assistant",
        epilog="""
Examples:
  python main.py tests/messy_code.py "refactor this file"
  python main.py src/ "generate documentation"
  python main.py app.py "add type hints and improve error handling"
  python main.py --no-backup code.py "optimize performance"
        """
    )
    parser.add_argument("path", help="Path to a file or folder")
    parser.add_argument("instruction", help="Instruction for the assistant (e.g., 'refactor this file', 'generate tests')")
    parser.add_argument("--no-backup", action="store_true", help="Disable automatic backup of modified files")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying them (coming soon)")
    
    try:
        args = parser.parse_args()
    except SystemExit:
        print("\n[!] Usage Tip: python main.py <file_path> \"<instruction>\"")
        print("Example: python main.py tests/messy_code.py \"refactor this code\"")
        print("\nFor more options, use: python main.py --help")
        sys.exit(1)
    
    if not os.path.exists(args.path):
        print(f"Error: Path {args.path} does not exist.")
        sys.exit(1)

    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please add it to your .env file or export it in your shell.")
        sys.exit(1)

    # Create coordinator with backup setting
    backup_enabled = not args.no_backup
    coordinator = Coordinator(backup_enabled=backup_enabled)
    
    if args.dry_run:
        print("[*] DRY RUN MODE: Changes will be previewed but not applied")
        # TODO: Implement dry-run mode
    
    report = coordinator.execute_request(args.path, args.instruction)
    
    print("\n" + "="*50)
    print("FINAL REPORT")
    print("="*50)
    print(report)

if __name__ == "__main__":
    main()
