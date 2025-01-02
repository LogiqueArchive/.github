from aiohttp import ClientSession
from asyncio import run
from typing import List
from datetime import datetime


async def fetch_repos(username: str):
    url = f'https://api.github.com/users/{username}/repos'
    async with ClientSession() as session:
        async with session.get(url) as response:
            print(response.status)
            if response.status == 200:
                repos = await response.json()
                return repos
            else:
                print(f"Failed to fetch repositories for user {username}")
                return []


def sort_repos(repos_obj: List[dict]):
    main_text = (
        "<div align='center'>\n"
        "<h1>🌟 Welcome to My Archive of Repositories 🌟</h1>\n"
        "<p>A curated list of all my public repositories on GitHub.</p>\n"
        "</div>\n\n"
        "---\n\n"
        "## 📜 Repository List\n\n"
    )

    for repo in repos_obj:
        repo_name = repo.get('name', 'Unknown')
        description = repo.get('description', 'No description available.')
        created_at = repo.get('created_at', None)
        stars = repo.get('stargazers_count', 0)
        forks = repo.get('forks_count', 0)
        top_language = repo.get('language', 'Unknown')

        created_at_utc = (
            datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S UTC")
            if created_at
            else "Unknown creation date"
        )

        main_text += (
            f"### 📂 [{repo_name}](https://github.com/LogiqueArchive/{repo_name})\n"
            f"- **Description**: {description}\n"
            f"- **Created At**: {created_at_utc}\n"
            f"- **Stars**: ⭐ {stars}\n"
            f"- **Forks**: 🍴 {forks}\n"
            f"- **Top Language**: {top_language}\n\n"
        )

    main_text += (
        "---\n\n"
        "<div align='center'>\n"
        "<p>⭐ Feel free to explore, fork, and contribute! ⭐</p>\n"
        "</div>\n"
    )

    return main_text


async def main():
    username = 'LogiqueArchive'
    repos = await fetch_repos(username)
    text = sort_repos(repos)

    with open("README.md", "w") as file:
        file.write(text)


if __name__ == '__main__':
    run(main())
