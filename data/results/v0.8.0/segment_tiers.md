# Segment-count tiering (pred vs ground-truth segments)

Rules (relative error = |pred - gt| / gt):

- **Success**: relative error ≤ 5% (over- or under-segmented within 5%).
- **Average**: relative error > 5% and ≤ 20%.
- **Big failure**: relative error > 20%.
- **Extraction failure**: run errored (no metrics), e.g. API/image errors.

**Source run**: 2026-04-20T07:37:14.618419+00:00 — **documents**: 124

## Counts

| Tier | Count |
| --- | ---: |
| Success (≤5%) | 30 |
| Average (5%–20%) | 16 |
| Big failure (>20%) | 60 |
| Extraction failure | 18 |

## Best performers — success tier (sorted by F1@100, then title F1)

Documents where segment count matched ground truth within **5%**.

| Rank | Document | Pred/GT | Rel % vs GT | F1@100 | Title F1 |
| --- | --- | --- | --- | --- | --- |
| 1 | W3KG239_I3KG1025_474df5_google_books | 20/20 | 0.00% | 1.0000 | 1.0000 |
| 2 | W3CN5929_I3CN5936_2e3692_google_books | 15/15 | 0.00% | 1.0000 | 1.0000 |
| 3 | W3PD229_I2PD20057_ccbc3f_google_books | 9/9 | 0.00% | 1.0000 | 1.0000 |
| 4 | W2KG208030_I2KG208057_6fe1ab_google_books | 8/8 | 0.00% | 1.0000 | 1.0000 |
| 5 | W2KG212708_I2KG213918_19542c_google_books | 7/7 | 0.00% | 1.0000 | 1.0000 |
| 6 | W3CN5929_I3CN5935_f5a53d_google_books | 7/7 | 0.00% | 1.0000 | 1.0000 |
| 7 | W3CN22340_I4CN10050_b08c5b_google_books | 26/26 | 0.00% | 0.9615 | 1.0000 |
| 8 | W1KG16653_I4PD2722_ec63ef_google_books | 21/21 | 0.00% | 0.9524 | 0.7619 |
| 9 | W2KG212708_I2KG213913_493dcb_google_books | 19/19 | 0.00% | 0.9474 | 0.8421 |
| 10 | W1KG16653_I4PD2705_f7f5c4_google_books | 17/17 | 0.00% | 0.9412 | 1.0000 |
| 11 | W1PD133170_I2PD19749_6c2b30_google_books | 41/40 | 2.50% | 0.9383 | 0.9877 |
| 12 | W3CN21547_I3CN21953_88a8c0_google_books | 15/15 | 0.00% | 0.9333 | 0.9333 |
| 13 | W2KG208030_I2KG208058_a450f6_google_books | 14/14 | 0.00% | 0.9286 | 1.0000 |
| 14 | W3CN3416_I3CN8607_0cf1ef_google_books | 52/52 | 0.00% | 0.9038 | 0.9808 |
| 15 | W1PD137884_I2PD18589_03dd81_google_books | 29/29 | 0.00% | 0.8966 | 0.9655 |
| 16 | W3KG53_I3KG292_c529e9_google_books | 33/34 | 2.94% | 0.8955 | 0.8955 |
| 17 | W3CN5929_I3CN5939_4ce70d_google_books | 9/9 | 0.00% | 0.8889 | 1.0000 |
| 18 | W3CN5929_I3CN5938_054238_google_books | 9/9 | 0.00% | 0.8889 | 0.8889 |
| 19 | W2PD17465_I4PD1679_f28e45_google_books | 28/28 | 0.00% | 0.7857 | 0.3571 |
| 20 | W1KG16652_I4PD2623_3a5420_google_books | 9/9 | 0.00% | 0.7778 | 1.0000 |
| 21 | W3CN25710_I3CN25805_b757c0_google_books | 9/9 | 0.00% | 0.6667 | 0.7778 |
| 22 | W2PD17429_I4PD2569_eaafd9_google_books | 5/5 | 0.00% | 0.6000 | 0.8000 |
| 23 | W2PD17465_I4PD1687_440c1e_google_books | 69/70 | 1.43% | 0.5899 | 0.7429 |
| 24 | W2KG212706_I2KG213897_cc54e6_google_books | 19/20 | 5.00% | 0.5128 | 0.9744 |
| 25 | W2PD17465_I4PD1675_a06840_google_books | 21/22 | 4.55% | 0.5116 | 0.5000 |
| 26 | W2KG201051_I2KG207544_a3983a_google_books | 8/8 | 0.00% | 0.5000 | 0.8750 |
| 27 | W1PD137839_I1KG24141_2a65b2_google_vision | 7/7 | 0.00% | 0.2857 | 1.0000 |
| 28 | W2PD17465_I4PD1682_878767_google_books | 43/42 | 2.38% | 0.2824 | 0.7765 |
| 29 | W3KG53_I3KG295_ee1e5e_google_books | 9/9 | 0.00% | 0.2222 | 1.0000 |
| 30 | W1PD137839_I1KG24160_f6178b_google_vision | 9/9 | 0.00% | 0.1111 | 1.0000 |

