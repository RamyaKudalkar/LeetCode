import os
import re
import time
import requests
from collections import Counter


# ==================================================
# SETTINGS
# ==================================================

BASE_FOLDER = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

LEETCODE_URL = "https://leetcode.com/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0"
}


# ==================================================
# GET LEETCODE SLUG FROM README
# ==================================================

def get_slug_from_readme(folder):

    readme_path = os.path.join(
        BASE_FOLDER,
        folder,
        "README.md"
    )

    if not os.path.exists(readme_path):
        return None

    with open(
        readme_path,
        "r",
        encoding="utf-8"
    ) as file:
        content = file.read()

    match = re.search(
        r"leetcode\.com/problems/([^/?\"\s]+)",
        content,
        re.IGNORECASE
    )

    if match:
        return match.group(1)

    return None


# ==================================================
# GET PROBLEM INFORMATION FROM LEETCODE
# ==================================================

def get_problem_info(slug):

    query = """
    query($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            title
            difficulty
        }
    }
    """

    # Retry up to 3 times if LeetCode times out
    for attempt in range(3):

        try:

            response = requests.post(
                LEETCODE_URL,
                json={
                    "query": query,
                    "variables": {
                        "titleSlug": slug
                    }
                },
                headers=HEADERS,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            question = (
                data
                .get("data", {})
                .get("question")
            )

            if question:
                return question

        except requests.RequestException as e:

            print(
                f"⚠️ Attempt {attempt + 1}/3 "
                f"failed for {slug}: {e}"
            )

            if attempt < 2:
                time.sleep(2)

    return None


# ==================================================
# FIND ALL LEETCODE PROBLEM FOLDERS
# ==================================================

problem_folders = []

for item in os.listdir(BASE_FOLDER):

    path = os.path.join(
        BASE_FOLDER,
        item
    )

    if (
        os.path.isdir(path)
        and item
        and item[0].isdigit()
    ):

        problem_folders.append(item)


problem_folders.sort()


# ==================================================
# COLLECT LEETCODE INFORMATION
# ==================================================

difficulty_count = Counter()

solved_problems = []

failed_problems = []

print(
    "Fetching LeetCode information...\n"
)


for folder in problem_folders:

    slug = get_slug_from_readme(
        folder
    )

    if not slug:

        print(
            f"⚠️ Could not find slug: {folder}"
        )

        failed_problems.append(folder)

        continue

    info = get_problem_info(
        slug
    )

    if not info:

        print(
            f"❌ Failed after 3 attempts: {slug}"
        )

        failed_problems.append(folder)

        continue

    title = info["title"]

    difficulty = info["difficulty"]

    solved_problems.append(
        title
    )

    difficulty_count[
        difficulty
    ] += 1

    print(
        f"✓ {title}"
    )


# ==================================================
# STOP IF ANY PROBLEM FAILED
# ==================================================

if failed_problems:

    print(
        "\n========================================"
    )

    print(
        "README WAS NOT UPDATED"
    )

    print(
        "========================================"
    )

    print(
        "\nThe following problems could not be fetched:"
    )

    for problem in failed_problems:

        print(
            f"- {problem}"
        )

    print(
        "\nPlease run the script again."
    )

    print(
        "Your existing README was left unchanged."
    )

    raise SystemExit(1)


# ==================================================
# TOTAL SOLVED
# ==================================================

total_solved = len(
    problem_folders
)


# ==================================================
# README DASHBOARD
# ==================================================

dashboard = f"""### 🎯 Total Solved

**{total_solved} Problems**

### 📈 Difficulty

| Difficulty | Problems |
|------------|----------:|
| 🟢 Easy | {difficulty_count['Easy']} |
| 🟠 Medium | {difficulty_count['Medium']} |
| 🔴 Hard | {difficulty_count['Hard']} |

"""


# ==================================================
# UPDATE README
# ==================================================

readme_path = os.path.join(
    BASE_FOLDER,
    "README.md"
)

with open(
    readme_path,
    "r",
    encoding="utf-8"
) as file:

    readme = file.read()


start_marker = (
    "<!-- LEETCODE_PROGRESS_START -->"
)

end_marker = (
    "<!-- LEETCODE_PROGRESS_END -->"
)


start = readme.find(
    start_marker
)

end = readme.find(
    end_marker
)


if start == -1 or end == -1:

    print(
        "\n⚠️ README markers were not found."
    )

    raise SystemExit(1)


start_content = (
    start
    + len(start_marker)
)


new_readme = (
    readme[:start_content]
    + "\n\n"
    + dashboard
    + readme[end:]
)


with open(
    readme_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        new_readme
    )


# ==================================================
# FINAL RESULT
# ==================================================

print(
    "\n========================================"
)

print(
    "README UPDATED SUCCESSFULLY!"
)

print(
    "========================================"
)

print(
    f"\nTotal Solved: {total_solved}"
)

print(
    f"Easy: {difficulty_count['Easy']}"
)

print(
    f"Medium: {difficulty_count['Medium']}"
)

print(
    f"Hard: {difficulty_count['Hard']}"
)

print(
    "\nYour README was updated successfully! 🚀"
)