#!/usr/bin/env python3
"""Generate MODS.md from mod data."""

import json
import re
from pathlib import Path
from typing import NamedTuple

import diskcache  # type: ignore
import requests
from bs4 import BeautifulSoup

cache = diskcache.Cache(".mods_cache")  # type: ignore


class ModInfo(NamedTuple):
    """Information about a mod."""

    mod_id: str
    name: str
    summary: str


MODS: dict[str, tuple[str, ...]] = {
    "ArmA Ukraine": (
        "6532E6F9EB9EFCE1",
        "6609256947C552DA",
        "665AD1CC40E3710F",
        "6630F76C73A2532B",
    ),
    "ACE": (
        "60C4E0B49618CC62",
        "5DBD560C5148E1DA",
        "5EB744C5F42E0800",
        "606C369BAC3F6CC3",
        "60C4C12DAE90727B",
        "60C53A9372ED3964",
        "60E573C9B04CC408",
        "60EAEA0389DB3CC2",
        "611CB1D409001EB0",
        "61226BB18D360BDD",
        "61B7763A8AEB53B7",
        "62F802951CC8A37E",
        "64475DC102F2BDA4",
        "646D52AF8BB3FF15",
    ),
    "Монстри": (
        "622120A5448725E3",
        "6534B9CEB6D12EE7",
        "65F2F0F322747C37",
    ),
    "Ігрові Режими": (
        "CAFEBABEF0CACC1A",
        "631B4E07FFD86258",
        "59B657D731E2A11D",
        "664E0A097C173E83",
    ),
    "Фракції": (
        "65DB713038B8533C",
        "64CF25A41DCBDBE0",
        "624A8B96AA67EFEB",
        "595F2BF2F44836FB",
    ),
    "Зброя": (
        "620E584B1D2C96A4",
        "61BD6595183FCEBD",
        "5AB301290317994A",
        "60E6F54E174C53C5",
        "61344BDC155A5A28",
        "6190F1B505C08562",
        "62A711001B8FDEEA",
    ),
    "Одяг": ("655EE30F57F15220",),
    "Техніка": ("617AC5E57EF1D9E3",),
    "Game Master": (
        "60CC94C046837439",
        "5994AD5A9F33BE57",
        "5964E0B3BB7410CE",
        "5EB51D581C99E590",
        "5F2944B7474F043F",
        "65784C1E51244157",
    ),
    "Ігролад і зручність": (
        "656AC01634459D8D",
        "6548DCE9E8C60CA6",
        "648297C0F03CE43A",
        "631CA3F82A68518D",
        "606B100247F5C709",
        "6052A9DD45564825",
        "5F27399D7277A18A",
        "5F268647F8A1A1F4",
        "5EF8AADD3B3C81F2",
        "5DAC39D2C3D4C8CD",
        "5C9758250C8C56F1",
        "612556FA56F1B1FF",
    ),
    "Звук та візуал": (
        "64ED6553B8AF6B62",
        "62FCEB51DF8527B6",
        "59673B6FBB95459F",
        "59651354B2904BA6",
        "658B25CD90247D38",
    ),
    "Карти": (
        "6489749415C9E6DE",
        "5D58A217A9611AFB",
    ),
    "Проблемні моди": ("59674C21AA886D57",),
}


def fetch_mod_info(mod_url: str) -> tuple[str, str]:
    """Fetch the title and summary from the mod's workshop page."""
    try:
        response = requests.get(mod_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Get title
        title_tag = soup.find("title")
        title: str = "Unknown"
        if title_tag:
            title = title_tag.text.strip()
            # Remove common suffixes like " - Arma Reforger"
            title = re.sub(r"\s*-\s*Arma Reforger.*$", "", title)

        # Get summary/description
        summary: str = ""
        # Look for description meta tag or workshop description
        desc_tag = soup.find("meta", {"name": "description"})
        if desc_tag and desc_tag.get("content"):  # type: ignore
            summary = str(desc_tag["content"].strip())  # type: ignore

        return title, summary
    except Exception as e:
        print(f"Failed to fetch info for {mod_url}: {e}")

    # Fallback to URL-based name
    match = re.search(r"/workshop/[A-F0-9]+-(.+)$", mod_url)
    title = match.group(1) if match else "Unknown"
    return title, ""


@cache.memoize()  # type: ignore
def extract_mod_info(mod_id: str) -> ModInfo:
    """Extract mod ID and fetch title and summary from workshop page."""
    mod_url = f"https://reforger.armaplatform.com/workshop/{mod_id}"
    mod_name, mod_summary = fetch_mod_info(mod_url)
    return ModInfo(mod_id=mod_id, name=mod_name, summary=mod_summary)


def validate_no_duplicates() -> None:
    """Validate that there are no duplicate mod IDs across all categories."""
    all_mod_ids: list[str] = []
    for mod_ids in MODS.values():
        all_mod_ids.extend(mod_ids)

    duplicates: set[str] = set()
    seen: set[str] = set()
    for mod_id in all_mod_ids:
        if mod_id in seen:
            duplicates.add(mod_id)
        seen.add(mod_id)

    if duplicates:
        raise ValueError(f"Duplicate mod IDs found: {sorted(duplicates)}")


def generate_mods_md():
    """Generate MODS.md file with URLs and JSON snippets."""
    validate_no_duplicates()
    content: list[str] = [
        "# MODS",
        "",
        "Курований список перевірених модів що використовуються спільнотою.",
        "",
    ]

    for category, mod_ids in MODS.items():
        # Add category header
        content.append(f"## {category}")
        content.append("")

        for mod_id in mod_ids:
            mod_info = extract_mod_info(mod_id)
            mod_url = f"https://reforger.armaplatform.com/workshop/{mod_info.mod_id}"

            # Add mod header as URL
            content.append(f"### [{mod_info.name}]({mod_url})")
            content.append("")

            # Add summary if available
            if mod_info.summary:
                content.append(mod_info.summary)
                content.append("")

            # Add JSON snippet
            mod_json = {"modId": mod_info.mod_id, "name": mod_info.name}
            json_str = json.dumps(mod_json, indent=4)
            content.extend(
                [
                    "```json",
                    json_str + ",",
                    "```",
                    "",
                ]
            )

    mods_md_path = Path(__file__).parent / "MODS.md"
    mods_md_path.write_text("\n".join(content), encoding="utf-8")
    print(f"Generated {mods_md_path}")


if __name__ == "__main__":
    generate_mods_md()