## Average tier (5% < relative error ≤ 20%)

| Document | Pred/GT | Rel % vs GT | F1@100 | Title F1 |
| --- | --- | --- | --- | --- |
| W3CN22339_I4CN10021_601a5e_google_books | 16/17 | 5.88% | 0.7879 | 1.0000 |
| W1KG16653_I4PD2712_c0f0c6_google_books | 15/16 | 6.25% | 0.8387 | 0.8750 |
| W2KG208030_I2KG208051_5d6f2b_google_books | 16/15 | 6.67% | 0.9032 | 0.9032 |
| W3CN5929_I3CN5942_876811_google_books | 15/14 | 7.14% | 0.8966 | 0.9655 |
| W3CN25710_I3CN25800_766083_google_books | 13/14 | 7.14% | 0.7407 | 0.6429 |
| W2KG201051_I2KG207546_a2ae4b_google_books | 13/14 | 7.14% | 0.6667 | 0.8571 |
| W2PD17465_I4PD1688_ff0ce9_google_books | 11/10 | 10.00% | 0.7619 | 0.7619 |
| W2PD19769_I2PD19953_48cfb2_google_vision | 60/54 | 11.11% | 0.6667 | 0.6842 |
| W1PD137838_I2PD18305_fa75b3_google_books | 8/9 | 11.11% | 0.5882 | 1.0000 |
| W4PD502_I4PD4111_7e82fa_google_books | 7/8 | 12.50% | 0.9333 | 0.9333 |
| W3CN22953_I4CN10448_1c3c7f_google_books | 7/8 | 12.50% | 0.6667 | 0.8750 |
| W1KG11903_I1KG12023_aa5962_google_books | 5/6 | 16.67% | 0.3636 | 1.0000 |
| W3CN22339_I4CN10011_b5dd4d_google_books | 45/38 | 18.42% | 0.0482 | 0.8571 |
| W1KG4324_I1KG4382_5b4620_google_books | 8/10 | 20.00% | 0.6667 | 1.0000 |
| W2PD17465_I4PD1681_ffbd04_google_books | 6/5 | 20.00% | 0.5455 | 0.1818 |
| W2PD16805_I4PD2844_7b4b07_google_books | 36/30 | 20.00% | 0.0303 | 0.0000 |

## Big failure tier (relative error > 20%)

