"""Gross margin per operation, written to an xlsx.

Usage: python margins.py <cleaned.csv> <out.xlsx>
"""

import sys

import pandas as pd


def main(src: str, dst: str) -> None:
    frame = pd.read_csv(src)
    grouped = frame.groupby("operation")[["revenue", "cogs"]].sum()
    grouped["margin"] = (grouped["revenue"] - grouped["cogs"]) / grouped["revenue"]
    grouped.sort_values("margin").to_excel(dst)
    print(f"{len(grouped)} operations → {dst}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
