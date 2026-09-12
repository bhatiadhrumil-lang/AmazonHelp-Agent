# Cluster Analysis (initial HDBSCAN run)

Rows analyzed: 93,171
Non-noise clusters: 203
Noise points (label -1): 49,621 (53.3%)

## Cluster size summary
| cluster_id | size | share | median_probability | intra_cluster_cosine |
|---|---:|---:|---:|---:|
| 0 | 35 | 0.038% | 1.000 | 1.000 |
| 1 | 79 | 0.085% | 0.614 | 0.991 |
| 2 | 49 | 0.053% | 1.000 | 0.995 |
| 3 | 33 | 0.035% | 1.000 | 1.000 |
| 4 | 82 | 0.088% | 0.752 | 0.989 |
| 5 | 67 | 0.072% | 0.920 | 0.985 |
| 6 | 34 | 0.036% | 1.000 | 0.987 |
| 7 | 12,267 | 13.166% | 1.000 | 0.487 |
| 8 | 126 | 0.135% | 0.666 | 0.444 |
| 9 | 35 | 0.038% | 1.000 | 0.629 |
| 10 | 82 | 0.088% | 0.991 | 0.615 |
| 11 | 59 | 0.063% | 1.000 | 0.606 |
| 12 | 157 | 0.169% | 0.456 | 0.412 |
| 13 | 59 | 0.063% | 1.000 | 0.384 |
| 14 | 481 | 0.516% | 0.742 | 0.514 |
| 15 | 76 | 0.082% | 0.903 | 0.480 |
| 16 | 43 | 0.046% | 1.000 | 0.488 |
| 17 | 36 | 0.039% | 1.000 | 0.940 |
| 18 | 84 | 0.090% | 0.760 | 0.618 |
| 19 | 63 | 0.068% | 0.913 | 0.463 |
| 20 | 32 | 0.034% | 1.000 | 0.532 |
| 21 | 56 | 0.060% | 1.000 | 0.463 |
| 22 | 122 | 0.131% | 0.749 | 0.622 |
| 23 | 92 | 0.099% | 0.797 | 0.515 |
| 24 | 44 | 0.047% | 1.000 | 0.548 |
| 25 | 83 | 0.089% | 0.726 | 0.738 |
| 26 | 273 | 0.293% | 0.382 | 0.529 |
| 27 | 38 | 0.041% | 1.000 | 0.449 |
| 28 | 37 | 0.040% | 1.000 | 0.540 |
| 29 | 552 | 0.592% | 0.497 | 0.439 |
| 30 | 205 | 0.220% | 0.503 | 0.524 |
| 31 | 49 | 0.053% | 1.000 | 0.472 |
| 32 | 54 | 0.058% | 1.000 | 0.400 |
| 33 | 126 | 0.135% | 0.669 | 0.420 |
| 34 | 43 | 0.046% | 1.000 | 0.676 |
| 35 | 69 | 0.074% | 0.932 | 0.538 |
| 36 | 59 | 0.063% | 1.000 | 0.547 |
| 37 | 69 | 0.074% | 1.000 | 0.394 |
| 38 | 50 | 0.054% | 1.000 | 0.526 |
| 39 | 70 | 0.075% | 0.911 | 0.549 |
| 40 | 287 | 0.308% | 0.623 | 0.421 |
| 41 | 79 | 0.085% | 0.836 | 0.538 |
| 42 | 648 | 0.695% | 0.384 | 0.456 |
| 43 | 61 | 0.065% | 0.984 | 0.477 |
| 44 | 80 | 0.086% | 0.680 | 0.369 |
| 45 | 31 | 0.033% | 1.000 | 0.963 |
| 46 | 50 | 0.054% | 1.000 | 0.561 |
| 47 | 63 | 0.068% | 0.984 | 0.541 |
| 48 | 33 | 0.035% | 1.000 | 0.616 |
| 49 | 32 | 0.034% | 1.000 | 0.475 |
| 50 | 378 | 0.406% | 0.517 | 0.516 |
| 51 | 72 | 0.077% | 0.849 | 0.583 |
| 52 | 47 | 0.050% | 1.000 | 0.729 |
| 53 | 36 | 0.039% | 1.000 | 0.529 |
| 54 | 48 | 0.052% | 1.000 | 0.635 |
| 55 | 137 | 0.147% | 0.632 | 0.589 |
| 56 | 32 | 0.034% | 1.000 | 0.634 |
| 57 | 78 | 0.084% | 0.912 | 0.614 |
| 58 | 325 | 0.349% | 1.000 | 0.450 |
| 59 | 1,097 | 1.177% | 1.000 | 0.501 |
| 60 | 126 | 0.135% | 0.698 | 0.524 |
| 61 | 35 | 0.038% | 1.000 | 0.519 |
| 62 | 39 | 0.042% | 1.000 | 0.609 |
| 63 | 122 | 0.131% | 0.651 | 0.440 |
| 64 | 139 | 0.149% | 0.694 | 0.530 |
| 65 | 62 | 0.067% | 1.000 | 0.645 |
| 66 | 73 | 0.078% | 0.821 | 0.436 |
| 67 | 110 | 0.118% | 0.719 | 0.390 |
| 68 | 140 | 0.150% | 0.456 | 0.447 |
| 69 | 137 | 0.147% | 0.606 | 0.441 |
| 70 | 394 | 0.423% | 0.526 | 0.521 |
| 71 | 171 | 0.184% | 0.764 | 0.641 |
| 72 | 80 | 0.086% | 0.983 | 0.656 |
| 73 | 44 | 0.047% | 1.000 | 0.512 |
| 74 | 47 | 0.050% | 1.000 | 0.600 |
| 75 | 132 | 0.142% | 0.695 | 0.559 |
| 76 | 33 | 0.035% | 1.000 | 0.587 |
| 77 | 49 | 0.053% | 1.000 | 0.538 |
| 78 | 122 | 0.131% | 0.543 | 0.509 |
| 79 | 31 | 0.033% | 1.000 | 0.507 |
| 80 | 36 | 0.039% | 1.000 | 0.586 |
| 81 | 34 | 0.036% | 1.000 | 0.512 |
| 82 | 46 | 0.049% | 1.000 | 0.550 |
| 83 | 89 | 0.096% | 0.918 | 0.424 |
| 84 | 40 | 0.043% | 1.000 | 0.511 |
| 85 | 175 | 0.188% | 1.000 | 0.761 |
| 86 | 33 | 0.035% | 1.000 | 0.670 |
| 87 | 34 | 0.036% | 1.000 | 0.854 |
| 88 | 32 | 0.034% | 1.000 | 0.582 |
| 89 | 319 | 0.342% | 0.544 | 0.504 |
| 90 | 34 | 0.036% | 1.000 | 0.490 |
| 91 | 55 | 0.059% | 1.000 | 0.733 |
| 92 | 101 | 0.108% | 0.891 | 0.703 |
| 93 | 32 | 0.034% | 1.000 | 0.912 |
| 94 | 130 | 0.140% | 0.721 | 0.425 |
| 95 | 32 | 0.034% | 1.000 | 0.554 |
| 96 | 46 | 0.049% | 1.000 | 0.585 |
| 97 | 42 | 0.045% | 1.000 | 0.631 |
| 98 | 37 | 0.040% | 1.000 | 0.567 |
| 99 | 41 | 0.044% | 1.000 | 0.574 |
| 100 | 66 | 0.071% | 0.981 | 0.525 |
| 101 | 213 | 0.229% | 0.562 | 0.455 |
| 102 | 542 | 0.582% | 0.961 | 0.373 |
| 103 | 229 | 0.246% | 0.986 | 0.366 |
| 104 | 64 | 0.069% | 0.981 | 0.454 |
| 105 | 164 | 0.176% | 0.741 | 0.393 |
| 106 | 58 | 0.062% | 1.000 | 0.547 |
| 107 | 193 | 0.207% | 0.580 | 0.639 |
| 108 | 107 | 0.115% | 0.651 | 0.568 |
| 109 | 1,057 | 1.134% | 1.000 | 0.332 |
| 110 | 42 | 0.045% | 1.000 | 0.720 |
| 111 | 76 | 0.082% | 0.884 | 0.753 |
| 112 | 113 | 0.121% | 1.000 | 0.818 |
| 113 | 53 | 0.057% | 1.000 | 0.867 |
| 114 | 49 | 0.053% | 1.000 | 0.747 |
| 115 | 255 | 0.274% | 0.502 | 0.474 |
| 116 | 44 | 0.047% | 1.000 | 0.791 |
| 117 | 33 | 0.035% | 1.000 | 0.718 |
| 118 | 77 | 0.083% | 1.000 | 0.451 |
| 119 | 35 | 0.038% | 1.000 | 0.473 |
| 120 | 75 | 0.080% | 0.959 | 0.566 |
| 121 | 93 | 0.100% | 0.828 | 0.732 |
| 122 | 580 | 0.623% | 0.960 | 0.470 |
| 123 | 37 | 0.040% | 1.000 | 0.782 |
| 124 | 31 | 0.033% | 1.000 | 0.780 |
| 125 | 101 | 0.108% | 0.808 | 0.700 |
| 126 | 120 | 0.129% | 0.469 | 0.619 |
| 127 | 87 | 0.093% | 0.925 | 0.873 |
| 128 | 36 | 0.039% | 1.000 | 0.960 |
| 129 | 35 | 0.038% | 1.000 | 0.545 |
| 130 | 197 | 0.211% | 0.600 | 0.657 |
| 131 | 44 | 0.047% | 1.000 | 0.827 |
| 132 | 89 | 0.096% | 0.781 | 0.881 |
| 133 | 31 | 0.033% | 1.000 | 0.903 |
| 134 | 356 | 0.382% | 1.000 | 0.794 |
| 135 | 30 | 0.032% | 1.000 | 0.494 |
| 136 | 38 | 0.041% | 1.000 | 0.654 |
| 137 | 342 | 0.367% | 0.897 | 0.467 |
| 138 | 57 | 0.061% | 1.000 | 0.418 |
| 139 | 1,521 | 1.632% | 1.000 | 0.410 |
| 140 | 40 | 0.043% | 1.000 | 0.603 |
| 141 | 209 | 0.224% | 1.000 | 0.488 |
| 142 | 61 | 0.065% | 0.969 | 0.508 |
| 143 | 261 | 0.280% | 1.000 | 0.411 |
| 144 | 333 | 0.357% | 0.617 | 0.387 |
| 145 | 305 | 0.327% | 0.951 | 0.441 |
| 146 | 654 | 0.702% | 0.987 | 0.507 |
| 147 | 38 | 0.041% | 1.000 | 0.612 |
| 148 | 74 | 0.079% | 0.707 | 0.544 |
| 149 | 40 | 0.043% | 1.000 | 0.724 |
| 150 | 111 | 0.119% | 0.485 | 0.652 |
| 151 | 129 | 0.138% | 0.694 | 0.553 |
| 152 | 50 | 0.054% | 1.000 | 0.611 |
| 153 | 59 | 0.063% | 1.000 | 0.621 |
| 154 | 50 | 0.054% | 1.000 | 0.537 |
| 155 | 128 | 0.137% | 0.654 | 0.603 |
| 156 | 1,967 | 2.111% | 1.000 | 0.449 |
| 157 | 324 | 0.348% | 0.449 | 0.605 |
| 158 | 37 | 0.040% | 1.000 | 0.697 |
| 159 | 101 | 0.108% | 0.882 | 0.682 |
| 160 | 33 | 0.035% | 1.000 | 0.558 |
| 161 | 31 | 0.033% | 1.000 | 0.591 |
| 162 | 46 | 0.049% | 1.000 | 0.573 |
| 163 | 183 | 0.196% | 1.000 | 0.523 |
| 164 | 40 | 0.043% | 1.000 | 0.532 |
| 165 | 96 | 0.103% | 0.654 | 0.505 |
| 166 | 30 | 0.032% | 1.000 | 0.567 |
| 167 | 340 | 0.365% | 0.308 | 0.588 |
| 168 | 181 | 0.194% | 0.749 | 0.513 |
| 169 | 155 | 0.166% | 0.804 | 0.486 |
| 170 | 49 | 0.053% | 1.000 | 0.488 |
| 171 | 169 | 0.181% | 0.811 | 0.439 |
| 172 | 133 | 0.143% | 0.848 | 0.586 |
| 173 | 254 | 0.273% | 1.000 | 0.447 |
| 174 | 72 | 0.077% | 0.888 | 0.550 |
| 175 | 89 | 0.096% | 0.842 | 0.641 |
| 176 | 189 | 0.203% | 0.900 | 0.536 |
| 177 | 47 | 0.050% | 1.000 | 0.550 |
| 178 | 84 | 0.090% | 0.846 | 0.647 |
| 179 | 113 | 0.121% | 0.921 | 0.508 |
| 180 | 70 | 0.075% | 0.953 | 0.533 |
| 181 | 373 | 0.400% | 0.961 | 0.482 |
| 182 | 51 | 0.055% | 1.000 | 0.555 |
| 183 | 112 | 0.120% | 0.944 | 0.655 |
| 184 | 1,044 | 1.121% | 1.000 | 0.479 |
| 185 | 332 | 0.356% | 0.528 | 0.568 |
| 186 | 110 | 0.118% | 0.916 | 0.569 |
| 187 | 70 | 0.075% | 0.939 | 0.529 |
| 188 | 30 | 0.032% | 1.000 | 0.580 |
| 189 | 864 | 0.927% | 1.000 | 0.539 |
| 190 | 273 | 0.293% | 0.472 | 0.652 |
| 191 | 76 | 0.082% | 0.873 | 0.687 |
| 192 | 69 | 0.074% | 1.000 | 0.682 |
| 193 | 263 | 0.282% | 0.671 | 0.649 |
| 194 | 46 | 0.049% | 1.000 | 0.645 |
| 195 | 352 | 0.378% | 0.983 | 0.559 |
| 196 | 48 | 0.052% | 1.000 | 0.673 |
| 197 | 369 | 0.396% | 0.694 | 0.417 |
| 198 | 410 | 0.440% | 0.608 | 0.471 |
| 199 | 55 | 0.059% | 1.000 | 0.596 |
| 200 | 157 | 0.169% | 0.813 | 0.647 |
| 201 | 214 | 0.230% | 0.559 | 0.703 |
| 202 | 329 | 0.353% | 0.930 | 0.519 |

## Representative examples per cluster

Representatives are chosen near the cluster centroid in UMAP space, with diversity enforced in embedding space (no near-duplicate reps). Full representative tables (cluster_<id>_representatives.csv) contain customer_message_id, conversation_id, probability, and original text.

### Cluster 0
- id=1215407 conv=1215405 p=1.00 :: @AmazonHelp Thank you
- id=1176285 conv=1176279 p=1.00 :: @AmazonHelp Thank you
- id=1306406 conv=1306407 p=1.00 :: @AmazonHelp Thank you
- id=1117010 conv=1117012 p=1.00 :: @AmazonHelp Thank you
- id=1339600 conv=1339601 p=1.00 :: @AmazonHelp Thank you
- id=899524 conv=899525 p=1.00 :: @AmazonHelp Thank you
- id=1505436 conv=1505437 p=1.00 :: @AmazonHelp Thank you
- id=842133 conv=842139 p=1.00 :: @AmazonHelp Thank you

### Cluster 1
- id=2931864 conv=2931865 p=0.04 :: @AmazonHelp Thank You!
- id=2396353 conv=2396359 p=0.06 :: @AmazonHelp Thank you!
- id=572418 conv=572416 p=0.04 :: @AmazonHelp Thank You!
- id=1411659 conv=1411660 p=0.07 :: @AmazonHelp Thank you thank you!
- id=522531 conv=522527 p=0.04 :: @AmazonHelp Thank You!
- id=164810 conv=164813 p=0.43 :: @AmazonHelp Thank you!
- id=69840 conv=69841 p=0.43 :: @AmazonHelp Thank you!
- id=158609 conv=158610 p=0.47 :: @AmazonHelp Thank you!

### Cluster 2
- id=1302329 conv=1302331 p=0.74 :: @AmazonHelp Thank you!
- id=734680 conv=734676 p=0.03 :: @AmazonHelp thank you! c:
- id=1345571 conv=1345569 p=0.82 :: @AmazonHelp Thank you!
- id=1385278 conv=1385280 p=1.00 :: @AmazonHelp Thank you!
- id=1165671 conv=1165669 p=1.00 :: @AmazonHelp Thank you!
- id=1248266 conv=1248264 p=1.00 :: @AmazonHelp Thank you!
- id=342968 conv=342969 p=1.00 :: @AmazonHelp Thank you!
- id=438004 conv=438006 p=1.00 :: @AmazonHelp Thank you!

### Cluster 3
- id=408793 conv=408792 p=1.00 :: @AmazonHelp Thank you
- id=388027 conv=388028 p=1.00 :: @AmazonHelp Thank you
- id=382880 conv=382878 p=1.00 :: @AmazonHelp Thank you
- id=382809 conv=382810 p=1.00 :: @AmazonHelp Thank you
- id=434524 conv=434516 p=1.00 :: @AmazonHelp Thank you
- id=472435 conv=472424 p=1.00 :: @AmazonHelp Thank you
- id=667735 conv=667736 p=1.00 :: @AmazonHelp Thank you
- id=675251 conv=675252 p=1.00 :: @AmazonHelp Thank you

### Cluster 4
- id=2434981 conv=2434985 p=0.04 :: @AmazonHelp Thanku ^CT
- id=2488403 conv=2488404 p=1.00 :: @AmazonHelp Thank you
- id=2283511 conv=2283514 p=0.01 :: @AmazonHelp Thank you Shonna
- id=2492224 conv=2492220 p=1.00 :: @AmazonHelp Thank you
- id=2474879 conv=2474877 p=1.00 :: @AmazonHelp Thank you
- id=1043140 conv=1043141 p=1.00 :: @AmazonHelp Thank you
- id=1136228 conv=1136229 p=1.00 :: @AmazonHelp Thank you
- id=2538167 conv=2538159 p=1.00 :: @AmazonHelp Thank you

### Cluster 5
- id=2488509 conv=2488511 p=0.10 :: @AmazonHelp Thank You.
- id=1286974 conv=1286999 p=1.00 :: @AmazonHelp Thank you, CR.
- id=697970 conv=697971 p=0.00 :: @AmazonHelp Thanks. Appreciate &amp; look forward.
- id=1397887 conv=1397885 p=0.11 :: @AmazonHelp Thank You.
- id=1479132 conv=1479133 p=1.00 :: @AmazonHelp Thank you.
- id=1508637 conv=1508638 p=1.00 :: @AmazonHelp Thank you.
- id=1490293 conv=1490294 p=1.00 :: @AmazonHelp Thank you.
- id=1609617 conv=1609618 p=1.00 :: @AmazonHelp Thank you.

### Cluster 6
- id=535067 conv=535070 p=1.00 :: @AmazonHelp Ok thanks
- id=499969 conv=499970 p=0.05 :: @AmazonHelp Ok thanks bv
- id=536522 conv=536528 p=1.00 :: @AmazonHelp Ok thanks
- id=58111 conv=58109 p=1.00 :: @AmazonHelp Ok thanks
- id=1006560 conv=1006554 p=1.00 :: @AmazonHelp Ok thanks
- id=529034 conv=529032 p=1.00 :: @AmazonHelp Ok thanks
- id=1936461 conv=5159 p=1.00 :: @AmazonHelp Ok thanks
- id=1015585 conv=1015583 p=1.00 :: @AmazonHelp Ok thanks

### Cluster 7
- id=721259 conv=721255 p=1.00 :: @AmazonHelp Eso que tiene que ver? Yo he comprado en Amazon y desde luego por teléfono no han puesto
- id=2141312 conv=2141319 p=1.00 :: @AmazonHelp I’ve a contract with you. I’ve paid for amazon Deck 109. Is this the same as block 109? 
- id=343680 conv=343702 p=1.00 :: @AmazonHelp D'après le SAV Amazon c'était soit Amazon soit moi qui aurait demandé ce retour, hors ce
- id=1661798 conv=1661793 p=1.00 :: @AmazonHelp No but I’ve been on their website for returns and amazon isn’t even an option
- id=255032 conv=255033 p=1.00 :: @AmazonHelp The Amazon seller app is reporting inaccurate info, searching Amazon shopping app return
- id=2141314 conv=2141319 p=1.00 :: @AmazonHelp Let me get this straight. I buy tickets off you. Confirmation says Amazon deck 109 NOTHI
- id=93641 conv=93632 p=1.00 :: @AmazonHelp Danke, damit konnten wenigstens Sie mir ein Stück weiterhelfen. Bzgl meines Anliegens ko
- id=765701 conv=765704 p=1.00 :: @AmazonHelp I did get back to Amzn with the feedback that police would not look into this as it is A

### Cluster 8
- id=985140 conv=985141 p=0.39 :: @AmazonHelp Do you think that Bombay Dyeing will put MRP of Rs.3711 or Rs.1799 depending upon the Re
- id=1563745 conv=1563746 p=0.47 :: @AmazonHelp Says taxes inclusive in MRP 😂😂
- id=132574 conv=132575 p=0.33 :: @AmazonHelp Due to GST every state have same MRP now and this product is manufactured after GST how 
- id=535151 conv=535149 p=0.24 :: @AmazonHelp Your invoice is showing more than mrp and I have made payment more than mrp to @24308
- id=135096 conv=135097 p=0.35 :: @AmazonHelp Again a lie. The product was manufactred much earlier and MRP printed is 320. Amount cha
- id=2553854 conv=2553855 p=0.19 :: @AmazonHelp Please guide me how I can get my 18 % GST back, which is added on MRP.
- id=1443283 conv=1443284 p=0.46 :: @AmazonHelp Fluctuations are fine, but when the MRP is ₹350, how can the tax invoice have a differen
- id=2376146 conv=2376147 p=0.55 :: @AmazonHelp @128484 Your pricing policy is to charge above the MRP?

### Cluster 9
- id=429009 conv=428987 p=1.00 :: @AmazonHelp @115851 is big joker and @115850 big looser not even keep their words
- id=1209111 conv=1208753 p=1.00 :: @AmazonHelp JOker looks at attachment.. @115851 big joker @115850 #resolutionteam &amp; #Cteam maste
- id=2511768 conv=19137 p=1.00 :: @AmazonHelp I've already given details multiple time But you #joker never responded only sorry and a
- id=2142166 conv=920929 p=1.00 :: @AmazonHelp There should be a limit of elaborating can't help if U joker's don't want to understand 
- id=1089227 conv=1003631 p=1.00 :: @AmazonHelp You joker's only say sorry only and your bigger joker @115851 always silent #jokers
- id=796394 conv=231795 p=1.00 :: @AmazonHelp @309902 Joker's🤔🤔always say sorry but did not learn from mistake my 3 order you and your
- id=2221877 conv=1387105 p=1.00 :: @AmazonHelp you jokers i've already given details but you never understand and it's your tendency ba
- id=1015275 conv=678646 p=1.00 :: @AmazonHelp You leave it joker's let @115851 reply jokers don't have courage to help me thanks

### Cluster 10
- id=2321006 conv=2321004 p=1.00 :: @AmazonHelp Both times it was amzl us
- id=377223 conv=377224 p=1.00 :: @AmazonHelp AMZL US.
- id=1076279 conv=1076282 p=1.00 :: @AmazonHelp “AMZL US” ?
- id=1241107 conv=1241110 p=1.00 :: @AmazonHelp By AMZL US
- id=304372 conv=304374 p=1.00 :: @AmazonHelp AMZL US?
- id=865622 conv=865617 p=1.00 :: @AmazonHelp amzl us was the for all three
- id=1724453 conv=1724454 p=1.00 :: @AmazonHelp Those with AMZL US
- id=450709 conv=450711 p=1.00 :: @AmazonHelp AMZL US - is that what you mean?

### Cluster 11
- id=2724967 conv=2724968 p=1.00 :: @AmazonHelp os mando la incidencia por privado (soy bueno) 😉
- id=1452908 conv=1452909 p=0.95 :: @AmazonHelp @132703 Sí! Os paso los datos por privado.
- id=754988 conv=754989 p=1.00 :: @AmazonHelp Os he dejado un privado
- id=739669 conv=739670 p=1.00 :: @AmazonHelp Eso os he preguntado por privado, que dónde debo poner la reclamación?
- id=2657673 conv=2657675 p=1.00 :: @AmazonHelp Well I sent you guys a private message can I talk in private in case
- id=2878657 conv=2878652 p=1.00 :: @AmazonHelp Vi ho scritto in privato
- id=2857257 conv=2857258 p=1.00 :: @AmazonHelp Os he mandado un privado a esa cuenta ahora mismo!
- id=1113558 conv=1113554 p=1.00 :: @AmazonHelp Envío mensaje privado

### Cluster 12
- id=73571 conv=73568 p=0.25 :: @AmazonHelp R u fooling me how many quiz contest ur conducted just on one plus 5t?
- id=468747 conv=468749 p=0.37 :: @AmazonHelp Thanks for sharing the details. I hope to be one of the winner of #OnePlus5T 😆
- id=2437725 conv=1273483 p=0.36 :: @AmazonHelp This result is not for 25th september quiz. I doubt that if the draw is really made or n
- id=1320513 conv=1320514 p=0.33 :: @AmazonHelp I checked the page and it still shows the results of the 25th August quiz. The September
- id=880018 conv=210417 p=0.32 :: @AmazonHelp @165805 I believe the results for the quiz held on 25th september will be out on 25th Oc
- id=1192271 conv=1192277 p=0.39 :: @AmazonHelp This is very odd. It's already 4 PM IST and the winners list page still contains the 25t
- id=2570405 conv=2570406 p=0.48 :: @AmazonHelp This is all fake you are showing same winners for 25th August quiz and 25th September Qu
- id=841863 conv=841328 p=0.38 :: @AmazonHelp LOL tried it already... playing all app quiz n contestS,,,,,

### Cluster 13
- id=999162 conv=144014 p=0.56 :: @AmazonHelp Second thing is as u told MSOP not guaranteed for COD method , i reffered to your COD T&
- id=2603024 conv=2603025 p=0.95 :: @AmazonHelp COD is available for another account of my friend. Our pincodes are also same. COD is no
- id=1893531 conv=1893489 p=1.00 :: @AmazonHelp I am unable to place the order for pincode 201005.pls help
- id=1631104 conv=962032 p=1.00 :: @AmazonHelp #apnidukaan what's the use of delivery to every pincode when u can't pick up returns
- id=292268 conv=292269 p=1.00 :: @AmazonHelp But flipkart and shop clues are giving COD facility in this pincode
- id=245837 conv=245829 p=1.00 :: @AmazonHelp Previously COD is available on same pin code.
- id=1565064 conv=1565065 p=1.00 :: @AmazonHelp Still ur website accept order for that pin code. 334803.
- id=1227965 conv=1208753 p=1.00 :: @AmazonHelp Delivery 🚚 problem in pincode 834002

### Cluster 14
- id=451874 conv=451871 p=0.73 :: @AmazonHelp não consegui. vou mandar DM pra vocês.
- id=319150 conv=319151 p=0.68 :: @AmazonHelp Thank you. I've followed the instructions given in the DM.
- id=1616797 conv=1616798 p=0.88 :: @AmazonHelp Just sent you a dm. Thanks.
- id=2410495 conv=2410498 p=0.74 :: @AmazonHelp They're DMing me now. Thanks.
- id=141970 conv=141971 p=0.47 :: @AmazonHelp en DM svp
- id=390809 conv=390805 p=0.73 :: @AmazonHelp Stop lying. There's nothing you sent as DM? WHY SUCH DOUBLE STANDARD?
- id=581877 conv=581872 p=0.46 :: @AmazonHelp 'Confirm'? I haven't actually told you in the first place. It's DPD.
- id=2787696 conv=2787697 p=0.87 :: @AmazonHelp I'll send you guys a DM!

