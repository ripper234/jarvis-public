#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import format_datetime
from html.parser import HTMLParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_HTML = ROOT / "projects.html"
STATE_PATH = ROOT / "data" / "projects-feed-state.json"
FEED_PATH = ROOT / "projects-feed.xml"
SITE_URL = "https://jarvis.ripper234.com"
FEED_URL = f"{SITE_URL}/projects-feed.xml"


@dataclass
class ProjectCard:
    section: str
    href: str
    tag: str
    title: str
    desc: str

    @property
    def key(self) -> str:
        href = self.href.strip() or self.title.strip().lower()
        return href.rstrip("/")

    @property
    def absolute_href(self) -> str:
        href = self.href.strip()
        if href.startswith("http://") or href.startswith("https://"):
            return href
        return f"{SITE_URL}/{href.lstrip('/')}"

    @property
    def signature(self) -> str:
        payload = "|".join([
            self.section.strip(),
            self.tag.strip(),
            self.title.strip(),
            self.desc.strip(),
            self.href.strip(),
        ])
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class ProjectsHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.projects: list[ProjectCard] = []
        self.current_section = ""
        self.in_h2 = False
        self.capture_field: str | None = None
        self.buffer: list[str] = []
        self.current_card: dict[str, str] | None = None
        self.card_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = {k: (v or "") for k, v in attrs}
        classes = set(attrs_dict.get("class", "").split())

        if tag == "h2":
            self.in_h2 = True
            self.buffer = []
            return

        if tag == "a" and {"card", "project-card"}.issubset(classes):
            self.current_card = {
                "section": self.current_section,
                "href": attrs_dict.get("href", ""),
                "tag": "",
                "title": "",
                "desc": "",
            }
            self.card_depth = 1
            return

        if self.current_card is not None:
            if tag == "a":
                self.card_depth += 1
            if tag == "span" and "tag" in classes:
                self.capture_field = "tag"
                self.buffer = []
            elif tag == "div" and "card-title" in classes:
                self.capture_field = "title"
                self.buffer = []
            elif tag == "div" and "card-desc" in classes:
                self.capture_field = "desc"
                self.buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2" and self.in_h2:
            self.current_section = self._clean("".join(self.buffer))
            self.in_h2 = False
            self.buffer = []
            return

        if self.current_card is not None:
            if self.capture_field and tag in {"span", "div"}:
                self.current_card[self.capture_field] = self._clean("".join(self.buffer))
                self.capture_field = None
                self.buffer = []
            if tag == "a":
                self.card_depth -= 1
                if self.card_depth == 0:
                    self.projects.append(ProjectCard(**self.current_card))
                    self.current_card = None
            return

    def handle_data(self, data: str) -> None:
        if self.in_h2 or self.capture_field:
            self.buffer.append(data)

    @staticmethod
    def _clean(text: str) -> str:
        text = text.replace("\xa0", " ")
        text = re.sub(r"\s+", " ", text)
        return text.strip()


def parse_projects() -> list[ProjectCard]:
    parser = ProjectsHTMLParser()
    parser.feed(PROJECTS_HTML.read_text(encoding="utf-8"))
    return parser.projects


def load_state() -> dict:
    if not STATE_PATH.exists():
        return {"projects": {}}
    return json.loads(STATE_PATH.read_text(encoding="utf-8"))


def rank_status(project: ProjectCard) -> int:
    section_rank = {
        "Ideas": 0,
        "Active Projects": 1,
        "Main Projects": 1,
        "Launched Projects": 2,
    }
    tag_rank = {
        "idea": 0,
        "beta": 1,
        "active": 1,
        "live": 2,
        "deployed": 2,
        "launched": 2,
    }
    return max(section_rank.get(project.section, 0), tag_rank.get(project.tag.lower(), 0))


def event_type(previous: dict | None, project: ProjectCard) -> str:
    if previous is None:
        return "new"
    previous_rank = previous.get("rank", 0)
    current_rank = rank_status(project)
    if current_rank > previous_rank:
        return "matured"
    return "updated"


def event_title(project: ProjectCard, kind: str) -> str:
    if kind == "new":
        prefix = "New project"
    elif kind == "matured":
        prefix = "Project matured"
    else:
        prefix = "Project updated"
    return f"{prefix}: {project.title}"


def update_state(projects: list[ProjectCard]) -> dict:
    state = load_state()
    existing = state.setdefault("projects", {})
    now_iso = datetime.now(timezone.utc).isoformat()
    new_state: dict[str, dict] = {}

    for project in projects:
        prev = existing.get(project.key)
        changed = prev is None or prev.get("signature") != project.signature
        current_rank = rank_status(project)
        if changed:
            kind = event_type(prev, project)
            first_seen = prev.get("firstSeen", now_iso) if prev else now_iso
            last_changed = now_iso
        else:
            kind = prev.get("eventType", "new")
            first_seen = prev.get("firstSeen", now_iso)
            last_changed = prev.get("lastChanged", now_iso)

        new_state[project.key] = {
            "key": project.key,
            "title": project.title,
            "href": project.absolute_href,
            "section": project.section,
            "tag": project.tag,
            "desc": project.desc,
            "signature": project.signature,
            "firstSeen": first_seen,
            "lastChanged": last_changed,
            "eventType": kind,
            "rank": current_rank,
        }

    state["projects"] = new_state
    return state


def build_feed(state: dict) -> ET.Element:
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = "Ron Gross Projects"
    ET.SubElement(channel, "link").text = f"{SITE_URL}/projects.html"
    ET.SubElement(channel, "description").text = (
        "New projects and major project-status updates from Ron Gross."
    )
    ET.SubElement(channel, "language").text = "en"
    ET.SubElement(channel, "generator").text = "jarvis-public/scripts/generate_projects_feed.py"

    items = sorted(
        state.get("projects", {}).values(),
        key=lambda item: item.get("lastChanged", ""),
        reverse=True,
    )

    if items:
        latest = datetime.fromisoformat(items[0]["lastChanged"])
    else:
        latest = datetime.now(timezone.utc)
    ET.SubElement(channel, "lastBuildDate").text = format_datetime(latest)
    ET.SubElement(channel, "atom:link", {
        "xmlns:atom": "http://www.w3.org/2005/Atom",
        "href": FEED_URL,
        "rel": "self",
        "type": "application/rss+xml",
    })

    for item in items:
        event_dt = datetime.fromisoformat(item["lastChanged"])
        title = event_title(ProjectCard(
            section=item["section"],
            href=item["href"],
            tag=item["tag"],
            title=item["title"],
            desc=item["desc"],
        ), item.get("eventType", "updated"))
        description = (
            f"{item['desc']} ({item['tag']} • {item['section']})"
            if item.get("tag")
            else f"{item['desc']} ({item['section']})"
        )
        feed_item = ET.SubElement(channel, "item")
        ET.SubElement(feed_item, "title").text = title
        ET.SubElement(feed_item, "link").text = item["href"]
        ET.SubElement(feed_item, "guid").text = f"{item['key']}#{item['lastChanged']}"
        ET.SubElement(feed_item, "pubDate").text = format_datetime(event_dt)
        ET.SubElement(feed_item, "description").text = description

    return rss


def write_xml(root: ET.Element) -> None:
    xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    FEED_PATH.write_bytes(xml)


def main() -> None:
    projects = parse_projects()
    state = update_state(projects)
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_xml(build_feed(state))
    print(f"Generated {FEED_PATH.relative_to(ROOT)} for {len(projects)} projects")


if __name__ == "__main__":
    main()
