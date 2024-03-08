from __future__ import annotations

import collections
import string
import time
import typing
from contextlib import suppress
from functools import lru_cache
from typing import Literal
from typing import Sequence
from typing import TypedDict

import easyocr  # type: ignore[import-untyped]
import numpy as np
from ahk import AHK
from ahk.directives import NoTrayIcon
from mss import mss
from mss.base import MSSBase


class Region(TypedDict):
    left: int
    top: int
    width: int
    height: int


ahk = AHK(version='v1', directives=[NoTrayIcon])

STRATAGEMS: dict[str, list[Literal['Down', 'Left', 'Up', 'Right']]] = {
    'OCI Ready': [],  # No inputs when "Get ready" is shown on screen... OCR usually recognizes as "OCI Ready"
    'Resupply': ['Down', 'Down', 'Up', 'Right'],
    'Orbital Illumination Flare': ['Right', 'Right', 'Left', 'Left'],
    'hellbomb': ['Down', 'Up', 'Left', 'Down', 'Up', 'Right', 'Down', 'Up'],
    'Reinforce': ['Up', 'Down', 'Right', 'Left', 'Up'],
    'Machine Gun': ['Down', 'Left', 'Down', 'Up', 'Right'],
    'Anti-Material Rifle': ['Down', 'Left', 'Right', 'Up', 'Down'],
    'Stalwart': ['Down', 'Left', 'Down', 'Up', 'Up', 'Left'],
    'Expendable Anti-Tank': ['Down', 'Down', 'Left', 'Up', 'Right'],
    'Recoilless Rifle': ['Down', 'Left', 'Right', 'Right', 'Left'],
    'Flamethrower': ['Down', 'Left', 'Up', 'Down', 'Up'],
    'Autocannon': ['Down', 'Left', 'Down', 'Up', 'Up', 'Right'],
    'Railgun': ['Down', 'Right', 'Down', 'Up', 'Left', 'Right'],
    'Spear': ['Down', 'Down', 'Up', 'Down', 'Down'],
    'Eagle Strafing Run': ['Up', 'Right', 'Right'],
    'Eagle Airstrike': ['Up', 'Right', 'Down', 'Right'],
    'Eagle Cluster Bomb': ['Up', 'Right', 'Down', 'Down', 'Right'],
    'Eagle Napalm Airstrike': ['Up', 'Right', 'Down', 'Up'],
    'Jump Pack': ['Down', 'Up', 'Up', 'Down', 'Up'],
    'Eagle Smoke Strike': ['Up', 'Right', 'Up', 'Down'],
    'Eagle 110MM Rocket Pods': ['Up', 'Right', 'Up', 'Left'],
    'Eagle 500KG Bomb': ['Up', 'Right', 'Down', 'Down', 'Down'],
    'Orbital Gatling Barrage': ['Right', 'Down', 'Left', 'Up', 'Up'],
    'Orbital Airburst Strike': ['Right', 'Right', 'Right'],
    'Orbital 120MM HE Barrage': ['Right', 'Right', 'Down', 'Left', 'Right', 'Down'],
    'Orbital Walking Barrage': ['Right', 'Down', 'Up', 'Up', 'Left', 'Down', 'Down'],
    'Orbital 380MM HE Barrage': ['Right', 'Down', 'Up', 'Up', 'Left', 'Down', 'Down'],
    'Orbital Lasers': ['Right', 'Down', 'Up', 'Right', 'Down'],
    'Orbital Railcannon Strike': ['Right', 'Up', 'Down', 'Down', 'Right'],
    'Orbital Precision Strike': ['Right', 'Right', 'Up'],
    'Orbital Gas Strike': ['Right', 'Right', 'Down', 'Right'],
    'Orbital EMS Strike': ['Right', 'Right', 'Left', 'Down'],
    'Orbital Smoke Strike': ['Right', 'Right', 'Down', 'Up'],
    'HMG Emplacement': ['Down', 'Up', 'Left', 'Right', 'Right', 'Left'],
    'Shield Generation Relay': ['Down', 'Up', 'Left', 'Down', 'Right', 'Right'],
    'Tesla Tower': ['Down', 'Up', 'Right', 'Up', 'Left', 'Right'],
    'Machine Gun Sentry': ['Down', 'Up', 'Right', 'Right', 'Up'],
    'Gatling Sentry': ['Down', 'Up', 'Right', 'Left'],
    'Mortar Sentry': ['Down', 'Up', 'Right', 'Right', 'Down'],
    'Guard Dog': ['Down', 'Up', 'Left', 'Up', 'Right', 'Down'],
    'Autocannon Sentry': ['Down', 'Up', 'Right', 'Up', 'Left', 'Up'],
    'Rocket Sentry': ['Down', 'Up', 'Right', 'Right', 'Left'],
    'EMS Mortar Sentry': ['Down', 'Down', 'Up', 'Up', 'Left'],
    'Anti-Personnel Minefield': ['Down', 'Left', 'Up', 'Right'],
    'Supply Pack': ['Down', 'Left', 'Down', 'Up', 'Up', 'Down'],
    'Grenade Launcher': ['Down', 'Left', 'Up', 'Left', 'Down'],
    'Laser Cannon': ['Down', 'Left', 'Down', 'Up', 'Left'],
    'Incendiary Mines': ['Down', 'Left', 'Left', 'Down'],
    'Guard Dog Rover': ['Down', 'Up', 'Left', 'Up', 'Right', 'Right'],
    'Ballistic Shield Backpack': ['Down', 'Left', 'Up', 'Up', 'Right'],
    'Arc thrower': ['Down', 'Right', 'Up', 'Left', 'Down'],
    'Shield Generator Pack': ['Down', 'Up', 'Left', 'Right', 'Left', 'Right'],
}

