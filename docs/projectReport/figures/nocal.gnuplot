set term postscript eps enhanced color
set output "nocal.eps"
set xlabel "k" font "Times-Roman, 16"
set ylabel "Root Mean Square Error (RMSE)" font "Times-Roman, 16"
set yrange [0.9:1.25]
set xtics font "Times-Roman, 12"
set ytics font "Times-Roman, 12"
set yrange [0.8:1.4]
set grid
set nokey
#set key 600, 45
#set key spacing 3.0
set pointsize 1.5
set key
plot  "nocal.dat" using 1:2 title "With Normalization" with linespoints lw 5 lt 1, \
  "nocalnonorm.dat" using 1:2 title "Without Normalization" with linespoints lw 5 lt 3