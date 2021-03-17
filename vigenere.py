import numpy as np
import string
LETTER_FREQ = [0.08167, 0.01492, 0.02202, 0.04253, 0.12702, 0.02228, 0.02015,
               0.06094, 0.06966, 0.00153, 0.01292, 0.04025, 0.02406, 0.06749,
               0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09356, 0.02758,
               0.00978, 0.02560, 0.00150, 0.01994, 0.00077]
ASSIGN_CRYPTOGRAM = "UTAHELHUSBXLZAZYMVXXGELAUOGDTEMOQRTUKGHCQRGTQNMUATMVASMYANZMARMOQLBIQRMPQSHMUTLWQOISQCTUNELADOGNQNHBSHMVYABUFABUUTLLJILAQNVLUNZYQAMLYEKNQNVPQSHUFHBZBOBUFTALBRXZQNMYQBXSXIHUNRHBSHMVGRKLBUUSUCMVMSXCQRXAQSMHZDMOQPKLEIWLZTBHXEELOTBVZOVJGRKPZGBUDEZBXAKJAUKZQDNYUNZATEKLNEESUOGHPDXKZOMHXIMAXEMVFHXZFRTPZTALETKPREHMFHXLXEVAUOGPEBNATUFHZNTAGRXWDAVAUCTSXYTWBLBLPTHATEYHOTLPZTALOALL"


def encrypt(b: str, k: str) -> str:
    def caesar_e(b, k):
        c = np.zeros(len(b), dtype=int)
        for i in range(len(b)):
            c[i] = (ord(b[i]) + ord(k[0]) - 2 * ord('A')) % 26 + ord('A')
        return c

    cryptogram = np.zeros(len(b), dtype=int)
    plaintext = list(b)

    # Encrypt each letter with Caesar cypher corresponding to the key
    for i in range(len(b)):
        cryptogram[i] = caesar_e(plaintext[i], k[i % len(k)])

    return ''.join(chr(i) for i in cryptogram)


def decrypt(c: str, k: str) -> str:
    def caesar_d(b, k):
        c = np.zeros(len(b), dtype=int)
        for i in range(len(b)):
            c[i] = (ord(b[i]) - ord(k[0]) - 2 * ord('A')) % 26 + ord('A')
        return c

    plaintext = np.zeros(len(c), dtype=int)
    cryptogram = list(c)

    # Decrypt each letter with Caesar cypher corresponding to the key
    for i in range(len(c)):
        plaintext[i] = caesar_d(cryptogram[i], k[i % len(k)])

    return ''.join(chr(i) for i in plaintext)


def calculate_ko(ciphertext):
    # calculate ciphertext letter frequencies
    N = len(ciphertext)
    nis = np.zeros(26)
    for i, k in zip(range(26), list(string.ascii_uppercase)):
        nis[i] = ciphertext.count(k)
    ko = 0
    for i in range(26):
        ko += nis[i] * (nis[i]-1)
    return ko / (N * (N-1))


# https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher#Friedman_test
def estimate_key_length(ciphertext):
    kp = 0.067
    kr = 0.0385
    ko = calculate_ko(ciphertext)
    length_estimate = (kp - kr) / (ko - kr)
    return length_estimate


def calculate_letter_distribution(text, key):
    def caesar_d(b, k):
        c = np.zeros(len(b), dtype=int)
        for i in range(len(b)):
            c[i] = (ord(b[i]) - ord(k[0]) - 2 * ord('A')) % 26 + ord('A')
        return ''.join(chr(i) for i in c)

    # Decrypt from caesar and calculate letter distribution
    ptext = caesar_d(text, key)

    nis = np.zeros(26)
    for i, k in zip(range(26), list(string.ascii_uppercase)):
        nis[i] = ptext.count(k) / len(ptext)
    return nis


def crack_caesar(ciphertext):
    # Frequency analysis - find the best candidate for the key
    keys = np.zeros(26)
    for i, k in zip(range(26), list(string.ascii_uppercase)):
        distribution = calculate_letter_distribution(ciphertext, k)
        keys[i] = sum(np.square(distribution - LETTER_FREQ))

    # Return the best (best distribution match) key candidate
    return list(string.ascii_uppercase)[np.argmin(keys)]


def crack_vigenere(ciphertext):
    # Estimate key length
    key_len = round(estimate_key_length(ciphertext)-1)

    # Crack key_len (key-length) separate caesar cyphers by frequency analysis
    key_estimate = ''
    for i in range(key_len):
        subsequence = ciphertext[i::key_len]
        key_estimate += crack_caesar(subsequence)

    return key_estimate


if __name__ == "__main__":
    # Test encryption and decryption
    print(encrypt("VNAPAD", "ABC"))
    print(decrypt("VOCPBF", "ABC"))

    # Test subroutines
    print(estimate_key_length(ASSIGN_CRYPTOGRAM))
    print(crack_caesar("OXQVSCRDOHDPYBCYWODRSXQDYDKVVIBKXNYWNOMBIZDSXQDOHDKXNCDEPPGYBNCKBOSXOXQVSCR"))

    # Crack the assignment criptogram
    print(crack_vigenere(ASSIGN_CRYPTOGRAM))
    print(decrypt(ASSIGN_CRYPTOGRAM, crack_vigenere(ASSIGN_CRYPTOGRAM)))























