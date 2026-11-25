"""Render real public GitHub statistics without a third-party image service."""

import json
import os
import re
from datetime import datetime, timezone
from html import escape
from pathlib import Path
from urllib.request import Request, urlopen


def api(path, payload=None):
    token = os.environ["GH_TOKEN"]
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "Jussixss-profile-assets",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    data = None
    if payload is not None:
        data = json.dumps(payload).encode()
        headers["Content-Type"] = "application/json"
    request = Request("https://api.github.com/" + path, data=data, headers=headers)
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
    if isinstance(result, dict) and result.get("errors"):
        raise RuntimeError("GitHub GraphQL returned errors; preserving the last good assets")
    return result


def render(owner, account, stars, contributions, date):
    metrics = [
        ("PUBLIC REPOS", account["public_repos"]),
        ("STARS / OWNED REPOS", stars),
        ("FOLLOWERS", account["followers"]),
        ("CONTRIBUTIONS / YEAR", contributions),
    ]
    cells = []
    for index, (label, value) in enumerate(metrics):
        x = 35 + index * 248
        cells.append(f'<text x="{x}" y="117" class="value">{int(value):,}</text>'
                     f'<text x="{x}" y="151" class="label">{label}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1040" height="210" viewBox="0 0 1040 210" role="img" aria-labelledby="title desc">
  <title id="title">{escape(owner)} GitHub statistics</title>
  <desc id="desc">Public repository and follower counts, stars on owned public repositories, and contributions during GitHub's last-year window. Updated {date} UTC.</desc>
  <style>.label{{font:12px monospace;fill:#b3a1c7;letter-spacing:1px}}.value{{font:bold 42px Arial,sans-serif;fill:#f3eaff}}</style>
  <rect x="1" y="1" width="1038" height="208" rx="14" fill="#0e0b1b" stroke="#48315f"/>
  <path d="M283 72V166M531 72V166M779 72V166" stroke="#322446"/>
  <text x="35" y="38" class="label" style="fill:#43f4f4">GITHUB / {escape(owner.upper())}</text>
  <text x="1005" y="38" text-anchor="end" class="label">PUBLIC SIGNAL</text>
  {''.join(cells)}
  <text x="35" y="189" class="label">UPDATED {date} UTC · DAILY SNAPSHOT</text>
</svg>
'''


def main():
    owner = os.environ.get("PROFILE_OWNER", "Jussixss")
    if not re.fullmatch(r"[A-Za-z0-9-]{1,39}", owner):
        raise ValueError("Invalid GitHub username")
    account = api(f"users/{owner}")
    repos = []
    page = 1
    while True:
        batch = api(f"users/{owner}/repos?type=owner&per_page=100&page={page}")
        repos.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    stars = sum(repo["stargazers_count"] for repo in repos)
    result = api("graphql", {
        "query": "query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions}}}}",
        "variables": {"login": owner},
    })
    contributions = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    target = Path("assets/generated/stats.svg")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render(owner, account, stars, contributions, date), encoding="utf-8")
    print(f"Rendered statistics for {owner} from GitHub API")


if __name__ == "__main__":
    main()
