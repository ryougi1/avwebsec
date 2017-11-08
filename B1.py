
#def calcSum(cardNr):
cardNr = [1, 2, 7, 7, 4, 2, 1, 2, 8, 5, 7, 'X', 4, 1, 0, 9]
sum = 0
checkDigit = cardNr[-1]
counter = 0

"""
Luhn Algorithm:
In this case, all card numbers have 16 digits, where the last digit is the check digit. Starting from the check digit 
and moving left, double the value of every second digit. If the result of the doubling is greater than 9, subtract 9. 
If value is unknown, in our case 'X', skip over it. Once done, take the sum of all the digits not including the check
digit. 

In Luhn's algorithm, the check digit is calculated by subtracting the last digit of the sum (unit digit) from 10. 
In this case, we are given the check digit, so find the unit digit by subtracting the check digit from 10. Know we know 
what the last digit of sum+X should be. Find X by adding for all possible values in the range (0, 9) to the sum
and checking if then last digit matches the unit digit.     
"""
for i in range (0, 15):
    if cardNr[i] == 'X':
        counter += 1
    elif counter % 2 == 0:
        cardNr[counter] = cardNr[counter] * 2
        if cardNr[counter] > 9:
            cardNr[counter] = cardNr[counter] - 9

        sum += cardNr[counter]
        counter += 1
    else:
        sum += cardNr[counter]
        counter += 1

print("Sum =", sum, "+ X")
unitDigit = 10-checkDigit
print("Unit digit = 10 -", checkDigit, "=", unitDigit)
for j in range (0, 10):
    secondSum = sum + j
    if secondSum % 10 == unitDigit:
        print("X =", j, "gives sum =", sum+j, "mod10 = 1 = unit digit")











