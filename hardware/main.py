#!/usr/bin/env python3

import argparse
import requests
from time import sleep

from ev3dev2.motor import LargeMotor, OUTPUT_A, SpeedPercent
from ev3dev2.sound import Sound
from ev3dev2.display import Display
from ev3dev2.console import Console

URL = "http://localhost:3000"

console = Console()
console.set_font("Lat15-TerminusBold16.psf.gz", True)

mid_col = console.columns // 2
mid_row = console.rows // 2

def main():
    while True:
        sleep(1)

        res = requests.get(URL + "/queue")
        res = res.json()

        if not len(res):
            console.text_at(
                "Queue is empty", column=mid_col, row=mid_row, alignment="C"
            )
            continue

        make_drink(res[0], len(res))


def make_drink(order, length):
    _id = order["_id"]
    name = order["options"]["name"]
    tea = order["options"]["tea"]
    sugar = order["options"]["sugar"]
    ice = order["options"]["ice"]

    console.text_at(
        "Making Order for "
        + name
        + "\n"
        + tea
        + " "
        + sugar
        + "%"
        + " "
        + ice
        + "%"
        + "\nQueue Size: "
        + length,
        column=mid_col,
        row=mid_row,
        alignment="C",
    )

    m = LargeMotor(OUTPUT_A)
    m.on_for_rotations(SpeedPercent(75), 5)

    sound = Sound()
    sound.speak("Your boba drink is finished!")

    requests.patch(URL + "/queue/" + _id, json={})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run a script to listen for order queue updates."
    )
    parser.add_argument("--url", default=URL, help="URL to listen on.")
    args = parser.parse_args()
    URL = args.url
    main()
