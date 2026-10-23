# M4 tables

Generated from data/snapshot (data through 2026-10-22). Position: 200 g per leg, signals at day t's close, fills at the next eligible day's VWAP, exit before tender. Base slippage 1 tick per order.

## 0. Why slippage is assumed: EDGE (Ardia, Guidotti & Kroencke 2024) on daily OHLC, per contract

|   year |   GOLD |   GOLDGUINEA |   GOLDM |   GOLDPETAL |   GOLDTEN |
|-------:|-------:|-------------:|--------:|------------:|----------:|
|   2023 |   13.6 |         19.6 |    11.1 |        10.4 |     nan   |
|   2024 |   16.6 |         15   |    19.9 |        15.1 |     nan   |
|   2025 |   27.7 |         21.4 |    24.3 |        23.6 |      27.9 |
|   2026 |   92.9 |         68.8 |    72.4 |        58.5 |      56.3 |
|   2027 |   24.7 |         24.1 |    30   |        28.4 |      34.7 |

Correlation of EDGE with daily volatility across contracts: 0.89. Tick size: {'GOLD': 0.07, 'GOLDGUINEA': 0.08, 'GOLDM': 0.07, 'GOLDPETAL': 0.65, 'GOLDTEN': 0.07} bp.

## 1. Scored strategies (DRIFT: no tuning; MR walk-forward: out-of-sample only)

| pair                 | strategy        |   trades |   cycles |   mean_gross_bp |   mean_cost_bp |   mean_net_bp |   ci_lo_bp |   ci_hi_bp |   hit_rate |   sharpe_per_trade |   deflated_sharpe_prob |   random_entry_p |   mean_net_bp_ex_crash |   ex_crash_ci_lo_bp |   ex_crash_ci_hi_bp |   trades_ex_crash |   breakeven_slippage_ticks |   spread_leg_share |   total_net_inr |
|:---------------------|:----------------|---------:|---------:|----------------:|---------------:|--------------:|-----------:|-----------:|-----------:|-------------------:|-----------------------:|-----------------:|-----------------------:|--------------------:|--------------------:|------------------:|---------------------------:|-------------------:|----------------:|
| GOLDGUINEA/GOLDTEN   | DRIFT           |       23 |       23 |           18.08 |           4.31 |         13.77 |     -32.06 |      60.66 |       0.65 |               0.12 |                   0.09 |              nan |                  -0.59 |              -33.59 |               28.54 |                15 |                      70.64 |               1.26 |        144152   |
| GOLDGUINEA/GOLDTEN   | MR walk-forward |       29 |       11 |           48.29 |           4.26 |         44.03 |      19.97 |      78.29 |       0.69 |               0.51 |                   0.88 |                0 |                  10.53 |                4.44 |               15.31 |                20 |                     150.04 |               1.05 |        388989   |
| GOLDPETAL/GOLDGUINEA | DRIFT           |       86 |       86 |           30.36 |           7.76 |         22.59 |       0.47 |      46.49 |       0.65 |               0.2  |                   0.01 |              nan |                  29.52 |                5.63 |               56.92 |                78 |                       4.11 |               0.95 |        120225   |
| GOLDPETAL/GOLDGUINEA | MR walk-forward |      138 |       73 |            5.82 |           7.52 |         -1.71 |     -10.89 |       6.51 |       0.53 |              -0.03 |                   0    |                0 |                  -3.77 |              -12.74 |                4.06 |               132 |                       1.94 |               1    |         58095.6 |
| GOLDPETAL/GOLDTEN    | DRIFT           |       24 |       24 |           10.53 |           5.71 |          4.82 |     -38.52 |      46.18 |       0.58 |               0.05 |                   0.17 |              nan |                   7.38 |              -28.09 |               39.54 |                16 |                       9.02 |               1.43 |         84736.6 |
| GOLDPETAL/GOLDTEN    | MR walk-forward |       40 |       15 |           39.11 |           5.66 |         33.45 |      11.43 |      58.39 |       0.6  |               0.4  |                   0.95 |                0 |                   6.81 |                0.49 |               15.25 |                28 |                      24.92 |               1.05 |        420955   |

## 2. MR walk-forward by period (out-of-sample, same-reference pairs)

