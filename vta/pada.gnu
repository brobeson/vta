#!/usr/bin/gnuplot

# vim: nospell

# This graphs the function used in the gradient reverse layer in TMFT. See the
# paper for a full explanation of the function.

set xlabel 'Training Iteration'
set ylabel 'Gradient Scalar'
set grid x y

h = 1.0
l = 0.0
a = 10.0
I = 100.0
f(x) = (2.0 * (h - l)) / (1.0 + exp(-a * x / I)) - h + 2 * l
plot [0:I] f(x)
pause -1
