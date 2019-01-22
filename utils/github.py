from github import Github

import config

repository_url = config.repository_url

_acc = Github(login_or_token=config.github_access_token)
_repo = _acc.get_user().get_repo(config.repository_name)


def stats(query):
    values = {
        "stars": _repo.stargazers_count,
        "open_issue_count": len(list(_repo.get_issues(state="open"))),
        "closed_issue_count": len(list(_repo.get_issues(state="closed"))),
        "commits": len(list(_repo.get_commits()))
    }
    return values[query]


def post_issue(author, author_id, content):
    _repo.create_issue(title=f"Bug reported by {author}",
                       body=f"This bug got reported with the bots bug report command.\nReported by: {author} ({author_id})\n\nBug:\n{content}",
                       labels=["Bug Report"])
