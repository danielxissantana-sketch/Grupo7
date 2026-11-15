import os
from pathlib import Path

class WorkspaceTools:
    def __init__(self, workspace_dir: str = "/workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(parents=True, exist_ok=True)

    def list_files(self) -> list:
        files = []
        for path in self.workspace_dir.glob("**/*"):
            if path.is_file() and not ".git" in path.parts:
                files.append(str(path.relative_to(self.workspace_dir)))
        return files

    def read_file(self, file_path: str) -> str:
        full_path = self.workspace_dir / file_path
        if not full_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, file_path: str, content: str) -> str:
        full_path = self.workspace_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Arquivo {file_path} alterado com sucesso."
