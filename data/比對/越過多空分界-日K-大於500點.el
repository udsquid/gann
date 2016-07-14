;; --- 行為 ---
;; 多數波段的波幅皆太短，大約只有 500~800 點，
;; 而一個基本對應角度約是 1500~1800，因此本身就不適用於波段推算上。
;; 故只能依 1000 點以上的波段來作判斷。
;;

;; --- 歸納 ---
;; 不少波段的波幅都只有 500~800 點，無法達到一個基本對應角度（約 1500~1800）。

;; --- 資料 ---
;; 
;; o: 9
;; x: 7
;; -: 13
;;
;; (+ 9 7 13)29
;; (* (/ 9  29.0) 100)31.03
;; (* (/ 7  29.0) 100)24.13
;; (* (/ 13 29.0) 100)44.82
;;

; 12682 -> 2485
(abs (- 12682 11550))                   ; -
(abs (- 11550 12321))                   ; -
(abs (- 12321 10995))                   ; o
(abs (- 10995 11720))                   ; -
(abs (- 11720 10887))                   ; -
(abs (- 10887 12065))                   ; x
(abs (- 12065 10145))                   ; o
(abs (- 10145 11282))                   ; -
(abs (- 11282 9405))                    ; x
(abs (- 9405 10011))                    ; -
(abs (- 10011 8652))                    ; x
(abs (- 8652 9838))                     ; x
(abs (- 9838 8252))                     ; x
(abs (- 8252 9062))                     ; -
(abs (- 9062 8125))                     ; -
(abs (- 8125 8689))                     ; -
(abs (- 8689 5822))                     ; o
(abs (- 5822 8007))                     ; o
(abs (- 8007 5758))                     ; o
(abs (- 5758 6606))                     ; -
(abs (- 6606 4450))                     ; o
(abs (- 4450 5286))                     ; x
(abs (- 5286 4522))                     ; -
(abs (- 4522 5825))                     ; x
(abs (- 5825 3788))                     ; o
(abs (- 3788 4391))                     ; -
(abs (- 4391 3021))                     ; o
(abs (- 3021 3812))                     ; -
(abs (- 3812 2485))                     ; o

; 2485 -> 6365
(abs (- 2485 3575))                     ; 1090
(abs (- 3575 3016))                     ; 559
(abs (- 3016 5027))                     ; 2011
(abs (- 5027 3986))                     ; 1041
(abs (- 3986 5267))                     ; 1281
(abs (- 5267 3773))                     ; 1494
(abs (- 3773 4533))                     ; 760
(abs (- 4533 3142))                     ; 1391
(abs (- 3142 5255))                     ; 2113
(abs (- 5255 4446))                     ; 809
(abs (- 4446 5715))                     ; 1269
(abs (- 5715 5202))                     ; 513
(abs (- 5202 6365))                     ; 1163

; 6365 -> 3098
(abs (- 6365 5681))                     ; 684
(abs (- 5681 6240))                     ; 559
(abs (- 6240 5556))                     ; 684
(abs (- 5556 6137))                     ; 581
(abs (- 6137 4781))                     ; 1356
(abs (- 4781 5282))                     ; 501
(abs (- 5282 4250))                     ; 1032
(abs (- 4250 4925))                     ; 675
(abs (- 4925 4032))                     ; 893
(abs (- 4032 5459))                     ; 1427
(abs (- 5459 4253))                     ; 1206
(abs (- 4253 4772))                     ; 519
(abs (- 4772 3098))                     ; 1674

; 3098 -> 7228
(abs (- 3098 5091))                     ; 1993
(abs (- 5091 3740))                     ; 1351
(abs (- 3740 6719))                     ; 2979
(abs (- 6719 5649))                     ; 1070
(abs (- 5649 6424))                     ; 775
(abs (- 6424 5125))                     ; 1299
(abs (- 5125 7228))                     ; 2103

; 7228 -> 4474
(abs (- 7228 5916))                     ; 1312
(abs (- 5916 6904))                     ; 988
(abs (- 6904 6153))                     ; 751
(abs (- 6153 7180))                     ; 1027
(abs (- 7180 6167))                     ; 1013
(abs (- 6167 6696))                     ; 529
(abs (- 6696 4474))                     ; 2222

; 4474 -> 10256
(abs (- 4474 5265))                     ; 791
(abs (- 5265 4530))                     ; 735
(abs (- 4530 5209))                     ; 679
(abs (- 5209 4672))                     ; 537
(abs (- 4672 6237))                     ; 1565
(abs (- 6237 5695))                     ; 542
(abs (- 5695 6624))                     ; 929
(abs (- 6624 5943))                     ; 681
(abs (- 5943 8599))                     ; 2656
(abs (- 8599 7830))                     ; 769
(abs (- 7830 8758))                     ; 928
(abs (- 8758 7893))                     ; 865
(abs (- 7893 9889))                     ; 1996
(abs (- 9889 9345))                     ; 544
(abs (- 9345 10167))                    ; 822
(abs (- 10167 9501))                    ; 666
(abs (- 9501 10256))                    ; 755

