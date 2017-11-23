from __future__ import print_function
import sys
import random
import math

nr_coins = 0
c = int(sys.argv[1])
u = pow(2, int(sys.argv[2]))
k = int(sys.argv[3])
samples = int(sys.argv[4])
width = int(sys.argv[5])

bins = [0] * u
iterations = 0
mean = 0
minimum = 0
maximum = 0

for i in range(0, samples):
    while nr_coins < c:
        n = random.randint(0, u - 1)
        bins[n] += 1
        if bins[n] == k:
            nr_coins += 1
        iterations += 1
    mean += iterations
    if iterations < minimum:
        minimum = iterations
    if iterations > maximum:
        maximum = iterations
    nr_coins = 0
    iterations = 0
    bins = [0] * u

std_deviation = math.sqrt(maximum - minimum)
if (3.66 * std_deviation / math.sqrt(samples)) > width:
    print("Outside of confidence interval!")
else:
    print("Mean number of iterations:", mean / samples)