### Cluster 15
- id=1375309 conv=1375310 p=0.98 :: @AmazonHelp Umm nothing just a refund. Kidding me after so much heartache and not getting my costume
- id=2671573 conv=2671574 p=1.00 :: @AmazonHelp Thanks for your assistance, but unless there's an option for a new costume by 3:00 p.m. 
- id=254061 conv=254059 p=1.00 :: @AmazonHelp I used @115821 for my Halloween costume because I trust the company. Now not only have t
- id=2641344 conv=2641346 p=1.00 :: @AmazonHelp Thanks! Unfortunately, I'm just going to have to return it when it arrives tomorrow (a d
- id=1300654 conv=1300657 p=1.00 :: @AmazonHelp It finally came and I was missing an item. Very upset I needed this for my Halloween cos
- id=1246394 conv=1246395 p=1.00 :: @AmazonHelp USPS.. Tracking says the costumes are in Kentucky. I just spoke with Arlene (#superhelpf
- id=789311 conv=789070 p=0.84 :: @AmazonHelp Try telling that to my son who won't have his costume for his school party!
- id=1246397 conv=1246395 p=0.75 :: @AmazonHelp The costumes arrived in more than enough time! Made their entire day and saved me from a

### Cluster 16
- id=1101752 conv=1101753 p=1.00 :: @AmazonHelp Hermes hat hier schon mehrfach angegeben geliefert zu haben, was nicht stimmte, gestern 
- id=78777 conv=78803 p=1.00 :: @AmazonHelp @4772 doch sie brauchen nur bei Hermes anrufen, sich mit dem örtlichen Zentrum (Stolberg
- id=994292 conv=994295 p=1.00 :: @AmazonHelp Es gibt zwei Varianten zu diesem Thema. Erste Variante: Hermes hat es nicht pünktlich ge
- id=1706215 conv=1706209 p=1.00 :: @AmazonHelp Hermes? You jest. Below is the only info given. No card (obviously) so no contact number
- id=1528648 conv=1528649 p=0.96 :: @AmazonHelp Wird zugestellt. Seit heute morgen. Hermes bekommt es leider nie hin pünktlich zu liefer
- id=727840 conv=727841 p=1.00 :: @AmazonHelp Zwei Gegenstände sollten gestern an die Hermes-Abholstation geliefert werden.Liegerverf:
- id=179444 conv=179452 p=1.00 :: @AmazonHelp So, ordered, lost by Hermes, cancelled, reordered. Which carrier do you chose this time?
- id=78791 conv=78803 p=1.00 :: @AmazonHelp aber ne Gutschrift oder für Hermes das Taxi bezahlen, könnten Sie bestimmt ;) bei dhl ni

### Cluster 17
- id=1293000 conv=1293004 p=1.00 :: @AmazonHelp okay thank you
- id=2849065 conv=2845506 p=1.00 :: @AmazonHelp Ok thank you for that
- id=1641390 conv=1641388 p=1.00 :: @AmazonHelp Ah fixed thanks
- id=816953 conv=816954 p=0.98 :: @AmazonHelp Right thanks
- id=1223096 conv=1223098 p=0.85 :: @AmazonHelp Ok thank you x
- id=758379 conv=758380 p=1.00 :: @AmazonHelp Okay thank you
- id=392621 conv=392622 p=1.00 :: @AmazonHelp Okay thankyou
- id=2971953 conv=2971955 p=1.00 :: @AmazonHelp Okay thank you

### Cluster 18
- id=1500722 conv=1500729 p=0.83 :: @AmazonHelp Royal Mail have confirmed their courier returned it to the depot to be delivered tomorro
- id=1331914 conv=1331915 p=0.81 :: @AmazonHelp This is Royal Mail! Why didn’t it get sent AM delivery?!
- id=2477373 conv=2477376 p=0.72 :: @AmazonHelp Royal Mail are meant to be delivering today, and you list it as 'Out for delivery' but t
- id=299002 conv=299004 p=0.73 :: @AmazonHelp Hi sorry didnt realise it was royal mail think its coming tomorrow x
- id=1346592 conv=1346593 p=0.80 :: @AmazonHelp A delay notice has been given, yes. Can Royal Mail still deliver this late?!
- id=2472381 conv=2472385 p=0.82 :: @AmazonHelp Hello there! As I thought Royal Mail did not make another delivery today and I haven’t r
- id=1290391 conv=1290393 p=0.73 :: @AmazonHelp 9pm. Surely you don't want to be associated with this sort of late delivery? DPD &amp; R
- id=448699 conv=448702 p=0.66 :: @AmazonHelp @126705 - Will it come today? Is there some kind of issue at Manchester Mail Centre?? ht

### Cluster 19
- id=2917239 conv=2917240 p=1.00 :: @AmazonHelp well it's a kind offer - but are you an actual human being? Or just another concerned bo
- id=2917217 conv=2917218 p=1.00 :: @AmazonHelp great response by a bot.
- id=1603790 conv=1603795 p=1.00 :: @AmazonHelp For an item that was never delivered? Whats your guess? Geez i hate bots....
- id=2419247 conv=2419243 p=1.00 :: @AmazonHelp Now I am getting the feeling I am talking to a bot. This just adds wasted time to a miss
- id=1206902 conv=1206903 p=1.00 :: @AmazonHelp @115850 Bot replies are so stupid ... Think about it!
- id=2935875 conv=2935876 p=1.00 :: @AmazonHelp I've been through this with another one of your bots!
- id=783396 conv=783416 p=1.00 :: @AmazonHelp U don't appreciate it. U are testing it right now. I am sure u are a bot And not a human
- id=2741793 conv=2741794 p=1.00 :: @AmazonHelp Does the B in VB stand for Bot? Because that was hella fast.

### Cluster 20
- id=503492 conv=503495 p=1.00 :: @AmazonHelp Intelcom the one who says they are too busy unpacking boxes to deliver mine
- id=2959927 conv=2959928 p=1.00 :: @AmazonHelp Intelcom. I never heard of them before and read bad reviews on them that are coming true
- id=2959941 conv=2959942 p=1.00 :: @AmazonHelp That link routes me to the US website and I ordered from The Canadian. It was Intelcom w
- id=652190 conv=649652 p=1.00 :: @AmazonHelp Option: refund (thanks). Insight: That your call center is getting complaints non-stop a
- id=609376 conv=609377 p=1.00 :: @AmazonHelp I received a refund for my mia package, but so far IntelCom is 2/2 on missing packages. 
- id=2431174 conv=2431166 p=1.00 :: @AmazonHelp Intelcom doesn't answer their phone, return messages or respond to email. I have filed n
- id=1327725 conv=1327726 p=1.00 :: @AmazonHelp Yes but that means nothing to Intelcom.
- id=2606682 conv=2606680 p=1.00 :: @AmazonHelp I spoke to someone on the phone. I was given a promo code but it still doesn't really fi

### Cluster 21
- id=1004535 conv=1004536 p=1.00 :: @AmazonHelp Non sur ordi il me demande le code en plus et je suis co. Mais la a chaque fois faut que
- id=1540966 conv=1540963 p=1.00 :: @AmazonHelp so am i going to get my code orrrr?
- id=2464834 conv=2464836 p=1.00 :: @AmazonHelp So, I did sign in using other methods. But I'd prefer if the temporary code method was a
- id=219171 conv=219175 p=1.00 :: @AmazonHelp there was no place to put in a code
- id=1427908 conv=1427914 p=1.00 :: @AmazonHelp I just did but it doesnt show any code or anyway to redeem the code
- id=2551959 conv=2551961 p=1.00 :: @AmazonHelp Tried that and all I get are more useless codes!?!
- id=2551953 conv=2551961 p=1.00 :: @AmazonHelp If you want to help then send a code that works! I've got about 10 that don't!
- id=2909147 conv=2909148 p=1.00 :: @AmazonHelp Not even if I send you the code you cannot help me !!

### Cluster 22
- id=2238103 conv=2238101 p=0.96 :: @AmazonHelp I've had it sorted thanks
- id=1764566 conv=1764567 p=1.00 :: @AmazonHelp Seems to have been sorted today. Big thanks to Lesley at Customer Services.
- id=1704096 conv=1704097 p=1.00 :: @AmazonHelp Thank you for your reply I managed to ring and get it sorted, thank you again :)
- id=2622579 conv=2622577 p=0.94 :: @AmazonHelp Already got it sorted, thanks 👏🏻
- id=2902581 conv=2902582 p=0.91 :: @AmazonHelp No vinay has sorted it. Thanks
- id=2902642 conv=2902640 p=1.00 :: @AmazonHelp Yep done that now. Thanks for quick response, let’s hope I can sort it
- id=714176 conv=714179 p=0.80 :: @AmazonHelp Thanks for the help, I got it all sorted out, thank you.
- id=2356701 conv=2356703 p=0.75 :: @AmazonHelp Can I have this sorted out ASAP PLEASE

### Cluster 23
- id=133736 conv=133762 p=1.00 :: @AmazonHelp Der Mitarbeiter sagt, dass der Artikel zu 100% nicht mehr kommen wird. Top 😂
- id=1201947 conv=1201945 p=1.00 :: @AmazonHelp Merci. Du coup, pour recevoir le bon article, je dois re-commander ?
- id=949627 conv=949628 p=1.00 :: @AmazonHelp Si. Estaba en stock las 3 veces. Lo mismo les informé en un tuit anterior. Es un problem
- id=2889187 conv=2889188 p=1.00 :: @AmazonHelp Danke erstmal für die Antwort bzw. Schnelle Hilfe, aber leider muss ich ab einer bestimm
- id=2320303 conv=2320304 p=1.00 :: @AmazonHelp nein, da es wohl eher ein grundlegendes Problem ist, dass nicht alle Artikel mit jeder V
- id=941414 conv=941415 p=1.00 :: @AmazonHelp Gracias. No quedaba claro que hiciese falta seleccionar el artículo en el pedido de un a
- id=529154 conv=529156 p=1.00 :: @AmazonHelp Ça ne semble pas me proposer un échange... Mais simplement de retourner l'article puis d
- id=2616359 conv=2616354 p=1.00 :: @AmazonHelp Merci ! Je vais voir ça. Mais je suppose qu'on me répondra que l'article a bien été expé

### Cluster 24
- id=912554 conv=912555 p=1.00 :: @AmazonHelp Online steht DHL. Habe heute morgen 1 anderes dhl paket schon erhalten. In der Sendungsv
- id=2552247 conv=2552241 p=1.00 :: @AmazonHelp Nach 4 Tagen noch keine Antwort, obwohl Link ausgefüllt. Langt doch wenn DHL unfähig ist
- id=397432 conv=397433 p=1.00 :: @AmazonHelp Lt. DHL- Sendungsverfolgung ist das Zeug nämlich schon ausgeliefert seit Stunden. https:
- id=814372 conv=814377 p=1.00 :: @AmazonHelp Danke, die haben schon geprüft. Schlechte Textbausteine, die behaupten, dass DHL ein Pak
- id=2588685 conv=2588687 p=1.00 :: @AmazonHelp seh grad die meldung: DHL konnte die adresse nicht finden...is ja nur deren eigene packs
- id=2841917 conv=2841915 p=1.00 :: @AmazonHelp Dort wo alle DHL Packstationen nicht wählbar sind? (Warum?) https://t.co/uqQzcgToij
- id=73426 conv=73427 p=1.00 :: @AmazonHelp What a bummer :( it’s not just this order, DHL is like a synonym for issues (at least on
- id=2621062 conv=2621068 p=1.00 :: @AmazonHelp Acabo de hablar con DHL y me dice que la guía se generó el 10 de noviembre, pero que aún

### Cluster 25
- id=1441391 conv=1441392 p=0.59 :: @AmazonHelp Danke! Dir noch einen schönen Tag.👍😉
- id=736518 conv=736507 p=0.77 :: @AmazonHelp D'accord merci à vous, bonne fin de journée
- id=479326 conv=479328 p=1.00 :: @AmazonHelp Sweet, will do. I appreciate the quick replies, hope you all have a good day.
- id=109988 conv=109989 p=0.92 :: @AmazonHelp Oh My bad, yeah got it. Thanks and Sorry !!! Have a nice day :D !!!
- id=685651 conv=685655 p=0.79 :: @AmazonHelp En vous remerciant de vos réponses. Passez une très bonne journée.
- id=2111012 conv=2111015 p=1.00 :: @AmazonHelp Thanks! will do. have a great day!
- id=1402861 conv=1402859 p=1.00 :: @AmazonHelp thanks! I'll bookmark this. Have a great rest of your day. ☺
- id=2770732 conv=2770733 p=0.81 :: @AmazonHelp Thanks you mate have a nice day, they replied me see ya!!!

### Cluster 26
- id=69913 conv=69933 p=0.54 :: @AmazonHelp No update till now! :(
- id=521656 conv=521652 p=0.45 :: @AmazonHelp Yes. It says need to update.
- id=126109 conv=126115 p=0.45 :: @AmazonHelp Still no update from your end!
- id=995457 conv=927512 p=0.43 :: @AmazonHelp I have updated it
- id=1610876 conv=1172677 p=0.58 :: @AmazonHelp I have already filled the details and what I am looking for an update. Please check your
- id=65633 conv=65655 p=0.52 :: @AmazonHelp What's the update
- id=523443 conv=523444 p=0.39 :: @AmazonHelp It has to be flash briefing. Covers news from #TOI, Business updates from #ET and #Bloom
- id=1735292 conv=1735288 p=0.53 :: @AmazonHelp Any update??

### Cluster 27
- id=1014813 conv=1014814 p=1.00 :: @AmazonHelp The reviews did not violate guidelines as far as s I know - can they be retrieved please
- id=2511447 conv=2511448 p=1.00 :: @AmazonHelp I checked your guidelines.. My review meets ALL the guidelines... so why is not posted? 
- id=837480 conv=837488 p=1.00 :: @AmazonHelp And I challenge you to show me what in that review doesn't meet your guidelines
- id=2019827 conv=2019828 p=1.00 :: @AmazonHelp @115821 have you read the review comments? Tell which part doesn’t meet guidelines ?
- id=226416 conv=226418 p=1.00 :: @AmazonHelp Hi. already seen this. Have also read conditions of use but no help. Does NOT say y my r
- id=1223247 conv=1223263 p=1.00 :: @AmazonHelp This is just 2 reviews? I have had every single review removed? I don't understand why? 
- id=2870729 conv=2870730 p=1.00 :: @AmazonHelp You really dont me submitting a review.
- id=893329 conv=893330 p=1.00 :: @AmazonHelp "previous review of this product did not comply with our Customer Reviews Guidelines." R

### Cluster 28
- id=281693 conv=281682 p=1.00 :: @AmazonHelp Hey I've got another issue with yet another Chinese seller/store. They are saying they a
- id=1522569 conv=1522566 p=1.00 :: @AmazonHelp The item options and instructions are not clear and half in Chinese. Some items you can'
- id=415111 conv=415109 p=1.00 :: @AmazonHelp It's says China post
- id=2938368 conv=2938366 p=1.00 :: @AmazonHelp Yes, I've just done that and awaiting a reply within 48hrs. However if I'm to return the
- id=2597096 conv=128093 p=1.00 :: @AmazonHelp Para ayudar? Me gan estado mandando correos hasta en chino! Pero no resuelven nada...
- id=2627615 conv=2627613 p=1.00 :: @AmazonHelp Es un proveedor de China
- id=734141 conv=734136 p=1.00 :: @AmazonHelp Comme vous le savez, la Chine livre en Corse. Merci de votre compréhension.
- id=1567499 conv=1567500 p=1.00 :: @AmazonHelp Los he buscado pero no me he podido contactar con el transportista, es de china post :/

### Cluster 29
- id=29572 conv=29573 p=0.82 :: @AmazonHelp Horrible response form your team still unable to solve the Issue....can someone call me 
- id=2555155 conv=685768 p=0.95 :: @AmazonHelp @283696 Why will we contact them..i have reported to your team..now please contact with 
- id=1875535 conv=1875536 p=0.91 :: @AmazonHelp I've contacted your support team everyday 4 d last 3 days &amp; I havn't gt a proper rep
- id=246454 conv=246446 p=0.91 :: @AmazonHelp No update from your team, worst service
- id=197987 conv=197995 p=0.95 :: @AmazonHelp @115851 Didn't get any response from your team. Please do it on priority
- id=180597 conv=180607 p=0.91 :: @AmazonHelp I can't see an option to reply... Why can't you go ahead and ask the concerned team to r
- id=918241 conv=918243 p=0.91 :: @AmazonHelp I want this to be visible to public. You can check internally that your team has not tak
- id=419880 conv=419885 p=0.95 :: @AmazonHelp Have not received any response till now from your busy team...@115850 @115850

### Cluster 30
- id=840901 conv=840904 p=0.58 :: @AmazonHelp can you please check with resolution team what was gone wrong and how many times #disgus
- id=124784 conv=124782 p=0.50 :: @AmazonHelp What was the resolution? @115851 shame on you
- id=1312530 conv=1312522 p=0.55 :: @AmazonHelp Don't tell me about future No bdy knws i want 2 have resolution now can you ensure recvr
- id=179374 conv=179401 p=0.67 :: @AmazonHelp Hye @115850 what are you doing? Another time period for resolution has been passed away 
- id=387566 conv=387561 p=0.64 :: @AmazonHelp I have submitted details but still no revert. When can I expect resolution from you guys
- id=2933663 conv=2933655 p=0.48 :: @AmazonHelp Lets see...dont contact me incomplete info abt my issue and without any resolution
- id=180834 conv=180859 p=0.53 :: @AmazonHelp but is the resolution ??? only sorry ????? writing 1000 time giving all evidence and fin
- id=973997 conv=974002 p=0.54 :: @AmazonHelp Done. Still no response/ resolution

### Cluster 31
- id=2151112 conv=2151106 p=1.00 :: @AmazonHelp Why do we people order on diwali...if you don't get that in your ceos big thick bald sku
- id=383337 conv=383325 p=1.00 :: @AmazonHelp You guys can deliver wrong items but you can't deliver right items before Diwali. #NotAG
- id=1064829 conv=931511 p=1.00 :: @AmazonHelp Now I don't need for that product but please improve your shipping and customer service 
- id=293342 conv=293343 p=1.00 :: @AmazonHelp Of course, I'll definitely shop before festival of Diwali.
- id=2113009 conv=2113011 p=0.90 :: @AmazonHelp Thanks you too for reasonable price and good service Happy Diwali
- id=2115649 conv=2115651 p=1.00 :: @AmazonHelp I ordered something on Diwali occasion and this is how your customer experience is????
- id=1137937 conv=1137940 p=0.96 :: @AmazonHelp If would have known this I would booked on this offer, the fact is only Diwali offer is 
- id=989141 conv=986155 p=1.00 :: @AmazonHelp Hi it's not a concern, just an image in reply to your promotion showing that I have comp

### Cluster 32
- id=577126 conv=577127 p=1.00 :: @AmazonHelp Is there anyone NOT in INDIA? IS BEEN 2 DAYS OF LIES ALREADY AND I AM ALREADY REALLY TIR
- id=294315 conv=293332 p=1.00 :: @AmazonHelp @115851 look what you have created in India
- id=859620 conv=859621 p=1.00 :: @AmazonHelp For everything , for each &amp; every city in India.😀
- id=2536345 conv=2536341 p=1.00 :: @AmazonHelp India please c the below picture https://t.co/iufTy0lywm
- id=2386331 conv=2386339 p=1.00 :: @AmazonHelp Thanks a lot for your help.i thought I was in London.. thank you for reminding me my dom
- id=2612289 conv=2612290 p=1.00 :: @AmazonHelp Ok. :) Plz do consider bringing it to India. Aside: consider using different initials th
- id=726772 conv=726773 p=1.00 :: @AmazonHelp This is available on https://t.co/5eo4tFWcUG right. You mean it's not here in India ?
- id=318168 conv=318173 p=1.00 :: @AmazonHelp Yes . And it is an India portal link. It was of no help

### Cluster 33
- id=1127175 conv=1127180 p=0.79 :: @AmazonHelp Hermes UK.
- id=2891937 conv=2891935 p=0.75 :: @AmazonHelp I’m in the Uk, is this only available in the US?
- id=65690 conv=65698 p=0.72 :: @AmazonHelp Also, not sure why I should give feedback in the UK if I live in the US. ;)
- id=1223076 conv=1223072 p=1.00 :: @AmazonHelp I see the link says UK-- is there a US one? Or does it not even matter?
- id=2297407 conv=2297413 p=0.45 :: @AmazonHelp This took me to the U.K. Site but I'm in the US.
- id=297974 conv=297975 p=1.00 :: @AmazonHelp It is related to UK only, not USA.
- id=2906695 conv=2906697 p=0.39 :: @AmazonHelp In the UK not US
- id=77498 conv=77496 p=0.91 :: @AmazonHelp ok but this is a link to the UK site and i live in the US

### Cluster 34
- id=2890594 conv=2890588 p=1.00 :: @AmazonHelp Just arrived so no need anymore i guess
- id=2550251 conv=2550248 p=1.00 :: @AmazonHelp It arrived! 😀👷‍♂️
- id=86150 conv=86144 p=1.00 :: @AmazonHelp It just arrived, safe and sound! Thank you very much for dealing with that.
- id=183062 conv=183065 p=1.00 :: @AmazonHelp It’s arrived thank you
- id=531586 conv=531587 p=1.00 :: @AmazonHelp It has just arrived as I typed, cheers!
- id=563920 conv=563922 p=1.00 :: @AmazonHelp Its arrived &lt;3 Thank you
- id=75921 conv=75917 p=1.00 :: @AmazonHelp It just arrived. Oh well
- id=1436639 conv=1436640 p=1.00 :: @AmazonHelp It's arrived now - was just the case of seeing everything else arrive.

### Cluster 35
- id=421254 conv=421244 p=1.00 :: @AmazonHelp Seems that ticket has been closed! No option to reply on that page.
- id=28462 conv=28463 p=1.00 :: @AmazonHelp Really? A contact form? This has been a terrible waste of time. Entitled to 2 tickets, c
- id=22156 conv=22152 p=0.84 :: @AmazonHelp It says that if I only select one ticket! What's going on?
- id=2676820 conv=2676821 p=0.95 :: @AmazonHelp 140 characters isn’t enough to explain. You didn’t send my tickets for an event on Thurs
- id=224269 conv=224271 p=1.00 :: @AmazonHelp Yes, 10/3. no response yet. Always high ticket items get held up.
- id=674237 conv=674239 p=1.00 :: @AmazonHelp Already did that yesterday morning - they are 'looking into it' for me but I've heard no
- id=1881701 conv=1881702 p=0.92 :: @AmazonHelp I tried for over one hour to purchase tickets and failed
- id=2721788 conv=2721789 p=1.00 :: @AmazonHelp Hi no I haven't been sent any emails from you, but I have read that some people who brou

### Cluster 36
- id=64202 conv=64214 p=1.00 :: @AmazonHelp The form/link I was sent was my details for somebody to call me back, I’ve never given m
- id=665610 conv=665633 p=1.00 :: @AmazonHelp I will call tomorrow however I’m based in the UK
- id=1689481 conv=1689488 p=1.00 :: @AmazonHelp I can't remember my password so cant use your link. I'll DM my phone number if I can get
- id=1741700 conv=1741702 p=1.00 :: @AmazonHelp Is there a UK number I can call or an email I can contact please?
- id=2286011 conv=2286013 p=1.00 :: @AmazonHelp Hi the number is going to a foreign call centre. I want to speak to someone in the UK. C
- id=1983531 conv=1983533 p=1.00 :: @AmazonHelp I need to speak to a uk advisor
- id=765448 conv=764169 p=1.00 :: @AmazonHelp Please help? I need a UK contact?
- id=36521 conv=36561 p=1.00 :: @AmazonHelp Not able to contact you, getting calls from UK https://t.co/zoVPnr8Z9r

### Cluster 37
- id=530805 conv=530811 p=0.99 :: @AmazonHelp El SAT en España es lamentable
- id=1384268 conv=1384266 p=1.00 :: @AmazonHelp Hablamos de Sevilla capital...
- id=1345918 conv=1345919 p=0.84 :: @AmazonHelp Livraison en point relais, à la boulangerie Richter sur Montpellier
- id=231539 conv=231540 p=0.94 :: @AmazonHelp Gracias por la rapidez en la respuesta, no aparecen vacantes en Sevilla, muchas gracias
- id=1863717 conv=1863718 p=1.00 :: @AmazonHelp Un colgante de plata de un gatito 😍 El servicio premium de España es muy bueno, merece l
- id=2721705 conv=2721712 p=1.00 :: @AmazonHelp Necesito un tlf soporte España! Y no encuentro por ninguna parte, por eso os he escrito 
- id=815584 conv=815582 p=1.00 :: @AmazonHelp Spain (.es)
- id=2828730 conv=2828732 p=1.00 :: @AmazonHelp No está disponible en España?

### Cluster 38
- id=673210 conv=673208 p=1.00 :: @AmazonHelp Until I have an order i.d I can't speak to you. I want to jnow the warranty details of a
- id=2297873 conv=2297874 p=1.00 :: @AmazonHelp I bought a mixer grinder and it started sparking after 1 mnth.. it is in wrnty and the s
- id=13865 conv=13897 p=1.00 :: @AmazonHelp you have wasted one month by bullsh****g me. now i am being told itvis out of warranty. 
- id=1209898 conv=1209899 p=1.00 :: @AmazonHelp Even still the product shows 5 years warranty and just now I have contacted prestige cus
- id=379575 conv=379577 p=1.00 :: @AmazonHelp One month. I don't see the warranty information on the product page.
- id=2528273 conv=2528274 p=1.00 :: @AmazonHelp Yes I have already sent an email regarding this. Also when I chatted with the customer c
- id=13870 conv=13897 p=1.00 :: @AmazonHelp same reply again and again. if the complaint is raised under warranty period and if @200
- id=689481 conv=689478 p=1.00 :: @AmazonHelp Not really, have no way to contact seller. I am looking at warranty replacement

### Cluster 39
- id=665607 conv=665633 p=1.00 :: @AmazonHelp Spoke to yr CS team who helped as much as poss although cld not change my Xbox OneX deli
- id=1773280 conv=1773282 p=1.00 :: @AmazonHelp Obviously regarding an Xbox One X order, however your team has told me that it's a probl
- id=1731168 conv=1731166 p=1.00 :: @AmazonHelp The attached picture isn't correct according to customer support and they don't know whe
- id=260353 conv=260356 p=1.00 :: @AmazonHelp Merci beaucoup je reviendrais voir pour décembre quand j'aurai la Xbox one X
- id=2089283 conv=2089268 p=1.00 :: @AmazonHelp had an email offering me £20 and an apology for no delivery of the new Xbox. Problem is 
- id=665612 conv=665633 p=1.00 :: @AmazonHelp Hi, yes I have. Because the Xbox is part of a bigger order and other items have been del
- id=815477 conv=815479 p=1.00 :: @AmazonHelp Xbox One hasn't arrived. Been given at least 5 different dates/times via email/app. Appa
- id=1746102 conv=1746100 p=1.00 :: @AmazonHelp Enfin d'après ce qu'on peut remarquer sur Twitter bcp de gens sont mécontents du retard 

### Cluster 40
- id=2338163 conv=2338164 p=0.83 :: @AmazonHelp This is not the first time it happened. Paid full price for a game from the UK that has 
- id=1331206 conv=1331208 p=0.95 :: @AmazonHelp As part of a pre-order, I was supposed to receive 3 free games. I’ve got just one so far
- id=131705 conv=131701 p=0.96 :: @AmazonHelp Managed to get one on there now but with a different game for the same price :)
- id=2350901 conv=2350902 p=0.96 :: @AmazonHelp I ordered it on Saturday and played extra for delivery today. Got the games but no conso
- id=181223 conv=181225 p=0.66 :: @AmazonHelp para ps4 tambien estoy esperando que pongan el play station 4 nuevamente para poder adqu
- id=946568 conv=946571 p=0.96 :: @AmazonHelp @344464 Werden alle spiele übertragen oder nur ausgewählte?
- id=2159677 conv=2159678 p=0.87 :: @AmazonHelp Thanks, will do, I understand restrictions on liquids etc but can't understand why this 
- id=376813 conv=376814 p=0.96 :: @AmazonHelp Thx for replying! It's not showing up... The discount for other pre-order games is worki

