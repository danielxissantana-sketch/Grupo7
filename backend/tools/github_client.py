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
            base_ref = self.repo.get_git_ref(f"heads/{base_branch}")
            try:
                existing_ref = self.repo.get_git_ref(f"heads/{head_branch}")
                existing_ref.edit(sha=base_ref.object.sha, force=True)
            except GithubException:
                self.repo.create_git_ref(ref=f"refs/heads/{head_branch}", sha=base_ref.object.sha)

            file_path = f"resolucoes/{head_branch}.md"
            commit_msg = f"feat: {title}"
            try:
                existing_file = self.repo.get_contents(file_path, ref=head_branch)
                self.repo.update_file(
                    path=file_path,
                    message=commit_msg,
                    content=body,
                    sha=existing_file.sha,
                    branch=head_branch
                )
            except GithubException:
                self.repo.create_file(
                    path=file_path,
                    message=commit_msg,
                    content=body,
                    branch=head_branch
                )

            open_prs = self.repo.get_pulls(state="open", head=f"{self.repo.owner.login}:{head_branch}", base=base_branch)
            if open_prs.totalCount > 0:
                return open_prs[0].html_url

            pr = self.repo.create_pull(
                title=title,
                body=body,
                head=head_branch,
                base=base_branch
            )
            return pr.html_url
        except GithubException as e:
            error_msg = e.data.get('message', str(e)) if hasattr(e, 'data') else str(e)
            print("ERRO REAL DO GITHUB:", e.status, getattr(e, 'data', str(e)), flush=True)
            raise Exception(f"GitHub ({e.status}): {error_msg}")