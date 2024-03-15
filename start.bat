PUSHD .
python "autodarts-pixelit.py" ^
-CON "127.0.0.1:8079" ^
-PEPS "your-first-pixelit-ip" "your-secondary-pixelit-ip" ^
-TP "absolute-path-to-your-template-files" ^
-BRI "255" ^
-HFO "51" ^
-HF "x" ^
-AS "call|Lets Play Darts -==-<" ^
-IDE "board|throw" ^
-G "board" ^
-M "board" ^
-B "dart|d:200|b:10" "dart0|d:200|b:20" "dart1|d:200|b:30" "dart2|d:200|b:40" "dart3|d:200|b:50" "dart4|d:200|b:60" "dart5|d:200|b:70" "dart6|d:200|b:80" "dart7|d:200|b:90" "dart8|d:200|b:100" "dart9|d:200|b:110" "dart10|d:200|b:120" "dart11|d:200|b:130" "dart12|b:140" ^
-PJ "board|b:255" ^
-PL "board" ^
-S3 "points|b:3" ^
-S60 "points|b:10" ^
-A1 "0-179" "points" ^
-DEB "1"