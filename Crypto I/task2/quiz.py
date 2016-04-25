def hex2(n):
     return hex (n & 0xffffffff)

#3
s = 2**128
count_devices = 4 * 10**12 / 200
count_keys = count_devices * 10**9
print (s/count_keys/86400/365)

#4
x = int("290b6e3a", 16)
print (hex2(~x))
x = int("5f67abaf", 16)
print (hex2(~x))
x = int("9d1a4f78", 16)
print (hex2(~x))
x = int("7b50baab", 16)
print (hex2(~x))

#8
print(len('The significance of this general conjecture, assuming its truth, is \
easy to see. It means that it may be feasible to design ciphers that \
are effectively unbreakable.'))
print(len('The most direct computation would be for the enemy to try \
all 2^r possible keys, one by one.'))
print(len('If qualified opinions incline to believe in the exponential \
conjecture, then I think we cannot afford not to make use of it.'))
print(len('In this letter I make some remarks on a general principle \
relevant to enciphering in general and my machine.'))