|                                        |   trades |   cycles |   mean_net_bp |   median_net_bp |   hit_rate |   net_inr |
|:---------------------------------------|---------:|---------:|--------------:|----------------:|-----------:|----------:|
| ('GOLDGUINEA/GOLDTEN', '2025')         |       20 |        8 |          10.5 |            15.8 |        0.6 |   45505.4 |
| ('GOLDGUINEA/GOLDTEN', 'Jan-Mar 2026') |        9 |        5 |         118.5 |            41.6 |        0.9 |  343483   |
| ('GOLDPETAL/GOLDTEN', '2025')          |       25 |       10 |           6.2 |             0.3 |        0.5 |   30690.7 |
| ('GOLDPETAL/GOLDTEN', 'Apr-Oct 2026')  |        3 |        2 |          11.7 |             3.2 |        0.7 |   10208.8 |
| ('GOLDPETAL/GOLDTEN', 'Jan-Mar 2026')  |       12 |        6 |          95.6 |            51.3 |        0.8 |  380055   |

## 3. Every config, full sample (in-sample; the trial set behind the Deflated Sharpe)

| config         |   ('size', 'GOLDGUINEA/GOLDTEN') |   ('size', 'GOLDPETAL/GOLDGUINEA') |   ('size', 'GOLDPETAL/GOLDTEN') |   ('mean', 'GOLDGUINEA/GOLDTEN') |   ('mean', 'GOLDPETAL/GOLDGUINEA') |   ('mean', 'GOLDPETAL/GOLDTEN') |
|:---------------|---------------------------------:|-----------------------------------:|--------------------------------:|---------------------------------:|-----------------------------------:|--------------------------------:|
| DRIFT          |                               23 |                                 86 |                              24 |                             13.8 |                               22.6 |                             4.8 |
| MR(W=20,k=1.0) |                              133 |                                261 |                             132 |                             29.3 |                               -0.3 |                            18.5 |
| MR(W=20,k=1.5) |                               94 |                                206 |                              82 |                             32.4 |                               -1.8 |                            17.8 |
| MR(W=20,k=2.0) |                               56 |                                134 |                              55 |                             32.8 |                               -2.4 |                            26.6 |
| MR(W=40,k=1.0) |                               56 |                                 94 |                              57 |                             22.3 |                                9.5 |                            14.4 |
| MR(W=40,k=1.5) |                               41 |                                 63 |                              36 |                             28.3 |                               10.7 |                            25.9 |
| MR(W=40,k=2.0) |                               26 |                                 32 |                              26 |                             45.8 |                               10   |                            29.8 |
| MR(W=60,k=1.0) |                               22 |                                 37 |                              26 |                             43.7 |                               12.4 |                             5.6 |
| MR(W=60,k=1.5) |                               14 |                                 16 |                              15 |                             58.5 |                               21.7 |                            14.5 |
| MR(W=60,k=2.0) |                                7 |                                 11 |                               9 |                            127.3 |                               24.3 |                            53.1 |

## 4. Slippage sensitivity: mean net bp per trade at 0 / 1 / 3 / 10 ticks per order

| pair                 | strategy        |   0 ticks |   1 ticks |   3 ticks |   10 ticks |
|:---------------------|:----------------|----------:|----------:|----------:|-----------:|
| GOLDGUINEA/GOLDTEN   | DRIFT           |      14.1 |      13.8 |      13   |       10.5 |
| GOLDGUINEA/GOLDTEN   | MR walk-forward |      44.4 |      44   |      43.3 |       40.8 |
| GOLDPETAL/GOLDGUINEA | DRIFT           |      26.1 |      22.6 |      15.5 |       -9.3 |
| GOLDPETAL/GOLDGUINEA | MR walk-forward |       1.7 |      -1.7 |      -8.5 |      -32.2 |
| GOLDPETAL/GOLDTEN    | DRIFT           |       6.6 |       4.8 |       1.3 |      -11.2 |
| GOLDPETAL/GOLDTEN    | MR walk-forward |      35.2 |      33.5 |      29.9 |       17.5 |

## 5. Delivery leg: held through settlement (Rs per gram, mean over expired cycles)

