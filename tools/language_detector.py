"""Language detection utility for code files."""
import os

# Language mappings
LANGUAGE_MAP = {
    '.py': 'python',
    '.js': 'javascript',
    '.jsx': 'javascript',
    '.ts': 'typescript',
    '.tsx': 'typescript',
    '.java': 'java',
    '.cpp': 'cpp',
    '.cc': 'cpp',
    '.cxx': 'cpp',
    '.c': 'c',
    '.h': 'c',
    '.hpp': 'cpp',
    '.go': 'go',
    '.rs': 'rust',
    '.rb': 'ruby',
    '.php': 'php',
    '.swift': 'swift',
    '.kt': 'kotlin',
    '.cs': 'csharp',
}

# Language-specific formatting rules
LANGUAGE_RULES = {
    'python': {
        'indent': 4,
        'style': 'PEP 8',
        'test_framework': 'pytest',
        'async_support': True,
    },
    'javascript': {
        'indent': 2,
        'style': 'ESLint/Prettier',
        'test_framework': 'Jest',
        'async_support': True,
    },
    'typescript': {
        'indent': 2,
        'style': 'ESLint/Prettier',
        'test_framework': 'Jest',
        'async_support': True,
    },
    'java': {
        'indent': 4,
        'style': 'Google Java Style',
        'test_framework': 'JUnit',
        'async_support': True,
    },
    'cpp': {
        'indent': 2,
        'style': 'Google C++ Style',
        'test_framework': 'Google Test',
        'async_support': True,
    },
    'go': {
        'indent': 'tabs',
        'style': 'gofmt',
        'test_framework': 'testing',
        'async_support': True,
    },
}

def detect_language(file_path):
    """Detect programming language from file extension."""
    _, ext = os.path.splitext(file_path)
    return LANGUAGE_MAP.get(ext.lower(), 'unknown')

def get_language_rules(language):
    """Get formatting rules for a specific language."""
    return LANGUAGE_RULES.get(language, {
        'indent': 4,
        'style': 'Generic',
        'test_framework': 'Unknown',
        'async_support': False,
    })

def get_test_file_name(original_file, language):
    """Generate appropriate test file name based on language conventions."""
    base_name = os.path.splitext(os.path.basename(original_file))[0]
    
    if language == 'python':
        return f"test_{base_name}.py"
    elif language in ['javascript', 'typescript']:
        return f"{base_name}.test.{language[:2]}"
    elif language == 'java':
        return f"{base_name}Test.java"
    elif language == 'go':
        return f"{base_name}_test.go"
    else:
        return f"{base_name}_test.{language}"
