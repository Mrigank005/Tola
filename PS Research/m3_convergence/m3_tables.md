# M3 tables

Generated from data/snapshot (data through 2026-10-22). Eligible day: both legs traded Rs 1 Cr+, neither in its tender window. A cycle counts with 10+ eligible days. Premiums are VWAP-based, bp = 1e4 x (small / big - 1), per gram at 999.

## 1. Pooled premium over expired cycles (cycle-bootstrap 95% CI)

| pair                 |   cycles | first_expiry   | last_expiry   |   pooled_vwap_bp |   ci_lo_bp |   ci_hi_bp |   hit_rate |   pooled_close_bp |   settlement_gap_bp_median |   given_up_bp_mean |   given_up_inr_g_mean |
|:---------------------|---------:|:---------------|:--------------|-----------------:|-----------:|-----------:|-----------:|------------------:|---------------------------:|-------------------:|----------------------:|
| GOLD/GOLDM           |       39 | 2020-02-05     | 2026-10-05    |            -1.55 |      -3.37 |       0.25 |       0.46 |             -1.64 |                       0    |               1.32 |                  0.44 |
| GOLDGUINEA/GOLDTEN   |       18 | 2025-04-30     | 2026-09-30    |            78.72 |      61.31 |      97.42 |       1    |             78.74 |                       0.01 |              68.31 |                 95.45 |
| GOLDPETAL/GOLDGUINEA |       81 | 2020-01-31     | 2026-09-30    |           -70.38 |     -88.26 |     -53.12 |       0.25 |            -70.32 |                      -3.71 |             -77.25 |                -42.79 |
| GOLDPETAL/GOLDTEN    |       18 | 2025-04-30     | 2026-09-30    |            94.18 |      80.3  |     108.8  |       1    |             94.55 |                      -3.81 |              94.92 |                132.56 |

## 2. Convergence profile: premium by trading days to expiry (expired cycles, mean of cycle means)

| bucket   |   GOLD/GOLDM |   GOLDGUINEA/GOLDTEN |   GOLDPETAL/GOLDGUINEA |   GOLDPETAL/GOLDTEN |
|:---------|-------------:|---------------------:|-----------------------:|--------------------:|
| 60+      |         -2.7 |                 87.4 |                   -0.5 |                96.7 |
| 40-59    |         -1.8 |                 77.9 |                  -58.5 |                95.5 |
| 20-39    |         -1.7 |                 68.6 |                  -64.6 |                88.4 |
| 10-19    |          3.2 |                 67.5 |                  -73.4 |                84.7 |
| 5-9      |          2.5 |                 76.3 |                  -84.9 |                90.8 |
| 0-4      |          2.8 |                100.2 |                   11.7 |               112.1 |

## 3. Premium by expiry year (mean of cycle means; live cycles included and marked in section 5)

|   year |   GOLD/GOLDM |   GOLDGUINEA/GOLDTEN |   GOLDPETAL/GOLDGUINEA |   GOLDPETAL/GOLDTEN |
|-------:|-------------:|---------------------:|-----------------------:|--------------------:|
|   2020 |         -2.6 |                nan   |                  -35.4 |               nan   |
|   2021 |         -5.5 |                nan   |                  -68.1 |               nan   |
|   2022 |         -2.9 |                nan   |                  -47   |               nan   |
|   2023 |          2.4 |                nan   |                 -110.4 |               nan   |
|   2024 |          1.9 |                nan   |                 -213.4 |               nan   |
|   2025 |          2.5 |                 49.1 |                   -5.2 |                73.6 |
|   2026 |         -9.8 |                 99.2 |                    4.5 |               104.6 |
|   2027 |        -30.4 |                 63.5 |                   -7.9 |                58.4 |

## 4. Control pair GOLD / GOLDM by period (expired cycles)

| period    |   cycles |   mean_bp |   ci_lo_bp |   ci_hi_bp |   hit_rate |
|:----------|---------:|----------:|-----------:|-----------:|-----------:|
| 2020-2025 |       35 |     -0.65 |      -2.39 |       1.11 |       0.51 |
| 2026      |        4 |     -9.45 |     -12.6  |      -6.59 |       0    |

