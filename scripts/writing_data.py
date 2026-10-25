"""Shared data for the Writing tab (build-home.py) and /reading (build-reading.py).

Add an article:  append one dict to the top of READING.
Fields: title, author, source, url, added (YYYY-MM-DD), topics (list), summary
(neutral, one sentence; leave "" to show no summary), note (Chae's own takeaway; leave "" to show none).
Add an essay: append one dict to ESSAYS (title, url, published, description). Set
"internal": True for a page on this site. "published" is YYYY-MM-DD or YYYY-MM, or "" if unknown.
Then run build-reading.py, build-home.py, build-llms.py and build-sitemap.py.
"""

# Newest first. Keep summaries neutral and in your own words; never paste article text.
READING = [
    {
        "title": "Product Management is Still All About Telling Stories",
        "author": "Josh Elman",
        "source": "a16z newsletter",
        "url": "https://www.a16z.news/p/product-management-is-still-all-about",
        "added": "2026-10-14",
        "topics": ["Product management", "AI"],
        "summary": "Elman argues that as AI makes building software cheaper and faster, a product manager's core value shifts to judgment about what to build and to communicating a product's purpose, especially through onboarding.",
        "note": "",
    },
    {
        "title": "A Product Manager's Job",
        "author": "Josh Elman",
        "source": "Medium",
        "url": "https://joshelman.medium.com/a-product-managers-job-63c09a43d0ec",
        "added": "2026-10-14",
        "topics": ["Product management"],
        "summary": "A short essay on what a product manager is responsible for, framing the job as helping a team ship the right product for users and breaking it into five smaller parts.",
        "note": "",
    },
    {
        "title": "My Blueprint",
        "author": "Josh Elman",
        "source": "Medium",
        "url": "https://joshelman.medium.com/my-blueprint-9693a6059a1a",
        "added": "2026-10-14",
        "topics": ["Working style", "Career"],
        "summary": "Elman shares his own personal blueprint, a written outline of how he works and his quirks, inspired by a friend's essay on the practice.",
        "note": "",
    },
    {
        "title": "51",
        "author": "Josh Elman",
        "source": "Medium",
        "url": "https://joshelman.medium.com/51-7fbfb877e869",
        "added": "2026-10-14",
        "topics": ["Career"],
        "summary": "",  # TODO: Medium blocked fetching; title taken from the URL slug. Confirm title and write a one-sentence summary.
        "note": "",
    },
]

# Chae's own essays, newest first. Descriptions are one neutral sentence; never
# include family or memoir details, money amounts, or names of other people.
ESSAYS = [
    {
        "title": "What\u2019s the Point of Preinstalled Apps?",
        "url": "/projects/preinstalled-apps",
        "internal": True,
        "published": "2026-10",
        "description": "What if a new iPhone greeted you with Siri instead of pages of apps? On Siri becoming the operating system, and what that means for apps, Apple, and the App Store.",
    },
    {
        "title": "2025–2026 Reflections: Onwards",
        "url": "https://chaewoonkim.medium.com/2025-2026-reflections-onwards-2bc4a878e448",
        "published": "2026-01-15",  # Medium RSS feed pubDate
        "description": "A personal essay reflecting on the last couple of years and what comes next.",
    },
    {
        "title": "A Story About Money",
        "url": "https://chaewoonkim.medium.com/a-story-about-money-afedd3e1ee00",
        "published": "2025-07-22",  # Medium RSS feed pubDate
        "description": "A personal essay on money.",
    },
]


MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def pub_label(p):
    """'2026-10' -> 'October 2026'; '2026-10-07' -> 'October 7, 2026'."""
    parts = p.split("-")
    if len(parts) == 2:
        return f"{MONTHS[int(parts[1]) - 1]} {parts[0]}"
    return f"{MONTHS[int(parts[1]) - 1]} {int(parts[2])}, {parts[0]}"
