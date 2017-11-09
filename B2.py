""" Luhn Algorithm:
In this case, all card numbers have 16 digits, where the last digit is the check digit. Starting from the check digit
and moving left, double the value of every second digit. If the result of the doubling is greater than 9, subtract 9.
If value is unknown, in our case 'X', skip over it. Once done, take the sum of all the digits not including the check
digit.
In Luhn's algorithm, the check digit is calculated by subtracting the last digit of the sum (unit digit) from 10.
In this case, we are given the check digit, so find the unit digit by subtracting the check digit from 10. Know we know
what the last digit of sum+X should be. Find X by adding for all possible values in the range (0, 9) to the sum
and checking if then last digit matches the unit digit. """
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