STRATAGEMS = {k.lower(): v for k, v in STRATAGEMS.items()}
# this works for ultrawide 3440x1440
# TODO: get region for common resolutions
region: Region = {'left': 1480, 'top': 640, 'width': 600, 'height': 100}
INPUT_MAPPING: typing.Final = {'Down': 'S', 'Up': 'W', 'Left': 'A', 'Right': 'D'}
choices = tuple(k.lower() for k in STRATAGEMS.keys())
alpha = string.ascii_letters + string.digits

reader = easyocr.Reader(['en'])


def capture_and_ocr(sct: MSSBase, region: Region) -> str:
    sct_img = sct.grab(region)  # type: ignore[arg-type]
    image_np = np.array(sct_img)
    results = reader.readtext(image_np, detail=0)
    text = ' '.join(results)
    return text


@lru_cache(maxsize=None)
def get_counts(s: str) -> dict[str, int]:
    counts: dict[str, int] = collections.Counter()
    for c in s:
        if c not in alpha:
            continue
        counts[c] += 1
    return counts


# pre-warm the cache
for ch in choices:
    get_counts(ch)


def simple_match(s: str, choices: Sequence[str]) -> tuple[str, int]:
    best = None
    string_counts = get_counts(s)
    assert len(choices) > 1
    for choice in choices:
        choice_counts = get_counts(choice)
        distance = 0
        cmp_chars: set[str] = set(string_counts) | set(choice_counts)
        for char in cmp_chars:
            choice_count = choice_counts[char]
            count = string_counts[char]
            distance += abs(choice_count - count)
        if best:
            best_choice, best_distance = best
            if distance < best_distance:
                best = choice, distance
        else:
            best = choice, distance
    assert best is not None
    return best


def main() -> int:
    for window in ahk.list_windows():
        if 'helldivers2' in window.process_path.lower():
            helldivers = window
            print('Found', helldivers.title, helldivers.process_path)
            key = 'w'
            print('STARTING GAME')
            helldivers.send(f"{{{key} DOWN}}", blocking=False)
            time.sleep(0.1)
            helldivers.send(f"{{{key} UP}}", blocking=False)
            print('WAITING FOR GAME START')
            time.sleep(2)
            print('LETS PLAY')
            break
    else:
        # Helldivers window was not found
        raise SystemExit(4)
    with mss() as sct:
        while True:
            with suppress(Exception):
                active_window = ahk.get_active_window()
                if active_window is not None and 'helldivers2' not in active_window.get_process_path().lower():
                    print('Helldivers not focused. Exiting.')
                    return 0
            text = capture_and_ocr(sct, region)
            if not text:
                print('No text found.')
                continue
            print(repr(text), 'Read from screen')

            if '9999' in text:
                print('Detected leaderboard screen. Ignoring.')
                continue

            strat, deviation = simple_match(text.lower().replace('score', ''), choices)
            input_code = STRATAGEMS[strat]
            print(strat.title(), f'({" ".join(input_code)})', 'matched. deviation:', deviation)
            if deviation > len(strat):
                # probably garbage, wait for clearer text
                print('Ignoring.')
                continue

            for direction in input_code:
                key = INPUT_MAPPING[direction]
                helldivers.send(f"{{{key} DOWN}}", blocking=False)
                time.sleep(0.05)
                helldivers.send(f"{{{key} UP}}", blocking=False)
                time.sleep(0.05)

            time.sleep(0.3)
            # when a strategem ends in keys that it begins with and inputs are dropped,
            # it can sometimes result in a loop that won't resolve itself
            # TODO: detect broken state and reset input string


if __name__ == '__main__':
    raise SystemExit(main())
