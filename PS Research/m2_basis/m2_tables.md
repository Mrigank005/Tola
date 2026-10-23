# M2 tables

Generated from data/snapshot (futures through 2026-10-22). Liquid = Rs 1 Cr+ turnover, outside the tender window.

## 1. Implied carry vs risk-free, by year (median, % a year)

|   year |   carry |   rf |   carry_minus_rf |   days | rf_source        |
|-------:|--------:|-----:|-----------------:|-------:|:-----------------|
|   2020 |    1.48 |  4   |            -2.78 |    256 | RBI repo (proxy) |
|   2021 |    2.64 |  4   |            -1.36 |    253 | RBI repo (proxy) |
|   2022 |    2.84 |  4.9 |            -2.1  |    257 | RBI repo (proxy) |
|   2023 |    3.9  |  6.5 |            -2.58 |    256 | RBI repo (proxy) |
|   2024 |    3.96 |  6.5 |            -2.54 |    257 | RBI repo (proxy) |
|   2025 |    5.55 |  5.5 |            -0.15 |    257 | RBI repo (proxy) |
|   2026 |   12.31 |  5.3 |             7.06 |    207 | FBIL 3M T-bill   |

## 2. Implied carry vs risk-free, by month since Jul 2025

| month   |   carry |   rf |   fit_rmse_bp | rf_source        |
|:--------|--------:|-----:|--------------:|:-----------------|
| 2025-07 |    5.25 | 5.5  |          6.38 | RBI repo (proxy) |
| 2025-08 |    5.78 | 5.5  |          8.43 | RBI repo (proxy) |
| 2025-09 |    5.71 | 5.5  |          9.1  | RBI repo (proxy) |
| 2025-10 |    6.69 | 5.48 |         19.43 | RBI repo (proxy) |
| 2025-11 |    7.9  | 5.4  |         20.28 | FBIL 3M T-bill   |
| 2025-12 |   12.85 | 5.27 |         18.81 | FBIL 3M T-bill   |
| 2026-01 |   17.21 | 5.34 |         34.3  | FBIL 3M T-bill   |
| 2026-02 |   13.53 | 5.3  |         38.44 | FBIL 3M T-bill   |
| 2026-03 |   14.99 | 5.31 |         14.71 | FBIL 3M T-bill   |
| 2026-04 |   10.85 | 5.25 |         11.36 | FBIL 3M T-bill   |
| 2026-05 |   13.39 | 5.42 |         11.8  | FBIL 3M T-bill   |
| 2026-06 |   14.18 | 5.25 |         12.52 | FBIL 3M T-bill   |
| 2026-07 |    6.9  | 5.29 |         12.97 | FBIL 3M T-bill   |
| 2026-08 |    7.21 | 5.26 |         13.14 | FBIL 3M T-bill   |
| 2026-09 |    7.4  | 5.3  |         13.84 | FBIL 3M T-bill   |
| 2026-10 |   10.48 | 5.65 |          9.43 | FBIL 3M T-bill   |

## 3. Timing term (spot poll ~5-6 pm vs futures close to ~11:30 pm), bp

|   year |    10% |   25% |   50% |   75% |    90% |
|-------:|-------:|------:|------:|------:|-------:|
|   2020 |  -86.2 | -37.3 |  11.3 |  94.1 | 1090.1 |
|   2021 |  -89.1 | -47.7 |  -6.4 |  27.5 |   68.6 |
|   2022 |  -72.9 | -38.4 |  -9.8 |  23.6 |   64.5 |
|   2023 |  -78.7 | -48.4 | -18.8 |  11.5 |   45.6 |
|   2024 |  -84.8 | -51.1 |  -9.2 |  30.5 |   73.9 |
|   2025 |  -87.8 | -44.3 |  -0.2 |  43.2 |   85.8 |
|   2026 | -133.6 | -56.4 |  -2   |  53.9 |  108.3 |

## 4. Residual by contract and year (median bp, liquid, pre-tender)

|   year |   GOLD |   GOLDM |   GOLDTEN |   GOLDGUINEA |   GOLDPETAL |
|-------:|-------:|--------:|----------:|-------------:|------------:|
|   2020 |   -1.4 |     1.8 |     nan   |         31.6 |        32   |
|   2021 |   -3.1 |     3.5 |     nan   |         12   |       -50.2 |
|   2022 |   -1.2 |     1.6 |     nan   |        -24.2 |       -70   |
|   2023 |   -1.2 |     0.4 |     nan   |         34.8 |       -90.9 |
|   2024 |   -0.4 |     1.1 |     nan   |         74.2 |      -144.1 |
|   2025 |   -1   |     0.9 |      -6.6 |         53.6 |        76.1 |
|   2026 |   -4.7 |     4.1 |      10.3 |         77.1 |        93.6 |

## 5. Residual vs making charge, 2025-26 (median bp)

| symbol     |   residual |   making_charge | making_charge_inr_g   |   days |
|:-----------|-----------:|----------------:|:----------------------|-------:|
| GOLD       |       -1.8 |           nan   | <NA>                  |   1574 |
| GOLDM      |        2.4 |           nan   | <NA>                  |   2118 |
| GOLDTEN    |        2.5 |            20.8 | 30.0                  |   1886 |
| GOLDGUINEA |       66.4 |            17.8 | 25.0                  |   2016 |
| GOLDPETAL  |       84.9 |            70.2 | 100.0                 |   2263 |

## 6. Reference term: GOLDPETAL Mumbai spot vs Ahmedabad 999 (median bp)

|   year |   GOLDPETAL reference_bp |
|-------:|-------------------------:|
|   2020 |                     -7.5 |
|   2021 |                     -3.7 |
|   2022 |                     -2.1 |
|   2023 |                     -1.3 |
|   2024 |                     -3.4 |
|   2025 |                     -2.4 |
|   2026 |                     -7.6 |
