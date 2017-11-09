
""" Luhn Algorithm:
In this case, all card numbers have 16 digits, where the last digit is the check digit. Starting from the check digit 
and moving left, double the value of every second digit. If the result of the doubling is greater than 9, subtract 9. 
If value is unknown, in our case 'X', skip over it. Once done, take the sum of all the digits not including the check
digit. 
In Luhn's algorithm, the check digit is calculated by subtracting the last digit of the sum (unit digit) from 10. 
In this case, we are given the check digit, so find the unit digit by subtracting the check digit from 10. Know we know 
what the last digit of sum+X should be. Find X by adding for all possible values in the range (0, 9) to the sum
and checking if then last digit matches the unit digit. """

class Luhn:
    cardNr = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    def __init__(self, cardNr):
        self.cardNr = cardNr

    def calc_check_digit(self, cardNr):
        cardNr = cardNr
        #print(cardNr)
        sum = 0
        for i in range(0, 15):
            if i % 2 == 0:
                cardNr[i] = cardNr[i] * 2
                if cardNr[i] > 9:
                    cardNr[i] = cardNr[i] - 9
                sum += cardNr[i]
            else:
                sum += cardNr[i]
        #print("Sum =", sum)
        #print("10 - unit digit =", 10-(sum % 10), "= check digit")
        print(10-(sum%10), end="")
        #print(10 - (sum % 10))

    def calc_card_number(self, cardNr):
        cardNr = cardNr
        #print(cardNr)
        sum = 0
        checker = None
        checkDigit = cardNr[-1]

        for i in range(0, 15):
            if i % 2 == 0:
                if cardNr[i] == 'X':
                    #cardNr[i] = '2X'
                    checker = True
                else:
                    cardNr[i] = cardNr[i] * 2
                    if cardNr[i] > 9:
                        cardNr[i] = cardNr[i] - 9
                    sum += cardNr[i]
            else:
                if cardNr[i] != 'X':
                    sum += cardNr[i]

        #print("Sum =", sum, "+ X")
        unitDigit = 10 - checkDigit
        if unitDigit == 10:
            unitDigit = 0
        #print("Unit digit = 10 -", checkDigit, "=", unitDigit)
        for j in range(0, 10):
            secondSum = sum + j
            if secondSum % 10 == unitDigit:
                if checker:
                    if j < 5 or j % 2 == 0:
                        print(int(j / 2), end="")
                        #print(int(j / 2))
                    else:
                        print(int((j+9)/2), end="")
                        #print(int((j + 9) / 2))
                else:
                    #print("X =", j, "gives sum =", sum + j, "mod10 = 1 = unit digit")
                    print(j, end="")
                    #print(j)


file = open('cardnrlistjames', 'r')
cardsCounted = 0
for line in file:
    cardsCounted += 1
    cardNrString = list(line)
    cardNr = []
    for k in range (0, 16):
        try:
            cardNr.insert(k, int(cardNrString[k]))
        except ValueError:
            cardNr.insert(k, cardNrString[k])

    Luhn1 = Luhn(cardNr)
    if cardNr[-1] == 'X':
        Luhn1.calc_check_digit(cardNr)
    else:
        Luhn1.calc_card_number(cardNr)


