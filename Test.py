import decimal

x = {1, 2, 34, 4}
y = {2, 3, 67, 8, 4}
# set intersection
print(y & x)

x = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four'}
for k, v in x.items():
    print(k, v, sep=':-', end=';')
print('')
z = 0.1 + 0.1 + 0.1 - 0.3
print(z)

z1 = decimal.Decimal("0.1") + decimal.Decimal("0.1") + decimal.Decimal("0.1") - decimal.Decimal("0.3")
print(z1)

print('a'+'b'
+'c')
