#!/usr/bin/env python3
"""Semantic validation for Unraid CA template XML files."""

import glob
import re
import sys
import xml.etree.ElementTree as ET

BLACKLISTED_CHARS = re.compile(r'[<>&"\']')

WARNINGS = 0
ERRORS = 0


def warn(msg):
    global WARNINGS
    WARNINGS += 1
    print(f"  WARNING: {msg}")


def error(msg):
    global ERRORS
    ERRORS += 1
    print(f"  ERROR: {msg}")


def check_template(path):
    print(f"\nChecking {path}...")
    try:
        tree = ET.parse(path)
    except ET.ParseError as e:
        error(f"Invalid XML: {e}")
        return

    root = tree.getroot()
    name_el = root.find("Name")
    name = name_el.text if name_el is not None else path

    # Required tags
    repo = root.find("Repository")
    if repo is None or not repo.text:
        error(f"{name}: Missing or empty <Repository>")

    network = root.find("Network")
    if network is None or not network.text:
        error(f"{name}: Missing or empty <Network>")

    # Recommended tags
    support = root.find("Support")
    if support is None or not support.text:
        warn(f"{name}: Missing <Support> link")

    project = root.find("Project")
    if project is None or not project.text:
        warn(f"{name}: Missing <Project> link")

    category = root.find("Category")
    if category is None or not category.text:
        warn(f"{name}: Missing <Category>")

    registry = root.find("Registry")
    if registry is None or not registry.text:
        warn(f"{name}: Missing <Registry>")

    icon = root.find("Icon")
    if icon is None or not icon.text:
        warn(f"{name}: Missing <Icon>")

    # Check for "Converted By Community Applications" in Overview
    overview = root.find("Overview")
    if overview is not None and overview.text:
        if "Converted By Community Applications" in overview.text:
            error(f"{name}: Overview contains 'Converted By Community Applications' (auto-converted template)")

    # Check for blacklisted chars in user-input tags
    user_tags = ["Name", "Overview", "Description"]
    for tag_name in user_tags:
        el = root.find(tag_name)
        if el is not None and el.text:
            if BLACKLISTED_CHARS.search(el.text):
                warn(f"{name}: <{tag_name}> contains blacklisted characters")

    # Warn about unnecessary tags
    unnecessary = ["DateInstalled", "Networking", "Data", "Environment"]
    for tag_name in unnecessary:
        if root.find(tag_name) is not None:
            warn(f"{name}: Unnecessary tag <{tag_name}> found")

    # Validate WebUI port matches a Config port target
    webui = root.find("WebUI")
    if webui is not None and webui.text:
        port_match = re.search(r'\[PORT:(\d+)\]', webui.text)
        if port_match:
            webui_port = port_match.group(1)
            found = False
            for config in root.findall("Config"):
                if config.get("Type") == "Port" and config.get("Target") == webui_port:
                    found = True
                    break
            if not found:
                warn(f"{name}: WebUI port {webui_port} doesn't match any Config port Target")


def main():
    templates = sorted(glob.glob("templates/*.xml"))
    if not templates:
        print("No XML templates found.")
        sys.exit(0)

    for path in templates:
        check_template(path)

    print(f"\n{'='*40}")
    print(f"Checked {len(templates)} templates: {ERRORS} errors, {WARNINGS} warnings")
    sys.exit(1 if ERRORS > 0 else 0)


if __name__ == "__main__":
    main()
