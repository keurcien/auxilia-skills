"""Generate a fake order export for testing clean.py and margins.py.

Usage: python fake_data.py <out.csv> [--orders N] [--seed S] [--raw]

By default revenue and cogs are plain numbers, so the file feeds margins.py
directly and also passes through clean.py unchanged. With --raw they are
written the way real exports come in ("12,50€"), so clean.py is required first.

A few operations are generated deliberately below their category target from
references/rules.md, and a few orders are cancelled, so both scripts have
something to do.
"""

import argparse
import random

import pandas as pd

# (operation, category, intended gross margin). Targets: Fashion 45%, Home 40%,
# Beauty 50%, Food 30%. Operations marked below are more than two points under.
OPERATIONS = [
    ("Maison Lenoir", "Fashion", 0.48),
    ("Atelier Brume", "Fashion", 0.46),
    ("Rue Verte", "Fashion", 0.39),  # below target
    ("Nordholm Living", "Home", 0.42),
    ("Casa Ombra", "Home", 0.41),
    ("Lampe & Co", "Home", 0.33),  # below target
    ("Lueur Cosmetics", "Beauty", 0.53),
    ("Pure Argile", "Beauty", 0.51),
    ("Velours Skin", "Beauty", 0.44),  # below target
    ("Ferme Bertille", "Food", 0.32),
    ("Cacao Rousseau", "Food", 0.31),
    ("Épicerie Marin", "Food", 0.24),  # below target
]

STATUSES = ["delivered"] * 8 + ["shipped", "cancelled"]


def build(orders: int, seed: int) -> pd.DataFrame:
    rng = random.Random(seed)
    rows = []
    for order_id in range(1, orders + 1):
        operation, category, margin = rng.choice(OPERATIONS)
        revenue = round(rng.uniform(15, 250), 2)
        # Jitter the margin per order so the recomputed figure is not exact.
        order_margin = margin + rng.gauss(0, 0.03)
        cogs = round(revenue * (1 - order_margin), 2)
        rows.append(
            {
                "order_id": f"ORD-{order_id:05d}",
                "operation": operation,
                "category": category,
                "status": rng.choice(STATUSES),
                "revenue": revenue,
                "cogs": cogs,
            }
        )
    return pd.DataFrame(rows)


def to_raw(frame: pd.DataFrame) -> pd.DataFrame:
    """Format currency columns like a real export: comma decimals, euro sign."""
    frame = frame.copy()
    for column in ("revenue", "cogs"):
        frame[column] = frame[column].map(lambda value: f"{value:.2f}€".replace(".", ","))
    return frame


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("dst", help="output CSV path")
    parser.add_argument("--orders", type=int, default=500, help="number of orders (default 500)")
    parser.add_argument("--seed", type=int, default=42, help="random seed (default 42)")
    parser.add_argument("--raw", action="store_true", help="write currency as '12,50€' strings")
    args = parser.parse_args()

    frame = build(args.orders, args.seed)
    if args.raw:
        frame = to_raw(frame)
    frame.to_csv(args.dst, index=False)
    print(f"{len(frame)} orders across {frame['operation'].nunique()} operations → {args.dst}")


if __name__ == "__main__":
    main()
