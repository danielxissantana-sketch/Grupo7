import os
from github import Github, GithubException

class GitHubClient:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo_name = os.getenv("GITHUB_REPO")
        if not self.token or not self.repo_name:
            raise ValueError("GITHUB_TOKEN e GITHUB_REPO devem estar configurados no ambiente.")
        
        self.g = Github(self.token)
        self.repo = self.g.get_repo(self.repo_name)

    def get_issue(self, issue_number: int) -> dict:
        try:
            issue = self.repo.get_issue(number=issue_number)
            return {
                "number": issue.number,
                "title": issue.title,
                "body": issue.body or "",
                "user": issue.user.login,
                "labels": [label.name for label in issue.labels]
            }
        except GithubException as e:
            raise Exception(f"Erro ao buscar issue #{issue_number}: {e.data.get('message', str(e))}")

    def create_pull_request(self, title: str, body: str, head_branch: str, base_branch: str = "main") -> str:
        try:
            pr = self.repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base_branch
            )
            return pr.html_url
        except GithubException as e:
            raise Exception(f"Erro ao criar Pull Request: {e.data.get('message', str(e))}")
