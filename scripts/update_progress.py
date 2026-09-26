import os
import re
import time
import math
import html
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
        r"leetcode\.com/problems/([^\"/?]+)",
        content
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
            topicTags {
                name
            }
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
# GENERATE LEETCODE-STYLE TOPIC BUBBLE CHART
# ==================================================

def generate_topic_bubbles(topic_count):

    assets_folder = os.path.join(
        BASE_FOLDER,
        "assets"
    )

    os.makedirs(
        assets_folder,
        exist_ok=True
    )

    svg_path = os.path.join(
        assets_folder,
        "topic-bubbles.svg"
    )

    topics = topic_count.most_common()

    if not topics:
        return

    # ------------------------------------------------
    # CANVAS
    # ------------------------------------------------

    width = 1000
    height = 700

    # ------------------------------------------------
    # BUBBLE SIZE
    # ------------------------------------------------

    max_count = max(
        topic_count.values()
    )

    bubbles = []

    for topic, count in topics:

        # Bigger topic count = bigger bubble
        #
        # The square-root scaling keeps the bubbles
        # visually balanced.

        radius = (
            38
            + 82 * math.sqrt(
                count / max_count
            )
        )

        bubbles.append({
            "topic": topic,
            "count": count,
            "radius": radius,
            "x": width / 2,
            "y": height / 2
        })

    # ------------------------------------------------
    # INITIAL POSITIONS
    # ------------------------------------------------

    for i, bubble in enumerate(bubbles):

        angle = i * 2.39996

        distance = (
            20
            + i * 48
        )

        bubble["x"] = (
            width / 2
            + math.cos(angle) * distance
        )

        bubble["y"] = (
            height / 2
            + math.sin(angle) * distance
        )

    # ------------------------------------------------
    # BUBBLE PACKING
    # ------------------------------------------------

    for _ in range(700):

        moved = False

        for i in range(len(bubbles)):

            a = bubbles[i]

            for j in range(i + 1, len(bubbles)):

                b = bubbles[j]

                dx = (
                    b["x"]
                    - a["x"]
                )

                dy = (
                    b["y"]
                    - a["y"]
                )

                distance = math.sqrt(
                    dx * dx
                    + dy * dy
                )

                minimum_distance = (
                    a["radius"]
                    + b["radius"]
                    + 7
                )

                if distance < minimum_distance:

                    if distance == 0:

                        dx = 1
                        dy = 0
                        distance = 1

                    push = (
                        minimum_distance
                        - distance
                    ) / 2

                    dx /= distance
                    dy /= distance

                    a["x"] -= (
                        dx * push
                    )

                    a["y"] -= (
                        dy * push
                    )

                    b["x"] += (
                        dx * push
                    )

                    b["y"] += (
                        dy * push
                    )

                    moved = True

        # ------------------------------------------------
        # KEEP BUBBLES INSIDE CANVAS
        # ------------------------------------------------

        for bubble in bubbles:

            r = bubble["radius"]

            bubble["x"] = max(
                r + 15,
                min(
                    width - r - 15,
                    bubble["x"]
                )
            )

            bubble["y"] = max(
                r + 15,
                min(
                    height - r - 15,
                    bubble["y"]
                )
            )

        if not moved:
            break

    # ==================================================
    # SVG
    # ==================================================

    svg = f'''<svg
xmlns="http://www.w3.org/2000/svg"
width="{width}"
height="{height}"
viewBox="0 0 {width} {height}">

<rect
width="100%"
height="100%"
fill="white"/>

<style>

.bubble {{
    fill: #f0f0f0;
    stroke: #d9d9d9;
    stroke-width: 1;
}}

.topic {{
    fill: #008000;
    font-family: Arial, sans-serif;
    font-size: 15px;
    font-weight: 500;
    text-anchor: middle;
    dominant-baseline: middle;
}}

.count {{
    fill: #008000;
    font-family: Arial, sans-serif;
    font-size: 14px;
    font-weight: 600;
    text-anchor: middle;
    dominant-baseline: middle;
}}

</style>
'''

    # ==================================================
    # DRAW BUBBLES
    # ==================================================

    for bubble in bubbles:

        x = bubble["x"]
        y = bubble["y"]
        r = bubble["radius"]

        topic = bubble["topic"]
        count = bubble["count"]

        # ------------------------------------------------
        # BREAK LONG TOPIC NAMES
        # ------------------------------------------------

        words = topic.split()

        lines = []

        current = ""

        for word in words:

            test = (
                current
                + " "
                + word
            ).strip()

            if len(test) <= 15:

                current = test

            else:

                if current:
                    lines.append(current)

                current = word

        if current:
            lines.append(current)

        # ------------------------------------------------
        # CIRCLE
        # ------------------------------------------------

        svg += f'''
<circle
class="bubble"
cx="{x:.2f}"
cy="{y:.2f}"
r="{r:.2f}"/>
'''

        # ------------------------------------------------
        # TOPIC NAME
        # ------------------------------------------------

        if len(lines) == 1:

            topic_y = y - 8

            svg += f'''
<text
class="topic"
x="{x:.2f}"
y="{topic_y:.2f}">
{html.escape(lines[0])}
</text>
'''

        else:

            start_y = (
                y
                - (
                    len(lines)
                    * 8
                )
            )

            for index, line in enumerate(lines):

                svg += f'''
<text
class="topic"
x="{x:.2f}"
y="{start_y + index * 17:.2f}">
{html.escape(line)}
</text>
'''

        # ------------------------------------------------
        # QUESTION COUNT
        # ------------------------------------------------

        svg += f'''
<text
class="count"
x="{x:.2f}"
y="{y + 20:.2f}">
{count}
</text>
'''

    # ------------------------------------------------
    # CLOSE SVG
    # ------------------------------------------------

    svg += """
</svg>
"""

    # ==================================================
    # SAVE SVG
    # ==================================================

    with open(
        svg_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(svg)

    print(
        f"✓ Topic bubble chart generated: "
        f"{svg_path}"
    )


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

topic_count = Counter()

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
            f"⚠️ Could not find slug: "
            f"{folder}"
        )

        failed_problems.append(folder)

        continue

    info = get_problem_info(
        slug
    )

    if not info:

        print(
            f"❌ Failed after 3 attempts: "
            f"{slug}"
        )

        failed_problems.append(folder)

        continue

    title = info["title"]

    difficulty = info["difficulty"]

    topics = [
        tag["name"]
        for tag in info["topicTags"]
    ]

    solved_problems.append(
        title
    )

    difficulty_count[
        difficulty
    ] += 1

    for topic in topics:

        topic_count[
            topic
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
        "\nThe following problems "
        "could not be fetched:"
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
# GENERATE TOPIC BUBBLES
# ==================================================

generate_topic_bubbles(
    topic_count
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

### 🧠 Topics

![LeetCode Topics](assets/topic-bubbles.svg)

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
    "\nYour README now contains "
    "the LeetCode-style topic bubbles! 🚀"
)