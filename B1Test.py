def number_sum(figure):
    nums = str(figure)
    nums = list(map(lambda n_str: int(n_str), nums))
    return sum(nums)

def calculate_unknown_value(missing, unknownValue):
    # Om det måste specialhanteras
    if missing % unknownValue["multiplier"] != 0:
        before_multiplier = 10 + (missing - 1)
        value = before_multiplier / unknownValue["multiplier"]
    else:
        value = missing / unknownValue["multiplier"]

    return int(value)

file = open("cardnr", "r")

result = ""
for input in file:
    input = input.strip()
    values = []
    currentMultiplier = 2
    unknownValue = {}
    for char in input[::-1]:
        currentMultiplier = 2 if currentMultiplier == 1 else 1
        try:
            val = int(char)
        except ValueError:
            val = None
            unknownValue = {
                "value": None,
                "multiplier": currentMultiplier
            }
            continue
        values.append({
            "value": val,
            "multiplier": currentMultiplier
        })

    # Multiply
    values = list(map(lambda val: val["value"] * val["multiplier"], values))

    # Numbersum all results
    values = list(map(lambda num: number_sum(num), values))

    # Calculate total sum
    total_sum = sum(values)

    # Calculate missing value
    rest = total_sum%10
    missing_value = 10 - rest if rest != 0 else 0

    value = calculate_unknown_value(missing_value, unknownValue)
    result += str(value)

print(result)
