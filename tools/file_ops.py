import os
import shutil
from datetime import datetime

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def write_file(file_path, content):
    try:
        os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing file {file_path}: {str(e)}"

def create_backup(file_path):
    """Create a backup of a file before modification."""
    if not os.path.exists(file_path):
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{file_path}.backup_{timestamp}"
    
    try:
        shutil.copy2(file_path, backup_path)
        return backup_path
    except Exception as e:
        print(f"Warning: Could not create backup: {str(e)}")
        return None

def write_file_safely(file_path, content, create_backup_flag=True):
    """Write file with optional backup."""
    backup_path = None
    
    if create_backup_flag and os.path.exists(file_path):
        backup_path = create_backup(file_path)
    
    result = write_file(file_path, content)
    
    if backup_path:
        return f"{result}\nBackup created: {backup_path}"
    return result

def restore_from_backup(backup_path, original_path):
    """Restore a file from its backup."""
    try:
        shutil.copy2(backup_path, original_path)
        return f"Successfully restored {original_path} from backup"
    except Exception as e:
        return f"Error restoring from backup: {str(e)}"

def list_files(directory, ignore_dirs=None, extensions=None):
    """List files in directory with optional filtering."""
    if ignore_dirs is None:
        ignore_dirs = ['.git', '__pycache__', 'node_modules', '.gemini', '.venv', 'venv']
    
    file_list = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            if extensions is None or any(file.endswith(ext) for ext in extensions):
                file_list.append(os.path.join(root, file))
    return file_list

def get_file_info(file_path):
    """Get metadata about a file."""
    if not os.path.exists(file_path):
        return None
    
    stat = os.stat(file_path)
    return {
        'path': file_path,
        'size': stat.st_size,
        'modified': datetime.fromtimestamp(stat.st_mtime),
        'is_file': os.path.isfile(file_path),
        'is_dir': os.path.isdir(file_path),
    }