## 5. Live cycles: latest premium vs expired cycles at the same stage

| pair                 | expiry     | date       |   tdte | bucket   | eligible   |   premium_vwap_bp |   change_5d_bp |   history_cycles |   history_mean_bp |   history_pct_rank |
|:---------------------|:-----------|:-----------|-------:|:---------|:-----------|------------------:|---------------:|-----------------:|------------------:|-------------------:|
| GOLD/GOLDM           | 2026-12-04 | 2026-10-22 |     31 | 20-39    | True       |              2.03 |           1.91 |               39 |             -1.74 |               0.77 |
| GOLD/GOLDM           | 2027-02-05 | 2026-10-22 |     76 | 60+      | True       |             -9.57 |           4.63 |               38 |             -2.74 |               0.29 |
| GOLD/GOLDM           | 2027-04-05 | 2026-10-22 |    117 | 60+      | True       |            -34.84 |         -17.49 |               38 |             -2.74 |               0    |
| GOLDGUINEA/GOLDTEN   | 2026-10-30 | 2026-10-22 |      6 | 5-9      | True       |             45.3  |          -3.91 |               18 |             76.28 |               0.44 |
| GOLDGUINEA/GOLDTEN   | 2026-11-30 | 2026-10-22 |     27 | 20-39    | True       |             45.47 |           0.58 |               18 |             68.63 |               0.39 |
| GOLDGUINEA/GOLDTEN   | 2026-12-31 | 2026-10-22 |     50 | 40-59    | True       |             40.8  |          -6.66 |               17 |             77.94 |               0.24 |
| GOLDGUINEA/GOLDTEN   | 2027-01-29 | 2026-10-22 |     71 | 60+      | True       |             31.83 |          -1.25 |               16 |             87.44 |               0.19 |
| GOLDGUINEA/GOLDTEN   | 2027-02-26 | 2026-10-22 |     91 | 60+      | True       |             43.01 |           7.6  |               16 |             87.44 |               0.19 |
| GOLDGUINEA/GOLDTEN   | 2027-03-31 | 2026-10-22 |    114 | 60+      | True       |             34.22 |         -10.99 |               16 |             87.44 |               0.19 |
| GOLDPETAL/GOLDGUINEA | 2026-10-30 | 2026-10-22 |      6 | 5-9      | True       |              3.17 |           2.63 |               18 |             14.46 |               0.33 |
| GOLDPETAL/GOLDGUINEA | 2026-11-30 | 2026-10-22 |     27 | 20-39    | True       |              0.1  |           5.23 |               18 |             19.37 |               0.06 |
| GOLDPETAL/GOLDGUINEA | 2026-12-31 | 2026-10-22 |     50 | 40-59    | True       |             -1.57 |           3.66 |               18 |             13.75 |               0.22 |
| GOLDPETAL/GOLDGUINEA | 2027-01-29 | 2026-10-22 |     71 | 60+      | True       |             -4.59 |         -11.1  |               18 |             -0.46 |               0.39 |
| GOLDPETAL/GOLDGUINEA | 2027-02-26 | 2026-10-22 |     91 | 60+      | True       |            -18.96 |         -28.07 |               18 |             -0.46 |               0.11 |
| GOLDPETAL/GOLDGUINEA | 2027-03-31 | 2026-10-22 |    114 | 60+      | True       |              3.81 |           8.43 |               18 |             -0.46 |               0.44 |
| GOLDPETAL/GOLDTEN    | 2026-10-30 | 2026-10-22 |      6 | 5-9      | True       |             48.49 |          -1.27 |               18 |             90.8  |               0.17 |
| GOLDPETAL/GOLDTEN    | 2026-11-30 | 2026-10-22 |     27 | 20-39    | True       |             45.57 |           5.84 |               18 |             88.45 |               0.06 |
| GOLDPETAL/GOLDTEN    | 2026-12-31 | 2026-10-22 |     50 | 40-59    | True       |             39.22 |          -2.98 |               17 |             95.48 |               0    |
| GOLDPETAL/GOLDTEN    | 2027-01-29 | 2026-10-22 |     71 | 60+      | True       |             27.22 |         -12.39 |               16 |             96.68 |               0    |
| GOLDPETAL/GOLDTEN    | 2027-02-26 | 2026-10-22 |     91 | 60+      | True       |             23.97 |         -20.58 |               16 |             96.68 |               0    |
| GOLDPETAL/GOLDTEN    | 2027-03-31 | 2026-10-22 |    114 | 60+      | True       |             38.04 |          -2.53 |               16 |             96.68 |               0.12 |

