"""Drop cancelled orders and normalise currency columns.

Usage: python clean.py <export.csv> <out.csv>
"""

import sys

import pandas as pd


def main(src: str, dst: str) -> None:
    frame = pd.read_csv(src)
    frame = frame[frame["status"].str.lower() != "cancelled"]
    for column in ("revenue", "cogs"):
        frame[column] = (
            frame[column].astype(str).str.replace(",", ".").str.replace("€", "").astype(float)
        )
    frame.to_csv(dst, index=False)
    print(f"{len(frame)} orders kept → {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
