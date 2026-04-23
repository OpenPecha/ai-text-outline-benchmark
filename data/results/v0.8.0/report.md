# Benchmark Evaluation Report

**Package version**: 0.7.0
**Timestamp**: 2026-04-20T07:37:14.618419+00:00
**Documents evaluated**: 124
**Success rate**: 0.8548

## Aggregate Metrics

| Metric                    |    Mean |     Std |   Min |     Max |
|---------------------------|---------|---------|-------|---------|
| Breakpoint F1 @50         |  0.3961 |  0.3428 |     0 |  1      |
| Breakpoint F1 @100        |  0.4316 |  0.3511 |     0 |  1      |
| Breakpoint F1 @200        |  0.4613 |  0.3604 |     0 |  1      |
| Breakpoint F1 @500        |  0.4796 |  0.3605 |     0 |  1      |
| Segment Count MAE         | 17.6792 | 26.866  |     0 | 95      |
| Title F1                  |  0.5376 |  0.3943 |     0 |  1      |
| Pk (lower=better)         |  0.2066 |  0.2033 |     0 |  0.8572 |
| WindowDiff (lower=better) |  0.2646 |  0.2394 |     0 |  1      |

## Per-Document Results

| Document                                 | Pred/GT Segs   | F1@100   | F1@200   | Title F1   | Pk     | Status   |
|------------------------------------------|----------------|----------|----------|------------|--------|----------|
| W3JT13533_I3KG1460_c4003c_google_vision  | ERROR          | -        | -        | -          | -      | -        |
| W3JT13533_I3KG1466_c5ef66_google_vision  | ERROR          | -        | -        | -          | -      | -        |
| W4CZ354445_I4CZ355076_0ae8c1_google_book | ERROR          | -        | -        | -          | -      | -        |
| W2PD17465_I4PD1687_440c1e_google_books   | 69/70          | 0.5899   | 0.7626   | 0.7429     | 0.0508 | OK       |
| W3JT13533_I3KG1462_2640fb_google_vision  | ERROR          | -        | -        | -          | -      | -        |
| W3JT13533_I3KG1484_b36760_google_vision  | ERROR          | -        | -        | -          | -      | -        |
| W2PD19769_I2PD19953_48cfb2_google_vision | 60/54          | 0.6667   | 0.6667   | 0.6842     | 0.1694 | OK       |
| W1KG11871_I1KG16476_777578_google_books  | 0/54           | 0.0      | 0.0      | 0.0        | 0.4046 | OK       |
| W3CN3416_I3CN8607_0cf1ef_google_books    | 52/52          | 0.9038   | 0.9038   | 0.9808     | 0.0336 | OK       |
| W4CZ57130_I4CZ57139_471489_google_books  | ERROR          | -        | -        | -          | -      | -        |
| W2PD17465_I4PD1682_878767_google_books   | 43/42          | 0.2824   | 0.8235   | 0.7765     | 0.0883 | OK       |
| W2PD17465_I4PD1678_d9cbaf_google_books   | 49/40          | 0.4045   | 0.7865   | 0.4719     | 0.1038 | OK       |
| W1KG16648_I4PD2559_0459be_google_books   | 12/40          | 0.4615   | 0.4615   | 0.8354     | 0.2727 | OK       |
| W3PD188_I3PD276_e7b213_google_books      | ERROR          | -        | -        | -          | -      | -        |
| W1PD133170_I2PD19749_6c2b30_google_books | 41/40          | 0.9383   | 0.963    | 0.9877     | 0.0272 | OK       |
| W3CN22339_I4CN10011_b5dd4d_google_books  | 45/38          | 0.0482   | 0.1687   | 0.8571     | 0.0321 | OK       |
| W2PD17538_I4PD1569_eddef2_google_books   | 25/37          | 0.2258   | 0.2258   | 0.2133     | 0.3896 | OK       |
| W3KG53_I3KG292_c529e9_google_books       | 33/34          | 0.8955   | 0.8955   | 0.8955     | 0.0169 | OK       |
| W4PD504_I4PD4404_de4fff_google_books     | 38/30          | 0.5294   | 0.5588   | 0.3478     | 0.1457 | OK       |
| W4CZ364088_I4CZ367200_631368_google_book | 52/30          | 0.4146   | 0.439    | 0.4368     | 0.2802 | OK       |
| W2PD16805_I4PD2844_7b4b07_google_books   | 36/30          | 0.0303   | 0.0303   | 0.0        | 0.4261 | OK       |
| W2KG5037_I2KG217543_411839_google_books  | 36/29          | 0.6462   | 0.6462   | 0.6944     | 0.079  | OK       |
| W1PD137884_I2PD18589_03dd81_google_books | 29/29          | 0.8966   | 0.8966   | 0.9655     | 0.0099 | OK       |
| W1KG17189_I1KG17469_c8c886_google_books  | 16/28          | 0.3636   | 0.3636   | 0.7273     | 0.2121 | OK       |
| W2PD17465_I4PD1679_f28e45_google_books   | 28/28          | 0.7857   | 0.8214   | 0.3571     | 0.0923 | OK       |
| W4CZ57130_I4CZ57135_215bdd_google_books  | ERROR          | -        | -        | -          | -      | -        |
| W3CN22340_I4CN10050_b08c5b_google_books  | 26/26          | 0.9615   | 0.9615   | 1.0        | 0.0008 | OK       |
| W2KG209077_I2KG209092_05189f_google_book | 19/25          | 0.7727   | 0.7727   | 0.7727     | 0.01   | OK       |
| W3CN22339_I4CN10014_3fac10_google_books  | 43/22          | 0.4      | 0.4      | 0.4615     | 0.3307 | OK       |
| W2PD17465_I4PD1675_a06840_google_books   | 21/22          | 0.5116   | 0.8372   | 0.5        | 0.0522 | OK       |
| W1KG16653_I4PD2722_ec63ef_google_books   | 21/21          | 0.9524   | 1.0      | 0.7619     | 0.001  | OK       |
| W2KG212706_I2KG213897_cc54e6_google_book | 19/20          | 0.5128   | 0.5641   | 0.9744     | 0.1635 | OK       |
| W3KG239_I3KG1025_474df5_google_books     | 20/20          | 1.0      | 1.0      | 1.0        | 0.0008 | OK       |
| W2KG209077_I2KG209091_f4b05c_google_book | 13/20          | 0.7273   | 0.7273   | 0.7273     | 0.0996 | OK       |
| W2KG212708_I2KG213913_493dcb_google_book | 19/19          | 0.9474   | 0.9474   | 0.8421     | 0.0065 | OK       |
| W1KG16655_I4PD2649_682015_google_books   | 9/19           | 0.4286   | 0.4286   | 0.6207     | 0.0814 | OK       |
| W1KG11871_I1KG16480_9321c4_google_books  | 4/19           | 0.3478   | 0.3478   | 0.0        | 0.2845 | OK       |
| W2PD16805_I4PD2841_90d121_google_books   | 48/18          | 0.0      | 0.0      | 0.0        | 0.4255 | OK       |
| W3PD188_I3PD275_e02d59_google_books      | ERROR          | -        | -        | -          | -      | -        |
| W3CN22339_I4CN10021_601a5e_google_books  | 16/17          | 0.7879   | 0.7879   | 1.0        | 0.0335 | OK       |
| W2PD16805_I4PD2839_09db12_google_books   | 24/17          | 0.0488   | 0.0488   | 0.0488     | 0.4087 | OK       |
| W1KG16653_I4PD2705_f7f5c4_google_books   | 17/17          | 0.9412   | 0.9412   | 1.0        | 0.0002 | OK       |
| W3CN21563_I3CN21985_eb40d1_google_books  | 13/17          | 0.1333   | 0.2      | 0.6        | 0.2171 | OK       |
| W1KG16655_I4PD2662_31cc1d_google_books   | 2/16           | 0.0      | 0.0      | 1.0        | 0.3043 | OK       |
| W1KG16653_I4PD2712_c0f0c6_google_books   | 15/16          | 0.8387   | 0.8387   | 0.875      | 0.037  | OK       |
| W2KG208030_I2KG208051_5d6f2b_google_book | 16/15          | 0.9032   | 0.9032   | 0.9032     | 0.007  | OK       |
| W3CN5929_I3CN5936_2e3692_google_books    | 15/15          | 1.0      | 1.0      | 1.0        | 0.0    | OK       |
| W3CN21547_I3CN21953_88a8c0_google_books  | 15/15          | 0.9333   | 0.9333   | 0.9333     | 0.0006 | OK       |
| W2PD16805_I4PD2840_803703_google_books   | 24/14          | 0.0      | 0.0      | 0.0        | 0.3855 | OK       |
| W3PD189_I2PD18694_40d8f8_google_books    | 10/14          | 0.6667   | 0.6667   | 0.8966     | 0.1199 | OK       |
| W2KG208030_I2KG208058_a450f6_google_book | 14/14          | 0.9286   | 0.9286   | 1.0        | 0.0056 | OK       |
| W3CN25710_I3CN25800_766083_google_books  | 13/14          | 0.7407   | 0.7407   | 0.6429     | 0.0111 | OK       |
| W3CN3416_I3CN8608_53c1c2_google_books    | 19/14          | 0.303    | 0.303    | 0.7778     | 0.1876 | OK       |
| W2PD19769_I2PD19957_878e5f_google_vision | 21/14          | 0.5714   | 0.5714   | 0.6667     | 0.2651 | OK       |
| W2KG201051_I2KG207546_a2ae4b_google_book | 13/14          | 0.6667   | 0.7407   | 0.8571     | 0.0433 | OK       |
| W2KG5037_I2KG217533_7486b0_google_books  | 10/14          | 0.5      | 0.5      | 0.7333     | 0.0965 | OK       |
| W3CN5929_I3CN5942_876811_google_books    | 15/14          | 0.8966   | 0.8966   | 0.9655     | 0.0264 | OK       |
| W2PD19769_I2PD19967_2cf72a_google_vision | 9/13           | 0.5455   | 0.5455   | 0.8333     | 0.1959 | OK       |
| W4CZ62374_I4CZ62376_ef5a59_google_books  | ERROR          | -        | -        | -          | -      | -        |
| W4PD502_I4PD4097_bbaa69_google_vision    | 85/13          | 0.0612   | 0.0612   | 0.1284     | 0.4779 | OK       |
| W2PD16805_I4PD2817_e32786_google_books   | 33/13          | 0.0435   | 0.087    | 0.0        | 0.4338 | OK       |
| W2PD16805_I4PD2845_944b66_google_books   | 24/13          | 0.0      | 0.0      | 0.0        | 0.4584 | OK       |
| W2KG5037_I2KG217544_1d2fec_google_books  | 17/12          | 0.2069   | 0.2069   | 0.1778     | 0.2497 | OK       |
| W1PD159398_I4PD3450_888ee9_google_vision | 53/12          | 0.1538   | 0.1846   | 0.3692     | 0.4914 | OK       |
| W1KG4324_I1KG4382_5b4620_google_books    | 8/10           | 0.6667   | 0.7778   | 1.0        | 0.1387 | OK       |
| W2PD16805_I4PD2855_1c6661_google_books   | 23/10          | 0.0      | 0.0606   | 0.0        | 0.4604 | OK       |
| W2PD17465_I4PD1688_ff0ce9_google_books   | 11/10          | 0.7619   | 0.8571   | 0.7619     | 0.0543 | OK       |
| W3CN21526_I3CN21726_002128_google_books  | 91/10          | 0.1584   | 0.1584   | 0.1373     | 0.2501 | OK       |
| W2PD16805_I4PD2866_d95858_google_books   | 42/10          | 0.0      | 0.0      | 0.0        | 0.5454 | OK       |
| W3KG55_I3KG325_391e7b_google_books       | 2/10           | 0.0      | 0.0      | 0.3333     | 0.3731 | OK       |
| W1KG16652_I4PD2623_3a5420_google_books   | 9/9            | 0.7778   | 0.7778   | 1.0        | 0.0652 | OK       |
| W3KG53_I3KG295_ee1e5e_google_books       | 9/9            | 0.2222   | 0.4444   | 1.0        | 0.0029 | OK       |
| W3CN5929_I3CN5938_054238_google_books    | 9/9            | 0.8889   | 0.8889   | 0.8889     | 0.0    | OK       |
| W3CN25710_I3CN25805_b757c0_google_books  | 9/9            | 0.6667   | 0.6667   | 0.7778     | 0.0052 | OK       |
| W1PD137839_I1KG24160_f6178b_google_visio | 9/9            | 0.1111   | 0.1111   | 1.0        | 0.227  | OK       |
| W3PD229_I2PD20057_ccbc3f_google_books    | 9/9            | 1.0      | 1.0      | 1.0        | 0.0    | OK       |
| W4CZ46031_I4CZ46033_4602af_google_vision | 2/9            | 0.1818   | 0.1818   | 0.0        | 0.2046 | OK       |
| W2PD19769_I2PD19971_cbcf74_google_vision | 104/9          | 0.0708   | 0.0708   | 0.0877     | 0.59   | OK       |
| W1PD137838_I2PD18305_fa75b3_google_books | 8/9            | 0.5882   | 0.5882   | 1.0        | 0.0285 | OK       |
| W4PD502_I4PD4101_075f2e_google_books     | 88/9           | 0.0      | 0.0      | 0.0577     | 0.5822 | OK       |
| W3CN5929_I3CN5939_4ce70d_google_books    | 9/9            | 0.8889   | 0.8889   | 1.0        | 0.0043 | OK       |
| W3JT13533_I3KG1464_1cf3de_google_vision  | ERROR          | -        | -        | -          | -      | -        |
| W3JT13533_I3KG1459_0bfb20_google_vision  | ERROR          | -        | -        | -          | -      | -        |
| W2KG201051_I2KG207544_a3983a_google_book | 8/8            | 0.5      | 0.625    | 0.875      | 0.0597 | OK       |
| W2KG208030_I2KG208057_6fe1ab_google_book | 8/8            | 1.0      | 1.0      | 1.0        | 0.0    | OK       |
| W3CN25710_I3CN25794_2f1b10_google_books  | 15/8           | 0.4348   | 0.4348   | 0.4348     | 0.1865 | OK       |
| W4PD502_I4PD4111_7e82fa_google_books     | 7/8            | 0.9333   | 0.9333   | 0.9333     | 0.0586 | OK       |
| W3JT13533_I3KG1463_02dbec_google_vision  | ERROR          | -        | -        | -          | -      | -        |
| W4PD502_I4PD3973_8374fc_google_books     | 90/8           | 0.0204   | 0.0204   | 0.0204     | 0.6034 | OK       |
| W3JT13533_I3KG1487_2f6753_google_vision  | ERROR          | -        | -        | -          | -      | -        |
| W2PD19769_I2PD19942_22e942_google_vision | 92/8           | 0.14     | 0.16     | 0.14       | 0.2383 | OK       |
| W3CN22953_I4CN10448_1c3c7f_google_books  | 7/8            | 0.6667   | 0.6667   | 0.875      | 0.0588 | OK       |
| W2KG5037_I2KG217541_5a348d_google_books  | 50/8           | 0.1379   | 0.1379   | 0.1316     | 0.4199 | OK       |
| W2PD16805_I4PD2870_932210_google_books   | 34/8           | 0.0      | 0.0      | 0.0476     | 0.4813 | OK       |
| W2KG5037_I2KG217546_947ce7_google_books  | 9/7            | 0.375    | 0.375    | 0.25       | 0.0122 | OK       |
| W1PD137839_I1KG24136_65ea89_google_visio | 0/7            | 0.0      | 0.0      | 0.0        | 0.2044 | OK       |
| W2PD16805_I4PD2884_738ecd_google_books   | 91/7           | 0.0408   | 0.0408   | 0.0202     | 0.1967 | OK       |
| W1KG16652_I4PD2605_7520a8_google_books   | 23/7           | 0.3333   | 0.3333   | 0.4        | 0.1047 | OK       |
| W2KG212708_I2KG213918_19542c_google_book | 7/7            | 1.0      | 1.0      | 1.0        | 0.0    | OK       |
| W4PD502_I4PD4114_24e317_google_books     | 56/7           | 0.1905   | 0.1905   | 0.0        | 0.3742 | OK       |
| W3PD188_I3PD280_dc995b_google_books      | ERROR          | -        | -        | -          | -      | -        |
| W2PD16805_I4PD2871_5c2590_google_books   | 59/7           | 0.0606   | 0.0606   | 0.0        | 0.3557 | OK       |
| W1PD137839_I1KG24141_2a65b2_google_visio | 7/7            | 0.2857   | 0.2857   | 1.0        | 0.0089 | OK       |
| W2KG5037_I2KG217547_378462_google_books  | 29/7           | 0.0556   | 0.0556   | 0.186      | 0.6489 | OK       |
| W3CN21525_I3CN21724_bb7ef7_google_books  | 43/7           | 0.2      | 0.2      | 0.1961     | 0.3881 | OK       |
| W3CN5929_I3CN5935_f5a53d_google_books    | 7/7            | 1.0      | 1.0      | 1.0        | 0.0    | OK       |
| W8LS20390_I8LS20413_d18521_google_books  | 10/7           | 0.4706   | 0.4706   | 0.3529     | 0.1328 | OK       |
| W2KG5037_I2KG217572_c270bc_google_books  | 22/7           | 0.069    | 0.069    | 0.0702     | 0.2435 | OK       |
| W4PD502_I4PD4102_dbc7d6_google_books     | 86/7           | 0.1075   | 0.1075   | 0.0645     | 0.0986 | OK       |
| W3JT13533_I3KG1465_e68ae8_google_vision  | ERROR          | -        | -        | -          | -      | -        |
| W4PD502_I4PD4091_50d5d2_google_books     | 79/6           | 0.0235   | 0.0235   | 0.0465     | 0.5405 | OK       |
| W3JT13533_I3KG1455_b268d6_google_vision  | ERROR          | -        | -        | -          | -      | -        |
| W3PD188_I3PD272_c566b6_google_books      | ERROR          | -        | -        | -          | -      | -        |
| W1KG11903_I1KG12023_aa5962_google_books  | 5/6            | 0.3636   | 0.5455   | 1.0        | 0.2619 | OK       |
| W4PD502_I4PD4092_6662d8_google_books     | 57/6           | 0.0635   | 0.0635   | 0.0909     | 0.6383 | OK       |
| W3CN21526_I3CN21730_cf3017_google_books  | 18/6           | 0.4167   | 0.4167   | 0.5        | 0.4655 | OK       |
| W1AC375_I4PD2770_60e0c1_google_books     | 2/5            | 0.0      | 0.0      | 1.0        | 0.0119 | OK       |
| W3CN22340_I4CN10040_64ff40_google_books  | 68/5           | 0.137    | 0.137    | 0.137      | 0.8572 | OK       |
| W2PD19769_I2PD19951_606b1d_google_vision | 97/5           | 0.0392   | 0.0392   | 0.0385     | 0.6863 | OK       |
| W4PD502_I4PD4104_4c78da_google_books     | 91/5           | 0.0208   | 0.0208   | 0.0385     | 0.3147 | OK       |
| W2PD17465_I4PD1681_ffbd04_google_books   | 6/5            | 0.5455   | 0.9091   | 0.1818     | 0.0011 | OK       |
| W2PD17429_I4PD2569_eaafd9_google_books   | 5/5            | 0.6      | 0.6      | 0.8        | 0.0957 | OK       |
| W4PD502_I4PD4099_5bd464_google_books     | 85/5           | 0.0222   | 0.0222   | 0.0652     | 0.528  | OK       |
| W1PD137839_I1KG24132_29e646_google_visio | 0/5            | 0.0      | 0.0      | 0.0        | 0.3394 | OK       |

## Failure Analysis

- **W3JT13533_I3KG1460_c4003c_google_vision**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3JT13533_I3KG1466_c5ef66_google_vision**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W4CZ354445_I4CZ355076_0ae8c1_google_books**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3JT13533_I3KG1462_2640fb_google_vision**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3JT13533_I3KG1484_b36760_google_vision**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W4CZ57130_I4CZ57139_471489_google_books**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3PD188_I3PD276_e7b213_google_books**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W4CZ57130_I4CZ57135_215bdd_google_books**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3PD188_I3PD275_e02d59_google_books**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W4CZ62374_I4CZ62376_ef5a59_google_books**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3JT13533_I3KG1464_1cf3de_google_vision**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3JT13533_I3KG1459_0bfb20_google_vision**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3JT13533_I3KG1463_02dbec_google_vision**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3JT13533_I3KG1487_2f6753_google_vision**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3PD188_I3PD280_dc995b_google_books**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3JT13533_I3KG1465_e68ae8_google_vision**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3JT13533_I3KG1455_b268d6_google_vision**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
- **W3PD188_I3PD272_c566b6_google_books**: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Unable to process input image. Please retry or report in https://developers.generativeai.google/guide/troubleshooting', 'status': 'INVALID_ARGUMENT'}}