## 6. Per-cycle detail, same-reference pairs (expired)

| pair               | expiry     |   eligible_days |   mean_vwap_bp |   vwap_60+_bp |   vwap_5-9_bp |   last_premium_vwap_bp |   settlement_gap_bp |   given_up_bp |   given_up_inr_g |
|:-------------------|:-----------|----------------:|---------------:|--------------:|--------------:|-----------------------:|--------------------:|--------------:|-----------------:|
| GOLDGUINEA/GOLDTEN | 2025-04-30 |              16 |           38.2 |         nan   |          33.3 |                   32.8 |                -0.1 |          32.9 |             31.4 |
| GOLDGUINEA/GOLDTEN | 2025-05-30 |              38 |           48.8 |         nan   |          24.4 |                    1.3 |                 0   |           1.3 |              1.3 |
| GOLDGUINEA/GOLDTEN | 2025-06-30 |              58 |           54.3 |          91.9 |          48.6 |                   48.5 |                 0   |          48.5 |             48.1 |
| GOLDGUINEA/GOLDTEN | 2025-07-31 |              61 |           40   |          63.6 |          17.1 |                   41.5 |                 0.1 |          41.5 |             40.9 |
| GOLDGUINEA/GOLDTEN | 2025-08-29 |              59 |           34.2 |           5.5 |          37.6 |                   15.8 |                 0   |          15.7 |             15.6 |
| GOLDGUINEA/GOLDTEN | 2025-09-30 |              60 |           33.9 |          56.2 |          18.7 |                   35.4 |                 0   |          35.4 |             40.3 |
| GOLDGUINEA/GOLDTEN | 2025-10-31 |              59 |           48.1 |          29.9 |          59.8 |                   77.4 |                -0   |          77.4 |             94.7 |
| GOLDGUINEA/GOLDTEN | 2025-11-28 |              59 |           65.4 |          31.5 |         120.8 |                  120.4 |                 0   |         120.4 |            148.4 |
| GOLDGUINEA/GOLDTEN | 2025-12-31 |              68 |           78.8 |          54.5 |         106.5 |                  119.5 |                 0.1 |         119.4 |            164.1 |
| GOLDGUINEA/GOLDTEN | 2026-01-30 |              84 |          114   |          79.1 |         231.4 |                  246.6 |                 0   |         246.6 |            393.2 |
| GOLDGUINEA/GOLDTEN | 2026-02-27 |              98 |          124.7 |          86.3 |         194.4 |                  147.8 |                -0   |         147.8 |            233.6 |
| GOLDGUINEA/GOLDTEN | 2026-03-31 |             108 |          142.7 |         111.4 |         193.5 |                  110.8 |                 0.1 |         110.8 |            159.8 |
| GOLDGUINEA/GOLDTEN | 2026-04-30 |             106 |          142.3 |         169.8 |          57.6 |                   58.2 |                -0   |          58.2 |             87.7 |
| GOLDGUINEA/GOLDTEN | 2026-05-29 |             114 |          139.7 |         202.1 |          36.1 |                   24.4 |                 0   |          24.3 |             38.3 |
| GOLDGUINEA/GOLDTEN | 2026-06-30 |             120 |          121.3 |         185.3 |          67.6 |                   54.1 |                 0   |          54.1 |             76   |
| GOLDGUINEA/GOLDTEN | 2026-07-31 |             111 |           81.5 |         114.4 |          59.7 |                   32.3 |                 0   |          32.2 |             45.7 |
| GOLDGUINEA/GOLDTEN | 2026-08-31 |             108 |           61   |          70.6 |          39.3 |                   45.7 |                -0   |          45.8 |             73.2 |
| GOLDGUINEA/GOLDTEN | 2026-09-30 |             100 |           48.1 |          46.9 |          26.5 |                   17.1 |                 0   |          17.1 |             25.9 |
| GOLDPETAL/GOLDTEN  | 2025-04-30 |              16 |           77.8 |         nan   |          70   |                   81.9 |                 2.5 |          79.4 |             75.7 |
| GOLDPETAL/GOLDTEN  | 2025-05-30 |              38 |           86   |         nan   |          62.2 |                   38.6 |                -2.1 |          40.7 |             39.1 |
| GOLDPETAL/GOLDTEN  | 2025-06-30 |              58 |           84.9 |         135.1 |          71.4 |                   72.6 |                -2.2 |          74.8 |             74.1 |
| GOLDPETAL/GOLDTEN  | 2025-07-31 |              61 |           75.5 |          90.5 |          50.4 |                   71   |                 8.9 |          62.1 |             61.3 |
| GOLDPETAL/GOLDTEN  | 2025-08-29 |              59 |           65.8 |          29.2 |          62   |                   30.8 |                10.1 |          20.7 |             20.6 |
| GOLDPETAL/GOLDTEN  | 2025-09-30 |              60 |           56.5 |         102.2 |          20.1 |                   -6.7 |                -6.2 |          -0.5 |             -0.6 |
| GOLDPETAL/GOLDTEN  | 2025-10-31 |              59 |           56.7 |          46.3 |          84.6 |                   89.6 |                 3.8 |          85.8 |            105   |
| GOLDPETAL/GOLDTEN  | 2025-11-28 |              59 |           73.4 |          34.8 |         143.7 |                  145.8 |                -6.3 |         152.1 |            187.5 |
| GOLDPETAL/GOLDTEN  | 2025-12-31 |              68 |           85.9 |          49.6 |         112.8 |                  113.2 |                 3.5 |         109.6 |            150.7 |
| GOLDPETAL/GOLDTEN  | 2026-01-30 |              86 |          111.3 |          71.1 |         227.1 |                  201.6 |              -166   |         367.7 |            586.1 |
| GOLDPETAL/GOLDTEN  | 2026-02-27 |             104 |          120.7 |          76.5 |         216.1 |                  234   |                -8.4 |         242.4 |            383   |
| GOLDPETAL/GOLDTEN  | 2026-03-31 |             114 |          142.9 |          96.1 |         203.5 |                  146.9 |                -2.9 |         149.9 |            216.2 |
| GOLDPETAL/GOLDTEN  | 2026-04-30 |             114 |          145.3 |         142.2 |          83.9 |                   83   |                -7.9 |          90.9 |            136.8 |
| GOLDPETAL/GOLDTEN  | 2026-05-29 |             119 |          145.2 |         183.3 |          53.9 |                   30.1 |               -21.8 |          51.9 |             81.6 |
| GOLDPETAL/GOLDTEN  | 2026-06-30 |             123 |          137.6 |         198.6 |          63.6 |                   51.8 |               -20.5 |          72.3 |            101.6 |
| GOLDPETAL/GOLDTEN  | 2026-07-31 |             124 |           99.1 |         135.5 |          53.3 |                   23   |                -4.7 |          27.7 |             39.2 |
| GOLDPETAL/GOLDTEN  | 2026-08-31 |             118 |           71   |          85.5 |          36.2 |                   36.8 |               -25.6 |          62.4 |             99.8 |
| GOLDPETAL/GOLDTEN  | 2026-09-30 |             122 |           59.5 |          70.4 |          19.7 |                   17.7 |                -1.1 |          18.8 |             28.4 |

## 7. Monthly median premium, same-reference pairs (eligible days, calendar months since Jan 2026)

| date    |   GOLDGUINEA/GOLDTEN |   GOLDPETAL/GOLDTEN |
|:--------|---------------------:|--------------------:|
| 2026-01 |                  180 |                 170 |
| 2026-02 |                  160 |                 191 |
| 2026-03 |                  166 |                 199 |
| 2026-04 |                   54 |                  76 |
| 2026-05 |                   36 |                  62 |
| 2026-06 |                   64 |                  72 |
| 2026-07 |                   70 |                  73 |
| 2026-08 |                   53 |                  54 |
| 2026-09 |                   56 |                  50 |
| 2026-10 |                   43 |                  42 |