| Document | Pred/GT | Rel % vs GT | F1@100 | Title F1 |
| --- | --- | --- | --- | --- |
| W2PD19769_I2PD19951_606b1d_google_vision | 97/5 | 1840.00% | 0.0392 | 0.0385 |
| W4PD502_I4PD4104_4c78da_google_books | 91/5 | 1720.00% | 0.0208 | 0.0385 |
| W4PD502_I4PD4099_5bd464_google_books | 85/5 | 1600.00% | 0.0222 | 0.0652 |
| W3CN22340_I4CN10040_64ff40_google_books | 68/5 | 1260.00% | 0.1370 | 0.1370 |
| W4PD502_I4PD4091_50d5d2_google_books | 79/6 | 1216.67% | 0.0235 | 0.0465 |
| W2PD16805_I4PD2884_738ecd_google_books | 91/7 | 1200.00% | 0.0408 | 0.0202 |
| W4PD502_I4PD4102_dbc7d6_google_books | 86/7 | 1128.57% | 0.1075 | 0.0645 |
| W2PD19769_I2PD19971_cbcf74_google_vision | 104/9 | 1055.56% | 0.0708 | 0.0877 |
| W2PD19769_I2PD19942_22e942_google_vision | 92/8 | 1050.00% | 0.1400 | 0.1400 |
| W4PD502_I4PD3973_8374fc_google_books | 90/8 | 1025.00% | 0.0204 | 0.0204 |
| W4PD502_I4PD4101_075f2e_google_books | 88/9 | 877.78% | 0.0000 | 0.0577 |
| W4PD502_I4PD4092_6662d8_google_books | 57/6 | 850.00% | 0.0635 | 0.0909 |
| W3CN21526_I3CN21726_002128_google_books | 91/10 | 810.00% | 0.1584 | 0.1373 |
| W2PD16805_I4PD2871_5c2590_google_books | 59/7 | 742.86% | 0.0606 | 0.0000 |
| W4PD502_I4PD4114_24e317_google_books | 56/7 | 700.00% | 0.1905 | 0.0000 |
| W4PD502_I4PD4097_bbaa69_google_vision | 85/13 | 553.85% | 0.0612 | 0.1284 |
| W2KG5037_I2KG217541_5a348d_google_books | 50/8 | 525.00% | 0.1379 | 0.1316 |
| W3CN21525_I3CN21724_bb7ef7_google_books | 43/7 | 514.29% | 0.2000 | 0.1961 |
| W1PD159398_I4PD3450_888ee9_google_vision | 53/12 | 341.67% | 0.1538 | 0.3692 |
| W2PD16805_I4PD2870_932210_google_books | 34/8 | 325.00% | 0.0000 | 0.0476 |
| W2PD16805_I4PD2866_d95858_google_books | 42/10 | 320.00% | 0.0000 | 0.0000 |
| W2KG5037_I2KG217547_378462_google_books | 29/7 | 314.29% | 0.0556 | 0.1860 |
| W1KG16652_I4PD2605_7520a8_google_books | 23/7 | 228.57% | 0.3333 | 0.4000 |
| W2KG5037_I2KG217572_c270bc_google_books | 22/7 | 214.29% | 0.0690 | 0.0702 |
| W3CN21526_I3CN21730_cf3017_google_books | 18/6 | 200.00% | 0.4167 | 0.5000 |
| W2PD16805_I4PD2841_90d121_google_books | 48/18 | 166.67% | 0.0000 | 0.0000 |
| W2PD16805_I4PD2817_e32786_google_books | 33/13 | 153.85% | 0.0435 | 0.0000 |
| W2PD16805_I4PD2855_1c6661_google_books | 23/10 | 130.00% | 0.0000 | 0.0000 |
| W1KG11871_I1KG16476_777578_google_books | 0/54 | 100.00% | 0.0000 | 0.0000 |
| W1PD137839_I1KG24136_65ea89_google_vision | 0/7 | 100.00% | 0.0000 | 0.0000 |
| W1PD137839_I1KG24132_29e646_google_vision | 0/5 | 100.00% | 0.0000 | 0.0000 |
| W3CN22339_I4CN10014_3fac10_google_books | 43/22 | 95.45% | 0.4000 | 0.4615 |
| W1KG16655_I4PD2662_31cc1d_google_books | 2/16 | 87.50% | 0.0000 | 1.0000 |
| W3CN25710_I3CN25794_2f1b10_google_books | 15/8 | 87.50% | 0.4348 | 0.4348 |
| W2PD16805_I4PD2845_944b66_google_books | 24/13 | 84.62% | 0.0000 | 0.0000 |
| W3KG55_I3KG325_391e7b_google_books | 2/10 | 80.00% | 0.0000 | 0.3333 |
| W1KG11871_I1KG16480_9321c4_google_books | 4/19 | 78.95% | 0.3478 | 0.0000 |
| W4CZ46031_I4CZ46033_4602af_google_vision | 2/9 | 77.78% | 0.1818 | 0.0000 |
| W4CZ364088_I4CZ367200_631368_google_books | 52/30 | 73.33% | 0.4146 | 0.4368 |
| W2PD16805_I4PD2840_803703_google_books | 24/14 | 71.43% | 0.0000 | 0.0000 |
| W1KG16648_I4PD2559_0459be_google_books | 12/40 | 70.00% | 0.4615 | 0.8354 |
| W1AC375_I4PD2770_60e0c1_google_books | 2/5 | 60.00% | 0.0000 | 1.0000 |
| W1KG16655_I4PD2649_682015_google_books | 9/19 | 52.63% | 0.4286 | 0.6207 |
| W2PD19769_I2PD19957_878e5f_google_vision | 21/14 | 50.00% | 0.5714 | 0.6667 |
| W1KG17189_I1KG17469_c8c886_google_books | 16/28 | 42.86% | 0.3636 | 0.7273 |
| W8LS20390_I8LS20413_d18521_google_books | 10/7 | 42.86% | 0.4706 | 0.3529 |
| W2KG5037_I2KG217544_1d2fec_google_books | 17/12 | 41.67% | 0.2069 | 0.1778 |
| W2PD16805_I4PD2839_09db12_google_books | 24/17 | 41.18% | 0.0488 | 0.0488 |
| W3CN3416_I3CN8608_53c1c2_google_books | 19/14 | 35.71% | 0.3030 | 0.7778 |
| W2KG209077_I2KG209091_f4b05c_google_books | 13/20 | 35.00% | 0.7273 | 0.7273 |
| W2PD17538_I4PD1569_eddef2_google_books | 25/37 | 32.43% | 0.2258 | 0.2133 |
| W2PD19769_I2PD19967_2cf72a_google_vision | 9/13 | 30.77% | 0.5455 | 0.8333 |
| W2KG5037_I2KG217546_947ce7_google_books | 9/7 | 28.57% | 0.3750 | 0.2500 |
| W2KG5037_I2KG217533_7486b0_google_books | 10/14 | 28.57% | 0.5000 | 0.7333 |
| W3PD189_I2PD18694_40d8f8_google_books | 10/14 | 28.57% | 0.6667 | 0.8966 |
| W4PD504_I4PD4404_de4fff_google_books | 38/30 | 26.67% | 0.5294 | 0.3478 |
| W2KG5037_I2KG217543_411839_google_books | 36/29 | 24.14% | 0.6462 | 0.6944 |
| W2KG209077_I2KG209092_05189f_google_books | 19/25 | 24.00% | 0.7727 | 0.7727 |
| W3CN21563_I3CN21985_eb40d1_google_books | 13/17 | 23.53% | 0.1333 | 0.6000 |
| W2PD17465_I4PD1678_d9cbaf_google_books | 49/40 | 22.50% | 0.4045 | 0.4719 |

## Extraction / API failures (no successful metrics)

| Document | Error (truncated) |
| --- | --- |
| W3JT13533_I3KG1460_c4003c_google_vision | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3JT13533_I3KG1466_c5ef66_google_vision | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W4CZ354445_I4CZ355076_0ae8c1_google_books | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3JT13533_I3KG1462_2640fb_google_vision | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3JT13533_I3KG1484_b36760_google_vision | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W4CZ57130_I4CZ57139_471489_google_books | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3PD188_I3PD276_e7b213_google_books | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W4CZ57130_I4CZ57135_215bdd_google_books | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3PD188_I3PD275_e02d59_google_books | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W4CZ62374_I4CZ62376_ef5a59_google_books | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3JT13533_I3KG1464_1cf3de_google_vision | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3JT13533_I3KG1459_0bfb20_google_vision | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3JT13533_I3KG1463_02dbec_google_vision | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3JT13533_I3KG1487_2f6753_google_vision | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3PD188_I3PD280_dc995b_google_books | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3JT13533_I3KG1465_e68ae8_google_vision | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3JT13533_I3KG1455_b268d6_google_vision | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
| W3PD188_I3PD272_c566b6_google_books | 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https... |
