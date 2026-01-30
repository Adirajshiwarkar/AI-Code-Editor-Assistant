"""Diff generation and comparison utilities."""
import difflib
from typing import List, Tuple

def generate_unified_diff(original: str, modified: str, filename: str = "file") -> str:
    """Generate a unified diff between original and modified content."""
    original_lines = original.splitlines(keepends=True)
    modified_lines = modified.splitlines(keepends=True)
    
    diff = difflib.unified_diff(
        original_lines,
        modified_lines,
        fromfile=f"a/{filename}",
        tofile=f"b/{filename}",
        lineterm=''
    )
    
    return ''.join(diff)

def generate_side_by_side(original: str, modified: str, width: int = 80) -> str:
    """Generate a side-by-side comparison of changes."""
    original_lines = original.splitlines()
    modified_lines = modified.splitlines()
    
    result = []
    result.append("=" * (width * 2 + 3))
    result.append(f"{'ORIGINAL':<{width}} | {'MODIFIED':<{width}}")
    result.append("=" * (width * 2 + 3))
    
    max_lines = max(len(original_lines), len(modified_lines))
    
    for i in range(max_lines):
        orig_line = original_lines[i] if i < len(original_lines) else ""
        mod_line = modified_lines[i] if i < len(modified_lines) else ""
        
        # Truncate if too long
        if len(orig_line) > width - 3:
            orig_line = orig_line[:width-6] + "..."
        if len(mod_line) > width - 3:
            mod_line = mod_line[:width-6] + "..."
        
        result.append(f"{orig_line:<{width}} | {mod_line:<{width}}")
    
    result.append("=" * (width * 2 + 3))
    return '\n'.join(result)

def get_change_summary(original: str, modified: str) -> dict:
    """Get a summary of changes between two versions."""
    original_lines = original.splitlines()
    modified_lines = modified.splitlines()
    
    diff = list(difflib.unified_diff(original_lines, modified_lines, lineterm=''))
    
    additions = sum(1 for line in diff if line.startswith('+') and not line.startswith('+++'))
    deletions = sum(1 for line in diff if line.startswith('-') and not line.startswith('---'))
    
    return {
        'additions': additions,
        'deletions': deletions,
        'total_changes': additions + deletions,
        'original_lines': len(original_lines),
        'modified_lines': len(modified_lines),
    }

def highlight_changes(original: str, modified: str) -> List[Tuple[str, str, str]]:
    """Identify specific line changes with context."""
    original_lines = original.splitlines()
    modified_lines = modified.splitlines()
    
    changes = []
    matcher = difflib.SequenceMatcher(None, original_lines, modified_lines)
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace':
            changes.append(('modified', '\n'.join(original_lines[i1:i2]), '\n'.join(modified_lines[j1:j2])))
        elif tag == 'delete':
            changes.append(('deleted', '\n'.join(original_lines[i1:i2]), ''))
        elif tag == 'insert':
            changes.append(('added', '', '\n'.join(modified_lines[j1:j2])))
    
    return changes
