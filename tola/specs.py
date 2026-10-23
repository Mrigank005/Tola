"""Versioned contract specifications (data/specs/gold.yaml)."""
from datetime import date
from functools import lru_cache
from pathlib import Path

import yaml

SPEC_FILE = Path(__file__).resolve().parent.parent / "data" / "specs" / "gold.yaml"


@lru_cache(maxsize=1)
def load():
    return yaml.safe_load(SPEC_FILE.read_text(encoding="utf-8"))["symbols"]


def symbols():
    return list(load())


def basis(symbol):
    return load()[symbol]["basis"]


def spot(symbol):
    return load()[symbol]["spot"]


def _month(v):
    """YAML reads 2025-04 as a string; normalise to (year, month)."""
    y, m = str(v).split("-")[:2]
    return int(y), int(m)


def version_for(symbol, expiry: date):
    """The spec version governing the contract that expires on `expiry`, or None if older than every version we hold."""
    found = None
    for v in load()[symbol]["versions"]:
        if _month(v["from"]) <= (expiry.year, expiry.month):
            found = v
    return found


def version_id(symbol, v):
    return None if v is None else f"{symbol}@{v['from']}"


def first_version(symbol):
    return load()[symbol]["versions"][0]