| pair               | entry               |   cycles |   entry_premium_bp |   futures_inr_g |   making_net_inr_g |   headroom_inr_g |   breakeven_coin_premium_pct |   breakeven_min_pct |   breakeven_max_pct |   retail_coin_premium_pct |   retail_net_inr_g |   retail_profitable_share |
|:-------------------|:--------------------|---------:|-------------------:|----------------:|-------------------:|-----------------:|-----------------------------:|--------------------:|--------------------:|--------------------------:|-------------------:|--------------------------:|
| GOLDGUINEA/GOLDTEN | early (60+ days)    |       16 |              87.44 |          123.5  |                 -5 |            69.02 |                         0.47 |               -0.39 |                1.63 |                       3.6 |            -416.28 |                         0 |
| GOLDGUINEA/GOLDTEN | last pre-tender day |       18 |              68.32 |           95.45 |                 -5 |            42.2  |                         0.27 |               -0.44 |                2.08 |                       3.6 |            -427.44 |                         0 |
| GOLDPETAL/GOLDTEN  | early (60+ days)    |       16 |              96.68 |          157.53 |                 70 |           177.17 |                         1.28 |                0.49 |                2.45 |                       5.5 |            -564.26 |                         0 |
| GOLDPETAL/GOLDTEN  | last pre-tender day |       18 |              81.21 |          132.56 |                 70 |           153.44 |                         1.13 |                0.22 |                3.75 |                       5.5 |            -564.07 |                         0 |

## 6. Delivery leg per cycle, entered on the last pre-tender day

