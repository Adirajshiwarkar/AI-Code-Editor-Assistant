from crewai.tools import tool
from tools.file_ops import read_file, write_file, list_files
import os

@tool("read_file_tool")
def read_file_tool(file_path: str) -> str:
    """Reads the content of a file given its path."""
    return read_file(file_path)

@tool("write_file_tool")
def write_file_tool(file_path: str, content: str) -> str:
    """Writes content to a file. Overwrites if it exists."""
    return write_file(file_path, content)

@tool("list_files_tool")
def list_files_tool(directory: str) -> str:
    """Lists all files in a directory recursively."""
    files = list_files(directory)
    return "\n".join(files)
