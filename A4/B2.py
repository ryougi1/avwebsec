import requests


url = "https://eitn41.eit.lth.se:3119/ha4/addgrade.php?name=Kalle&grade=5&signature="
chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
times = [0] * 16

for j in range(20): # Signature length (20 hex characters)
    for i in range(len(chars)):
        response = requests.get(url + chars[i], verify=False)
        times[i] = response.elapsed.total_seconds()
    url += chars[times.index(max(times))]
    print(url[len(url) - 1:])

print(requests.get(url, verify=False).text)
