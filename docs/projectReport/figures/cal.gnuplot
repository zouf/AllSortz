set term postscript eps enhanced color
set output "cal.eps"
set xlabel "k" font "Times-Roman, 16"
set ylabel "Root Mean Square Error (RMSE)" font "Times-Roman, 16"
set yrange [0.9:1.25]
set xtics font "Times-Roman, 16"
set ytics font "Times-Roman, 16"
set yrange [0.8:1.5]
set grid
set nokey
#set key 600, 45
#set key spacing 3.0
set pointsize 1.5
set key
plot  "cal.dat" using 1:2 with linespoints lw 5 lt 1 title "All California Businesses",\
	 "calfood.dat" using 1:2 with linespoints lw 5 lt 2 title "Food-related California Businesses"
	
