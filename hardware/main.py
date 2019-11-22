#!/usr/bin/env python3

import argparse
import requests
from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, SpeedPercent
from ev3dev2.sound import Sound
from ev3dev2.display import Display
from ev3dev2.console import Console

URL = "http://35.230.20.197:5000" or "http://bobafetch.me:5000"

console = Console()
console.set_font("Lat15-TerminusBold16.psf.gz", True)

# mid_col = console.columns // 2
# mid_row = console.rows // 2
mid_col = 1
mid_row = 1
alignment="L"

def main():
    console.text_at(
        "Mindstorms is running", column=mid_col, row=mid_row, alignment=alignment, reset_console=True
    )
    while True:
        sleep(1)

        res = requests.get(URL + "/queue")
        res = res.json()

        if not len(res):
            console.text_at(
                "Queue is empty", column=mid_col, row=mid_row, alignment=alignment, reset_console=True
            )
            continue

        make_drink(res[0], len(res))


def make_drink(order, length):
    _id = order["_id"]
    name = order["name"]
    tea = order["options"]["tea"]
    sugar = order["options"]["sugar"]
    ice = order["options"]["ice"]

    console.text_at(
        "Making Order for "
        + name
        + "\n"
        + tea
        + " "
        + str(sugar)
        + "%"
        + " "
        + str(ice)
        + "%"
        + "\nQueue Size: "
        + str(length),
        column=mid_col,
        row=mid_row,
        alignment=alignment,
        reset_console=True
    )

    m = LargeMotor(OUTPUT_A)
    m.on_for_rotations(SpeedPercent(75), 5)

    s = name + ", your boba drink is finished. Please come pick it up"

    console.text_at(
        s, 
        column=mid_col,
        row=mid_row,
        alignment=alignment,
        reset_console=True
    ) 

    sound = Sound()
    sound.speak(s)

    requests.patch(URL + "/queue/" + _id, json={})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a script to listen for order queue updates."
    )
    parser.add_argument("--url", default=URL, help="URL to listen on.")
    args = parser.parse_args()
    URL = args.url
    main()
