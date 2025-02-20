from pathlib import Path

def find_project_root(current_file: str) -> Path:
    """Intelligently find the project root directory"""
    current_path = Path(current_file).resolve()
    
    # Development mode: go up 3 levels from src/chatanvil/utils/project.py
    for _ in range(3):
        current_path = current_path.parent
    
    # Check if it is the project root directory (contains pyproject.toml or .env)
    if (current_path / "pyproject.toml").exists() or (current_path / ".env").exists():
        return current_path
    
    # Installation mode: try the current working directory
    cwd = Path.cwd()
    if (cwd / ".env").exists():
        return cwd
    
    # Finally, fall back to the development mode path
    return current_path