'''
To fucking many arguments to take them in da terminal :(
Can't figure out why so much information is shared since it
doesn't seem to be needed.
'''

# Private polynomial
poly = [13, 8, 11, 1, 5]

# Shares from other participants polynomials, i.e. f(1) for each
shares = [75, 75, 54, 52, 77, 54, 43]

# The sum of the two above becomes the first point, i.e. f(1)

# Points on the master polynomial from other participants (and private) on form (x, y)
points = [(1, sum(poly) + sum(shares)), (2, 2782), (4, 30822), (5, 70960), (7, 256422)]

result = 0

# For every point calculate Lagrange polynomial according to:
# L0 = (x - x1)(x - x2) ... (x - xn) / (x0 - x1)(x0 - x2) ... (x0 - xn)
# although x = 0 the whole time since we are only interested in the x^0 term.

for i in range(len(points)):
    numerator = 1
    denominator = 1
    for j in range(len(points)):
        if i is not j:
            numerator *= 0 - points[j][0]
            denominator *= points[i][0] - points[j][0]

    result += points[i][1] * numerator / denominator

# Gotta add .5 to round correctly, otherwise 109.99999999997817 is rounded down to 109.
print(int(result + .5))