| pair               | expiry     |   entry_premium_bp |   settlement_gap_bp |   futures_inr_g |   making_received_inr_g |   making_paid_inr_g |   margin_funding_inr_g |   entry_costs_inr_g |   headroom_inr_g |   breakeven_coin_premium_pct |   retail_net_inr_g |
|:-------------------|:-----------|-------------------:|--------------------:|----------------:|------------------------:|--------------------:|-----------------------:|--------------------:|-----------------:|-----------------------------:|-------------------:|
| GOLDGUINEA/GOLDTEN | 2025-04-30 |               32.8 |                -0.1 |            31.4 |                      25 |                  30 |                    2.4 |                 2.1 |            -11.9 |                         -0.1 |             -355.2 |
| GOLDGUINEA/GOLDTEN | 2025-05-30 |                1.3 |                 0   |             1.3 |                      25 |                  30 |                    2.4 |                 2.1 |            -42.2 |                         -0.4 |             -387.6 |
| GOLDGUINEA/GOLDTEN | 2025-06-30 |               48.5 |                 0   |            48.1 |                      25 |                  30 |                    2.2 |                 2.2 |              3.9 |                          0   |             -352.7 |
| GOLDGUINEA/GOLDTEN | 2025-07-31 |               41.5 |                 0.1 |            40.9 |                      25 |                  30 |                    2.2 |                 2.2 |             -3.1 |                         -0   |             -358.3 |
| GOLDGUINEA/GOLDTEN | 2025-08-29 |               15.8 |                 0   |            15.6 |                      25 |                  30 |                    2.2 |                 2.2 |            -28.6 |                         -0.3 |             -386.6 |
| GOLDGUINEA/GOLDTEN | 2025-09-30 |               35.4 |                 0   |            40.3 |                      25 |                  30 |                    2.6 |                 2.4 |             -8.2 |                         -0.1 |             -417.6 |
| GOLDGUINEA/GOLDTEN | 2025-10-31 |               77.4 |                -0   |            94.7 |                      25 |                  30 |                    2.7 |                 2.6 |             43.8 |                          0.4 |             -396.6 |
| GOLDGUINEA/GOLDTEN | 2025-11-28 |              120.4 |                 0   |           148.4 |                      25 |                  30 |                    2.7 |                 2.6 |             97.3 |                          0.8 |             -346.4 |
| GOLDGUINEA/GOLDTEN | 2025-12-31 |              119.5 |                 0.1 |           164.1 |                      25 |                  30 |                    3   |                 2.8 |            109   |                          0.8 |             -386   |
| GOLDGUINEA/GOLDTEN | 2026-01-30 |              246.6 |                 0   |           393.2 |                      25 |                  30 |                    3.6 |                 3.3 |            331.5 |                          2.1 |             -242.4 |
| GOLDGUINEA/GOLDTEN | 2026-02-27 |              147.8 |                -0   |           233.6 |                      25 |                  30 |                    3.4 |                 3.2 |            172.4 |                          1.1 |             -396.4 |
| GOLDGUINEA/GOLDTEN | 2026-03-31 |              110.8 |                 0.1 |           159.8 |                      25 |                  30 |                    3.2 |                 3   |            102.6 |                          0.7 |             -416.8 |
| GOLDGUINEA/GOLDTEN | 2026-04-30 |               58.2 |                -0   |            87.7 |                      25 |                  30 |                    3.3 |                 3.1 |             28.7 |                          0.2 |             -513.2 |
| GOLDGUINEA/GOLDTEN | 2026-05-29 |               24.4 |                 0   |            38.3 |                      25 |                  30 |                    3.6 |                 3.2 |            -22.8 |                         -0.1 |             -588.7 |
| GOLDGUINEA/GOLDTEN | 2026-06-30 |               54.1 |                 0   |            76   |                      25 |                  30 |                    3   |                 2.9 |             20   |                          0.1 |             -485.7 |
| GOLDGUINEA/GOLDTEN | 2026-07-31 |               32.3 |                 0   |            45.7 |                      25 |                  30 |                    3.1 |                 2.9 |            -10.7 |                         -0.1 |             -520.5 |
| GOLDGUINEA/GOLDTEN | 2026-08-31 |               45.7 |                -0   |            73.2 |                      25 |                  30 |                    3.5 |                 3.2 |             11.6 |                          0.1 |             -564.4 |
| GOLDGUINEA/GOLDTEN | 2026-09-30 |               17.1 |                 0   |            25.9 |                      25 |                  30 |                    3.4 |                 3.1 |            -33.4 |                         -0.2 |             -578.6 |
| GOLDPETAL/GOLDTEN  | 2025-04-30 |               81.9 |                 2.5 |            75.7 |                     100 |                  30 |                    2.4 |                 3   |            106.5 |                          1.1 |             -418   |
| GOLDPETAL/GOLDTEN  | 2025-05-30 |               38.6 |                -2.1 |            39.1 |                     100 |                  30 |                    2.4 |                 3   |             69.7 |                          0.7 |             -458.1 |
| GOLDPETAL/GOLDTEN  | 2025-06-30 |               72.6 |                -2.2 |            74.1 |                     100 |                  30 |                    2.2 |                 3   |            104   |                          1   |             -440.8 |
| GOLDPETAL/GOLDTEN  | 2025-07-31 |               71   |                 8.9 |            61.3 |                     100 |                  30 |                    2.2 |                 3   |             91.3 |                          0.9 |             -451.3 |
| GOLDPETAL/GOLDTEN  | 2025-08-29 |               30.8 |                10.1 |            20.6 |                     100 |                  30 |                    2.2 |                 3   |             50.4 |                          0.5 |             -496.5 |
| GOLDPETAL/GOLDTEN  | 2025-09-30 |               -6.7 |                -6.2 |            -0.6 |                     100 |                  30 |                    2.6 |                 3.3 |             25.1 |                          0.2 |             -600.4 |
| GOLDPETAL/GOLDTEN  | 2025-10-31 |               89.6 |                 3.8 |           105   |                     100 |                  30 |                    2.7 |                 3.5 |            128.2 |                          1   |             -544.6 |
| GOLDPETAL/GOLDTEN  | 2025-11-28 |              145.8 |                -6.3 |           187.5 |                     100 |                  30 |                    2.7 |                 3.5 |            210.5 |                          1.7 |             -467.4 |
| GOLDPETAL/GOLDTEN  | 2025-12-31 |              113.2 |                 3.5 |           150.7 |                     100 |                  30 |                    3   |                 3.7 |            169.7 |                          1.2 |             -586.5 |
| GOLDPETAL/GOLDTEN  | 2026-01-30 |              201.6 |              -166   |           586.1 |                     100 |                  30 |                    3.6 |                 4.1 |            598.6 |                          3.8 |             -278.2 |
| GOLDPETAL/GOLDTEN  | 2026-02-27 |              234   |                -8.4 |           383   |                     100 |                  30 |                    3.4 |                 4.1 |            396   |                          2.5 |             -473.1 |
| GOLDPETAL/GOLDTEN  | 2026-03-31 |              146.9 |                -2.9 |           216.2 |                     100 |                  30 |                    3.2 |                 3.8 |            233.1 |                          1.6 |             -560.3 |
| GOLDPETAL/GOLDTEN  | 2026-04-30 |               83   |                -7.9 |           136.8 |                     100 |                  30 |                    3.3 |                 3.9 |            151.9 |                          1   |             -675.9 |
| GOLDPETAL/GOLDTEN  | 2026-05-29 |               30.1 |               -21.8 |            81.6 |                     100 |                  30 |                    3.6 |                 4   |             94.6 |                          0.6 |             -770   |
| GOLDPETAL/GOLDTEN  | 2026-06-30 |               51.8 |               -20.5 |           101.6 |                     100 |                  30 |                    3   |                 3.8 |            119.7 |                          0.9 |             -652.9 |
| GOLDPETAL/GOLDTEN  | 2026-07-31 |               23   |                -4.7 |            39.2 |                     100 |                  30 |                    3.1 |                 3.8 |             56.9 |                          0.4 |             -721.9 |
| GOLDPETAL/GOLDTEN  | 2026-08-31 |               36.8 |               -25.6 |            99.8 |                     100 |                  30 |                    3.5 |                 4.1 |            112.3 |                          0.7 |             -767.7 |
| GOLDPETAL/GOLDTEN  | 2026-09-30 |               17.7 |                -1.1 |            28.4 |                     100 |                  30 |                    3.4 |                 3.9 |             43.2 |                          0.3 |             -789.7 |

