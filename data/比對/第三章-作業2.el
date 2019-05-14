;;; Legend:
;;;   wei-da: 未到達角度
;;;   dao-da: 到達角度
;;;   dang: 擋在前面
;;;   guo: 越過角度
;;;   po: 跌破角度
;;;   gui-dao: 軌道角度
;;;   di-er: 第二切線角度
;;;   dui-ying: 角線的對應角度
;;;   3/4: 角線的 3/4 角度
;;;   yuan-zhou: 圓周角度
;;;   swing: 區間振盪
;;;   angle: 基數在角線位置
;;;   cross: 基數在十字線位置

;;; Summary (500-600 點):
;;;   1. 角線波段最長走到被擋在 3/4 角度（目前只有一例），
;;;      目前未越過 3/4 者皆是反轉走勢（例外狀況為第 2 點）
;;;   2. 如果波段走勢受阻（擋在第二角度、3/4 角度），但下一段亦是受阻的情況下，
;;;      就會形成續跌/漲局勢
;;;   3. 越過第二角度，後勢續高（有 2 次例外）
;;;   4. 越過軌道線，仍不能說已形成波段（每次都發生在空頭趨勢）
;;;   5. 角線波段約有 85% 的比例可到達/越過「對應角度」
;;;   6. 十字線波段約有 85% 的比例可越過「軌道角度」
;;;   7. 一個趨勢出來的波段，總是能到達「對應角度」（角線）或是「軌道角度」（十字線）

;;; Summary (700-900 點):
;;;   1. 角線波段到達「對應角度」比例：30%；到達 「3/4」 比例：60%；到達「圓周」比例：10%
;;;   2. 十字線到達「軌道角度」：36%；到達「第二角度」：50%；到達「圓周」：13%
;;;   3. 700-900 點的波幅，能再往前一個角度
;;;     （700-900 結論的重要性不高，因為 500-600 已經能到達特定角度）

;;; Summary:
;;;   1. 角線波段到達「對應角度」比例：51%；到達 「3/4」 比例：36%；到達「圓周」比例：6%
;;;   2. 十字線到達「軌道角度」：55%；到達「第二角度」：30%；到達「圓周」：6%
;;;   3. 表示只要是趨勢出來的波段，就可以到達「對應角度」（角線）或「軌道角度」（十字線）

(abs (- 12682 11550))1132
(abs (- 11550 12321))771                ; 7-9, angle, guo, dui-ying, new, low
(abs (- 12321 10995))1326
(abs (- 10995 11720))725                ; 7-9, cross, guo, gui-dao, new, low
(abs (- 11720 10887))833                ; 7-9, cross, wei-da, di-er, new, high
(abs (- 10887 12065))1178
(abs (- 12065 10145))1920
(abs (- 10145 11282))1137
(abs (- 11282 9405))1877
(abs (- 9405 10011))606                 ; 5-6, cross, dang, gui-dao, new, low
(abs (- 10011 8652))1359
(abs (- 8652 9838))1186
(abs (- 9838 8252))1586
(abs (- 8252 9062))810                  ; 7-9, cross, wei-da, di-er, new, low
(abs (- 9062 8125))937                  ; 7-9, cross, wei-da, yuan-zhou, keep, low
(abs (- 8125 8689))564                  ; 5-6, angle, dang, dui-ying, new, low
(abs (- 8689 5822))2867
(abs (- 5822 8007))2185
(abs (- 8007 5758))2249
(abs (- 5758 6606))848                  ; 7-9, angle, guo, 3/4, new, low
(abs (- 6606 4450))2156
(abs (- 4450 5286))836                  ; 7-9, cross, guo, di-er, keep, high
(abs (- 5286 4522))764                  ; 7-9, angle, guo, 3/4, new, high
(abs (- 4522 5825))1303
(abs (- 5825 3788))2037
(abs (- 3788 4391))603                  ; 5-6, angle, dang, 3/4, new, low
(abs (- 4391 3021))1370
(abs (- 3021 3812))791                  ; 7-9, cross, guo, yuan-zhou, new, low
(abs (- 3812 2485))1327