### Cluster 41
- id=313655 conv=313653 p=1.00 :: @AmazonHelp Now check it.
- id=21474 conv=19137 p=1.00 :: @AmazonHelp You can check it
- id=2669972 conv=2669986 p=1.00 :: @AmazonHelp Ouï mais vérifiez quoi ?
- id=2318582 conv=2318591 p=1.00 :: @AmazonHelp Alors cette vérification de dossier ? :))
- id=652056 conv=652068 p=1.00 :: @AmazonHelp Pouvez-vous faire une vérification ? S'il vous plaît ?
- id=2312500 conv=2312501 p=1.00 :: @AmazonHelp I will check and get back to yiy
- id=1553268 conv=1553275 p=1.00 :: @AmazonHelp Ok il check
- id=183518 conv=183522 p=1.00 :: @AmazonHelp Let me check

### Cluster 42
- id=2396394 conv=2396395 p=0.45 :: @AmazonHelp I already talked to customer service which is why I ultimately deleted the tweet, though
- id=1289687 conv=1289689 p=0.54 :: @AmazonHelp Missed your tweet before I switched off. Will get the timestamp for you tomorrow.
- id=534956 conv=534958 p=0.42 :: @AmazonHelp Je croyais qu'il fallait le signaler ici , c'est pour ça que je vous ai fait un tweet, v
- id=350640 conv=350642 p=0.53 :: @AmazonHelp Similar case was with tata docomo. Hence had to take help if twitter. The tata docomo te
- id=1772664 conv=1772665 p=0.52 :: @AmazonHelp I haven't yet. I need to be less annoyed first. Also, they updated the character count f
- id=1176218 conv=1176231 p=0.47 :: @AmazonHelp I didn’t actually lose a package. I just felt like my original tweets at the top of this
- id=637195 conv=637200 p=0.56 :: @AmazonHelp Si claro. Escribí el primer tweet y a las 4, me contestaron pidiendome información, les 
- id=1219952 conv=1219935 p=0.53 :: @AmazonHelp Tell me the answer why it was not checked when i tweet you on 6pm

### Cluster 43
- id=105132 conv=105134 p=1.00 :: @AmazonHelp No nothing except confirmation that an investigation is going on... it’s month end.. all
- id=78701 conv=78705 p=1.00 :: @AmazonHelp non juste qu'une enquête est en cours et qu'il faut attendre jusqu'au 4 décembre
- id=24491 conv=24505 p=1.00 :: @AmazonHelp Thanks but I have tried that every day since Sunday. "Still investigating" - you should 
- id=498393 conv=498394 p=1.00 :: @AmazonHelp Oui je viens de le faire. On m'a dit qu'une enquête était ouverte et que j'aurais des no
- id=1499731 conv=1499735 p=1.00 :: @AmazonHelp Told that investigate was happening. Items were ok this time but took 24 hours to find t
- id=2628831 conv=2628827 p=1.00 :: @AmazonHelp Merci. J'ai enfin eu une personne compétente au sav, le dossier est en cours d'investiga
- id=736511 conv=736507 p=1.00 :: @AmazonHelp Effectivement une enquête a été ouverte hier
- id=1140865 conv=1140869 p=1.00 :: @AmazonHelp Une enquête a été ouverte et j'espère qu'elle aboutira au plus vite afin que je puisse e

### Cluster 44
- id=2216655 conv=2216656 p=0.75 :: @AmazonHelp Is there a link for Germany as well ?
- id=136255 conv=136252 p=0.61 :: @AmazonHelp Und FYI „Berlin ist groß“ zieht hier nicht. Hinter dem Berlin, Deutschland“ liegen gps D
- id=1499885 conv=1499886 p=0.92 :: @AmazonHelp And it's the German marketplace I'm inquiring about FYI
- id=318884 conv=318885 p=0.57 :: @AmazonHelp Seriously though, you're having quite serious network problems around Germany, don't you
- id=54418 conv=54414 p=0.84 :: @AmazonHelp Er schickt eine Mail wie das mit dem Prime gratis verlängern läuft oder so. Ich konnte s
- id=95342 conv=95301 p=0.57 :: @AmazonHelp An I hope you can have the service in Germany as serious and reliable as you have in oth
- id=1262350 conv=1262351 p=1.00 :: @AmazonHelp on the german site
- id=1761041 conv=1761043 p=0.71 :: @AmazonHelp ASIN: B003CXOB1G nach Berlin https://t.co/NAwepSTgaA

### Cluster 45
- id=2971950 conv=2971955 p=1.00 :: @AmazonHelp Okay thank you.
- id=1385714 conv=1385709 p=1.00 :: @AmazonHelp Alright. Thank you TP.
- id=510382 conv=510383 p=1.00 :: @AmazonHelp Okay thank you.
- id=262567 conv=262569 p=1.00 :: @AmazonHelp Ok, thank you
- id=2115556 conv=2115560 p=1.00 :: @AmazonHelp Ok, thank you
- id=1373688 conv=1373691 p=1.00 :: @AmazonHelp Alright thank you.
- id=444326 conv=444334 p=1.00 :: @AmazonHelp Okay. Thank you
- id=2292123 conv=2292124 p=1.00 :: @AmazonHelp ok thank you.

### Cluster 46
- id=668472 conv=214365 p=1.00 :: @AmazonHelp guys it is so sad that still the return pickup is not done for more than 20 days since s
- id=1137726 conv=1137727 p=1.00 :: @AmazonHelp Just got a msg that pickup has been rescheduled for tomorrow. Will get back to you for a
- id=182604 conv=182606 p=1.00 :: @AmazonHelp Have done so. The return pickup is scheduled for next Tue as that is the earliest availa
- id=180121 conv=180139 p=1.00 :: @AmazonHelp I received a mail yesterday that pickup will be done but till now nothing happened. I'm 
- id=898727 conv=898764 p=1.00 :: @AmazonHelp Pickup has been successfully done. Please check and process REFUND asap.
- id=879183 conv=879177 p=1.00 :: @AmazonHelp Hi team , called customer support and rescheduled the pickup tomorrow.
- id=1665827 conv=1665830 p=1.00 :: @AmazonHelp Hi I had place a request for a pick up for an item that had to be returned. They cancell
- id=180346 conv=180354 p=1.00 :: @AmazonHelp I want the pickup to be done today I can't wait for Tom u have the invoice with u with I

### Cluster 47
- id=1676625 conv=1676621 p=1.00 :: @AmazonHelp I m not sure product will be delivered today or not. Let see what is going to happen you
- id=422007 conv=422005 p=1.00 :: @AmazonHelp Am i getting my product delivered today?
- id=1545460 conv=1545457 p=1.00 :: @AmazonHelp Well. Then you are kindly requested to expedite the process and arrange to get the produ
- id=2281453 conv=2281456 p=1.00 :: @AmazonHelp I have DM my query, please make sure the products get delivered on time by 9-10 am morni
- id=130848 conv=130869 p=1.00 :: @AmazonHelp Is there any status of my product, it's now more than 72 hours
- id=1043693 conv=1043727 p=1.00 :: @AmazonHelp @115821 @115850 Since Sunday you are working on this. Haven't you got update yet. When w
- id=1786140 conv=1786141 p=0.98 :: @AmazonHelp Already done! The pick up is tomorrow. I hope the right product is delivered this time. 
- id=1043654 conv=1043727 p=1.00 :: @AmazonHelp @115821 @115850 Can you tell me if I can expect delivery of my product today?

### Cluster 48
- id=2594324 conv=2594326 p=1.00 :: @AmazonHelp Solicite mi producto el dia de ayer para entrega garantizada el dia de hoy segun su app,
- id=293780 conv=293781 p=1.00 :: @AmazonHelp Nope, app says will be delivered tomorrow but is delayed and to follow instructions on a
- id=2590348 conv=2590351 p=1.00 :: @AmazonHelp It's ok I'll wait till tomorrow. I'd be more concerned about the app showing an item "ar
- id=2795297 conv=2795298 p=1.00 :: @AmazonHelp Only by checking the app myself, three separate parcels now late that said they would be
- id=1537520 conv=1537521 p=1.00 :: @AmazonHelp supposed to be delivered today and now app is saying won’t be here until Wednesday possi
- id=2724466 conv=2724464 p=1.00 :: @AmazonHelp This is what is says on my app, I have been told by customer service that it will not be
- id=657882 conv=657872 p=1.00 :: @AmazonHelp You tweeted it above. If it hasn’t arrived by 1200 today (and the status on my app hasn’
- id=1069884 conv=1069885 p=1.00 :: @AmazonHelp Yes, I've received 2 updates from the app since, both with conflicting information and i

### Cluster 49
- id=643812 conv=643818 p=1.00 :: @AmazonHelp Nothing is there Stop fooling us You should response
- id=1729707 conv=1729701 p=1.00 :: @AmazonHelp Why are you here. To mislead the people, or make the people fool.
- id=1357637 conv=1357655 p=1.00 :: @AmazonHelp Don't you guys get tired of spreading the same lie again n again
- id=707335 conv=707336 p=1.00 :: @AmazonHelp That's a bold face lie.
- id=1014783 conv=1014703 p=1.00 :: @AmazonHelp Lie is your habbit
- id=1487716 conv=1487710 p=1.00 :: @AmazonHelp Why are you making my fool, nothing is there. i think i should file a complaint against 
- id=313847 conv=313842 p=1.00 :: @AmazonHelp Lies lies lies - why lie to people? Do you think we are stupid?
- id=2379754 conv=2379755 p=1.00 :: @AmazonHelp Talking to someone about it now, but honestly brazen lies are noooooooot a good look. ht

### Cluster 50
- id=2349516 conv=2349509 p=0.74 :: @AmazonHelp I've filled the form. Now sort out my problem asap.
- id=1585032 conv=994246 p=0.72 :: @AmazonHelp I have already filled the form. It hasn't helped me much.
- id=63935 conv=63826 p=0.69 :: @AmazonHelp i am ok with the information have filled the form please call asap now and solve this ma
- id=758938 conv=758939 p=0.72 :: @AmazonHelp I am messaging you the details,see if you care enough as you say .I am sick of filling t
- id=182863 conv=182873 p=0.71 :: @AmazonHelp No no more forms please thanks I have had enough disappointment thanks
- id=227880 conv=227867 p=0.81 :: @AmazonHelp I already filled this form number of time but no reply and I did it Just now also so pls
- id=1137391 conv=1137399 p=0.71 :: @AmazonHelp This form I have submitted yesterday. Can you plz check. Why can't you handle the proble
- id=140909 conv=137096 p=0.67 :: @AmazonHelp Filled the form again wid details please contact me at earliest directly

### Cluster 51
- id=301037 conv=301042 p=1.00 :: @AmazonHelp I have filled it out again
- id=126792 conv=126799 p=1.00 :: @AmazonHelp Filled.... Plzzzzz check
- id=65791 conv=65795 p=0.68 :: @AmazonHelp Have filled it again. Please check.
- id=1143385 conv=1143373 p=0.73 :: @AmazonHelp I have filled up again . Hoping for quick result
- id=1034711 conv=1034704 p=1.00 :: @AmazonHelp filled it .. please check
- id=711114 conv=711112 p=1.00 :: @AmazonHelp Ok I have filled it out
- id=307192 conv=307211 p=1.00 :: @AmazonHelp Ok, I filled it out.
- id=2568069 conv=2568075 p=1.00 :: @AmazonHelp I have filled it

### Cluster 52
- id=2781844 conv=2781845 p=1.00 :: @AmazonHelp Super merci de l'info
- id=294774 conv=294771 p=1.00 :: @AmazonHelp Ok thanks for the information 👍
- id=318644 conv=318645 p=1.00 :: @AmazonHelp OK thanks for the information.
- id=61009 conv=35857 p=1.00 :: @AmazonHelp Así es, gracias por la información.
- id=1594614 conv=1594612 p=1.00 :: @AmazonHelp Achso, danke für die Info!
- id=2126702 conv=2126703 p=1.00 :: @AmazonHelp Muchas gracias por la información y pronta respuesta.
- id=244167 conv=244165 p=1.00 :: @AmazonHelp Thanks for informing
- id=2698979 conv=2698977 p=1.00 :: @AmazonHelp Gracias por la información

### Cluster 53
- id=180863 conv=180868 p=1.00 :: @AmazonHelp No error message- just a completely blank page.
- id=645 conv=646 p=1.00 :: @AmazonHelp That page is useless - doesn’t allow me to state it hasn’t been delivered; only tells me
- id=2907802 conv=2907804 p=1.00 :: @AmazonHelp says no page found 🤔
- id=2113573 conv=2113580 p=1.00 :: @AmazonHelp Ha, yeah, that page doesn't work.
- id=1715677 conv=1715678 p=1.00 :: @AmazonHelp I get a blank page. Super helpful. 👍🏼
- id=984198 conv=984199 p=1.00 :: @AmazonHelp Hi, I don't want to return it - I want to read it! I think the problem here is it's a 2-
- id=374537 conv=374538 p=1.00 :: @AmazonHelp it just never showed and then the page changed to "if not by wed then..." after we canx 
- id=1573518 conv=1573511 p=1.00 :: @AmazonHelp That page doesn't have those items listed.

### Cluster 54
- id=2781887 conv=2781889 p=1.00 :: @AmazonHelp It's called Link
- id=197637 conv=197649 p=1.00 :: @AmazonHelp Where is the link????????????
- id=1007017 conv=1007015 p=1.00 :: @AmazonHelp Where is the link ?
- id=914801 conv=914802 p=1.00 :: @AmazonHelp What use is that link precisely?
- id=956252 conv=956254 p=1.00 :: @AmazonHelp What link ?
- id=25843 conv=25839 p=1.00 :: @AmazonHelp I'm not sure I know what link you mean, I can't seem to find one!
- id=1762297 conv=1762293 p=1.00 :: @AmazonHelp ok thanks. What is FR? Where can I find the link?
- id=2509237 conv=2509234 p=1.00 :: @AmazonHelp "with the link provided by SP" - What is 'SP'?

### Cluster 55
- id=126794 conv=126799 p=0.98 :: @AmazonHelp The provided link didn't help me
- id=1279202 conv=1279203 p=1.00 :: @AmazonHelp Yes, but when I follow that link, there are no links to subtopics on my left sidebar. We
- id=1427889 conv=1427893 p=0.96 :: @AmazonHelp That link is not working for me
- id=676939 conv=676940 p=1.00 :: @AmazonHelp I am not able to open this link.
- id=629610 conv=629612 p=1.00 :: @AmazonHelp none of link provided is working....
- id=1774580 conv=1774581 p=0.95 :: @AmazonHelp Nothing of the link provided helps
- id=439685 conv=348045 p=0.84 :: @AmazonHelp No such link is shared.
- id=1272927 conv=1272924 p=0.79 :: @AmazonHelp That link is not helping.

### Cluster 56
- id=210491 conv=210519 p=1.00 :: @AmazonHelp Please send me link,we don't get link from your side,please provide us and worl fast
- id=644026 conv=474336 p=1.00 :: @AmazonHelp Provide me the link here
- id=1744048 conv=1744042 p=1.00 :: @AmazonHelp please share link again.
- id=81048 conv=81054 p=1.00 :: @AmazonHelp Plz send me the link
- id=2652385 conv=2652371 p=1.00 :: @AmazonHelp Filled the link out, thanks.
- id=2290046 conv=2116190 p=1.00 :: @AmazonHelp Send me the link again
- id=2884928 conv=2884931 p=1.00 :: @AmazonHelp That already filled in that link.
- id=737151 conv=737147 p=1.00 :: @AmazonHelp Send the link again I will update details

### Cluster 57
- id=929178 conv=929179 p=1.00 :: @AmazonHelp I have shared my detail here as your link is not working. Please share delivery proof AS
- id=965075 conv=964970 p=1.00 :: @AmazonHelp Please send me the link 1nce again where I had shared my details.
- id=424073 conv=424069 p=1.00 :: @AmazonHelp Yes I have shared the details on the link shared. I can share everything here as well po
- id=834806 conv=834803 p=1.00 :: @AmazonHelp Already shared the details on the link
- id=1212691 conv=1212686 p=1.00 :: @AmazonHelp I have already provided my details on the given link
- id=1973381 conv=1973387 p=1.00 :: @AmazonHelp I have already sent the details on the link about 2 minutes ago
- id=1608658 conv=1608663 p=1.00 :: @AmazonHelp Shared the details at given link.please check
- id=613992 conv=613993 p=1.00 :: @AmazonHelp I am send details in above link

### Cluster 58
- id=21468 conv=19137 p=1.00 :: @AmazonHelp Allready mention all information
- id=1125348 conv=1125345 p=1.00 :: @AmazonHelp Already Shared The Details....
- id=2291137 conv=2291135 p=1.00 :: @AmazonHelp I have send the details....
- id=236618 conv=236614 p=1.00 :: @AmazonHelp I have shard the details
- id=2670728 conv=2670731 p=1.00 :: @AmazonHelp Sent the details..
- id=1128078 conv=1128064 p=1.00 :: @AmazonHelp Already provided the details...
- id=604993 conv=604995 p=1.00 :: @AmazonHelp I HAVE ALREADY DROPPED THE DETAILS...
- id=969111 conv=969120 p=1.00 :: @AmazonHelp I Share All My Details

### Cluster 59
- id=595700 conv=595701 p=1.00 :: @AmazonHelp Ty ily i got it https://t.co/7p36VzAWD6
- id=2290532 conv=2290538 p=1.00 :: @AmazonHelp I don't know. This is all I have. https://t.co/V0E2r2fnix
- id=420257 conv=420255 p=1.00 :: @AmazonHelp I never got it !! https://t.co/dENOyNcGBr
- id=440256 conv=440270 p=1.00 :: @AmazonHelp 1/3 @115850 https://t.co/GQvLJEXGDS
- id=570096 conv=570099 p=1.00 :: @AmazonHelp This is all I’m told https://t.co/5CJLvJc9xz
- id=598031 conv=598027 p=1.00 :: @AmazonHelp https://t.co/k2I3flOM44 and https://t.co/P1T8oXnM1t
- id=1234062 conv=1234063 p=1.00 :: @AmazonHelp All i get is this.... https://t.co/AAFVuNKYG1
- id=450685 conv=450687 p=1.00 :: @AmazonHelp que es esto? https://t.co/CBHhiELFKD

### Cluster 60
- id=1264483 conv=1264450 p=0.73 :: @AmazonHelp I have replied more than 3 times first read the screen shots and than say anything https
- id=353599 conv=353605 p=0.83 :: @AmazonHelp I had submit the info which was being ask on that link here is the screenshot https://t.
- id=25931 conv=25935 p=0.87 :: @AmazonHelp Screenshot wurde vor 10 Minuten gemacht :) Danke für die schnelle Rückmeldung.
- id=561637 conv=561642 p=0.93 :: @AmazonHelp Please check the screenshot attached
- id=1729621 conv=1729623 p=0.63 :: @AmazonHelp Attached the screenshot of the error. This is occuring since last 4 days https://t.co/x6
- id=490417 conv=490418 p=0.67 :: @AmazonHelp That means you have not seen the attached image properly. Please have a look
- id=1727533 conv=1727534 p=0.75 :: @AmazonHelp screenshot of what exactly..??
- id=2761263 conv=2761264 p=0.92 :: @AmazonHelp Not working for me. I hope this screenshot will clear your doubt. Thanks. https://t.co/8

