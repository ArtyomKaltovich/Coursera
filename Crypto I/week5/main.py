from gmpy2 import *

p = mpz('13407807929942597099574024998205846127479365820592393377723561443721764030073546976801874298166903427690031858186486050853753882811946569946433649006084171')
g = mpz('11717829880366207009516117596335367088558084999998952205599979459063929499736583746670572176471460312928594829675428279466566527115212748467589894601965568')
h = mpz('3239475104050450443565264378728065788649097520952449527834792452971981976143292558073856937958553180532878928001494706097394108577585732452307673444020333')
B = mpz(2**20)
h_divided_by_g = divm(h, g, p)
g_pow_B = powmod(g, B, p)

x0 = x1 = 0

left_part = {}
for i in range(0, 2**20 + 1):
	left_part[divm(h, powmod(g, mpz(i), p), p)] =  i

for i in range(0, 2**20 + 1):
	key = powmod(g, mpz(i*B), p)
	if key in left_part:
		x0 = mpz(i)
		x1 = left_part[key]
		break

print(x0 * B + x1)