(abs (- 2485 3575))1090
(abs (- 3575 3016))559                  ; 5-6, cross, wei-da, di-er, new, high
(abs (- 3016 5027))2011
(abs (- 5027 3986))1041
(abs (- 3986 5267))1281
(abs (- 5267 3773))1494
(abs (- 3773 4533))760                  ; 7-9, cross, wei-da, yuan-zhou, new, low
(abs (- 4533 3142))1391
(abs (- 3142 5255))2113
(abs (- 5255 4446))809                  ; 7-9, cross, dao-da, di-er, new, high
(abs (- 4446 5715))1269
(abs (- 5715 5202))513                  ; 5-6, cross, po, gui-dao, new, high
(abs (- 5202 6365))1163

(abs (- 6365 5681))684                  ; 5-6, cross, dang, di-er, keep, low
(abs (- 5681 6240))559                  ; 5-6, cross, wei-da, di-er, new, low
(abs (- 6240 5556))684                  ; 5-6, angle, dang, 3/4, keep, low
(abs (- 5556 6137))581                  ; 5-6, angle, guo, dui-ying, new, low
(abs (- 6137 4781))1356
(abs (- 4781 5282))501                  ; 5-6, cross, wei-da, di-er, new, low
(abs (- 5282 4250))1032
(abs (- 4250 4925))675                  ; 5-6, cross, wei-da, di-er, new, low
(abs (- 4925 4032))893                  ; 7-9, cross, guo, yuan-zhou, new, high

(abs (- 4032 5459))1427

(abs (- 5459 4253))1206
(abs (- 4253 4772))519                  ; 5-6, cross, wei-da, di-er, new, low
(abs (- 4772 3098))1674

(abs (- 3098 5091))1993

(abs (- 5091 3740))1351

(abs (- 3740 6719))2979

(abs (- 6719 5649))1070
(abs (- 5649 6424))775                  ; 7-9, cross, guo, di-er, new, low
(abs (- 6424 5125))1299

(abs (- 5125 7228))2103

(abs (- 7228 5916))1312
(abs (- 5916 6904))988                  ; 7-9, cross, dao-da, yuan-zhou, keep, high, swing
(abs (- 6904 6153))751                  ; 7-9, cross, dang, di-er, new, high
(abs (- 6153 7180))1027
(abs (- 7180 6167))1013
(abs (- 6167 6696))529                  ; 5-6, cross, guo, gui-dao, new, low, swing
(abs (- 6696 4474))2222

(abs (- 4474 5265))791                  ; 7-9, cross, guo, di-er, keep, high, swing
(abs (- 5265 4530))735                  ; 7-9, angle, guo, 3/4, new, high, swing
(abs (- 4530 5209))679                  ; 5-6, cross, guo, di-er, keep, high, swing
(abs (- 5209 4672))537                  ; 5-6, cross, wei-da, di-er, new, high, swing
(abs (- 4672 6237))1565
(abs (- 6237 5695))542                  ; 5-6, angle, po, dui-ying, new, high
(abs (- 5695 6624))929                  ; 7-9, cross, wei-da, yuan-zhou, keep, high, swing
(abs (- 6624 5943))681                  ; 5-6, cross, wei-da, di-er, new, high, swing
(abs (- 5943 8599))2656
(abs (- 8599 7830))769                  ; 7-9, cross, wei-da, di-er, new, high
(abs (- 7830 8758))928                  ; 7-9, angle, guo, 3/4, keep, high, swing
(abs (- 8758 7893))865                  ; 7-9, cross, guo, di-er, new, high
(abs (- 7893 9889))1996
(abs (- 9889 9345))544                  ; 5-6, cross, po, di-yi, new, high
(abs (- 9345 10167))822                 ; 7-9, angle, wei-da, 3/4, keep, high
(abs (- 10167 9501))666                 ; 5-6, cross, po, gui-dao, new, high
(abs (- 9501 10256))755                 ; 7-9, cross, wei-da, di-er, new, low

