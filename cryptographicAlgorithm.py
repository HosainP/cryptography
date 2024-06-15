import conversion

# Permute function to rearrange the bits
def permute(k, arr, n):
	permutation = ""
	for i in range(0, n):
		permutation = permutation + k[arr[i] - 1]
	return permutation

# shifting the bits towards left by nth shifts


def shift_left(k, nth_shifts):
	s = ""
	for i in range(nth_shifts):
		for j in range(1, len(k)):
			s = s + k[j]
		s = s + k[0]
		k = s
		s = ""
	return k

# calculating xow of two strings of binary number a and b


def xor(a, b):
	ans = ""
	for i in range(len(a)):
		if a[i] == b[i]:
			ans = ans + "0"
		else:
			ans = ans + "1"
	return ans


def encrypt(pt, rkb, rk):
	pt = conversion.hex2bin(pt)

	# Splitting
	left = pt[0:32]
	right = pt[32:64]
	for i in range(0, 4):

		# XOR RoundKey[i] and right
		xor_x = xor(right, rkb[i])

		# XOR left and sbox_str
		result = xor(left, xor_x)
		left = result

		# Swapper
		if(i != 3):
			left, right = right, left
		print("Round ", i + 1, " ", conversion.bin2hex(left),
			" ", conversion.bin2hex(right), " ", rk[i])

	# Combination
	cipher_text = left + right

	return cipher_text


def encrypt_pt_key(pt, key):

	# Key generation
	key = conversion.hex2bin(key)

	# --parity bit drop table
	keyp = [57, 49, 41, 33, 25, 17, 9,
			1, 58, 50, 42, 34, 26, 18,
			10, 2, 59, 51, 43, 35, 27,
			19, 11, 3, 60, 52, 44, 36,
			63, 55, 47, 39, 31, 23, 15,
			7, 62, 54, 46, 38, 30, 22,
			14, 6, 61, 53, 45, 37, 29,
			21, 13, 5, 28, 20, 12, 4]

	# getting 56 bit key from 64 bit using the parity bits
	key = permute(key, keyp, 56)

	# Number of bit shifts
	shift_table = [1, 1, 2, 2,
				2, 2, 2, 2,
				1, 2, 2, 2,
				2, 2, 2, 1]

	# Key- Compression Table : Compression of key from 56 bits to 48 bits
	key_comp = [14, 17, 11, 24, 1, 5,
				3, 28, 15, 6, 21, 10,
				23, 19, 12, 4, 26, 8,
				16, 7, 27, 20, 13, 2,
				41, 52, 31, 37, 47, 55,
				30, 40, 51, 45, 33, 48,
				44, 49, 39, 56, 34, 53,
				46, 42, 50, 36, 29, 32]

	# Splitting
	left = key[0:28] # rkb for RoundKeys in binary
	right = key[28:56] # rk for RoundKeys in hexadecimal

	rkb = []
	rk = []
	for i in range(0, 4):
		# Shifting the bits by nth shifts by checking from shift table
		left = shift_left(left, shift_table[i])
		right = shift_left(right, shift_table[i])

		# Combination of left and right string
		combine_str = left + right

		# Compression of key from 56 to 32 bits
		round_key = permute(combine_str, key_comp, 32)

		rkb.append(round_key)
		rk.append(conversion.bin2hex(round_key))

	print("Encryption")
	cipher_text = conversion.bin2hex(encrypt(pt, rkb, rk))
	print("Cipher Text : ", cipher_text)
	print("----------------------------------------------------------------")
	print("Decryption")
	rkb_rev = rkb[::-1]
	rk_rev = rk[::-1]
	text = conversion.bin2hex(encrypt(cipher_text, rkb_rev, rk_rev))
	print("Plain Text : ", text)