; 10256 -> 5422
(abs (- 10256 7274))                    ; 2982
(abs (- 7274 7901))                     ; 627
(abs (- 7901 7040))                     ; 861
(abs (- 7040 8137))                     ; 1097
(abs (- 8137 7400))                     ; 737
(abs (- 7400 8532))                     ; 1132
(abs (- 8532 7375))                     ; 1157
(abs (- 7375 9378))                     ; 2003
(abs (- 9378 8630))                     ; 748
(abs (- 8630 9337))                     ; 707
(abs (- 9337 7073))                     ; 2264
(abs (- 7073 8116))                     ; 1043
(abs (- 8116 6219))                     ; 1897
(abs (- 6219 7218))                     ; 999
(abs (- 7218 6384))                     ; 834
(abs (- 6384 7249))                     ; 865
(abs (- 7249 6643))                     ; 606
(abs (- 6643 7488))                     ; 845
(abs (- 7488 5988))                     ; 1500
(abs (- 5988 6577))                     ; 589
(abs (- 6577 5422))                     ; 1155

; 5422 -> 10393
(abs (- 5422 8710))                     ; 3288
(abs (- 8710 7068))                     ; 1642
(abs (- 7068 7830))                     ; 762
(abs (- 7830 6771))                     ; 1059
(abs (- 6771 8414))                     ; 1643
(abs (- 8414 7415))                     ; 999
(abs (- 7415 7959))                     ; 544
(abs (- 7959 7261))                     ; 698
(abs (- 7261 8152))                     ; 891
(abs (- 8152 7558))                     ; 594
(abs (- 7558 10393))                    ; 2835

; 10393 -> 3411
(abs (- 10393 8250))                    ; 2143
(abs (- 8250 10328))                    ; 2078
(abs (- 10328 8780))                    ; 1548
(abs (- 8780 9477))                     ; 697
(abs (- 9477 8281))                     ; 1196
(abs (- 8281 9167))                     ; 886
(abs (- 9167 8386))                     ; 781
(abs (- 8386 9209))                     ; 823
(abs (- 9209 7988))                     ; 1221
(abs (- 7988 8643))                     ; 655
(abs (- 8643 7670))                     ; 973
(abs (- 7670 8305))                     ; 635
(abs (- 8305 5904))                     ; 2401
(abs (- 5904 6425))                     ; 521
(abs (- 6425 5074))                     ; 1351
(abs (- 5074 6035))                     ; 961
(abs (- 6035 5381))                     ; 654
(abs (- 5381 6164))                     ; 783
(abs (- 6164 4760))                     ; 1404
(abs (- 4760 5526))                     ; 766
(abs (- 5526 4555))                     ; 971
(abs (- 4555 6198))                     ; 1643
(abs (- 6198 5471))                     ; 727
(abs (- 5471 5981))                     ; 510
(abs (- 5981 4008))                     ; 1973
(abs (- 4008 4715))                     ; 707
(abs (- 4715 3411))                     ; 1304

; 3411 -> 9859
(abs (- 3411 5651))                     ; 2240
(abs (- 5651 5090))                     ; 561
(abs (- 5090 5926))                     ; 836
(abs (- 5926 5375))                     ; 551
(abs (- 5375 6049))                     ; 674
(abs (- 6049 5492))                     ; 557
(abs (- 5492 6484))                     ; 992
(abs (- 6484 4808))                     ; 1676
(abs (- 4808 5460))                     ; 652
(abs (- 5460 4506))                     ; 954
(abs (- 4506 5030))                     ; 524
(abs (- 5030 3845))                     ; 1185
(abs (- 3845 5141))                     ; 1296
(abs (- 5141 4044))                     ; 1097
(abs (- 4044 7135))                     ; 3091
(abs (- 7135 6020))                     ; 1115
(abs (- 6020 6916))                     ; 896
(abs (- 6916 5450))                     ; 1466
(abs (- 5450 6137))                     ; 687
(abs (- 6137 5255))                     ; 882
(abs (- 5255 6135))                     ; 880
(abs (- 6135 5597))                     ; 538
(abs (- 5597 6267))                     ; 670
(abs (- 6267 5565))                     ; 702
(abs (- 5565 6481))                     ; 916
(abs (- 6481 5618))                     ; 863
(abs (- 5618 7476))                     ; 1858
(abs (- 7476 6268))                     ; 1208
(abs (- 6268 6789))                     ; 521
(abs (- 6789 6232))                     ; 557
(abs (- 6232 7999))                     ; 1767
(abs (- 7999 7306))                     ; 693
(abs (- 7306 9807))                     ; 2501
(abs (- 9807 7987))                     ; 1820
(abs (- 7987 9783))                     ; 1796
(abs (- 9783 9275))                     ; 508
(abs (- 9275 9859))                     ; 584
