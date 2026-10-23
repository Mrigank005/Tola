from datetime import date

from tola import specs


def test_every_symbol_has_basis_spot_and_versions():
    for s in specs.symbols():
        assert {"lot_g", "quote_g", "purity"} <= set(specs.basis(s))
        assert specs.spot(s)["unit_g"] == specs.basis(s)["quote_g"], "DDR maths assumes spot is quoted per quote unit"
        assert specs.load()[s]["versions"], s


def test_versions_are_ordered_and_sourced():
    for s in specs.symbols():
        froms = [specs._month(v["from"]) for v in specs.load()[s]["versions"]]
        assert froms == sorted(froms), s
        for v in specs.load()[s]["versions"]:
            assert v["source"].endswith(".pdf") and v["url"].startswith("https://www.mcxindia.com/"), (s, v["from"])


def test_version_lookup_by_expiry_month():
    assert specs.version_for("GOLDTEN", date(2025, 10, 31))["tender"]["days"] == 5
    assert specs.version_for("GOLDTEN", date(2025, 11, 28))["tender"]["days"] == 3
    assert specs.version_for("GOLDPETAL", date(2024, 12, 31)) is None       # older than the first PDF we hold
    assert str(specs.version_for("GOLD", date(2027, 2, 5))["from"]) == "2027-02"
    assert specs.version_for("GOLD", date(2026, 12, 4))["tender"]["days"] == 3


def test_making_charges_match_the_pdfs():
    per_g = {s: specs.version_for(s, date(2026, 10, 30))["making_charge_inr_per_g"] for s in ("GOLDTEN", "GOLDGUINEA", "GOLDPETAL")}
    assert per_g == {"GOLDTEN": 30, "GOLDGUINEA": 25, "GOLDPETAL": 100}