(abs (- 10256 7274))2982
(abs (- 7274 7901))627                  ; 5-6, angle, guo, dui-ying, new, low
(abs (- 7901 7040))861                  ; 7-9, cross, po, di-er, new, high
(abs (- 7040 8137))1097
(abs (- 8137 7400))737                  ; 7-9, angle, wei-da, 3/4, new, high
(abs (- 7400 8532))1132
(abs (- 8532 7375))1157
(abs (- 7375 9378))2003

(abs (- 9378 8630))748                  ; 7-9, cross, po, di-er, keep, low, swing
(abs (- 8630 9337))707                  ; 7-9, cross, wei-da, di-er, new, low
(abs (- 9337 7073))2264
(abs (- 7073 8116))1043
(abs (- 8116 6219))1897

(abs (- 6219 7218))999                  ; 7-9, cross, dang, yuan-zhou, keep, high, swing
(abs (- 7218 6384))834                  ; 7-9, cross, wei-da, di-er, new, high, swing
(abs (- 6384 7249))865                  ; 7-9, cross, guo, di-er, keep, high
(abs (- 7249 6643))606                  ; 5-6, cross, po, gui-dao, new, high
(abs (- 6643 7488))845                  ; 7-9, cross, guo, di-er, new, low

(abs (- 7488 5988))1500
(abs (- 5988 6577))589                  ; 5-6, angle, guo, dui-ying, new, low
(abs (- 6577 5422))1155

(abs (- 5422 8710))3288

(abs (- 8710 7068))1642
(abs (- 7068 7830))762                  ; 7-9, angle, wei-da, 3/4, new, low
(abs (- 7830 6771))1059

(abs (- 6771 8414))1643
(abs (- 8414 7415))999                  ; 7-9, angle, wei-da, yuan-zhou, new, low, swing
(abs (- 7415 7959))544                  ; 5-6, cross, dang, gui-dao, new, low
(abs (- 7959 7261))698                  ; 5-6, cross, wei-da, di-er, new, high
(abs (- 7261 8152))891                  ; 7-9, angle, guo, 3/4, keep, high, swing
(abs (- 8152 7558))594                  ; 5-6, angle, dao-da, dui-ying, new, high
(abs (- 7558 10393))2835

(abs (- 10393 8250))2143

(abs (- 8250 10328))2078

(abs (- 10328 8780))1548
(abs (- 8780 9477))697                  ; 5-6, cross, guo, gui-dao, new, low
(abs (- 9477 8281))1196
(abs (- 8281 9167))886                  ; 7-9, cross, guo, di-er, keep, high
(abs (- 9167 8386))781                  ; 7-9, cross, wei-da, di-er, new, high
(abs (- 8386 9209))823                  ; 7-9, angle, wei-da, 3/4, new, low
(abs (- 9209 7988))1221
(abs (- 7988 8643))655                  ; 5-6, cross, guo, gui-dao, new, low
(abs (- 8643 7670))973                  ; 7-9, cross, wei-da, di-er, keep, low
(abs (- 7670 8305))635                  ; 5-6, cross, guo, gui-dao, new, low
(abs (- 8305 5904))2401
(abs (- 5904 6425))521                  ; 5-6, cross, guo, gui-dao, new, low
(abs (- 6425 5074))1351
(abs (- 5074 6035))961                  ; 7-9, angle, dao-da, yuan-zhou, keep, high
(abs (- 6035 5381))654                  ; 5-6, angle, po, dui-ying, new, high
(abs (- 5381 6164))783                  ; 7-9, cross, dao-da, di-er, new, low
(abs (- 6164 4760))1404
(abs (- 4760 5526))766                  ; 7-9, cross, guo, di-er, new, low
(abs (- 5526 4555))971                  ; 7-9, angle, po, yuan-zhou, new, high

(abs (- 4555 6198))1643

