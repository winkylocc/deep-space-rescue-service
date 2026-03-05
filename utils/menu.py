from __future__ import annotations

from typing import Callable, Dict, Generic, List, TypeVar

T = TypeVar("T")

def choose_from_options(
        option: Dict[str, T],
        *,
        title: str = "Choose an option:",
        line_formatter: Callable[[str, T], str] | None = None,
        prompt: str = "> "
) -> T:
    """Generic menu using numbered options to select for a {name: object} catalog"""

    if not option:
        raise ValueError("Catalog is empty.")
    keys: List[str] = list(option.keys())

    if line_formatter is None:
        # Default: "1) Key"
        line_formatter = lambda key, item: f"{key}"

    while True:
        print(f"\n{title}")
        for i, key in enumerate(keys, start=1):
            item = option[key]
            print(f"{i}) {line_formatter(key, item)}")

        raw = input(prompt).strip()
        try:
            choice = int(raw)
        except ValueError:
            print("Invalid input. Please enter a whole number (ex: 1).")
            continue
        if 1<= choice <= len(keys):
            selected_key = keys[choice -1]
            return option[selected_key]
        
        print(f"Please enter a number between 1 and {len(keys)}.")