## 7. Delivery headroom without the two assumed costs (bar resale discount, logistics)

|                                               |   headroom_inr_g |   headroom_ex_assumed |   breakeven_coin_premium_pct |   breakeven_ex_assumed_pct |
|:----------------------------------------------|-----------------:|----------------------:|-----------------------------:|---------------------------:|
| ('GOLDGUINEA/GOLDTEN', 'early (60+ days)')    |            69.02 |                112.72 |                         0.47 |                       0.79 |
| ('GOLDGUINEA/GOLDTEN', 'last pre-tender day') |            42.2  |                 84.82 |                         0.27 |                       0.6  |
| ('GOLDPETAL/GOLDTEN', 'early (60+ days)')     |           177.17 |                220.88 |                         1.28 |                       1.61 |
| ('GOLDPETAL/GOLDTEN', 'last pre-tender day')  |           153.44 |                196.06 |                         1.13 |                       1.46 |

## 8. Current contract regime without Jan-Mar 2026: every config (in-sample, contracts expiring Apr 2025 on)

| config         |   ('mean', 'GOLDGUINEA/GOLDTEN') |   ('mean', 'GOLDPETAL/GOLDGUINEA') |   ('mean', 'GOLDPETAL/GOLDTEN') |   ('size', 'GOLDGUINEA/GOLDTEN') |   ('size', 'GOLDPETAL/GOLDGUINEA') |   ('size', 'GOLDPETAL/GOLDTEN') |
|:---------------|---------------------------------:|-----------------------------------:|--------------------------------:|---------------------------------:|-----------------------------------:|--------------------------------:|
| DRIFT          |                             -0.6 |                              -12.7 |                             7.4 |                               15 |                                 15 |                              16 |
| MR(W=20,k=1.0) |                              9.5 |                                1.8 |                             6.3 |                              102 |                                112 |                             102 |
| MR(W=20,k=1.5) |                             11.5 |                                1.9 |                             5.7 |                               72 |                                 91 |                              68 |
| MR(W=20,k=2.0) |                             14.2 |                                2.9 |                             7.7 |                               44 |                                 54 |                              42 |
| MR(W=40,k=1.0) |                              7.8 |                                4.7 |                             1.8 |                               44 |                                 57 |                              40 |
| MR(W=40,k=1.5) |                              8.7 |                                6.5 |                             5.8 |                               31 |                                 34 |                              26 |
| MR(W=40,k=2.0) |                             13.7 |                                5.1 |                             4.3 |                               16 |                                 16 |                              16 |
| MR(W=60,k=1.0) |                              9.8 |                                0.9 |                             2.9 |                               12 |                                 24 |                              13 |
| MR(W=60,k=1.5) |                             11.4 |                                7.4 |                            10.9 |                                6 |                                 10 |                               8 |
| MR(W=60,k=2.0) |                            nan   |                                7.9 |                            17.7 |                              nan |                                  6 |                               3 |

Configs with a positive mean: GOLDGUINEA/GOLDTEN: 8 of 10, GOLDPETAL/GOLDGUINEA: 9 of 10, GOLDPETAL/GOLDTEN: 10 of 10

## 9. Walk-forward by contract era (out-of-sample)

|                                             |   size |   mean |   median |
|:--------------------------------------------|-------:|-------:|---------:|
| ('GOLDGUINEA/GOLDTEN', 'Apr 2025 on')       |     29 |   44   |     24.3 |
| ('GOLDPETAL/GOLDGUINEA', 'Apr 2025 on')     |     36 |   14.2 |      9.1 |
| ('GOLDPETAL/GOLDGUINEA', 'before Apr 2025') |    102 |   -7.3 |     -1.7 |
| ('GOLDPETAL/GOLDTEN', 'Apr 2025 on')        |     40 |   33.5 |      5.1 |

## 10. Pre-registered forward test: walk-forward trades entered after 22 Oct 2026

No forward trades yet.
