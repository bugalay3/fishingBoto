balance = 0
rate = 80
rate = rate / 365 / 100
days = 30
inf = 20 
inf = inf / 365 / 100
dollarRate = 115

spentUSD = 0
ptn = 0

topupRUB = 1000

for i in range(days):
    ptn += (topupRUB * (inf*i))
    topupUSD = (topupRUB - (topupRUB * (inf*i))) / dollarRate
    spentUSD += topupUSD
    balance += topupUSD
    balance = balance + (balance * rate)
    print(f'баланс день {i+1}: ${round(balance, 2)}')

totalPlusUSD = balance-spentUSD

print('')

print(f'инфляция сажрала: ${round(ptn / dollarRate, 2)}')

print('')

print(f'итого плюс: ${round(totalPlusUSD, 2)}\n')