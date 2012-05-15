set term postscript eps enhanced color
set output "nocalnonorm.eps"
set xlabel "k" font "Times-Roman, 16"
set ylabel "Root Mean Square Error (RMSE)" font "Times-Roman, 16"
set yrange [1.1:1.45]
set xtics font "Times-Roman, 12"
set ytics font "Times-Roman, 12"
set yrange [0.8:1.4]
set grid
set nokey
#set key 600, 45
#set key spacing 3.0
set pointsize 1.5
plot  "nocalnonorm.dat" using 1:2 with linespoints lw 5 lt 1