### Cluster 61
- id=277253 conv=277260 p=1.00 :: @AmazonHelp Managed to get through to someone who is on the case 👌🏼
- id=946617 conv=946601 p=1.00 :: @AmazonHelp its more than 1 month to raise on this , but my case is pending till now no resolving th
- id=619112 conv=619114 p=1.00 :: @AmazonHelp Wat more details ur support team is already aware of this pending case
- id=984193 conv=984195 p=1.00 :: @AmazonHelp there is no option for such a case ..please help
- id=991749 conv=991747 p=1.00 :: @AmazonHelp Ok we shall wait. FYI CASE ID 4059776082
- id=832737 conv=832695 p=1.00 :: @AmazonHelp Can u people can contact via phone to resolve the case .
- id=421249 conv=421244 p=1.00 :: @AmazonHelp Hello it`s been 6 days since I provided the details about the case. May I know the statu
- id=979564 conv=979566 p=1.00 :: @AmazonHelp You can resolve the case through Twitter or can call me right now. Order 402-2481615-329

### Cluster 62
- id=1772321 conv=1772324 p=1.00 :: @AmazonHelp I mean, it's pretty simple. You give me a guaranteed delivery date, and AMZL gets it her
- id=2308109 conv=2308110 p=1.00 :: @AmazonHelp but I paid extra for one day delivery!
- id=493491 conv=493493 p=1.00 :: @AmazonHelp I pay for your prime service and I was supposed to receive a makeup vanity today. My boy
- id=1443123 conv=1443124 p=1.00 :: @AmazonHelp Oh I plan to, especially since I paid the extra shipping for the package arrival.
- id=1398055 conv=1398053 p=1.00 :: @AmazonHelp I can understand that, the point of the matter is i pay for a service where I get next d
- id=2756027 conv=2756028 p=1.00 :: @AmazonHelp I paid $5.99 to have same day , it said it was delivered yet nothing is here.
- id=1459765 conv=1459768 p=1.00 :: @AmazonHelp Losing faith on ever getting this delivery. It's not like you've got over £500 of my mon
- id=1776901 conv=1776903 p=1.00 :: @AmazonHelp I paid for it to be delivered today

### Cluster 63
- id=1202812 conv=1202816 p=0.65 :: @AmazonHelp Is there anything else I can do?
- id=1072168 conv=1072161 p=0.69 :: @AmazonHelp What to do?
- id=284032 conv=284038 p=0.69 :: @AmazonHelp vendedor externo. o que eu devo fazer?
- id=388431 conv=388429 p=0.69 :: @AmazonHelp Ok so what do I need to do?
- id=371422 conv=371423 p=0.69 :: @AmazonHelp What can I do
- id=2757409 conv=2757410 p=0.52 :: @AmazonHelp Is there anything that can be done?
- id=1492770 conv=1489455 p=0.69 :: @AmazonHelp Was soll ich auf der Seite Machen?
- id=1137408 conv=1137399 p=0.69 :: @AmazonHelp So what am I supposed to do

### Cluster 64
- id=51576 conv=51574 p=1.00 :: @AmazonHelp Done- complaint sent.
- id=231861 conv=231857 p=1.00 :: @AmazonHelp Any Progress regarding my complaint
- id=223871 conv=223866 p=1.00 :: @AmazonHelp I have already registered my complaint. Please take some action.
- id=517553 conv=517559 p=1.00 :: @AmazonHelp I need someone that will actually resolve the issue instead of just doing the bare minim
- id=1592443 conv=1592451 p=1.00 :: @AmazonHelp what happ sir about me complaint.because already more than 1 month.iam waiting for this
- id=1053455 conv=1053461 p=1.00 :: @AmazonHelp Hi, been on this 3 times. I would like to escalate my complaint to someone who has autho
- id=900371 conv=900382 p=1.00 :: @AmazonHelp Thats a standard reply and i am not satisfied with the same and would like to file a com
- id=1645637 conv=1645617 p=1.00 :: @AmazonHelp Necesito que tomen mi reclamo y lo resuelvan.

### Cluster 65
- id=1220819 conv=1220821 p=1.00 :: @AmazonHelp Successs!!! Somehow it Works now!! Thanks 😩🙏🏼🙌🏽
- id=1445336 conv=1445337 p=1.00 :: @AmazonHelp Thanks. Yes did this and now works fine xx
- id=492190 conv=492191 p=1.00 :: @AmazonHelp It worked thanks 👍🏾
- id=246354 conv=246344 p=0.90 :: @AmazonHelp Yes it's working fine, thanks!
- id=644736 conv=644734 p=0.91 :: @AmazonHelp Yes, other commands are working fine
- id=1160653 conv=1160651 p=1.00 :: @AmazonHelp Yes, it worked, and why necessary???
- id=1499747 conv=1499751 p=0.90 :: @AmazonHelp Thanks ... it works
- id=2119350 conv=2119354 p=0.97 :: @AmazonHelp It worked now miraculously.... 👍

### Cluster 66
- id=836882 conv=836876 p=1.00 :: @AmazonHelp I haven't yet received any update on my complain. Worse part is that I can't hear anythi
- id=313241 conv=313242 p=0.82 :: @AmazonHelp Les écouteurs oui le reste non
- id=1473290 conv=1473294 p=1.00 :: @AmazonHelp Yes. I had headphones that were supposed to come today but didn’t and I wanna listen to 
- id=607291 conv=607297 p=1.00 :: @AmazonHelp Ok thanks ! But these are earphones so does it mean same policy apply for these as well
- id=313255 conv=313256 p=1.00 :: @AmazonHelp Certains oui d'autre non. Les écouteurs sont notés comme" livrés" pr exemple j'ai pas de
- id=932303 conv=932301 p=1.00 :: @AmazonHelp Ultimate Ears BOOM 2 Wireless/Bluetooth Speaker (Waterproof and Shockproof) - Purple/Ora
- id=1135079 conv=1135081 p=1.00 :: @AmazonHelp It’s a earphone one side not working properly
- id=1574528 conv=1574529 p=1.00 :: @AmazonHelp Ear headphone white

### Cluster 67
- id=373952 conv=373953 p=1.00 :: @AmazonHelp No. It only plays a handful of the songs by the artist. Even though all of them say they
- id=480364 conv=480365 p=1.00 :: @AmazonHelp Bei Musik unlimited geht nichts?! https://t.co/wCvGaXW8ll
- id=941344 conv=941342 p=1.00 :: @AmazonHelp There are some songs that are greyed out but others are completely gone
- id=1188523 conv=1188526 p=1.00 :: @AmazonHelp Android. Unter Meine Musik/Online-Musik habe ich hinter den Titeln diesen Haken, unter M
- id=2298465 conv=2298466 p=1.00 :: @AmazonHelp Danke für eure Reaktion :) Die angebotene Auswahl der Songs ist das Problem (Jens Friebe
- id=480367 conv=480365 p=1.00 :: @AmazonHelp Bei TuneIn kann ich suchen… nur Musik Unlimited geht nicht :(
- id=1424685 conv=1424686 p=1.00 :: @AmazonHelp That didn’t work it still keeps doing it. Only works when I ask for specific albums not 
- id=682542 conv=682539 p=1.00 :: @AmazonHelp It's music lol I didn't order extra music coverage so I will handle it on my end. This i

### Cluster 68
- id=1588767 conv=1588769 p=0.49 :: @AmazonHelp Me: Alexa, turn off my kitchen lights. Akexa: I found several devices matching that name
- id=1519854 conv=1519855 p=0.45 :: @AmazonHelp Nope. Alexa needs to step up her game for African artists! Shorty slacking!
- id=656094 conv=656095 p=0.46 :: @AmazonHelp It’s not a skill unfortunately. We figured it out, you have to say “Alexa sing ME happy 
- id=662671 conv=662669 p=0.53 :: @AmazonHelp No because the issue is with Alexa’s “routines”. A routine can’t send the off command to
- id=697232 conv=697235 p=0.72 :: @AmazonHelp @286361 Well played, but Alexa doesn't have a mouse to speak into.
- id=531565 conv=528986 p=0.64 :: @AmazonHelp Hab vom firetv1 Stick auf den mit Alexa gewechselt. Da lief alles problemlos. Hab den Co
- id=2752080 conv=2752072 p=0.74 :: @AmazonHelp It’s not that. But that skill is probably not available in the India Alexa marketplace.
- id=128133 conv=128131 p=0.39 :: @AmazonHelp Haha I remember when I first got my Alexa in 2015 (I think the year it came out?) and wa

### Cluster 69
- id=1009194 conv=1009195 p=0.80 :: @AmazonHelp I’ve change it to Echo see how i get on...
- id=551984 conv=551985 p=1.00 :: @AmazonHelp Thanks for the response! Correct, I'm in a small room with one Echo device, I make a req
- id=1582918 conv=1582919 p=1.00 :: @AmazonHelp Wird auf der Echo Produktseite als 3 und 2 pack angeboten https://t.co/7M13TXJwgp
- id=238005 conv=238008 p=0.70 :: @AmazonHelp Was actually talking about in the promo for the new Echo, 👨🏻 played music in the 👦🏻's ro
- id=2226387 conv=2226389 p=1.00 :: @AmazonHelp Thanks for your reply. Do you know why I so often see them paired w/ the Echo Dot in Dai
- id=1426697 conv=1426698 p=1.00 :: @AmazonHelp Yes, I'm aware of that, and that was the case with the first generation echo, but it's n
- id=551987 conv=551985 p=1.00 :: @AmazonHelp Same wake word. But according to that article, ESP makes it so Echo intelligently knows 
- id=1892089 conv=1892090 p=1.00 :: @AmazonHelp Thanks, can I just ask does the new Echo need to be plugged in constantly for it to work

### Cluster 70
- id=43689 conv=5159 p=0.70 :: @AmazonHelp @115851 I bet you won’t like to take any interest on this.......
- id=2513681 conv=2513682 p=0.68 :: @AmazonHelp @716307 Ja hat geklappt.
- id=1066692 conv=1066696 p=0.64 :: @AmazonHelp Muy serios los de @137605 . Muy serios.
- id=48890 conv=48907 p=0.57 :: @AmazonHelp @126908 machst du mein frau an oder was @126910
- id=2033208 conv=2033196 p=0.70 :: @AmazonHelp @601204 This doesn't explain the Capri Sun 😂
- id=123383 conv=123388 p=0.62 :: @AmazonHelp @143566 Quem está no período experimental do kindle unlimited pode assinar por 1,99??? N
- id=1424173 conv=1424174 p=0.68 :: @AmazonHelp @450930 Warum nur muss ich jetzt an QualityLand von @59713 denken?
- id=528217 conv=528222 p=0.64 :: @AmazonHelp @242290 Really !!!???

### Cluster 71
- id=429070 conv=429066 p=0.99 :: @AmazonHelp N° DE COMMANDE 403-4401776-1509903 car y a pas de numero de suvi
- id=787618 conv=787609 p=1.00 :: @AmazonHelp 5180700103714
- id=1557680 conv=1557690 p=0.60 :: @AmazonHelp Oui c’est le: C10044824983
- id=2011928 conv=2011930 p=1.00 :: @AmazonHelp 407-3669141-2543566
- id=993210 conv=993213 p=1.00 :: @AmazonHelp You already know the issue. #404-4139617-3649915.
- id=2528796 conv=2528792 p=0.68 :: @AmazonHelp Odr no is 405-8007011-8476306
- id=313453 conv=313455 p=1.00 :: @AmazonHelp 795001, Imphal
- id=944148 conv=944144 p=1.00 :: @AmazonHelp 701-7531331-2821029 and last weekend 701-0207309-2537026. There’s more but let’s start w

### Cluster 72
- id=1292018 conv=1292019 p=1.00 :: @AmazonHelp Okay, thanks – I'll try that.
- id=637035 conv=637053 p=1.00 :: @AmazonHelp Ok. Will try this. Thanks
- id=2690672 conv=2690679 p=1.00 :: @AmazonHelp Ok. Well… I’ll keep on trying. Thanks.
- id=977906 conv=977907 p=0.81 :: @AmazonHelp Wird ausprobiert, danke!
- id=473257 conv=473266 p=0.89 :: @AmazonHelp Ok. I will try again. Thanks
- id=1137859 conv=884873 p=1.00 :: @AmazonHelp Sure will try it..get back to you..thank you
- id=2668957 conv=2668958 p=1.00 :: @AmazonHelp will try it. Thanks
- id=2847309 conv=2847310 p=1.00 :: @AmazonHelp Ok I'm going to try ot. Thanks

### Cluster 73
- id=1936551 conv=1936552 p=1.00 :: @AmazonHelp I have replied on that many times
- id=1223000 conv=1223037 p=0.97 :: @AmazonHelp I have replied at least a dozen times... You asking me tovreply will not change ny claim
- id=69910 conv=69933 p=1.00 :: @AmazonHelp I’ve sent in the reply.
- id=319414 conv=319453 p=1.00 :: @AmazonHelp Which one I m confused. Haven’t you seen the chain of replies I have received today. Pls
- id=1141903 conv=1141890 p=1.00 :: @AmazonHelp Same reply I am hearing from last 15 days.
- id=2154068 conv=2154083 p=0.98 :: @AmazonHelp I have replied and given details
- id=206089 conv=206090 p=1.00 :: @AmazonHelp I have replied on the form.
- id=30513 conv=30544 p=1.00 :: @AmazonHelp I have replied as well

### Cluster 74
- id=1325666 conv=1325664 p=1.00 :: @AmazonHelp I have updated in the 'delovery feedback' section. Kindly act on it.
- id=558490 conv=558493 p=1.00 :: @AmazonHelp Yep, just submitted feedback.
- id=1305192 conv=1305193 p=1.00 :: @AmazonHelp I submitted a report through the link to help you guys with gathering feedback. ^_^ Than
- id=739100 conv=739101 p=1.00 :: @AmazonHelp Have informed you through rating &amp; comments section.
- id=1730795 conv=1730796 p=1.00 :: @AmazonHelp Wie soll dieses Feedback was nützen, ohne jegliche Info wo euer Angebot noch ausbaufähig
- id=1536937 conv=1536934 p=1.00 :: @AmazonHelp Any feedback?
- id=1173862 conv=1173863 p=1.00 :: @AmazonHelp Thanks have left feedback
- id=409331 conv=409310 p=1.00 :: @AmazonHelp We will see, I gave feedback personally to your colleague, next time we'll see what happ

### Cluster 75
- id=334026 conv=334031 p=1.00 :: @AmazonHelp So still no response.
- id=440373 conv=440386 p=1.00 :: @AmazonHelp yes but did not get any reply
- id=1110243 conv=1110247 p=1.00 :: @AmazonHelp yes i did no response yet
- id=69838 conv=69841 p=1.00 :: @AmazonHelp Hi there, still no response from anyone!
- id=844069 conv=844080 p=0.91 :: @AmazonHelp Hello, I still don't have a response? What is happening?
- id=1232085 conv=1232086 p=1.00 :: @AmazonHelp Still no reply no food
- id=69900 conv=69933 p=0.92 :: @AmazonHelp I haven’t got any reply yet!
- id=2289939 conv=2289940 p=0.77 :: @AmazonHelp Filled and replied yesterday but no response till 1921hrs.

### Cluster 76
- id=580677 conv=580680 p=1.00 :: @AmazonHelp OK thanks for getting back so quick :)
- id=1026037 conv=1026038 p=1.00 :: @AmazonHelp Thank you for getting back with me!! Going to the link now :)
- id=2767591 conv=2767585 p=1.00 :: @AmazonHelp Merci beaucoup. Je me suis occupé du retour par point relais à l'instant 😊
- id=468892 conv=468893 p=1.00 :: @AmazonHelp It came back! Bestill my heart. Thank you for responding so quickly. Phew! 😁
- id=1355377 conv=1355375 p=1.00 :: @AmazonHelp Ok thanks for getting back to.
- id=281637 conv=281638 p=1.00 :: @AmazonHelp Hi thx for coming back...Not sure? How do I check that out please?
- id=1100572 conv=1100573 p=1.00 :: @AmazonHelp Thank you for having my back
- id=1398440 conv=1398441 p=1.00 :: @AmazonHelp I take it all back - its here!! Thanks @115830

### Cluster 77
- id=286822 conv=286823 p=1.00 :: @AmazonHelp yep tried that. battery is down to 25% after less than a week with no usage. already tri
- id=270916 conv=270917 p=1.00 :: @AmazonHelp Without charger, battery doesn’t work, without battery, 4wheeler doesn’t work. If 4wheel
- id=21904 conv=21905 p=1.00 :: @AmazonHelp 1. Does it work without being plugged in to power? 2. If yes, what is battery life? 3. C
- id=1593386 conv=1593388 p=1.00 :: @AmazonHelp Not a battery operated fan but u say ppl bought those items together? #notRight #why htt
- id=21909 conv=21905 p=1.00 :: @AmazonHelp Your customer support told me it has battery!
- id=43264 conv=43265 p=1.00 :: @AmazonHelp I'm currently speaking with duracell as I think they are counterfeit batteries personall
- id=231468 conv=231469 p=1.00 :: @AmazonHelp 9V batteries are used in smoke detectors. That's where I used 1.
- id=1577274 conv=1577275 p=1.00 :: @AmazonHelp So basically my Samsung battery would've exploded on my face if I hadn't checked and I b

### Cluster 78
- id=2171058 conv=2171073 p=0.66 :: @AmazonHelp Replied already two times
- id=347912 conv=347913 p=0.68 :: @AmazonHelp Yes have done that twice
- id=2852136 conv=2852134 p=0.64 :: @AmazonHelp Have done that twice! No change
- id=2918159 conv=2918160 p=0.64 :: @AmazonHelp Twice now
- id=2596389 conv=2596397 p=0.70 :: @AmazonHelp Done twice
- id=2756040 conv=2756038 p=0.50 :: @AmazonHelp Thank you. If one looks close enough there are multiple such instances.
- id=138953 conv=138954 p=0.62 :: @AmazonHelp have done what u said just now 30-40 times.
- id=1403249 conv=1403250 p=0.62 :: @AmazonHelp Yes. Multiple times. Can you investigate the issue?

### Cluster 79
- id=745078 conv=745080 p=1.00 :: @AmazonHelp @115850 I hv done so much effort u do the same now some.Resolve it.no apologies no comp 
- id=2537495 conv=2537496 p=1.00 :: @AmazonHelp Usless reply No proper help U all just waste our time
- id=22578 conv=22579 p=1.00 :: @AmazonHelp U only email me that we vl solve ur problem but still it's not.. u r only wasting time
- id=1860352 conv=1856099 p=1.00 :: @AmazonHelp Becoz if once we leave the town then there is no point of u solving the query
- id=2317899 conv=2317883 p=1.00 :: @AmazonHelp Stop appreciate now u will never dplve my problem
- id=787167 conv=787158 p=1.00 :: @AmazonHelp We have already done this. Which part r u not understanding. We are getting standard ans
- id=787160 conv=787158 p=1.00 :: @AmazonHelp Pls note there is note there is no intimation from ur end also. What are werl supposed t
- id=440262 conv=440270 p=1.00 :: @AmazonHelp Already done, no response. Seema u ppl r busy looting other pupil

### Cluster 80
- id=583501 conv=463341 p=1.00 :: @AmazonHelp What about Samsung galaxy note 8
- id=583475 conv=463341 p=1.00 :: @AmazonHelp Nothing about Samsung galaxy note 8
- id=1698698 conv=1698699 p=1.00 :: @AmazonHelp Trying to order screen protector 4 my new Samsung Galaxy S8 &amp; I'm finding what I rec
- id=454588 conv=454589 p=1.00 :: @AmazonHelp I'm currently using a Samsung Galaxy S8
- id=2151934 conv=2151936 p=1.00 :: @AmazonHelp Samsung galaxy s7
- id=365225 conv=365220 p=1.00 :: @AmazonHelp Same was told to me 14 days before and am still waiting .. Samsung is worst
- id=447232 conv=447240 p=1.00 :: @AmazonHelp Ok, donc je chercherais du côté de chez Samsung la garantie, merci !
- id=297406 conv=297408 p=1.00 :: @AmazonHelp Samsung S8 64GB SIM-Free Smartphone - Midnight Black (SM-G950F) https://t.co/hmreD5QInj

### Cluster 81
- id=836507 conv=836508 p=1.00 :: @AmazonHelp Thanks! Punjabi movie industry has been doing really good work recently and having them 
- id=2269084 conv=2269087 p=1.00 :: @AmazonHelp @119624 Do upload punjabi movies also,
- id=812121 conv=698788 p=1.00 :: @AmazonHelp When Arjun reddy movie will be available in Europe region ? I can see few telugu movies 
- id=840890 conv=698788 p=1.00 :: @AmazonHelp Thanks.GRADE is popular film, people might take amazon prime membership to watch that fi
- id=816934 conv=816930 p=1.00 :: @AmazonHelp @115821 prime refund me full subscription fee😡 @115850 @AmazonHelp why the hell u don't 
- id=678323 conv=678324 p=1.00 :: @AmazonHelp It’s a Tollywood movie ( Telugu film industry, India) https://t.co/4uMCrsympz
- id=238108 conv=238149 p=1.00 :: @AmazonHelp Thank you. Please add Hindi movie Lootera on Prime.
- id=2387900 conv=2387903 p=1.00 :: @AmazonHelp @688073 Why there is no Malayalam movies in Prime. Kindly add it..there are more good mo

### Cluster 82
- id=238117 conv=238149 p=1.00 :: @AmazonHelp Please add Subtitles to Downton Abbet
- id=238106 conv=238149 p=1.00 :: @AmazonHelp Please add This is Us Season 2. Add subtitles to Downton Abbey.
- id=802344 conv=802342 p=1.00 :: @AmazonHelp Ok. So there are subtitles for this season, right?
- id=1891482 conv=1891483 p=1.00 :: @AmazonHelp https://t.co/HFUQIX5xYw eng subtitles become unavailable after episode 20
- id=238089 conv=238149 p=1.00 :: @AmazonHelp Subtitles aren't working again
- id=238098 conv=238149 p=1.00 :: @AmazonHelp I've turned on the subtitle option to English. It comes Subtitles are not available for 
- id=282164 conv=282165 p=1.00 :: @AmazonHelp did you get the list? When the English subtitles will be available for these anime title
- id=1579655 conv=1579656 p=1.00 :: @AmazonHelp Yeah I know about putting subtitles on. Not many films or tv shows have them

### Cluster 83
- id=352758 conv=352759 p=1.00 :: @AmazonHelp Sirve para algo? La última vez se limitaron a pedir disculpas y no hacer nada más
- id=1042211 conv=1042200 p=1.00 :: @AmazonHelp I have the rights to know, I'm the one who has suffered. Don't try to deceive me.
- id=333587 conv=333585 p=1.00 :: @AmazonHelp This situation is Shared Previously also and by your side not taking any action. Just ma
- id=1699053 conv=1699055 p=1.00 :: @AmazonHelp I did that an the explanations are always so poor. I just give up. You guys apologize bu
- id=1566752 conv=1566754 p=1.00 :: @AmazonHelp Comment le saurais je ? Je suis très en colère, je n’accepte pas cela et vos excuses ne 
- id=972770 conv=972754 p=0.98 :: @AmazonHelp Simply you people can say sorry. I can't share you how much damage happend to me in this
- id=982343 conv=982344 p=0.91 :: @AmazonHelp At least understand the issue you idiot, copycat. Its your mistake, not mine... what are
- id=1993262 conv=1993263 p=1.00 :: @AmazonHelp I was wrong, and I apologize

### Cluster 84
- id=1509859 conv=1509863 p=1.00 :: @AmazonHelp Hello? Is this not just blatant false advertising?
- id=278672 conv=278669 p=1.00 :: @AmazonHelp Complete loss of words as received email saying the issue has been addressed to!!! Basel
- id=1780041 conv=1780043 p=1.00 :: @AmazonHelp Because of false advertisement
- id=277116 conv=277105 p=1.00 :: @AmazonHelp Advertising.
- id=234209 conv=234220 p=1.00 :: @AmazonHelp false advertising. i had sent screen shots and information earlier
- id=2917155 conv=2917158 p=1.00 :: @AmazonHelp It is not the carriers fault, it is a labeling issue with your website...it is called fa
- id=1421911 conv=1421913 p=1.00 :: @AmazonHelp on 2 Nov ads are being run to join a prog that ended on 31st Oct ? Truly 'amazing'
- id=1092357 conv=1092349 p=1.00 :: @AmazonHelp @377765 Why are you advertising in breitbart? https://t.co/MV2QOjT9BA

### Cluster 85
- id=2663758 conv=2663755 p=0.83 :: @AmazonHelp Done ✅ 3:04a 10/30/17
- id=1041674 conv=1041676 p=1.00 :: @AmazonHelp done. Thanks.
- id=233503 conv=233505 p=1.00 :: @AmazonHelp Done... thanks
- id=419621 conv=419627 p=1.00 :: @AmazonHelp Done. Hopefully now I can get some answers
- id=20032 conv=20034 p=1.00 :: @AmazonHelp Thank u.......done
- id=422754 conv=422755 p=0.86 :: @AmazonHelp Thankyou , it's done!😍
- id=1727216 conv=1727218 p=0.86 :: @AmazonHelp It’s done. Thank you
- id=499892 conv=499893 p=1.00 :: @AmazonHelp Done 😀 thanks x

### Cluster 86
- id=2055060 conv=2055058 p=1.00 :: @AmazonHelp I never received one.
- id=2460808 conv=2460809 p=1.00 :: @AmazonHelp Didn't receive any!
- id=1293016 conv=1293022 p=1.00 :: @AmazonHelp I’ve said, nothing has been received!
- id=783427 conv=783429 p=1.00 :: @AmazonHelp I received none of them
- id=2819168 conv=2819161 p=1.00 :: @AmazonHelp i have not received anything dont you understand that , we are done here , nothing neede
- id=980035 conv=980029 p=1.00 :: @AmazonHelp Nothing received as of now
- id=2153009 conv=2153010 p=1.00 :: @AmazonHelp I did not receive one.
- id=1313010 conv=1281375 p=1.00 :: @AmazonHelp Not received.

### Cluster 87
- id=2536455 conv=2536453 p=1.00 :: @AmazonHelp Done already
- id=1370134 conv=1370135 p=1.00 :: @AmazonHelp I already was done
- id=1740737 conv=1740735 p=1.00 :: @AmazonHelp 4X already
- id=418776 conv=418777 p=1.00 :: @AmazonHelp Already handled lol
- id=2278931 conv=2278929 p=1.00 :: @AmazonHelp Yes already done
- id=1223032 conv=1223037 p=1.00 :: @AmazonHelp Already done once
- id=1872070 conv=1872071 p=0.96 :: @AmazonHelp already done this
- id=1424887 conv=26979 p=0.71 :: @AmazonHelp already done now need result

### Cluster 88
- id=322598 conv=322599 p=1.00 :: @AmazonHelp No solution to the problem yet. Not satisfied at all
- id=1085067 conv=1085076 p=1.00 :: @AmazonHelp Still problem is not solved
- id=1129348 conv=1129346 p=1.00 :: @AmazonHelp No and my problem remains unsolved
- id=1081770 conv=1081780 p=1.00 :: @AmazonHelp Problem is STILL unresolved.
- id=979620 conv=979609 p=1.00 :: @AmazonHelp Yes but problem has not been solved yet more than 48 bs hrs But no solution
- id=857753 conv=851605 p=1.00 :: @AmazonHelp still Ishu is not solved
- id=422231 conv=422234 p=1.00 :: @AmazonHelp Done but still no solution?
- id=567584 conv=567587 p=1.00 :: @AmazonHelp Not fully resolved, no.

### Cluster 89
- id=1049142 conv=1049143 p=0.63 :: @AmazonHelp my issue was solved. thanks guys
- id=2083450 conv=2083441 p=0.59 :: @AmazonHelp Thanku. Problem got addressed yest.
- id=19194 conv=19195 p=0.82 :: @AmazonHelp thnx, matter resolved.
- id=1645634 conv=1645617 p=0.65 :: @AmazonHelp Espero se resuelva el problema. Gracias
- id=444289 conv=444292 p=0.60 :: @AmazonHelp Thank you for the reply. Hope I will find solution.
- id=1243812 conv=1243808 p=0.66 :: @AmazonHelp The issue has been solved thank you
- id=1489144 conv=1489145 p=0.86 :: @AmazonHelp Thank you, hopefully problem now resolved.
- id=2473474 conv=2473477 p=0.47 :: @AmazonHelp Issue was resolved!!!!! 😭 thank you!!!! Been a pretty stressful morning and the girl who

### Cluster 90
- id=2915882 conv=2915870 p=1.00 :: @AmazonHelp Would you be satisfied with this purchase .. a laptop that breaks only 5 months after be
- id=65833 conv=65834 p=1.00 :: @AmazonHelp Hi PJ. I ordered a laptop from a 3rd party seller. They sent the right kind of laptop bu
- id=1091292 conv=1091293 p=1.00 :: @AmazonHelp Honey my 300 year old laptop wont let me look at it it goes black just give me the link 
- id=2469375 conv=2469377 p=1.00 :: @AmazonHelp Attached hereby the invoice screen shot, battery pic etc.. @1469 laptop not working that
- id=2915873 conv=2915870 p=1.00 :: @AmazonHelp I need my laptop to work and I would have one for a while since @115821 is keeping my mo
- id=2915888 conv=2915870 p=1.00 :: @AmazonHelp A laptop is not supposed to stop working 5 months after you sold it to me. It is obvious
- id=2241036 conv=2241038 p=1.00 :: @AmazonHelp The laptop should be mailed to me and your systems issues should be investigated and res
- id=163527 conv=163537 p=1.00 :: @AmazonHelp Laptop arrived. Defective. Top of the range @153825 laptop that I've saved and waited fo

### Cluster 91
- id=312098 conv=227095 p=1.00 :: @AmazonHelp Yes, i have already done that.
- id=1428267 conv=1428272 p=1.00 :: @AmazonHelp Ive been doing this
- id=2236311 conv=2236313 p=1.00 :: @AmazonHelp I already did this
- id=1300544 conv=1299401 p=1.00 :: @AmazonHelp I already compliant
- id=2459203 conv=2459196 p=0.77 :: @AmazonHelp I've already done it with photographs of product
- id=2298476 conv=2298485 p=1.00 :: @AmazonHelp yes I have recieved it
- id=347785 conv=347781 p=1.00 :: @AmazonHelp I have done this
- id=256640 conv=256641 p=1.00 :: @AmazonHelp I have done it 👍🏻

### Cluster 92
- id=75888 conv=75894 p=1.00 :: @AmazonHelp Yes i did
- id=1955350 conv=1955344 p=1.00 :: @AmazonHelp I did. It's SUER.
- id=1805081 conv=1805082 p=1.00 :: @AmazonHelp Just did.......
- id=487781 conv=487782 p=1.00 :: @AmazonHelp Yes I did, and it’s still doing it
- id=470819 conv=470824 p=0.98 :: @AmazonHelp Yes, I wrote back.
- id=2840169 conv=2840167 p=1.00 :: @AmazonHelp Yes, I did. I even rebooted.
- id=1267609 conv=1267607 p=0.76 :: @AmazonHelp I did. thanks.
- id=2308928 conv=2308924 p=0.89 :: @AmazonHelp Just did, returning and refunding right now

### Cluster 93
- id=1830683 conv=1830681 p=1.00 :: @AmazonHelp yes, i have
- id=1626620 conv=1626326 p=1.00 :: @AmazonHelp yes. I have raised.
- id=29500 conv=29510 p=1.00 :: @AmazonHelp Of course I have!
- id=665389 conv=665401 p=1.00 :: @AmazonHelp I have yes. No email anywhere
- id=562896 conv=562899 p=0.95 :: @AmazonHelp Yes I have! Thx. Still late.
- id=2585553 conv=2585554 p=1.00 :: @AmazonHelp Yes I have.
- id=1661490 conv=1661482 p=1.00 :: @AmazonHelp I have indeed.
- id=641652 conv=641653 p=1.00 :: @AmazonHelp Yes I have

### Cluster 94
- id=522433 conv=522478 p=0.98 :: @AmazonHelp i have a fire tv stick. how do i turn it off when im not using it? also so i dont use th
- id=402238 conv=402239 p=1.00 :: @AmazonHelp Probiere ich gerne nochmal aus. Da es jedoch auf dem FireTV Stick funktioniert schließe 
- id=709464 conv=709465 p=0.94 :: @AmazonHelp I'm unable to control the volume while using the FireStick, it affects normal TV functio
- id=2914467 conv=2913185 p=1.00 :: @AmazonHelp Por cierto...el modo "MIRACAST" para enviar la pantalla del móvil/tablet/ordenador a la 
- id=183719 conv=183721 p=0.94 :: @AmazonHelp N some of the videos keep freezing I have reset fire stick many times but that issue nev
- id=522447 conv=522478 p=1.00 :: @AmazonHelp how do i add storage to the fire tv stick 'stick' version?
- id=1223290 conv=1223291 p=1.00 :: @AmazonHelp Hi - Yes, sure have. We've tried all the tricks: power down, reinstall, delete cache, sp
- id=830160 conv=830161 p=1.00 :: @AmazonHelp Firestick and yes, an error message.

### Cluster 95
- id=954290 conv=924533 p=1.00 :: @AmazonHelp NOT HELPFUL
- id=205939 conv=205973 p=1.00 :: @AmazonHelp appreciated, but doesn't really help.
- id=183601 conv=180315 p=1.00 :: @AmazonHelp But that is not helpful
- id=2956994 conv=2957000 p=1.00 :: @AmazonHelp Again, not helpful
- id=2929603 conv=2885731 p=1.00 :: @AmazonHelp Ça ne m'aide pas vraiment
- id=1156744 conv=1156745 p=1.00 :: @AmazonHelp That does not help.
- id=1023619 conv=1023620 p=1.00 :: @AmazonHelp Thanks for your prompt response but it certainly did not help
- id=332022 conv=332010 p=1.00 :: @AmazonHelp This is not helping.

### Cluster 96
- id=103848 conv=103855 p=1.00 :: @AmazonHelp C'est étrange car au début c'est écrit : "Nous sommes ravis de vous rappeler que vous bé
- id=276491 conv=276492 p=1.00 :: @AmazonHelp Thanks for your prompt response. Hope @116329 would be helpful as U did. @117128 Please 
- id=2595439 conv=2595440 p=1.00 :: @AmazonHelp Es el primero. No sabía que tenía acceso a Prime Video por tener Amazon Prime. Muy buena
- id=676110 conv=676108 p=1.00 :: @AmazonHelp It says Amazon video is only available for customers in the uk?
- id=812122 conv=698788 p=0.97 :: @AmazonHelp @313519 When do we get this for USA audience? Are you planning to release in Amazon USA 
- id=825509 conv=825510 p=1.00 :: @AmazonHelp Yes. At least the ones that were applicable. Amazon video streaming fine otherwise. Just
- id=158791 conv=158793 p=1.00 :: @AmazonHelp It is the Amazon video app built into the TV.
- id=1143545 conv=1143541 p=1.00 :: @AmazonHelp I don't believe its a device or account issue. Happy to be proven wrong. Amazon can sure

### Cluster 97
- id=111868 conv=111869 p=1.00 :: @AmazonHelp Says non compatible
- id=238133 conv=238149 p=1.00 :: @AmazonHelp Ain't working
- id=133595 conv=133593 p=1.00 :: @AmazonHelp Yes it still doesnt work
- id=2298800 conv=2298798 p=1.00 :: @AmazonHelp Still doesn’t work
- id=486649 conv=486656 p=1.00 :: @AmazonHelp Leider funktioniert das auch nicht
- id=2335065 conv=2335066 p=1.00 :: @AmazonHelp Does not work.
- id=1637202 conv=1637200 p=1.00 :: @AmazonHelp Yea, didn't work good at all because it does not search for what you asked it to...
- id=2624130 conv=2624132 p=1.00 :: @AmazonHelp That didn’t work...please advise

### Cluster 98
- id=158683 conv=158681 p=1.00 :: @AmazonHelp Would put error when try too
- id=1447166 conv=1447162 p=1.00 :: @AmazonHelp i tried that long back. it rung but no one picked up
- id=1070058 conv=1070055 p=1.00 :: @AmazonHelp I tried but it did not work.
- id=1418568 conv=1418569 p=1.00 :: @AmazonHelp Yes and I’ve tried that! Nothing is working
- id=2452524 conv=2452525 p=1.00 :: @AmazonHelp Just tried that. Still not working.
- id=1757982 conv=1757983 p=1.00 :: @AmazonHelp yeah I've tried that. Still not working :(
- id=412302 conv=412303 p=1.00 :: @AmazonHelp I've tried all of the above already. Still doesn't work.
- id=2177986 conv=2177990 p=1.00 :: @AmazonHelp Thanks! Tried that and didn't work..

### Cluster 99
- id=111782 conv=111783 p=1.00 :: @AmazonHelp Seems kinda pointless seen as Netflix is working fine and dandy on my laptop... 🙄
- id=2303338 conv=2303339 p=1.00 :: @AmazonHelp Thanks. I’ll stick with just Netflix then. The current compatibility is subpar to be hon
- id=162007 conv=162008 p=1.00 :: @AmazonHelp And when I click on the Netflix app... https://t.co/MM3JmpHBgS
- id=2575232 conv=2575235 p=1.00 :: @AmazonHelp The link recommends updating device’s firmware. That’s exactly when this issue has start
- id=2332361 conv=2332362 p=1.00 :: @AmazonHelp Sure, when I Click the Netflix app, it freezes and nothing happens. I live in Mexico BTW
- id=1096778 conv=1096779 p=1.00 :: @AmazonHelp Netflix is working just fine, but our movie is on Amazon!
- id=1434018 conv=1434019 p=1.00 :: @AmazonHelp I did not see a list of apps on that link or any child link. Netflix, I am asking if I c
- id=2679496 conv=2679501 p=1.00 :: @AmazonHelp Als hätte ich dies in den vergangen 2 Wochen nicht schon ständig gemacht!! Bringt nix! A

### Cluster 100
- id=505748 conv=505749 p=1.00 :: @AmazonHelp None of those solutions worked, unfortunately. And now none of the Prime movies have vid
- id=2031125 conv=2031123 p=1.00 :: @AmazonHelp It's fine. I fixed it by removing prime. It messes with the video subscription.
- id=1844488 conv=1844489 p=0.93 :: @AmazonHelp ¿Pero debo de pagar por utilizar el servicio de prime video?
- id=354022 conv=354023 p=1.00 :: @AmazonHelp I tried.. couldn’t. When I log into Kindle it changes Prime Video’s login and vice versa
- id=2314524 conv=2314525 p=0.90 :: @AmazonHelp This did not work, all my other videos in Prime and on Fire Stick appear perfectly. Can 
- id=69269 conv=69267 p=0.86 :: @AmazonHelp no, it's the main US version, and I'm accessing prime video on my Roku
- id=868650 conv=868646 p=1.00 :: @AmazonHelp Thanks. Would also like some tweaks in your search engine. That's the only issue I have 
- id=1766847 conv=1766855 p=1.00 :: @AmazonHelp Do you have a different method for me to watch my prime video?

### Cluster 101
- id=1223090 conv=1223092 p=0.98 :: @AmazonHelp It’s all sorted now - thanks!! I think my internet connection was wonky. Turned iPad to 
- id=2698909 conv=2698911 p=0.93 :: @AmazonHelp I'm on my iPad--better to switch to a PC?
- id=2496339 conv=2496340 p=1.00 :: @AmazonHelp My iPhone. I always use it? Not sure why its suddenly saying that
- id=2153019 conv=2153020 p=1.00 :: @AmazonHelp I'm on my iPad.
- id=1529902 conv=1529906 p=0.82 :: @AmazonHelp It is a mini iPad 3rd generation
- id=1159327 conv=1159333 p=1.00 :: @AmazonHelp On both my IPad and my IPhone 6
- id=519749 conv=519751 p=1.00 :: @AmazonHelp iOS. It worked a couple of weeks ago.
- id=2565547 conv=2565552 p=1.00 :: @AmazonHelp Thanks! I’m on my iPhone right now but can switch to a laptop or iPad if need be.

### Cluster 102
- id=1031076 conv=1031077 p=1.00 :: @AmazonHelp There are no options in the app itself that I’ve seen.
- id=423231 conv=423232 p=1.00 :: @AmazonHelp Hab ich versucht, das ist es ja - ist über die App grad irgendwie nicht möglich. Springt
- id=562861 conv=562863 p=1.00 :: @AmazonHelp I downloaded the app and it won't open
- id=1675303 conv=1675307 p=0.98 :: @AmazonHelp I'm still having the same problem after I agree with the app details it keeps send me th
- id=1641400 conv=1641398 p=0.92 :: @AmazonHelp I figured out how to fix the problem using the app and the rep still didn't understand t
- id=1229688 conv=1159333 p=0.99 :: @AmazonHelp And text screwed up AGAIN… never know when I open the kindle app if THIS will be the tim
- id=575928 conv=575926 p=0.99 :: @AmazonHelp I can’t get through more than a couple clicks before the app becomes unresponsive and cl
- id=1428956 conv=1428957 p=1.00 :: @AmazonHelp Got a mail to download the app from the browser but I am getting no such prompt

### Cluster 103
- id=1157231 conv=1157232 p=0.99 :: @AmazonHelp I've tried everything. Factory reset etc. It's completely random, drops signal at any ti
- id=2529294 conv=2529295 p=1.00 :: @AmazonHelp I turned that off... the navigational support off.. everything off... restarted it and i
- id=2662725 conv=2662726 p=0.89 :: @AmazonHelp I guess maybe my internet was bugging out for a bit. It's working now!
- id=2107252 conv=2107264 p=1.00 :: @AmazonHelp No, it hasn't been dispatched. I tried that and it just keeps going back to the home scr
- id=317479 conv=317480 p=1.00 :: @AmazonHelp No..I've followed all instruction...router off etc... still stuck in reboot cycle
- id=2451649 conv=2451650 p=0.90 :: @AmazonHelp Every time we use it recently we have to reset it at least once or twice because it free
- id=2401460 conv=2401457 p=1.00 :: @AmazonHelp It has issues like heating up fast , fingerprint sensor, getting restart by it self
- id=2570098 conv=2570099 p=1.00 :: @AmazonHelp it just keeps restarting constantly

### Cluster 104
- id=382574 conv=382579 p=1.00 :: @AmazonHelp Your latest solution is to buy another TV? What so that @116324 can delay it again and I
- id=191524 conv=191531 p=1.00 :: @AmazonHelp I did. And I did fill it out but that doesn’t help me get my tv. And not the funds are i
- id=56900 conv=56898 p=1.00 :: @AmazonHelp Just had even more damaged replacement TV delivered. You overpackage unbreakable items a
- id=2346293 conv=2346296 p=1.00 :: @AmazonHelp No. And it seems that the tv I tried to buy over a week ago went up in price for your ‘b
- id=740447 conv=740448 p=0.95 :: @AmazonHelp Thank you. Please save your generic cut and paste responses and try some actual customer
- id=487820 conv=487823 p=1.00 :: @AmazonHelp £40 won’t even buy us a Smart TV box to compensate!!!!!
- id=2636923 conv=2636821 p=0.88 :: @AmazonHelp Hat sich erledigt. TV 1 Jahr zu früh gekauft.
- id=107330 conv=107328 p=1.00 :: @AmazonHelp Now a week late. Two missing TV’s, still no replacement and you have offered us a £5 vou

### Cluster 105
- id=473316 conv=473331 p=0.99 :: @AmazonHelp Dexter, jamais vu... Ca fait parti des "vieilles" séries que je dois voir avec House. Pa
- id=99802 conv=99804 p=0.85 :: @AmazonHelp Fast alle der ersten Staffel, soweit ich gesehen habe. Aber nicht dauerhaft. Kann jetzt 
- id=789052 conv=789060 p=0.72 :: @AmazonHelp @308159 Ich denke hier ist der Unterschied zwischen OV &amp; dt. Denn bei OV ist bei mir
- id=1616062 conv=1616060 p=0.79 :: @AmazonHelp Retomar series de hace años imposibles de encontrar en otro lugar: Sabrina y por supuest
- id=1178059 conv=1178064 p=0.83 :: @AmazonHelp Ab wann ist es denn in Deutsch verfügbar, aktuell gibt es die 3. Staffel nur in OV.
- id=2928928 conv=2928929 p=1.00 :: @AmazonHelp I watched 4 episodes and realized it was too good to finish all at once.
- id=789278 conv=789287 p=0.69 :: @AmazonHelp Oh I see. So do I have chance if I watch 5 new titles again?
- id=2298720 conv=2298721 p=1.00 :: @AmazonHelp But I took the membership primarily to watch @15710 . Request you to please the more epi

### Cluster 106
- id=2241065 conv=2241066 p=1.00 :: @AmazonHelp I selected the correct address but you d sent it to the wring one
- id=413993 conv=413991 p=1.00 :: @AmazonHelp Already arrived at the incorrect address.
- id=444395 conv=444396 p=1.00 :: @AmazonHelp Cuando introduje la dirección de envío la página se congeló, y en los detalles del pedid
- id=445448 conv=445446 p=1.00 :: @AmazonHelp Its going to my work address and im not going to be there for a bit. Thats why i asked t
- id=2475933 conv=2475936 p=1.00 :: @AmazonHelp And after 11 years it seems you have randomly decided our home address is a “commercial 
- id=877637 conv=877639 p=0.99 :: @AmazonHelp Oui et la 2e a était envoyer dans une poste et non a l'adresse indiqué ( j'ai mis 0 poin
- id=2475932 conv=2475936 p=1.00 :: @AmazonHelp So, your adviser tells me she’s deleted my address, I need to re-register it and “select
- id=1314574 conv=1314583 p=1.00 :: @AmazonHelp It doesn't!! Anywhere! That's the point! If it had i would have arranged alternate del. 

### Cluster 107
- id=1488817 conv=1488825 p=0.56 :: @AmazonHelp Thank you for helping 🌸✨
- id=1800789 conv=1800794 p=0.97 :: @AmazonHelp Ok. Thanks for you help. 😉
- id=198014 conv=198016 p=0.93 :: @AmazonHelp Ok, but need help regarding this.
- id=2632964 conv=2632966 p=0.78 :: @AmazonHelp Okay, thank you for your help - much appreciated.
- id=19441 conv=19444 p=0.85 :: @AmazonHelp Ok thank for helping.
- id=1005136 conv=1005134 p=0.95 :: @AmazonHelp Ok. Thank you. I appreciate the help.
- id=726955 conv=726958 p=0.65 :: @AmazonHelp D'acc! Merci de l'aide O/
- id=1724711 conv=1724712 p=1.00 :: @AmazonHelp Ok. Thank you for the help

### Cluster 108
- id=2265526 conv=2265542 p=0.46 :: @AmazonHelp Ye hi services h kya aapki
- id=786146 conv=439660 p=0.47 :: @AmazonHelp Mene participate kiya tha kuch nhi hua result bhi nhi aaya
- id=1262613 conv=1260789 p=0.51 :: @AmazonHelp Are me bewkoof nhii hu. Sab form fill ki tha aur ab bhibkia h.
- id=1266332 conv=1266330 p=0.48 :: @AmazonHelp Wah or jo mera pawo me ye chote or challe pade h uss ka kya hoga apne seller ko suspend 
- id=19452 conv=19448 p=0.51 :: @AmazonHelp Sorry sir but aap logo ne aaj ki date di thi refund krne ki.... Pr abhi tak hua nhi....
- id=1261891 conv=1260789 p=0.62 :: @AmazonHelp Le 4baar bhi kar deta hu. Agar is baar kuch solution nhii mila na toh jo note diye h unk
- id=390802 conv=390793 p=0.78 :: @AmazonHelp Detail dene par bhi koi activity nahi dikh raha.
- id=2934427 conv=2934429 p=0.69 :: @AmazonHelp aap log cashback Dena hi nai chahte ho. Agar Dena hota to kab ka de Diya hota. Agar cash

### Cluster 109
- id=2954390 conv=2954377 p=0.74 :: @AmazonHelp Porem eles entram pro governo e começa a descobrir coisas erradas e obscura é muito tris
- id=2852187 conv=2852188 p=0.97 :: @AmazonHelp Olha, mais ou menos porque eu tô tentando MUITO economizar, mas sei que minha irmã compr
- id=1669858 conv=1669859 p=0.73 :: @AmazonHelp si!!!! que es super complicado... miles de cosas que tengo que rellenar antes de publica
- id=1135884 conv=1135885 p=0.61 :: @AmazonHelp Grazie! Ma io compro prevalentemente libri e dvd 😊
- id=1405316 conv=1405313 p=1.00 :: @AmazonHelp Like the ability to lend out books to other family members?
- id=1547876 conv=1547877 p=1.00 :: @AmazonHelp Yeah. Its all good tho. I mean I kind of needed that textbook for class but shit happens
- id=126846 conv=126847 p=1.00 :: @AmazonHelp amo/sou fã mas queria um cuponzinho de desconto pra comprar uns ebooks 😉
- id=2474754 conv=2474762 p=1.00 :: @AmazonHelp En fait ils lisent de tout. Mon grand (bientôt 9 ans) lit surtout des bandes dessinées e

### Cluster 110
- id=2481440 conv=2481436 p=1.00 :: @AmazonHelp I will. Thank you
- id=2537425 conv=2537423 p=1.00 :: @AmazonHelp Ok I will. Thanks JJ
- id=2905073 conv=2905076 p=1.00 :: @AmazonHelp Thanks a bunch!! I certainly will.
- id=517602 conv=517607 p=1.00 :: @AmazonHelp i will, i appreciate it!
- id=1032339 conv=1032340 p=1.00 :: @AmazonHelp Yes i will, i have contaced you guys here before many times
- id=1457239 conv=1457243 p=1.00 :: @AmazonHelp Okay, I will. Thanks for your help.
- id=2562179 conv=2562177 p=1.00 :: @AmazonHelp I will, it’s for a birthday present tomorrow !
- id=2345643 conv=2345647 p=1.00 :: @AmazonHelp I sure will. Thanks for letting me know so quickly guys !

### Cluster 111
- id=1615516 conv=1615512 p=1.00 :: @AmazonHelp Will do 👍
- id=683066 conv=683059 p=1.00 :: @AmazonHelp Will do..
- id=1953354 conv=1953346 p=1.00 :: @AmazonHelp will do thks
- id=1691918 conv=1691924 p=1.00 :: @AmazonHelp Aim to or will do?
- id=844211 conv=844212 p=1.00 :: @AmazonHelp Will do. I’m soooo defeated !!
- id=2602881 conv=2602883 p=1.00 :: @AmazonHelp shall do
- id=2882675 conv=2882666 p=0.96 :: @AmazonHelp Will do, as there is no such a thing as a flat F in my building 🤔
- id=1247149 conv=1247150 p=1.00 :: @AmazonHelp i shall do so

### Cluster 112
- id=312140 conv=312144 p=1.00 :: @AmazonHelp Will do - thank you for the quick follow up!
- id=2695686 conv=2695687 p=1.00 :: @AmazonHelp will do ... thanks for the pointer
- id=1461517 conv=1461521 p=1.00 :: @AmazonHelp Will do, thank you!
- id=207627 conv=207625 p=1.00 :: @AmazonHelp Will do, thanks for responding
- id=1699077 conv=1699075 p=1.00 :: @AmazonHelp Shall do, thanks.
- id=436425 conv=436423 p=0.91 :: @AmazonHelp I will do. Thanks for your help
- id=1662292 conv=1661480 p=1.00 :: @AmazonHelp Will do and thanks for the prompt replies
- id=1844492 conv=1844493 p=1.00 :: @AmazonHelp Will do and thanks for your response!

### Cluster 113
- id=105249 conv=105250 p=1.00 :: @AmazonHelp Thanks, will do! Cheers
- id=288993 conv=288998 p=1.00 :: @AmazonHelp Okay will do, appreciate your assistance. Many thanks Robbie.
- id=1947055 conv=1947062 p=1.00 :: @AmazonHelp Thanks!! Will do.
- id=1408067 conv=1408068 p=1.00 :: @AmazonHelp Thanks JE, will do!
- id=1459745 conv=1459743 p=1.00 :: @AmazonHelp Thank you, will do
- id=1496033 conv=1496037 p=1.00 :: @AmazonHelp Ok thanks guys! Will do
- id=1238754 conv=1238756 p=0.90 :: @AmazonHelp Hi, thanks, I will do :)
- id=1445410 conv=1445413 p=0.93 :: @AmazonHelp Thanks a bunch, will do 😊

### Cluster 114
- id=264962 conv=264968 p=1.00 :: @AmazonHelp No, I haven't. Wish I did though.
- id=439315 conv=439335 p=1.00 :: @AmazonHelp I haven't.
- id=2283985 conv=2283983 p=1.00 :: @AmazonHelp I haven't. I am in bed with a rocking migraine.
- id=1768222 conv=1768223 p=0.83 :: @AmazonHelp no i havent
- id=197727 conv=197728 p=1.00 :: @AmazonHelp No I haven’t x
- id=317908 conv=317906 p=1.00 :: @AmazonHelp Haven't had one because I was sure I wouldn't be able to commit at the of the 30 days, s
- id=503463 conv=503464 p=1.00 :: @AmazonHelp I haven’t, no. Because, y’know, Friday night.
- id=1094273 conv=1094274 p=0.76 :: @AmazonHelp I haven’t! I’ll definitely do that. Thanks for the tip!

### Cluster 115
- id=2283879 conv=2283880 p=0.65 :: @AmazonHelp Ma evidentemente non c’è, quindi...
- id=1601858 conv=1601855 p=0.70 :: @AmazonHelp No it isnt
- id=467378 conv=467382 p=0.70 :: @AmazonHelp Nein ist es nicht
- id=1452396 conv=1452397 p=0.64 :: @AmazonHelp Yes. No joy.
- id=2560192 conv=2560196 p=0.69 :: @AmazonHelp Non pas du tout, ce n’est pas noté
- id=1186518 conv=1186520 p=0.70 :: @AmazonHelp I don't believe so. So I guess that means no.
- id=2622491 conv=2622492 p=0.65 :: @AmazonHelp Si, pero no hay nada 🤷🏻‍♀️
- id=2954315 conv=2954322 p=0.67 :: @AmazonHelp Doesn’t say

### Cluster 116
- id=2766895 conv=2766893 p=1.00 :: @AmazonHelp non pas encore
- id=1748610 conv=1748614 p=1.00 :: @AmazonHelp No not yet. Guide me oh wise ones…
- id=814893 conv=814891 p=1.00 :: @AmazonHelp Not currently
- id=2829458 conv=2829454 p=1.00 :: @AmazonHelp Pas cette fois non.
- id=83345 conv=83346 p=1.00 :: @AmazonHelp Not yet. But according to UPS info you will.
- id=318214 conv=318218 p=1.00 :: @AmazonHelp Non pas encore, mais est-ce vraiment utile ?
- id=1829420 conv=1829418 p=1.00 :: @AmazonHelp No not yet. Just estimated.
- id=1437409 conv=1437410 p=0.95 :: @AmazonHelp Not yet, will do

### Cluster 117
- id=1209471 conv=1209467 p=1.00 :: @AmazonHelp Still not committing to anything...
- id=191770 conv=191780 p=1.00 :: @AmazonHelp Still nothing
- id=2540382 conv=2540383 p=1.00 :: @AmazonHelp none as of now...thnx !
- id=2532222 conv=2532217 p=1.00 :: @AmazonHelp Still no sign
- id=1665804 conv=1665797 p=1.00 :: @AmazonHelp Still nothing yet.
- id=816978 conv=816979 p=1.00 :: @AmazonHelp still nothing... can you help please
- id=2866037 conv=2866035 p=1.00 :: @AmazonHelp still nothing... :(
- id=182609 conv=182612 p=1.00 :: @AmazonHelp Nope. Still high and dry.

### Cluster 118
- id=1556278 conv=1556279 p=1.00 :: @AmazonHelp C'est vraiment dommage...
- id=183378 conv=183379 p=1.00 :: @AmazonHelp Bummer..that's sad :(
- id=2162402 conv=2162399 p=1.00 :: @AmazonHelp This makes me sad :(
- id=142907 conv=142908 p=1.00 :: @AmazonHelp Que pena
- id=31374 conv=31375 p=1.00 :: @AmazonHelp Gah that's a real shame
- id=218893 conv=218891 p=1.00 :: @AmazonHelp That's very sad to hear...
- id=249063 conv=249064 p=1.00 :: @AmazonHelp That's really sad
- id=2410527 conv=2410528 p=1.00 :: @AmazonHelp that’s a shame:( thanks for answering

### Cluster 119
- id=2622461 conv=2622465 p=1.00 :: @AmazonHelp I did just feel I get copy and paste responses from there
- id=1131299 conv=1131318 p=1.00 :: @AmazonHelp Standard copy paste reply from u. I am getting this for 2 weeks now. Unprofessional atti
- id=1115242 conv=1115248 p=1.00 :: @AmazonHelp At least don't copy paste the same message three times! It just shows incompetence on yo
- id=778886 conv=778877 p=1.00 :: @AmazonHelp Yes, but i am getting the standard template reply from them and no use!
- id=2192387 conv=2192390 p=1.00 :: @AmazonHelp Why don’t you check if I already have instead of copy pasting generic responses blindly?
- id=2113725 conv=2113728 p=1.00 :: @AmazonHelp I am fed up of your copy paste reply the required information is already shared many tim
- id=956291 conv=956292 p=1.00 :: @AmazonHelp Copy paste Reply never serve any purpose.
- id=1315513 conv=1315514 p=1.00 :: @AmazonHelp Abraham, Manoj, Biba, Dennis - all sent me same message. Standard copy paste non-sense w

### Cluster 120
- id=347363 conv=347364 p=1.00 :: @AmazonHelp Sorry, I should have been more clear. The release date is on the page, only it is way do
- id=927823 conv=927824 p=0.97 :: @AmazonHelp Can't say it does. Considering when I pre-ordered it said the release date. https://t.co
- id=665689 conv=665692 p=0.99 :: @AmazonHelp There were 3 release dates for it. Today was another one. Might aswell cancel and try el
- id=167942 conv=167943 p=1.00 :: @AmazonHelp staying tuned since october. kuch toh karo #AurDikhao Can some higher authority comment 
- id=206838 conv=206839 p=1.00 :: @AmazonHelp No, just I note the release date on the product page suddenly changed sometime this pm
- id=2276825 conv=2276826 p=1.00 :: @AmazonHelp Except you have a release date for the standard version. The whole reason I'm paying ext
- id=757789 conv=757795 p=0.88 :: @AmazonHelp There is no option to have it delivered on release day. What should i do?
- id=1145961 conv=1145964 p=0.79 :: @AmazonHelp It's a pre-order. do I get it on release date or does it ship release date

### Cluster 121
- id=498352 conv=498358 p=0.85 :: @AmazonHelp Thanks, I'll head that way
- id=1578555 conv=1578558 p=0.74 :: @AmazonHelp Danke, mach ich!
- id=2500785 conv=2500777 p=1.00 :: @AmazonHelp Gracias por la atención. Así lo haré.
- id=814401 conv=814399 p=0.68 :: @AmazonHelp Pas de problème, je vais le faire. Merci 😊
- id=1298971 conv=1298969 p=0.83 :: @AmazonHelp ¡Enseguida lo hago! Gracias.
- id=1597020 conv=1595203 p=0.72 :: @AmazonHelp Will keep in mind next time. Thanks
- id=1996386 conv=1996387 p=1.00 :: @AmazonHelp Thanks, I’ll remember that in future
- id=888264 conv=888271 p=1.00 :: @AmazonHelp Thanks, that's very kind of you! I'll do this now.

### Cluster 122
- id=2390429 conv=2390433 p=0.91 :: @AmazonHelp Creo que vuestro dragón se comería mi unicornio.... 😫 PD: hacéis algún regalo a un recié
- id=490484 conv=490487 p=0.94 :: @AmazonHelp A dominação masculina do Bourdieu. 😊
- id=965077 conv=964970 p=1.00 :: @AmazonHelp I have already mentioned that in tum details. My como is down agai.
- id=198099 conv=198102 p=1.00 :: @AmazonHelp Mãos dadas 😊
- id=988883 conv=988881 p=1.00 :: @AmazonHelp Yaa loving it😍
- id=1806927 conv=1806928 p=1.00 :: @AmazonHelp Jajajja qué cracks!!! Nada nada. Os quiero 😍 igual
- id=1689249 conv=1689263 p=0.99 :: @AmazonHelp gosto, e não gosto pouco hahahaha 😁😌
- id=361038 conv=360636 p=1.00 :: @AmazonHelp ☹️ not even possible as a one time Goodwill gesture? Pls 🤞🏻

### Cluster 123
- id=2135775 conv=620004 p=1.00 :: @AmazonHelp Así es :(
- id=1121253 conv=1121249 p=1.00 :: @AmazonHelp So that's it!!
- id=1014757 conv=1014703 p=1.00 :: @AmazonHelp That's it
- id=1251992 conv=1251988 p=1.00 :: @AmazonHelp First come, first serve. That's it, that's all.
- id=383320 conv=383318 p=1.00 :: @AmazonHelp C'est fait !
- id=2840210 conv=2840219 p=1.00 :: @AmazonHelp Et voilà qui est fait ;)
- id=1737631 conv=1737629 p=1.00 :: @AmazonHelp Yes that's there over in talking about
- id=2508076 conv=2508079 p=1.00 :: @AmazonHelp Oui c'est fait un justificatif de domicile

### Cluster 124
- id=2162367 conv=2162368 p=1.00 :: @AmazonHelp Yes it is :)
- id=788227 conv=788228 p=1.00 :: @AmazonHelp As far as im aware, it is.
- id=1760398 conv=1760407 p=1.00 :: @AmazonHelp /. It is, yes.
- id=2499112 conv=2499113 p=1.00 :: @AmazonHelp Hope it is... Thanks for the reply though
- id=2283505 conv=2283509 p=1.00 :: @AmazonHelp Yes, they are.
- id=2719972 conv=2719973 p=1.00 :: @AmazonHelp Yes it is (£13.24)
- id=810294 conv=810295 p=1.00 :: @AmazonHelp It is, it is, it is! Thank you!!
- id=2849071 conv=2849072 p=1.00 :: @AmazonHelp Absolutely it is.

### Cluster 125
- id=2754642 conv=2754644 p=1.00 :: @AmazonHelp Na selbstverständlich.
- id=2961792 conv=2961790 p=1.00 :: @AmazonHelp Yeah correct
- id=825070 conv=825071 p=1.00 :: @AmazonHelp Yes, of course....
- id=611109 conv=611112 p=1.00 :: @AmazonHelp Yes sire
- id=430600 conv=430598 p=0.90 :: @AmazonHelp yeah sure. ^_^
- id=384810 conv=384811 p=1.00 :: @AmazonHelp Of course
- id=1439137 conv=1439140 p=1.00 :: @AmazonHelp Yes, exactly.
- id=941340 conv=941342 p=0.96 :: @AmazonHelp I'm pretty sure

### Cluster 126
- id=2104919 conv=2104907 p=0.34 :: @AmazonHelp Merci. Je dormirais beaucoup mieux ce soir. Bonne soirée à vous.😁
- id=553430 conv=553431 p=0.55 :: @AmazonHelp Tried that, thanks. Think my evening is better than yours
- id=2740617 conv=2740620 p=0.45 :: @AmazonHelp Il n'y a pas de quoi ^^ bonne soirée 😄
- id=2249765 conv=2249763 p=0.51 :: @AmazonHelp Vermutlich;) vorerst nicht, ich hoffe es kommt wenigstens bei euch an;) Schönen Abend.
- id=987781 conv=987789 p=0.31 :: @AmazonHelp WIE OFT NOCH??
- id=2573780 conv=2573774 p=0.74 :: @AmazonHelp Merci pour votre réactivité nocturne ! Bon courage :)
- id=2791910 conv=2791911 p=0.54 :: @AmazonHelp Danke für die schnelle Antwort :). Schade bestelle sowas eigentlich nur bei euch selber.
- id=5317 conv=5319 p=0.36 :: @AmazonHelp Danke für die schnelle Antwort... ja, ich werde mal nachfragen, was da schiefgelaufen se

### Cluster 127
- id=44535 conv=35857 p=0.91 :: @AmazonHelp De acuerdo, gracias!
- id=477803 conv=477807 p=0.92 :: @AmazonHelp Okey, gracias por el trato
- id=2730315 conv=2730317 p=0.91 :: @AmazonHelp Perfekt.Vielen Dank und auch nen guten Start :)
- id=1838872 conv=1838868 p=1.00 :: @AmazonHelp That's perfect, thank you
- id=1391199 conv=1391197 p=0.74 :: @AmazonHelp Yeah, no worries, thanks again. Cheers!
- id=2597932 conv=35857 p=0.72 :: @AmazonHelp Ok, Perfecto! Muchas gracias!
- id=2705738 conv=2705739 p=1.00 :: @AmazonHelp Perfect. Thank you!
- id=2241044 conv=2241038 p=0.84 :: @AmazonHelp Sigh. Thanks.

### Cluster 128
- id=1221770 conv=1221773 p=1.00 :: @AmazonHelp Ok. Thanks.
- id=2974797 conv=2974798 p=0.71 :: @AmazonHelp Alrighty then. Thanks. 😞
- id=1411662 conv=1411663 p=0.62 :: @AmazonHelp Okay, no issues. Thanks
- id=1263400 conv=1263401 p=1.00 :: @AmazonHelp Ok. Thanks
- id=964197 conv=964202 p=1.00 :: @AmazonHelp Okay. Thanks.
- id=15706 conv=15707 p=1.00 :: @AmazonHelp ok. Thanks.
- id=227936 conv=227937 p=1.00 :: @AmazonHelp Ok, Thanks.
- id=802346 conv=802342 p=1.00 :: @AmazonHelp Alright. Thanks.

### Cluster 129
- id=269493 conv=269495 p=1.00 :: @AmazonHelp I emailed last night and chatted with a representative last night and I still haven’t re
- id=2615141 conv=2615143 p=1.00 :: @AmazonHelp I have already done that and it was useless conversation with your representative
- id=798801 conv=798804 p=1.00 :: @AmazonHelp Your representative didnt have any answer
- id=789043 conv=789039 p=1.00 :: @AmazonHelp i had already have chat with your representative ... It doesn't work
- id=440997 conv=440994 p=1.00 :: @AmazonHelp I was told that your representative will call me and resolve the issues, nothing has hap
- id=735334 conv=735332 p=1.00 :: @AmazonHelp Spoke to the representative on chat. I have communicated my issue. Thanks for quick resp
- id=1415558 conv=1415559 p=1.00 :: @AmazonHelp Yes, I'm talking to a representative again but I'm still super disappointed.. The call I
- id=1467676 conv=1467677 p=1.00 :: @AmazonHelp Do you have a better method I can reach out by? The representatives through that area ne

### Cluster 130
- id=2310063 conv=2310065 p=0.63 :: @AmazonHelp Gracias por la pronta respuesta. Slds.
- id=1080663 conv=1080664 p=0.75 :: @AmazonHelp Thanks for the quick reply, no big deal, you are awesome! I will fill out the survey!
- id=2242538 conv=2242539 p=0.61 :: @AmazonHelp Agradezco la pronta respuesta.
- id=2310475 conv=2310479 p=0.55 :: @AmazonHelp Most definitely, thank you for responding! :)
- id=575340 conv=575338 p=0.61 :: @AmazonHelp thank you for your response!
- id=1210202 conv=1210203 p=0.94 :: @AmazonHelp Vielen Dank für die schnelle Antwort 👏
- id=1041663 conv=1041664 p=0.78 :: @AmazonHelp Oh! Thanks for the quick answer.
- id=1150863 conv=1150864 p=0.99 :: @AmazonHelp Thanks for the super quick response!!

### Cluster 131
- id=1742664 conv=1742666 p=1.00 :: @AmazonHelp That would be brilliant, thank you KN!
- id=2700789 conv=2700792 p=1.00 :: @AmazonHelp Fabulous, thanks v much
- id=35939 conv=35936 p=1.00 :: @AmazonHelp Awesome, thank you!
- id=989584 conv=989585 p=1.00 :: @AmazonHelp Thanks, that’s brilliant 👍
- id=810253 conv=810251 p=1.00 :: @AmazonHelp This is so great, thank you!
- id=680666 conv=680669 p=1.00 :: @AmazonHelp Great that’s fantastic. Thank you so much!
- id=2507301 conv=2507299 p=1.00 :: @AmazonHelp Great. Thanks.
- id=1725361 conv=1725368 p=0.82 :: @AmazonHelp That’s great 👍🏽 thanks again!!

### Cluster 132
- id=1112720 conv=1112718 p=0.70 :: @AmazonHelp okay, thank you for taking time to let me know!
- id=440423 conv=440424 p=0.71 :: @AmazonHelp Ooh thanks, good to know!
- id=2734222 conv=2734225 p=0.78 :: @AmazonHelp Ok, obrigada!
- id=2779155 conv=2779153 p=0.74 :: @AmazonHelp ok thanks :)
- id=1592887 conv=1592888 p=0.84 :: @AmazonHelp All set! Thanks
- id=823578 conv=823580 p=1.00 :: @AmazonHelp Okay! Thanks for letting me know!
- id=1300138 conv=1300139 p=0.86 :: @AmazonHelp Gotcha ok. Thanks!
- id=2410550 conv=2410551 p=1.00 :: @AmazonHelp okays thanks!

### Cluster 133
- id=2353717 conv=2353724 p=1.00 :: @AmazonHelp Jvous remercie
- id=1223067 conv=1223068 p=1.00 :: @AmazonHelp Grazie di esistere.
- id=1724726 conv=1724724 p=1.00 :: @AmazonHelp Simón, gracias.
- id=742377 conv=742382 p=1.00 :: @AmazonHelp Je l'espère merci.
- id=2811149 conv=2811147 p=0.99 :: @AmazonHelp Yeah I appreciate y'all :)
- id=590774 conv=590770 p=1.00 :: @AmazonHelp Super utile merci de mieux en mieux
- id=2616361 conv=2616354 p=1.00 :: @AmazonHelp Merci, vous aussi !
- id=1174746 conv=1174749 p=1.00 :: @AmazonHelp Merci à vous

### Cluster 134
- id=505912 conv=505909 p=0.87 :: @AmazonHelp Merci Ibtissam!
- id=1144954 conv=1144951 p=0.99 :: @AmazonHelp Thank you 🙂
- id=219483 conv=219490 p=1.00 :: @AmazonHelp Thank you Thank you Thank you Thank you Thank you Thank you Thank you Thank you Thank yo
- id=1374061 conv=1374065 p=0.87 :: @AmazonHelp Obrigada s2
- id=1493337 conv=1493338 p=1.00 :: @AmazonHelp Thank YOU! 🙏
- id=539707 conv=539703 p=0.90 :: @AmazonHelp Thanks JZ #fingerscrossed :-)
- id=914807 conv=914808 p=1.00 :: @AmazonHelp Many thanks 👍
- id=206056 conv=206057 p=0.92 :: @AmazonHelp Thanks KM, appreciate it!

### Cluster 135
- id=283117 conv=281966 p=1.00 :: @AmazonHelp Undelivered product and worst customer care.what u think a company outside of India come
- id=2221879 conv=1387105 p=1.00 :: @AmazonHelp done and got the unwanted advice of apologies and sorry but no one cares about a real is
- id=2278522 conv=1412827 p=1.00 :: @AmazonHelp You all @115850 @115821 will not improve because you know that india has a big populatio
- id=2450548 conv=2418984 p=1.00 :: @AmazonHelp If @115821 @115850 think that Indian Customer can be exploited then you r making mistake
- id=428992 conv=428987 p=1.00 :: @AmazonHelp @115851 @115850 making fool how long you will loot Indian customer???
- id=210307 conv=210320 p=1.00 :: @AmazonHelp Hope you will see all these messages one day Mr @115851 as I seriously want you to know 
- id=665461 conv=665464 p=1.00 :: @AmazonHelp @115851 ur Indian venture is a bloody cheater, they don't refund customers money,is this
- id=2522249 conv=2522238 p=1.00 :: @AmazonHelp FYI..filed a complain to consumer court in india. @115851 @115850 https://t.co/TpDzBqch6

### Cluster 136
- id=2457154 conv=2457155 p=1.00 :: @AmazonHelp I have sent a detailed email to customer service - please check and resolve ASAP
- id=944904 conv=944896 p=1.00 :: @AmazonHelp My email address is __email__ I have already raised the issue with customer care on chat
- id=2901100 conv=2901102 p=1.00 :: @AmazonHelp That’s correct Liz. I sent a final email to customer services, the last few said they wo
- id=2300062 conv=2300046 p=1.00 :: @AmazonHelp I have emailed you with details via the customer services in 'my orders'
- id=257182 conv=257183 p=1.00 :: @AmazonHelp I got an email from customer service. Thank you!
- id=518805 conv=518808 p=1.00 :: @AmazonHelp I have submitted an email to your customer service, thank you.
- id=1223613 conv=1223614 p=1.00 :: @AmazonHelp I went through customer service menu and sent email. Thank you.
- id=1603813 conv=1603814 p=1.00 :: @AmazonHelp yes sent mail to your customer care, need to resolve earlier

### Cluster 137
- id=1628966 conv=1628969 p=0.86 :: @AmazonHelp Your courier lied. Another complaint has been escalated. It will happen every time I nee
- id=1423072 conv=1423079 p=0.96 :: @AmazonHelp Been done. Instead your delivery guy is still failing to deliver to address that is open
- id=787190 conv=787191 p=1.00 :: @AmazonHelp My products are getting marked before being delivered. Delivery Guy’s Number is always o
- id=467523 conv=467400 p=0.85 :: @AmazonHelp Contact no. of delivery personnel is unavailable! There is a sense of lack of liability 
- id=1492737 conv=1492735 p=0.93 :: @AmazonHelp See the delivery person's details and contact number, it is switched off. what should on
- id=2251924 conv=2251918 p=0.91 :: @AmazonHelp pick by courier person...what's the way out man ???if I am going to call, they say "your
- id=2265626 conv=2265628 p=1.00 :: @AmazonHelp This is happening for the second time. The contact details provided of the delivery agen
- id=803944 conv=803946 p=0.88 :: @AmazonHelp they said we have cancelled your courier, they all told lie as still courier arrived, ev

### Cluster 138
- id=1506876 conv=1506872 p=0.99 :: @AmazonHelp Send it to me now Fraudsters, You cheap scammers..
- id=1615563 conv=1615547 p=0.97 :: @AmazonHelp This means you people are cheats! Just like ur Cuscare executives Harish who didn't reso
- id=430053 conv=430040 p=1.00 :: @AmazonHelp i am telling you are doing something fraud here
- id=179411 conv=179424 p=1.00 :: @AmazonHelp Always be fair. Once cheating spoils image forever. Let some responsible person talk to 
- id=575412 conv=575406 p=1.00 :: @AmazonHelp You keep me updated about this fraud.
- id=780035 conv=780016 p=1.00 :: @AmazonHelp I know you will not @115821 you are there to do frauds only , this is your work , my fir
- id=793885 conv=792679 p=1.00 :: @AmazonHelp #fakecompany #customersupport #makingfoolofcustomers #Cheat #loss #neverbuyfromamazon #w
- id=665201 conv=665205 p=1.00 :: @AmazonHelp I want that you scam should be highlighted n the fraud you All doing with innocent clien

### Cluster 139
- id=608032 conv=608040 p=1.00 :: @AmazonHelp You already have a DM from me and I’ve filled out your weblink. You’re not doing yoursel
- id=398709 conv=398710 p=1.00 :: @AmazonHelp So again one lousy dm and don't even answer my reply CONTEMPT for your customers
- id=334023 conv=334031 p=1.00 :: @AmazonHelp I wasn’t. Do you think that any of this is good customer service?
- id=1032362 conv=1032363 p=1.00 :: @AmazonHelp Unfortunately, 140 characters are not enough to tell you what is wrong with your service
- id=114393 conv=114397 p=1.00 :: @AmazonHelp Have rang and made a complaint but your customer service is shocking and I’m not expecti
- id=320050 conv=320019 p=1.00 :: @AmazonHelp Ridiculous customer support and the process you follow.. Escalation management very Poor
- id=2884894 conv=2884899 p=1.00 :: @AmazonHelp I did this yesterday via chat with zero progress. Your customer service is appalling, al
- id=1449062 conv=1449063 p=1.00 :: @AmazonHelp Yup! I’ve already contacted customer support where I was told “Don’t worry.” I’m not wor

### Cluster 140
- id=2477457 conv=2477475 p=1.00 :: @AmazonHelp evening I was told I would have a reply in 12 hours or so! Any updates thank you
- id=2220066 conv=2220068 p=1.00 :: @AmazonHelp I have filled in the details. It says I will get a response in 12 hours. I would expect 
- id=1297935 conv=1297933 p=1.00 :: @AmazonHelp 12 hour response time? That won't help lol
- id=2205516 conv=2205514 p=1.00 :: @AmazonHelp They say it takes up to 12hrs for a reply
- id=1575679 conv=1575675 p=1.00 :: @AmazonHelp So I should expect a response within 12 hours?
- id=2763477 conv=2763475 p=1.00 :: @AmazonHelp Thank for the support, I did it already, unfortunately it can take up to 12h to reply. H
- id=2428163 conv=2428164 p=1.00 :: @AmazonHelp Thank you. Just sent a message. However it says aim to reply within 12hours. That doesn’
- id=2804278 conv=2804276 p=1.00 :: @AmazonHelp May I know an estimated time it will take for a response I emailed at 6:22 PM EST today

### Cluster 141
- id=1082911 conv=1082914 p=1.00 :: @AmazonHelp I'd like to know why I was lied to, and what to be done about it. I also want to know wh
- id=318784 conv=318785 p=1.00 :: @AmazonHelp i dont understand why your supervisor provide me wrong details
- id=1307253 conv=1307254 p=1.00 :: @AmazonHelp asked to speak with a manager or someone I could complain to at the new Sacramento distr
- id=2113588 conv=2113593 p=1.00 :: @AmazonHelp Boss still speaking to your help line and no one is helping, despite paying premium I ha
- id=1127329 conv=1127327 p=1.00 :: @AmazonHelp STILL Not got any help from anyof your assistant my problem still continues
- id=1053516 conv=1053526 p=1.00 :: @AmazonHelp Ur supervisor ur managers are all afraid to take call wen I ask for call transfer those 
- id=1650797 conv=1650801 p=1.00 :: @AmazonHelp I have done this many times.. escalated and spoke to manager level,but no result😞
- id=1153722 conv=1153720 p=1.00 :: @AmazonHelp my request to speak to a supervisor was ignored. csr is filling out yet another form. th

### Cluster 142
- id=96787 conv=96784 p=1.00 :: @AmazonHelp As I have told you before they do not connect to an agent without placing an order. I ca
- id=180905 conv=180913 p=1.00 :: @AmazonHelp @115850 any way to speak to an agent and get pleased with some false assurances?
- id=930423 conv=930428 p=1.00 :: @AmazonHelp Thanks - I already did the whole chat with an agent, didn't make anything easier - just 
- id=631640 conv=631641 p=1.00 :: @AmazonHelp None!! Your agent submitted a report before we finished our conversation. When I asked t
- id=2793045 conv=2793046 p=1.00 :: @AmazonHelp Called 3 times. Extremely difficult to understand all 3 agents. One agent seemed complet
- id=2104274 conv=2104275 p=0.92 :: @AmazonHelp I asked the agent
- id=1254563 conv=1254559 p=0.92 :: @AmazonHelp No. I got frustrated with the agent after ~15 minutes. I sent the email ~30 minutes ago.
- id=244136 conv=244132 p=1.00 :: @AmazonHelp I'm on livechat with an agent now. Just getting the "sorry, won't happen again" line, wh

### Cluster 143
- id=1423806 conv=1423809 p=1.00 :: @AmazonHelp Twice. Nice that you ‘get’ it. Any chance my dad will ‘get’ his gift anytime today?
- id=1458020 conv=1458025 p=1.00 :: @AmazonHelp Oui mais bon. Mon mari aurait pu le voir c’était pour lui et vous aurez gâcher mon cadea
- id=589990 conv=590005 p=0.91 :: @AmazonHelp Chèque cadeau que j'ai insérer
- id=581191 conv=581193 p=0.92 :: @AmazonHelp I now need to buy her something else for Christmas Day! Think I’ll stick to the shops
- id=2390373 conv=2390374 p=0.98 :: @AmazonHelp It was a gift, she absolutely loves it!
- id=2318785 conv=2318786 p=1.00 :: @AmazonHelp I just hope my kids don't open the door to the next one - Xmas is stressful enough - I j
- id=43724 conv=43725 p=1.00 :: @AmazonHelp Ummm. This is the 3rd time we've complained. Lovely people in CustSvc, but full of empat
- id=2680308 conv=2680309 p=1.00 :: @AmazonHelp Weihnachtsgeschenke von meinem Mann für mich war weil ich sie unbedingt haben wollte. 😭

### Cluster 144
- id=283945 conv=283946 p=0.87 :: @AmazonHelp Got the replacement today &amp; its in 2 pieces. Are you guys out of bubble wraps/air po
- id=385923 conv=385924 p=0.71 :: @AmazonHelp Fragile food items like Maggi need more protective packaging. I received my pack of nood
- id=270640 conv=270641 p=0.85 :: @AmazonHelp Everything is okay and in order just poor packaging and delivery. It had good enough pad
- id=764802 conv=764803 p=0.79 :: @AmazonHelp I've arranged an exchange thank you, it's just infuriating as I need them ASAP! I would 
- id=74746 conv=74747 p=0.86 :: @AmazonHelp Hola, el producto como tal parece haber llegado en buen estado, sin embargo las cajas ve
- id=2685341 conv=2685342 p=0.85 :: @AmazonHelp Pues que compre ayer el Amiibo de Lucina, y ha llegado con la caja totalmente doblada. L
- id=737193 conv=737194 p=0.71 :: @AmazonHelp Cet emballage n'y figure pas :/
- id=646732 conv=646734 p=0.94 :: @AmazonHelp The whole thing is the item really, it's a screwdriver in a storage box. I haven't check

### Cluster 145
- id=1136259 conv=1136260 p=1.00 :: @AmazonHelp I want to buy another mobile.
- id=2819844 conv=2819846 p=1.00 :: @AmazonHelp Soo what should I do now I need to buy that phone with exhange offer
- id=180066 conv=180069 p=1.00 :: @AmazonHelp Ja schon aber genau dieses Geld wollte ich erst mal sparen für ein neues Handy was ich m
- id=1400656 conv=1281419 p=1.00 :: @AmazonHelp I can not go to service center. As phone not worked well for 12 days such a defective ph
- id=2987674 conv=2987675 p=1.00 :: @AmazonHelp Awesome phone for the price pay.
- id=226733 conv=224960 p=1.00 :: @AmazonHelp got mail for replacement. What about the phone which i bought as i cant wait for 20 days
- id=1003704 conv=1003702 p=1.00 :: @AmazonHelp Then i should change my mind for buying a new mobile isn't it?
- id=1498571 conv=1108234 p=1.00 :: @AmazonHelp its strange the other item i ordered along has reached me but not this phone.

### Cluster 146
- id=2135561 conv=2135563 p=1.00 :: @AmazonHelp It’s not missed but the tracking doesn’t even say out for delivery yet &amp; when I go o
- id=2925492 conv=2925497 p=1.00 :: @AmazonHelp This is what the tracking info says. It was ready to be shipped, and wasn’t shipped. I’m
- id=1258634 conv=1258638 p=1.00 :: @AmazonHelp Are you really asking if I checked the tracking information?? 😂 yes the tracking info sa
- id=10637 conv=10634 p=1.00 :: @AmazonHelp The tracking indicated as here, and then, it seemed to go back in time, saying it was no
- id=1284853 conv=1284849 p=1.00 :: @AmazonHelp the tracking says that it's in Stoughton, MA, US I'm located in Newton MA is there anywa
- id=2307825 conv=2307826 p=1.00 :: @AmazonHelp The only tracking info says it’s left the facility. Tomorrow I’m going shopping for item
- id=2668735 conv=2668736 p=1.00 :: @AmazonHelp Thank you, it says 36 on the tracking but my neighbour doesn’t have it?
- id=2891848 conv=2891850 p=1.00 :: @AmazonHelp Checked the tracking. Looks like a @81 issue. The business was definitely open at 10:38 

### Cluster 147
- id=1519864 conv=1519862 p=1.00 :: @AmazonHelp It says UPS
- id=886156 conv=886150 p=1.00 :: @AmazonHelp It appears to be UPS
- id=56853 conv=56854 p=1.00 :: @AmazonHelp UPS surepost
- id=555293 conv=555291 p=1.00 :: @AmazonHelp UPS Sure Post
- id=1247750 conv=1247754 p=1.00 :: @AmazonHelp UPS —the company is called Looseplus, I believe.
- id=2320947 conv=2320949 p=1.00 :: @AmazonHelp plz plz give me an option for UPS only
- id=296413 conv=296411 p=1.00 :: @AmazonHelp UPS &amp; no
- id=1811238 conv=1811236 p=1.00 :: @AmazonHelp I was told it was UPSP.

### Cluster 148
- id=339684 conv=339686 p=0.70 :: @AmazonHelp USPS and inconveniences like this have happened multiple times over the last couple mont
- id=2176516 conv=2176523 p=0.88 :: @AmazonHelp I spoke to someone 20 minutes ago, and was told that you’re blaming USPS for the screw u
- id=462560 conv=462561 p=1.00 :: @AmazonHelp Thank you for your response! It was through USPS
- id=1020161 conv=1020164 p=1.00 :: @AmazonHelp it says USPS. they both were assigned to that.
- id=1734586 conv=1734584 p=0.67 :: @AmazonHelp USPS. Received this evening! Thanks.
- id=2438442 conv=2438444 p=0.91 :: @AmazonHelp USPS is galactically unreliable and has HORRIBLE performance!
- id=2490624 conv=2490629 p=0.85 :: @AmazonHelp USPS seems very unreliable... they have the most problems.
- id=2923495 conv=2923497 p=0.71 :: @AmazonHelp They could not do anything because usps is closed. Everyone in the United States know US

### Cluster 149
- id=1590613 conv=1590614 p=1.00 :: @AmazonHelp Thank you the item was not damaged. The package was shipped with AMZL US.
- id=2605671 conv=2605672 p=1.00 :: @AmazonHelp It was shipped with AMZL US
- id=2971893 conv=2971894 p=1.00 :: @AmazonHelp It just says shipped with AMZL US. It has happened a few times, happening more frequentl
- id=936700 conv=936701 p=1.00 :: @AmazonHelp Bought from BB cosmetic, shipped by AMZL US
- id=1227032 conv=1227030 p=1.00 :: @AmazonHelp Yes. Has been shipped via AMZL US.
- id=863824 conv=863826 p=1.00 :: @AmazonHelp Shipped with AMZL US. It's no big deal, but I'm pretty worried about this happening duri
- id=2795350 conv=2795363 p=1.00 :: @AmazonHelp It just says shipped with AMZL US?
- id=458943 conv=458947 p=1.00 :: @AmazonHelp Shipped with AMZL US it what it says. Always have issues when shipped like that. Usps/up

### Cluster 150
- id=1628973 conv=1628974 p=0.44 :: @AmazonHelp The first one was Carrier: AMZL US. This one is USPS
- id=1210986 conv=1210989 p=0.40 :: @AmazonHelp It says that the carrier was: AMZL US
- id=945454 conv=945457 p=0.49 :: @AmazonHelp My carrier was AMZL US
- id=1173899 conv=1173900 p=0.38 :: @AmazonHelp Nothing was damaged,thankfully. And the carrier was AMZL US
- id=745043 conv=745046 p=0.51 :: @AmazonHelp AMZL US is the carrier. Last update was at 3am yesterday that it left Chino but no updat
- id=590812 conv=590813 p=0.32 :: @AmazonHelp Today's package says #USPS. The #canon #printer says the carrier is #amzlus.
- id=1892133 conv=1892139 p=0.47 :: @AmazonHelp Still not here. Carrier is listed as AMZL US
- id=888235 conv=888238 p=0.77 :: @AmazonHelp The carrier is AMZL US. Luckily no damage!

### Cluster 151
- id=517664 conv=517666 p=0.89 :: @AmazonHelp Thank you. There doesn’t appear to be a carrier listed at this stage.
- id=2623931 conv=2623932 p=0.98 :: @AmazonHelp it’s been two seperate orders over 1 month. I have no idea who the carrier is??
- id=887992 conv=887988 p=0.86 :: @AmazonHelp Already did but cannot reach the carrier, so there is no point
- id=136979 conv=136982 p=0.90 :: @AmazonHelp Tells me the carrier but no address and I don't have time to go and collect it
- id=2590349 conv=2590351 p=1.00 :: @AmazonHelp Nope. No carrier info either
- id=411444 conv=411445 p=1.00 :: @AmazonHelp No carrier is listed! Its held at the Newark, California facility
- id=465151 conv=465152 p=0.94 :: @AmazonHelp Thank you. For the carrier it saids ups
- id=89319 conv=89320 p=0.72 :: @AmazonHelp Yeap I am contacting the carrier now. Thanks for the support. I have no problem with DHL

### Cluster 152
- id=627853 conv=627854 p=1.00 :: @AmazonHelp This is the email I received. Is it genuine? https://t.co/TkNXYJyrF2
- id=1015612 conv=1015614 p=1.00 :: @AmazonHelp Nope, this is the email I received. https://t.co/wU0q2MOd39
- id=76068 conv=76078 p=1.00 :: @AmazonHelp I feel like you guys are just playing me now. This email makes no sense. https://t.co/YU
- id=275124 conv=275129 p=1.00 :: @AmazonHelp https://t.co/qyehiagvNC. I received this email but I never asked for a change! https://t
- id=1197342 conv=1197347 p=1.00 :: @AmazonHelp "https://t.co/YYqtC23syj rejected your message to the following email addresses"
- id=1482871 conv=1482875 p=1.00 :: @AmazonHelp Yes I got an email. Part of which is attached. https://t.co/ReqtF7N2Ik
- id=1501820 conv=1501822 p=1.00 :: @AmazonHelp Nope it's saying I'm not! Could it be a fake email sent out then? https://t.co/B6t63CkIt
- id=1645706 conv=1645710 p=1.00 :: @AmazonHelp @502872 Is this a fake email? It was sent by __email__ https://t.co/BrX1Vj7cJ1

### Cluster 153
- id=626594 conv=626596 p=1.00 :: @AmazonHelp Just says dispatched
- id=1731156 conv=1731157 p=0.99 :: @AmazonHelp No just says dispatching now which it has done for the past 5 hours
- id=2352296 conv=2352297 p=1.00 :: @AmazonHelp It says “Dispatching now”
- id=1687062 conv=1687063 p=1.00 :: @AmazonHelp My friends one has been dispatched but mine still says not yet dispatched
- id=1838552 conv=1838550 p=1.00 :: @AmazonHelp Just says not yet dispatched
- id=1691952 conv=1691924 p=1.00 :: @AmazonHelp But still no dispatch
- id=1665799 conv=1665797 p=1.00 :: @AmazonHelp Nothing at all. That's why I'm curious of dispatching limits. I live in Derbyshire, wher
- id=1707982 conv=1707983 p=1.00 :: @AmazonHelp Its not arrived and its still in dispatching stages fuming is not the word .. not good

### Cluster 154
- id=537522 conv=537523 p=1.00 :: @AmazonHelp Yeah I signed up for a free trial a few years ago, but just today got a letter saying I 
- id=1213448 conv=1213450 p=1.00 :: @AmazonHelp But I don't want to be charged next April hence why I'm trying to cancel it so surely I 
- id=145767 conv=145769 p=1.00 :: @AmazonHelp So, can you confirm, will I be able to Active the Trial at a later date or not if this i
- id=2850792 conv=2850793 p=1.00 :: @AmazonHelp I have cancelled it but seeing as i haven't used it in a while i was annoyed at the char
- id=985500 conv=985501 p=1.00 :: @AmazonHelp I was charged £7.99, when it was supposed to be a free trial, and had no credits
- id=378523 conv=378517 p=1.00 :: @AmazonHelp Ok I’ll try that next time. Still in trial period and I want to see how beneficial it is
- id=1556301 conv=1556302 p=1.00 :: @AmazonHelp Is there a way to cancel it so that I still have the opportunity to access the trial in 
- id=2504824 conv=2504826 p=1.00 :: @AmazonHelp Lol. None now that my free trial is over. Thank u tho.

### Cluster 155
- id=99981 conv=99983 p=0.78 :: @AmazonHelp Yeah but it was available to ship immediately, and your two day shipping has been 3 days
- id=339146 conv=339149 p=0.63 :: @AmazonHelp But I chose 2 day shipping at checkout
- id=284814 conv=284811 p=0.90 :: @AmazonHelp that doesn't even make sense. Best case scenario should not be given as estimate. Also w
- id=2889280 conv=2889194 p=0.84 :: @AmazonHelp yes but the item was in-stock, so why with 1 and 2 day shipping options is it not arrivi
- id=321141 conv=321143 p=0.66 :: @AmazonHelp And what do you mean by shipping speed?? Is it 2 days delivery for which I paid? Still i
- id=345280 conv=345281 p=0.70 :: @AmazonHelp Yeah, it says it’s been shipped but my guaranteed 2 day shipping has turned into 3 and I
- id=1083820 conv=1083821 p=1.00 :: @AmazonHelp Aka, standard shipping and not two day shipping as you advertise.
- id=176442 conv=176443 p=1.00 :: @AmazonHelp It's just disappointing to go from 2 days shipping to 7.

### Cluster 156
- id=1192977 conv=1192979 p=1.00 :: @AmazonHelp The first call dropped, the 2nd call said I would get Prime extended for a month, to che
- id=872656 conv=872658 p=1.00 :: @AmazonHelp Order received. From my little lady "few, it means your thought of cancelling Prime isn'
- id=349388 conv=349389 p=1.00 :: @AmazonHelp Chased up an order again, after 4 prev attempts. Previous Prime acc credit queried which
- id=616998 conv=616999 p=0.96 :: @AmazonHelp Yeah...but I’m disappointed as I have a prime account and you promised it yesterday and 
- id=449940 conv=449946 p=1.00 :: @AmazonHelp Many times, I contact support every time it happens but there is only so many times the 
- id=2297751 conv=2297753 p=1.00 :: @AmazonHelp Have shared. But this isn't the first time when my product didn't reach on time even aft
- id=180911 conv=180913 p=1.00 :: @AmazonHelp even after #prime and repeated customer calls, didn't get the package in time. Very unli
- id=2372148 conv=2372144 p=1.00 :: @AmazonHelp Spoken on chat. Looks as though my order got put on the wrong van. As a token of apology

### Cluster 157
- id=77615 conv=77617 p=0.50 :: @AmazonHelp call me on my registered number.
- id=1387208 conv=1387213 p=0.56 :: @AmazonHelp 9911190866 this is my no. Call me
- id=1456382 conv=1456389 p=0.46 :: @AmazonHelp Please ask them to call me on 9650563038
- id=879265 conv=879263 p=0.73 :: @AmazonHelp so what....call me 9718111527
- id=285617 conv=285157 p=0.69 :: @AmazonHelp Instead, can you call me on 9810486357.
- id=331312 conv=331304 p=0.74 :: @AmazonHelp 9545879019 call me right now as your no are unreachable
- id=1423034 conv=1423024 p=0.47 :: @AmazonHelp I understand I live on a street that has similar name to diff street 1 block over, but t
- id=1422835 conv=1422837 p=0.50 :: @AmazonHelp I need to speak to someone about this. Need a phone number NOW

### Cluster 158
- id=983828 conv=983831 p=1.00 :: @AmazonHelp Still waiting your response ? ???????????????
- id=298436 conv=298437 p=1.00 :: @AmazonHelp Waiting for reply
- id=1220884 conv=1220885 p=1.00 :: @AmazonHelp Still waiting for reply from your side
- id=301064 conv=301050 p=1.00 :: @AmazonHelp Still waiting for an answer. Reached out to whom?
- id=593372 conv=593373 p=1.00 :: @AmazonHelp I am still waiting for your reply
- id=856021 conv=856047 p=1.00 :: @AmazonHelp Nope, Just waiting for a response.
- id=1274822 conv=1274823 p=1.00 :: @AmazonHelp Waiting for your response
- id=1511946 conv=1511965 p=1.00 :: @AmazonHelp yea i await ur response

### Cluster 159
- id=358856 conv=358857 p=1.00 :: @AmazonHelp Waiting yar
- id=980143 conv=980152 p=1.00 :: @AmazonHelp Okkk, fine i am waiting. But this is totally wrong.
- id=2176685 conv=2176687 p=1.00 :: @AmazonHelp Ok I am waiting
- id=526597 conv=526598 p=1.00 :: @AmazonHelp yea k but awaiting very soon
- id=2943275 conv=2943271 p=1.00 :: @AmazonHelp Am waiting..
- id=388459 conv=388457 p=0.98 :: @AmazonHelp Waiting waiting .....😴😴😴😥
- id=426330 conv=426328 p=1.00 :: @AmazonHelp I am all waiting folks
- id=1890575 conv=1890569 p=1.00 :: @AmazonHelp That's what I am doing #Waiting

### Cluster 160
- id=1446377 conv=1446375 p=1.00 :: @AmazonHelp Tried to contact via phone same problem
- id=581182 conv=581180 p=1.00 :: @AmazonHelp I tried that on that call it doesn't accept my inputs that is main problem
- id=96786 conv=96784 p=1.00 :: @AmazonHelp Yes I have tried calling to them on 180030009009 number and application. Both ways but n
- id=673211 conv=673208 p=1.00 :: @AmazonHelp Unable to get in touch via phone. The call is hanging up as it has no option to talk abo
- id=274254 conv=274248 p=1.00 :: @AmazonHelp Your system doesn't allow me to request a call back via a switchboard and extension numb
- id=842212 conv=842214 p=1.00 :: @AmazonHelp From past 1 hr I am trying to connect but did not receive any call
- id=29514 conv=29516 p=1.00 :: @AmazonHelp Yes, try dialing 180030009009, select any option, IVR would say use the app the call wil
- id=1137290 conv=1137293 p=1.00 :: @AmazonHelp i tried call back request ..but still error , bot conectting my call ,

### Cluster 161
- id=1331203 conv=1331195 p=1.00 :: @AmazonHelp Ok merci. Comment puis je les contacter ?
- id=2139301 conv=2139299 p=1.00 :: @AmazonHelp If I’m not in the US right now, is there a way to contact them?
- id=1033093 conv=1033084 p=1.00 :: @AmazonHelp How would I reach them?
- id=1041126 conv=1041130 p=1.00 :: @AmazonHelp Ou puis-je les contacter ?
- id=2530738 conv=2530704 p=1.00 :: @AmazonHelp Donde me pongo en contacto con ellos?
- id=1141880 conv=1141881 p=1.00 :: @amazonhelp Sorry, do you mean I have to contact them?
- id=932293 conv=932290 p=1.00 :: @AmazonHelp Am I able to contact them directly? I've received an email with "Please don't hesitate t
- id=2919890 conv=2919891 p=1.00 :: @AmazonHelp How can I speak to costumer service reps based in the United States?

### Cluster 162
- id=1665735 conv=1665736 p=1.00 :: @AmazonHelp Yes guys.. Why cant i send the same info via email? How does using a street side fax mac
- id=1356297 conv=1356298 p=1.00 :: @AmazonHelp sim. mas não tem como eu mandar fax. há outra forma?
- id=1404013 conv=1404014 p=1.00 :: @AmazonHelp Oui, mais on me demande d'envoyer un fax avec des infos (qui utilise un fax en 2017😂) je
- id=166489 conv=166492 p=1.00 :: @AmazonHelp @154669 Na verdade voces pedem para enviar uns documentos por FAX... isso mesmo FAX ! Aq
- id=255480 conv=255484 p=1.00 :: @AmazonHelp What is fax number? Can you change verif addres with fax to use e-mail?
- id=2693899 conv=2693902 p=1.00 :: @AmazonHelp He intentado ya tres veces enviar el fax con los datos que me requieren y no se logra la
- id=1305578 conv=474336 p=1.00 :: @AmazonHelp I am not sure how easy to fax the details? Can't you guys handle over the email or SECUR
- id=1599627 conv=1599623 p=1.00 :: @AmazonHelp Sauf que je n'ai pas de fax. Donc ca veut dire par courrier. Sauf que ma commande est ur

### Cluster 163
- id=1046580 conv=1046577 p=0.94 :: @AmazonHelp How can i reach you through real time chat ? Because my problem is unsolved
- id=1224594 conv=1224585 p=0.93 :: @AmazonHelp Finally found the chat option (not easy to do. Needs simplifying! ) and being sorted now
- id=325839 conv=325842 p=1.00 :: @AmazonHelp That's fine I used the chat option in the end thank you for your help
- id=2797173 conv=2797174 p=1.00 :: @AmazonHelp Waiting for chat rep to come online. Thanks!
- id=2399406 conv=2399407 p=0.97 :: @AmazonHelp No. Have a look at my chat logs.
- id=629646 conv=629647 p=0.92 :: @AmazonHelp Ya he solucionado el problema por el chat en vivo. Gracias :3
- id=206180 conv=206188 p=0.86 :: @AmazonHelp No, but when I get to a computer I’ll do the chat thing again.
- id=2980964 conv=2980965 p=0.87 :: @AmazonHelp There’s no option to chat...

### Cluster 164
- id=660946 conv=660948 p=1.00 :: @AmazonHelp Well, that's two people who answered the phone and then hung up on me. Is the phone syst
- id=1012796 conv=1012797 p=0.99 :: @AmazonHelp I called so many times in day, But no outcomes found.
- id=420772 conv=420770 p=1.00 :: @AmazonHelp I called. Was on the phone for about 25 minutes, between being on hold with someone who 
- id=1374572 conv=1374568 p=1.00 :: @AmazonHelp several lengthy phone calls
- id=1648171 conv=1648168 p=1.00 :: @AmazonHelp No consigo hablar con ellos. He llamado tres veces al móvil desde el que me han “llamado
- id=1740760 conv=1740761 p=1.00 :: @AmazonHelp This is not the first time this has happened. It’s literally every single phone call. Wh
- id=2764434 conv=2761289 p=1.00 :: @AmazonHelp As i mentioned before, have called up there twice but of no use.
- id=1150889 conv=1150892 p=1.00 :: @AmazonHelp I used to never have to call about anything &amp; if I did, it was handled well right aw

### Cluster 165
- id=282178 conv=282176 p=1.00 :: @AmazonHelp I need this product tomorrow any how in my home address as I gift to my best buddies..
- id=293247 conv=293256 p=1.00 :: @AmazonHelp Can u plz confirm for the particular product.. ? Don't go with easy way outs..
- id=985086 conv=985088 p=1.00 :: @AmazonHelp Consider this matter with great responsibility ! Looking for product as soon as possible
- id=432951 conv=432947 p=1.00 :: @AmazonHelp details submitted, hope to recieve the product
- id=1638598 conv=1638599 p=1.00 :: @AmazonHelp Product received. Thanks for responding.
- id=2643615 conv=2643609 p=1.00 :: @AmazonHelp Hi Team, thanks for you support. Product has been picked-up by agent, but didn't got any
- id=233091 conv=233089 p=1.00 :: @AmazonHelp Thanks for promptly taking up the request. Have received the product.
- id=748761 conv=748762 p=0.94 :: @AmazonHelp @115850 I need my product today as any cost, i don't know,how you will do but you will

### Cluster 166
- id=2123813 conv=2123814 p=1.00 :: @AmazonHelp ha ha! I didn’t notice the date!
- id=1041784 conv=1041785 p=1.00 :: @AmazonHelp Honestly don’t know...just know the dates on website haven’t been accurate
- id=219168 conv=219163 p=1.00 :: @AmazonHelp They have changed more than 3 dates already .
- id=482353 conv=482355 p=1.00 :: @AmazonHelp Et ce midi la date a changé
- id=803024 conv=803025 p=1.00 :: @AmazonHelp There is no date. That's why I'm asking.
- id=2601445 conv=2601443 p=1.00 :: @AmazonHelp Il n'y pas de date
- id=842091 conv=842095 p=1.00 :: @AmazonHelp Ninguna no tienen fecha estimada ....
- id=2800384 conv=2780595 p=1.00 :: @AmazonHelp No date specified for either item.

### Cluster 167
- id=156688 conv=156690 p=0.42 :: @AmazonHelp la date indiqué est le Vendredi 24 Novembre 2017 donc aujourd'hui :)
- id=1387349 conv=1387320 p=0.39 :: @AmazonHelp It was 14-17 Oct.
- id=2900951 conv=2900956 p=0.35 :: @AmazonHelp El 4 o 5 de diciembre
- id=390052 conv=390050 p=0.39 :: @AmazonHelp 9th of Oct which was yesterday as per the calendar
- id=759732 conv=759734 p=0.39 :: @AmazonHelp Its 30th September Now when? I hope I will crack the list Please notify
- id=1332645 conv=1332646 p=0.41 :: @AmazonHelp Mean by 15th Nov?
- id=19113 conv=19114 p=0.32 :: @AmazonHelp The earliest contest participation date was from 13th september 2017 to 31st october 201
- id=380229 conv=380216 p=0.22 :: @AmazonHelp none after 9th october

### Cluster 168
- id=803072 conv=803070 p=0.99 :: @AmazonHelp sold by a seller. Charles Tyrwhitt
- id=2776318 conv=2776321 p=0.88 :: @AmazonHelp It was filled by a seller
- id=2486952 conv=2486956 p=0.85 :: @AmazonHelp vendido por BuyGifts entre prevista 15 nov
- id=25254 conv=25259 p=1.00 :: @AmazonHelp It’s from a seller
- id=245870 conv=245876 p=0.84 :: @AmazonHelp Vendido por “SOLUCIONES ALTHEA”.
- id=95363 conv=95370 p=1.00 :: @AmazonHelp Vendido*
- id=479366 conv=479368 p=0.93 :: @AmazonHelp The seller is now called go green batteries uk who advertises as a uk seller but the goo
- id=352076 conv=352077 p=1.00 :: @AmazonHelp There was a promotion Divali sale

### Cluster 169
- id=1053594 conv=1053568 p=0.82 :: @AmazonHelp I have a complaint against your seller then!
- id=1254127 conv=1254133 p=0.84 :: @AmazonHelp They should, but what's done is done. I don't want any further contact with this seller.
- id=1249705 conv=1249706 p=0.78 :: @AmazonHelp Can I search for everyone except a few select sellers that I’ve had problems with?
- id=2431098 conv=2431102 p=0.95 :: @AmazonHelp the link that you provided shows seller feedback. My issue is not with seller, it's with
- id=2931410 conv=2931417 p=0.74 :: @AmazonHelp I will order to someone else's house and reduce the risk factor by choosing only trusted
- id=1661475 conv=1661480 p=1.00 :: @AmazonHelp Have sent a message to seller support but suspect this will be quicker!
- id=921442 conv=921448 p=0.79 :: @AmazonHelp Your seller is faulty also
- id=1168818 conv=1168819 p=1.00 :: @AmazonHelp I'm trying to deal with this now on the phone. Its a very long story. Basically an outsi

### Cluster 170
- id=140939 conv=140941 p=1.00 :: @AmazonHelp Il n'y a pas encore de problème avec cette commande si ce n'est qu'il faut être TRES JOU
- id=3724 conv=3726 p=1.00 :: @AmazonHelp There was only one costing a lot more than £20 and FBA -stating eligibility !
- id=1570944 conv=1570945 p=1.00 :: @AmazonHelp Yeah. $3. 🙄
- id=1320477 conv=1320480 p=1.00 :: @AmazonHelp Buenas, el cargo es de 9,34 €
- id=1459782 conv=1459783 p=1.00 :: @AmazonHelp A £900 piece of eqiupment though? Really? Are you really all that dumb?
- id=167910 conv=167908 p=1.00 :: @AmazonHelp Enfin bon, 292€, c'est pas mince comme dépenses x_x
- id=2320773 conv=2320771 p=1.00 :: @AmazonHelp Ça me dit que je profite déjà du prime pouvez vous le dire si vous aller me débiter 24 e
- id=108103 conv=108106 p=1.00 :: @AmazonHelp Non. Aucun. Ca le coûte 9 euros, alors que pour zero ca arrivais a la meme date que cell

### Cluster 171
- id=2562185 conv=2562186 p=0.95 :: @AmazonHelp Thanks. But what’s confusing is that is was your price listed? And then it wasn’t? I jus
- id=895944 conv=895945 p=0.84 :: @AmazonHelp I know cart prices aren’t set in stone. But like, it went from on sale to more than the 
- id=204996 conv=205000 p=0.91 :: @AmazonHelp No it was super thin. Not what I need. Why is return shopping for any seller almost $20?
- id=998012 conv=998013 p=1.00 :: @AmazonHelp Did u even see the screenshot ? The price has increased more then 100 INR in last few ho
- id=633574 conv=633576 p=0.83 :: @AmazonHelp À ce prix là, autant s'acheter une voiture neuve plutôt que de laver l'ancienne.
- id=282470 conv=282473 p=0.86 :: @AmazonHelp Yes i know that. But it should offer at least the same price.
- id=136863 conv=136865 p=0.82 :: @AmazonHelp Ici le prix black Friday à 292 marqué anciennement moins cher à 237.90 https://t.co/Gwl5
- id=622559 conv=622568 p=1.00 :: @AmazonHelp Well didnt go well. Support agent gives me policy statement nd fails to even understand 

### Cluster 172
- id=1261844 conv=1261845 p=1.00 :: @AmazonHelp It just changed from Saturday to arriving today by 8:00. Here’s hoping it’s two hours ea
- id=2754593 conv=2754594 p=1.00 :: @AmazonHelp well it has said arriving today since Friday, then on Saturday and today so not sure wha
- id=1939128 conv=1939130 p=1.00 :: @AmazonHelp Thanks - on there it says arriving tomorrow??
- id=2805071 conv=2805072 p=1.00 :: @AmazonHelp Yes it was supposed to arrive today by 8 pm. So hopefully it's gets here in the next hou
- id=1414508 conv=1414509 p=1.00 :: @AmazonHelp Yes it was supposed to be here by 8 pm. Now it says the 3rd
- id=1312507 conv=1312508 p=1.00 :: @AmazonHelp Said it was supposed to be here by 8pm today
- id=1105823 conv=1105824 p=1.00 :: @AmazonHelp It says "arriving today". But it's said that since Friday.
- id=1090892 conv=1090893 p=0.90 :: @AmazonHelp We were told it would be here yesterday before 9pm. It wasn't updated until after 9pm to

### Cluster 173
- id=2405232 conv=2405234 p=1.00 :: @AmazonHelp 14 minutes now.
- id=812430 conv=812426 p=0.90 :: @AmazonHelp 8 days is slightly ?
- id=388000 conv=387998 p=1.00 :: @AmazonHelp How much time it gonna take more? It's already two days.
- id=2405231 conv=2405234 p=0.91 :: @AmazonHelp 15 mins now.
- id=2852128 conv=2852131 p=1.00 :: @AmazonHelp sorry 16 days
- id=1127362 conv=1127368 p=1.00 :: @AmazonHelp Sorry, I don't know. approx 12 hrs but that is a rough guess.
- id=927499 conv=234205 p=1.00 :: @AmazonHelp Not one, but two. Within a span of 10 days
- id=1406581 conv=1406585 p=1.00 :: @AmazonHelp In the next 25 mins

### Cluster 174
- id=530005 conv=530009 p=0.93 :: @AmazonHelp Nooo, just that there may be a delay.
- id=930344 conv=930345 p=1.00 :: @AmazonHelp So what are the unforeseen circumstances that will cause up to a 2 day delay? Thanks.
- id=547946 conv=547944 p=1.00 :: @AmazonHelp no reason at all except there may be a delay
- id=2863459 conv=2863460 p=1.00 :: @AmazonHelp Yes, and what exactly is a “preditive delay?”
- id=438690 conv=438688 p=0.88 :: @AmazonHelp by today, any clue on how long the delay would be?
- id=2318022 conv=2318028 p=0.88 :: @AmazonHelp Just that it’s an unexpected delay. The same thing you said the other two times it’s bee
- id=547950 conv=547944 p=0.94 :: @AmazonHelp no just that it may be delayed a few days
- id=734062 conv=281324 p=1.00 :: @AmazonHelp Never expected such delay.

### Cluster 175
- id=910718 conv=910725 p=1.00 :: @AmazonHelp Yes same day
- id=281019 conv=281012 p=0.99 :: @AmazonHelp Yep yesterday then today
- id=2980878 conv=2980879 p=1.00 :: @AmazonHelp Today this morning
- id=2632930 conv=2632928 p=1.00 :: @AmazonHelp Today :)
- id=91366 conv=91376 p=0.78 :: @AmazonHelp Hier matin
- id=1247279 conv=1247276 p=1.00 :: @AmazonHelp Yes it was today.
- id=320339 conv=320341 p=0.94 :: @AmazonHelp Since morning
- id=2073928 conv=2073956 p=1.00 :: @AmazonHelp Yes this morning

### Cluster 176
- id=2192491 conv=2192493 p=1.00 :: @AmazonHelp Gracias! Ya lo hice esta tarde. Por eso se que es a raíz de la huelga de Cataluña y que 
- id=133742 conv=133762 p=1.00 :: @AmazonHelp Alles Klar, wenn Ihr es bis 20:00 Uhr heute nicht schafft, dann wäre auch von 06:00 Uhr 
- id=2736293 conv=2736294 p=1.00 :: @AmazonHelp Yes now it's coming tomorrow I'm not impressed.
- id=1633265 conv=1633266 p=1.00 :: @AmazonHelp I mean if you can get it hear today that would be quite lovely 😂 But maybe it will be he
- id=2790590 conv=2790592 p=0.99 :: @AmazonHelp Saying it's now expected tomorrow. Which is incredibly helpful as I'm out all day. Very 
- id=2321150 conv=2321143 p=1.00 :: @AmazonHelp Ok pero no tendrán el día exacto que llegue?
- id=1710802 conv=1710803 p=0.97 :: @AmazonHelp Yep. It’s sometime in the next few days. Helpful when I need it tomorrow morning
- id=448675 conv=448677 p=1.00 :: @AmazonHelp La poste. J'espère que ça arrivera demain ...

### Cluster 177
- id=666159 conv=130309 p=1.00 :: @AmazonHelp Me puedes ayudar si te paso el numero de guía y transportista?
- id=1420503 conv=1420507 p=1.00 :: @AmazonHelp Sim. Já entrei em contato com o suporte e estou em contato direto com a transportadora.
- id=1756016 conv=1756019 p=1.00 :: @AmazonHelp No me pone agencia de transporte
- id=530842 conv=530843 p=1.00 :: @AmazonHelp El problema es que siempre me. Pasa lo mismo en teoría el transportista es @4496 pero NO
- id=1734548 conv=1734546 p=1.00 :: @AmazonHelp Ya lo he reportado pero no me han solucionado nada... no poder hablar con el transportis
- id=753469 conv=753472 p=1.00 :: @AmazonHelp el transportista no se ha comunicado conmigo, ademas que sois vosotros los transportista
- id=76009 conv=76017 p=1.00 :: @AmazonHelp a transportadora nunca responde
- id=2613222 conv=2613225 p=1.00 :: @AmazonHelp no me ha llegado mensaje del transportista

### Cluster 178
- id=1773522 conv=1773523 p=1.00 :: @AmazonHelp Full message sent.
- id=2402330 conv=2402328 p=1.00 :: @AmazonHelp message sent thanks
- id=421903 conv=421904 p=1.00 :: @AmazonHelp I have sent you a direct message! thanks.
- id=2492189 conv=2492191 p=0.95 :: @AmazonHelp j'ai envoyé un message merci
- id=448304 conv=448305 p=0.87 :: @AmazonHelp Buenas noches, acabo de enviarlos a la plataforma un e-mail explicándoos todos, de todas
- id=1342557 conv=1342555 p=0.90 :: @AmazonHelp I’ve messaged you thank s
- id=1509882 conv=1509884 p=0.94 :: @AmazonHelp Danke euch. Habe eine Nachricht geschrieben.
- id=2771673 conv=2771674 p=1.00 :: @AmazonHelp Have sent you a message!

### Cluster 179
- id=21526 conv=21534 p=1.00 :: @AmazonHelp What nonsense is this???? Bank is saying we can not lodge such complain
- id=417246 conv=417251 p=1.00 :: @AmazonHelp Also there is still proof on my bank statement. I am just feeling as if I got stole from
- id=2611554 conv=2611557 p=1.00 :: @AmazonHelp Thanks, it did say I wouldn’t be charged but £40.99 went out my account yesterday (16th)
- id=139995 conv=139996 p=1.00 :: @AmazonHelp What it was is you have taken £1 out of my account when i had the exact money for the pr
- id=115877 conv=115883 p=1.00 :: @AmazonHelp It’s a functional issue with your website and the Store Card that your reps keep blaming
- id=972634 conv=972641 p=0.99 :: @AmazonHelp Hi PK, I was asked to 'wait out' the bank's 'pending auth' and see if it 'drops off on i
- id=2469445 conv=2469446 p=1.00 :: @AmazonHelp £116.61 extra has been taken from my account.
- id=1181465 conv=1181466 p=0.99 :: @AmazonHelp Laut Support bin ich in einer "Prüfung" und darf in der Zeit meine Bankkonten nicht benu

### Cluster 180
- id=507125 conv=507123 p=1.00 :: @AmazonHelp It’s hard to know if I was charged for it because I don’t know how much it cost
- id=744115 conv=744097 p=1.00 :: @AmazonHelp @115850 pls reply why I was charged in that case...
- id=838617 conv=838618 p=1.00 :: @AmazonHelp Being charged twice, being told that the first charge is simply an authorization charge 
- id=153679 conv=153681 p=1.00 :: @AmazonHelp and is the charge reimbursed?
- id=2686406 conv=2686408 p=1.00 :: @AmazonHelp 24.99 charged today 11/19, but I have not purchased anything.
- id=2722368 conv=2722365 p=1.00 :: @AmazonHelp but i just got an email saying i could list things, and i've been charged 19p for someth
- id=1177639 conv=1177640 p=1.00 :: @AmazonHelp I think i was charged for USA membership which is clearly not useful or something I did 
- id=2945493 conv=2945488 p=1.00 :: @AmazonHelp It is definitely a charge. It appeared on my bill. None of these charges were authorized

### Cluster 181
- id=1427852 conv=343895 p=1.00 :: @AmazonHelp Ich habe nun eine Zurücksendung angefordert per Hermes aber ich habe ausgewählt das ich 
- id=1013777 conv=1013771 p=1.00 :: @AmazonHelp found it and cancelled, in the meantime we thought the card had been hacked, and got a n
- id=2303884 conv=2303900 p=1.00 :: @AmazonHelp No. Each rep told me they basically had no idea why it was doing this and that it must b
- id=2731137 conv=2731142 p=1.00 :: @AmazonHelp I've just taken my credit card details off so hopefully won't be able to get charged for
- id=1279799 conv=1279796 p=1.00 :: @AmazonHelp I see my current credit card on file (plus two old expired ones), and I have a chance to
- id=972626 conv=972641 p=1.00 :: @AmazonHelp The bank DIDN'T decline the card. Look at the image. See that big yellow bar on the righ
- id=1959475 conv=1959467 p=1.00 :: @AmazonHelp Ok so i used my maybank visa debit card and have tried FOUR times to pay using it. The s
- id=2954536 conv=2954539 p=1.00 :: @AmazonHelp so i can't get something from someone's wishlist if my payment method isn't a credit car

### Cluster 182
- id=917016 conv=917022 p=1.00 :: @AmazonHelp Hi its been 3 days please check with the issue and provide me the Gift Card as promised.
- id=324225 conv=324226 p=1.00 :: @AmazonHelp So how can o get a gift card for someone in Europe?
- id=1206833 conv=1206830 p=1.00 :: @AmazonHelp there are a lot of gift cards which have been locked out. How would you help? https://t.
- id=2230055 conv=2230056 p=1.00 :: @AmazonHelp Can you help as I need to print this gift card within the next hour! 😫😫😫
- id=1127337 conv=1127327 p=1.00 :: @AmazonHelp i have gift card id how to get gift card code
- id=2956982 conv=2956983 p=1.00 :: @AmazonHelp Pre-loaded gift card
- id=350292 conv=348936 p=1.00 :: @AmazonHelp I had a gift card of 50k I hv not used an ur team is saying that it has been used.. how 
- id=2435971 conv=2435973 p=1.00 :: @AmazonHelp yes one more question how can I apply the gift card on your site?

### Cluster 183
- id=191617 conv=191616 p=1.00 :: @AmazonHelp I am not asking for refund, how do I pay and get my order without any hassle. Also, re-t
- id=1607901 conv=1607902 p=0.97 :: @AmazonHelp That's my issue my order status isn't updated with refund as of now even though I had re
- id=1080689 conv=1080691 p=0.94 :: @AmazonHelp You are not able to get me my order by tomorrow. Ur people said they are issuing refunds
- id=2832872 conv=2832876 p=1.00 :: @AmazonHelp No, I was asked to select the order and the problem with it, then it just gave me the op
- id=283531 conv=283084 p=0.93 :: @AmazonHelp I ain't got time for doing this shit daily, I'm cancelling my COD orders and provide me 
- id=2355282 conv=2355279 p=1.00 :: @AmazonHelp @115850 @115851 You are just telling me that my order is delivered. I have requested for
- id=985039 conv=985045 p=1.00 :: @AmazonHelp Now the order is showing it can't be delivered and refund is initiated. Disgusting
- id=313896 conv=313897 p=0.90 :: @AmazonHelp Do you interested in refund or not please don't try to teach me just cancel my order and

### Cluster 184
- id=448708 conv=448710 p=1.00 :: @AmazonHelp Yes they are the ones that gave the stupid advice to log into my account when it's locke
- id=380786 conv=380784 p=0.85 :: @AmazonHelp M nt able to login from my account. Its saying id already exists.
- id=2734289 conv=930264 p=0.91 :: @AmazonHelp Can't do it until you let me log in. And it's consistently taking 25 minutes to get your
- id=2877789 conv=2877770 p=0.93 :: @AmazonHelp Thanks for quick help. Able to access my account now :)
- id=2906703 conv=2906704 p=1.00 :: @AmazonHelp Well, the problem was with @115823 but I can't tell what occurred bc you locked me out o
- id=2909255 conv=2909256 p=0.80 :: @AmazonHelp Thank you thank you thank you thank you!! I just submitted the info and I really appreci
- id=279425 conv=279455 p=0.82 :: @AmazonHelp That what I wanted to know, what information thebwant to activate my account ??
- id=2273514 conv=2273510 p=1.00 :: @AmazonHelp Yeah I called them they told my account is unlocked BUT ITS NOT!!!

### Cluster 185
- id=1735165 conv=1735163 p=0.45 :: @AmazonHelp But I still haven’t revived an email.
- id=835810 conv=834849 p=0.52 :: @AmazonHelp I have not reverted to your e mail, and for sure I am not going to give you more time.
- id=21418 conv=21423 p=0.55 :: @AmazonHelp Somebody else’s, I don’t have any of their emails or anything, it’s really urgent becaus
- id=1227286 conv=1227284 p=0.43 :: @AmazonHelp I haven't received any new emails from @115821 after I shared my details on the twitter 
- id=69811 conv=69821 p=0.51 :: @AmazonHelp I have not received any mail s from your end. My mail I'd is __email__
- id=9786 conv=9784 p=0.58 :: @AmazonHelp Haven’t received that email
- id=986078 conv=986074 p=0.66 :: @AmazonHelp Hey I will email but I have now emailed 3 times and no one has helped me since July
- id=836892 conv=836876 p=0.46 :: @AmazonHelp nothing yet. this is annoying where you'l are not even able to send one email.

### Cluster 186
- id=1213335 conv=1213342 p=1.00 :: @AmazonHelp Is there no way of finding out if my parcel will definitely be delivery today or if it i
- id=1354493 conv=1354489 p=1.00 :: @AmazonHelp Still no parcel, contacted customer service at 5pm, promised a response to whether they 
- id=279208 conv=279213 p=1.00 :: @AmazonHelp I got the parcel tht was meant to be delivered last Saturday before 1pm, yesterday. Just
- id=206930 conv=206931 p=1.00 :: @AmazonHelp I appreciate that but I'm just concerned where my parcel is? It's been "out for delivery
- id=1662622 conv=1662614 p=1.00 :: @AmazonHelp I’m wasting no more time with this - if the parcel does not arrive today I will take leg
- id=2903482 conv=2903475 p=1.00 :: @AmazonHelp I've already just done that from an earlier tweet so I hope to hear off somebody fairly 
- id=562883 conv=562874 p=1.00 :: @AmazonHelp Was told the parcel would be here first thing still waiting on it received an email tell
- id=2319020 conv=2319022 p=1.00 :: @AmazonHelp Can you explain what happened to my particular parcel? The parcel was out for delivery a

### Cluster 187
- id=535162 conv=535164 p=1.00 :: @AmazonHelp Thanks submitted the feedback, please make sure I get a properly sealed replacement.
- id=307917 conv=307921 p=1.00 :: @AmazonHelp I got a replacement ordered. Thank you
- id=1497318 conv=1497319 p=1.00 :: @AmazonHelp Thank you. I have contacted and I will be receiving a replacement next week as this one 
- id=833922 conv=833916 p=1.00 :: @AmazonHelp I was promised a replacement before tomorrow early morning.Bt I don't see any updates on
- id=1868769 conv=1868767 p=1.00 :: @AmazonHelp If I am able to secure a replacement today then I intend to.
- id=1770173 conv=1770171 p=1.00 :: @AmazonHelp I already went online and requested a replacement but thanks.
- id=320885 conv=320883 p=1.00 :: @AmazonHelp yes i have requested for the replacement and do it ASAP
- id=619245 conv=134867 p=1.00 :: @AmazonHelp Revert on the link mentioned... Looking fwd for immediate replacement without further st

### Cluster 188
- id=1046680 conv=1046681 p=1.00 :: @AmazonHelp This doesn't appear to work, it still just directs me to return an item which I did not 
- id=1681736 conv=1681737 p=1.00 :: @AmazonHelp I sent the item back for return on 31/08/17 if that helps
- id=91300 conv=91303 p=1.00 :: @AmazonHelp There's really no good way to report that an item was missing. It asks if I want to retu
- id=2297429 conv=2297425 p=1.00 :: @AmazonHelp The link on my gift receipt on how to do a return didn't work (I even played with the la
- id=715452 conv=715453 p=1.00 :: @AmazonHelp I’m able to return the item but they refuse to send me a replacement
- id=584589 conv=584590 p=1.00 :: @AmazonHelp When I try to go through claim it says I need to agree to return the item. How can I ret
- id=306609 conv=306190 p=1.00 :: @AmazonHelp I have only one extra item that was delivered today of the 4 original items that I can r
- id=622421 conv=622423 p=1.00 :: @AmazonHelp Hi, spoke to CS they said I have to return it myself usin ArrowXL. However, the phone nu

### Cluster 189
- id=1617270 conv=1617271 p=1.00 :: @AmazonHelp Yup, got refunded but still frustrated with persistent @2150 issues. Also wasted 30 mins
- id=77353 conv=77354 p=1.00 :: @AmazonHelp I have requested a refund.
- id=467408 conv=467409 p=1.00 :: @AmazonHelp Yes i was offered a refund which didnt solve the problem and i actually didnt even get t
- id=67540 conv=67541 p=1.00 :: @AmazonHelp All been sorted. Thank you. My refund should be with me in the next few days😊
- id=829492 conv=829482 p=1.00 :: @AmazonHelp Refund received. Thanks. Had I not raised an alarm this money would have never come back
- id=167875 conv=167876 p=1.00 :: @AmazonHelp I'm on the call now - you are REFUSING TO SEND MY STUFF. Only a Refund? Sadly this can't
- id=128054 conv=128087 p=1.00 :: @AmazonHelp That I have done more than 100 times..where is refund
- id=1449093 conv=1449083 p=1.00 :: @AmazonHelp I’ve already spoken to someone and received a refund but this is too important an issue 

### Cluster 190
- id=159521 conv=159523 p=0.53 :: @AmazonHelp there was an email thank you
- id=1296268 conv=1296269 p=0.42 :: @AmazonHelp Emailed you! 👌🏼
- id=1124088 conv=1124091 p=0.43 :: @AmazonHelp Heute. Ja. Per Email.
- id=478477 conv=478480 p=0.42 :: @AmazonHelp Thanks I'll look forward to that email
- id=1539909 conv=1539905 p=0.43 :: @AmazonHelp Yes, this morning via email.
- id=2549519 conv=2549520 p=0.47 :: @AmazonHelp Bonjour, oui je l'ai transférer par email également :)
- id=2791873 conv=2791877 p=0.45 :: @AmazonHelp Yes and the email just came in thanks.
- id=1480139 conv=1480137 p=0.43 :: @AmazonHelp Allright I just emailed you. thx.

### Cluster 191
- id=927588 conv=927590 p=0.97 :: @AmazonHelp What's ur email id on which I should write my problem
- id=1905605 conv=1905606 p=0.88 :: @AmazonHelp Everything related to the following email id :- __email__
- id=33248 conv=33231 p=0.81 :: @AmazonHelp Nice! 1st email was sent to my registered id and then other ones in app, fooling around 
- id=605167 conv=605168 p=0.88 :: @AmazonHelp Mon email : __email__
- id=2884904 conv=2884906 p=0.89 :: @AmazonHelp To which email adderess shall i send the email in italian? I can write in italian i just
- id=2448261 conv=2448263 p=1.00 :: @AmazonHelp I forward it to __email__
- id=2260735 conv=2260737 p=1.00 :: @AmazonHelp __email__ is the email
- id=907016 conv=907023 p=1.00 :: @AmazonHelp My mail I'd __email__

### Cluster 192
- id=2416111 conv=2416112 p=1.00 :: @AmazonHelp It says it will be delivered today. It's been saying that since Friday so I don't really
- id=179612 conv=179616 p=1.00 :: @AmazonHelp It says it’s being delivered tomorrow x
- id=2576957 conv=2576958 p=0.93 :: @AmazonHelp Yeah, it was supposed to be delivered today and now it says they don’t know when they’ll
- id=11593 conv=11594 p=0.93 :: @AmazonHelp Done that. Was told I would definitely have it by 9pm yesterday &amp; it's still not bee
- id=1326895 conv=1326893 p=1.00 :: @AmazonHelp I was told it will be delivered today by 9 PM !
- id=2437254 conv=2437252 p=1.00 :: @AmazonHelp Says it was delivered Saturday. I'll check and see if they drop it off tomorrow.
- id=2721717 conv=2721718 p=0.97 :: @AmazonHelp It said it was going to be delivered by 8pm today. I even spoke to someone on the online
- id=559882 conv=559883 p=1.00 :: @AmazonHelp No it was due to be delivered yesterday the 2nd of December. I wouldn’t have tweeted if 

### Cluster 193
- id=1309600 conv=1309603 p=1.00 :: @AmazonHelp The original delivery date was for today, Thursday 10/26
- id=77339 conv=77335 p=0.91 :: @AmazonHelp Delivery date changed once again!!
- id=1359047 conv=1359045 p=0.92 :: @AmazonHelp Nope no new delivery date hence the frustration
- id=765789 conv=765790 p=0.84 :: @AmazonHelp Well the delivery date give to me was 24th November. Haven't got my delivery and now it'
- id=63874 conv=63890 p=1.00 :: @AmazonHelp But no-one can give me a revised delivery date.... that is all I wanted to know!
- id=347916 conv=347921 p=0.94 :: @AmazonHelp After then he show to 11 Oct delivery date . I request you to plz don't believe his deli
- id=2618124 conv=2618125 p=0.72 :: @AmazonHelp If you see the screenshot attached, you will realise that the delivery date was 1Nov and
- id=480300 conv=480302 p=0.89 :: @AmazonHelp took the screenshot before purchasing, the Delivery date is Wednesday.

### Cluster 194
- id=191603 conv=191609 p=1.00 :: @AmazonHelp Is there a cut off time for next day delivery
- id=2871647 conv=2871642 p=1.00 :: @AmazonHelp My two day delivery is now two days late. That’s some BS.
- id=1474779 conv=1474772 p=1.00 :: @AmazonHelp Hey, remember this? Yeah still on going. 2 more cancelled delivery dates. What are you d
- id=334890 conv=334891 p=1.00 :: @AmazonHelp Already tried that. Wait 36 hours to see if it shows up is unacceptable for same day del
- id=1079403 conv=1079401 p=1.00 :: @AmazonHelp This is two times in two weeks that same day delivery has not been on time.
- id=453272 conv=453275 p=1.00 :: @AmazonHelp @222548 I hear you. It seems that delivery schedules are way off. Something that is supp
- id=538606 conv=538607 p=1.00 :: @AmazonHelp Yes the delivery dates are being missed, in one instance by almost a week. I understand 
- id=538502 conv=538510 p=1.00 :: @AmazonHelp I have not. I've come to expect and accept that type of delivery delay this time of year

### Cluster 195
- id=1537553 conv=1537545 p=1.00 :: @AmazonHelp Ha! Here's what it says about the package today. Said it was out for delivery this morni
- id=968621 conv=968623 p=0.99 :: @AmazonHelp Why the fuck is it my responsibility to wait for that package? How dumb are you guys?? I
- id=361015 conv=361016 p=1.00 :: @AmazonHelp Lady Faire ordered this package September 30th and it just arrived today. Not the first 
- id=567561 conv=567564 p=0.98 :: @AmazonHelp I️ filled out the information. But you still haven’t told me if I️ can pick up my packag
- id=1347633 conv=1347634 p=0.99 :: @AmazonHelp It's 8pm. No delivery. Where's my package @115821 @115828 ???? https://t.co/zYJnntyMZ5
- id=91441 conv=91445 p=1.00 :: @AmazonHelp Good morning! Package didn't show up yesterday. Now have the attached showing. A bit con
- id=567551 conv=567564 p=1.00 :: @AmazonHelp I️ cannot wait until Wednesday for this package! I️ could have picked it up faster! This
- id=307887 conv=307883 p=0.97 :: @AmazonHelp I need to know what is happening with this package. I have no idea when it's coming, if 

### Cluster 196
- id=1953352 conv=1953346 p=1.00 :: @AmazonHelp still showing as today for delivery
- id=1734578 conv=1734579 p=1.00 :: @AmazonHelp It says out for delivery but it's said that since Friday
- id=334012 conv=334031 p=1.00 :: @AmazonHelp Still says it’s out for delivery and has been for the last 10 hours
- id=2304434 conv=2304430 p=1.00 :: @AmazonHelp Still showing out for delivery from yesterday.
- id=1561943 conv=1561944 p=1.00 :: @AmazonHelp Still says out for delivery, last updated at 11:29am yesterday.
- id=2220948 conv=2220950 p=1.00 :: @AmazonHelp It says the same as it has for the last 8 days “out for delivery”
- id=1659007 conv=1659003 p=1.00 :: @AmazonHelp It’s says out for delivery today
- id=332423 conv=332424 p=1.00 :: @AmazonHelp Yes expected on the 5th still showing out for delivery

### Cluster 197
- id=1631312 conv=1631313 p=0.87 :: @AmazonHelp I already have it that if I’m not in, to deliver to neighbour but instead it was left ne
- id=2944369 conv=2944371 p=0.71 :: @AmazonHelp Will follow up tomorrow as it was at industrial site and we were closed today. Neighbour
- id=1369569 conv=1369570 p=0.76 :: @AmazonHelp yep! apparently got delivered to the wrong apartment or person
- id=2849026 conv=2849028 p=0.61 :: @AmazonHelp I live in a block of flats so leaving it next to my front door is a poor choice really, 
- id=67492 conv=67507 p=0.75 :: @AmazonHelp Downstairs my building unattended and it keeps happening and yes I was home - on one occ
- id=1445452 conv=1445455 p=0.73 :: @AmazonHelp My front door is directly to the left of my garage. Delivery is indicated as “back porch
- id=2889221 conv=2889199 p=0.65 :: @AmazonHelp A priori rien chez moi, je n’y suis pas mais ma mère n’a rien réceptionné et rien dans l
- id=2752024 conv=2752026 p=0.64 :: @AmazonHelp .com I am tired of going to neighbors porches to get my packages.

### Cluster 198
- id=358803 conv=358790 p=0.73 :: @AmazonHelp But your driver didn’t even come to the door at hence my frustration, let’s get my packa
- id=286253 conv=286254 p=0.75 :: @AmazonHelp can you ask driver to deliver item today as he did not ring or knock the door
- id=2094066 conv=2094067 p=0.63 :: @AmazonHelp It's fine, just found it funny that the driver put delivered to resident. It's all in wo
- id=189246 conv=189248 p=0.63 :: @AmazonHelp 30th of September. The driver stormed off angry after being asked who the parcel was for
- id=465801 conv=465802 p=0.68 :: @AmazonHelp Not saying yall are bad or want to get driver in trouble. Just was curious why no ring t
- id=1452912 conv=1452913 p=0.67 :: @AmazonHelp Done that twice. Got almost identical replies. Tracked driver on map, came close to my h
- id=1144134 conv=1144135 p=0.70 :: @AmazonHelp Your driver stole from me and i didnt receive my items
- id=434455 conv=434465 p=0.73 :: @AmazonHelp ah! Y el conductor literalmente me dijo q él sólo hacía turno de mañana y le dieron mi p

### Cluster 199
- id=2469391 conv=2469395 p=1.00 :: @AmazonHelp Just did that it keeps saying i only can watch stuff on the dam website if it still doin
- id=431628 conv=431629 p=1.00 :: @AmazonHelp So I need to cancel it? Wow!
- id=21102 conv=21100 p=1.00 :: @AmazonHelp Thanks for your help 🙄 I'll just cancel it
- id=2166562 conv=2166564 p=1.00 :: @AmazonHelp Ah no I think it's a kindle one so completely my mistake - I'll log on and cancel now, t
- id=1117989 conv=1117990 p=1.00 :: @AmazonHelp I'm going to have to cancel it.
- id=1021043 conv=1021044 p=1.00 :: @AmazonHelp I’ve cancelled it, it’s just a joke really
- id=1332117 conv=1332124 p=1.00 :: @AmazonHelp Cancelled
- id=304567 conv=304571 p=1.00 :: @AmazonHelp I actually need to cancel it because it need the item for a photoshoot tomorrow morning,

### Cluster 200
- id=854372 conv=854377 p=1.00 :: @AmazonHelp Cancel my order. You guys failed to understand the urgency of the situation. I don't nee
- id=348547 conv=348541 p=1.00 :: @AmazonHelp Finally order cancelled .. after all the drama
- id=1126127 conv=1126123 p=1.00 :: @AmazonHelp The only option I was given was "you can cancel your order if you don't want to wait"...
- id=1501809 conv=1501818 p=1.00 :: @AmazonHelp Cancelled the order but had a good chat.
- id=318618 conv=318619 p=1.00 :: @AmazonHelp Can I cancel the order?
- id=876300 conv=876301 p=1.00 :: @AmazonHelp “I've check your order and we cannot be able to change it to a Xbox version, and to make
- id=2633009 conv=2633010 p=1.00 :: @AmazonHelp Sorry sir but I cancelled my order i was disappointed. It was #HeartBroken moment for me
- id=96846 conv=96852 p=0.98 :: @AmazonHelp Still have heard nothing from you. Cancel the order. What a fucking joke.

### Cluster 201
- id=2292929 conv=2292931 p=0.68 :: @AmazonHelp Order number 114-1103849-5209821
- id=2882507 conv=2882508 p=0.65 :: @AmazonHelp It doesn’t say, order number is 026-8186667-6663554
- id=972719 conv=311013 p=0.57 :: @AmazonHelp ORDER # 403-7748261-3709940 id. now you will get my information. n tell the date when wi
- id=348669 conv=348657 p=0.63 :: @AmazonHelp ORDER NO #406-3971997-7415546 CT -09101222439 LAST WAS 6 SEPT NO DETAILS IN MY ACC NO TR
- id=227841 conv=227843 p=1.00 :: @AmazonHelp Order No 404-3398681-6013941
- id=331959 conv=331960 p=0.52 :: @AmazonHelp Chk order details 8650373360.. u will know how i was fooled
- id=2863467 conv=2863470 p=0.83 :: @AmazonHelp Order 204 7500565 3187547 if you’re interested but I have my doubts.
- id=814332 conv=814334 p=0.96 :: @AmazonHelp Here is the order number 112-1676920-8677027 good luck they haven't been much use to get

### Cluster 202
- id=976789 conv=976790 p=0.98 :: @AmazonHelp You have my order details... Stop asking for details and provide solution
- id=253968 conv=253964 p=0.99 :: @AmazonHelp Where is my order ?
- id=1511952 conv=1511965 p=0.96 :: @AmazonHelp I am getting a link to some other order..
- id=834857 conv=834858 p=1.00 :: @AmazonHelp Can I not just give you the order number? Because this isn’t the first time we’ve spoken
- id=153626 conv=153627 p=0.84 :: @AmazonHelp I have sent you a reply back via this link. Can you look into this ASAP please as the or
- id=276430 conv=276434 p=1.00 :: @AmazonHelp Please do it on priority basis, as i am stuck in placing the order.
- id=2832933 conv=2832934 p=0.91 :: @AmazonHelp I have gone through the order again and cannot see the option for this item please can y
- id=1674840 conv=1674841 p=1.00 :: @AmazonHelp Thank you - this order isn’t listed there?


> **Note:** these are tentative, unsupervised groupings. Cluster IDs are not business intents. No intent names ('delivery', 'refund', ...) are assigned yet.

## Diagnostics
{
  "n_rows": 93171,
  "n_clusters": 203,
  "n_noise": 49621,
  "noise_percentage": 53.257988000558115,
  "largest_cluster_size": 12267,
  "smallest_non_noise_cluster_size": 30,
  "median_cluster_size": 74.0,
  "cluster_size_quantiles": {
    "0.5": 74.0,
    "0.75": 157.0,
    "0.9": 341.6,
    "0.95": 550.9999999999998,
    "0.99": 1512.5199999999957
  },
  "mean_inter_cluster_cosine": 0.3020046353340149,
  "min_inter_cluster_cosine": -0.04996185377240181,
  "max_inter_cluster_cosine": 1.0
}