(abs (- 6198 5471))727                  ; 7-9, cross, wei-da, di-er, keep, low, swing
(abs (- 5471 5981))510                  ; 5-6, cross, guo, gui-dao, new, low
(abs (- 5981 4008))1973
(abs (- 4008 4715))707                  ; 7-9, angle, wei-da, yuan-zhou, new, low
(abs (- 4715 3411))1304

(abs (- 3411 5651))2240
(abs (- 5651 5090))561                  ; 5-6, cross, po, gui-dao, new, high
(abs (- 5090 5926))836                  ; 7-9, angle, wei-da, yuan-zhou, keep, high
(abs (- 5926 5375))551                  ; 5-6, cross, po, gui-dao, new, high
(abs (- 5375 6049))674                  ; 5-6, cross, wei-da, di-er, keep, high
(abs (- 6049 5492))557                  ; 5-6, angle, po, dui-ying, new, high
(abs (- 5492 6484))992                  ; 7-9, cross, dao-da, yuan-zhou, new, low

(abs (- 6484 4808))1676
(abs (- 4808 5460))652                  ; 5-6, cross, guo, di-er, new, low
(abs (- 5460 4506))954                  ; 7-9, cross, po, yuan-zhou, keep, low
(abs (- 4506 5030))524                  ; 5-6, cross, guo, gui-dao, new, low
(abs (- 5030 3845))1185

(abs (- 3845 5141))1296

(abs (- 5141 4044))1097

(abs (- 4044 7135))3091

(abs (- 7135 6020))1115
(abs (- 6020 6916))896                  ; 7-9, angle, wei-da, yuan-zhou, new, low
(abs (- 6916 5450))1466
(abs (- 5450 6137))687                  ; 5-6, cross, guo, di-er, new, low, swing
(abs (- 6137 5255))882                  ; 7-9, cross, wei-da, yuan-zhou, new, high, swing

(abs (- 5255 6135))880                  ; 7-9, cross, wei-da, yuan-zhou, keep, high, swing
(abs (- 6135 5597))538                  ; 5-6, cross, po, gui-dao, new, high, swing
(abs (- 5597 6267))670                  ; 5-6, cross, wei-da, di-er, new, low, swing
(abs (- 6267 5565))702                  ; 7-9, angle, wei-da, 3/4, new, high
(abs (- 5565 6481))916                  ; 7-9, angle, wei-da, yuan-zhou, keep, high, swing
(abs (- 6481 5618))863                  ; 7-9, angle, wei-da, yuan-zhou, new, high
(abs (- 5618 7476))1858

(abs (- 7476 6268))1208
(abs (- 6268 6789))521                  ; 5-6, angle, guo, dui-ying, new, low
(abs (- 6789 6232))557                  ; 5-6, angle, po, dui-ying, new, high

(abs (- 6232 7999))1767
(abs (- 7999 7306))693                  ; 5-6, cross, po, gui-dao, new, high
(abs (- 7306 9807))2501

(abs (- 9807 7987))1820

(abs (- 7987 9783))1796
(abs (- 9783 9275))508                  ; 5-6, cross, wei-da, gui-dao, new, high
(abs (- 9275 9859))584                  ; 5-6, cross, dang, gui-dao, new, low

(abs (- 9859 8207))1652
(abs (- 8207 8804))597                  ; 5-6, cross, guo, gui-dao, new, low
(abs (- 8804 7664))1140
(abs (- 7664 8532))868                  ; 7-9, cross, wei-da, di-er, keep, high
(abs (- 8532 7818))714                  ; 7-9, cross, wei-da, di-er, new, high
(abs (- 7818 8546))728                  ; 7-9, cross, guo, di-er, new, low
(abs (- 8546 7384))1162

(abs (- 7384 8658))1274
(abs (- 8658 7900))758                  ; 7-9, cross, guo, gui-dao, new, high
(abs (- 7900 9049))1149
(abs (- 9049 8419))630                  ; 5-6, angle, dang, dui-ying, new, high
(abs (- 8419 9309))890                  ; 7-9, angle, dao-da, 3/4, new, low
