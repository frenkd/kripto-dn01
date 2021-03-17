import numpy as np
import string

LETTER_FREQ = [0.08167, 0.01492, 0.02202, 0.04253, 0.12702, 0.02228, 0.02015,
               0.06094, 0.06966, 0.00153, 0.01292, 0.04025, 0.02406, 0.06749,
               0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09356, 0.02758,
               0.00978, 0.02560, 0.00150, 0.01994, 0.00077]
alphabet = list(string.ascii_uppercase)
ASSIGNMENT_CRIPTOGRAM = 'STSQALWTCJMIJMTHNFEBWZTVJWMRNNHPMFICJFNWSZSXGWPFHHAJFBNTWZTVTHIRMRCGVRJTAFXBWDIVMFWSNSTVLXIRACANWLYSIYVPJQMQNFLNMRPXSBHMWNJTIYNSZNHPHPIMNZDRWBPPNSHMSBUJMUHZXJHMWPSQHHJBMHHMWMJTAFXBWDICVETVLXIRANXFVETVUDWUHBWHEBMBSXHMWEEEHMANWUJUWWHAWWSNWZMLJXVXHWTVJTZZICACHHJTNWWTZRHWWTIYJSSUWSNSTVLWWWWHHPNSTVSNWWIYNSSOPFHMWEWHMHHMWNJTIYNSXPCQJTOQYFPBQKHMWEWHMHHMWNACHRNWHMWBSZWSIOGIICVETVLWWWWHHXANZRVZYWXUMVWZHDJHXAANHRUQZZOUNBTZTJFNSBUUMBVZSTTLHZXNWDTZELTVPPAJWTICVETVNNHPMFVZYWXUTVXBAJSQIUWWMHHMWNACHTGCTJIRGFCGVGSBYAPQITSDWISVPPNNZMWCIRMSFRSXHMWZEENFGDVBMHSYOYJHPBHLANXNNZVOSUSANTCVTVUMPSIATHYFAHEGCSPBWKNZMFWUYFIKXBMHHMWAAZWGJJAHSSWKVJANANXFVMAFSENLHMWBLZNDHMSBUJMNALWUFRSXWDMFWSVBTHLLJTYOSQWHYAGJHDJTXNNSTVMXTVJH'


def encrypt(plaintext, key):
    # Create the matrix key
    key = (4*key)[:4] # Enlengthen the key if its too short (might break, nonsingular matrix)
    key_matrix = np.zeros((2,2))
    key_matrix[0,0] = ord(key[0]) - ord('A')
    key_matrix[0,1] = ord(key[1]) - ord('A')
    key_matrix[1,0] = ord(key[2]) - ord('A')
    key_matrix[1,1] = ord(key[3]) - ord('A')

    # Reshape the plaintext
    n = len(plaintext)
    n_ext = n + (len(key) - (n % len(key))) if n % len(key) != 0 else n
    plainmatrix = np.zeros(n_ext)  # Add enough letters to match the key size
    for i, c in zip(range(n), plaintext):
        plainmatrix[i] = ord(plaintext[i]) - ord('A')
    plainmatrix = plainmatrix.reshape((2, len(plainmatrix)//2), order='F')

    # Encrypt the text (matrix multiplication)
    cyphermatrix = np.dot(key_matrix, plainmatrix)

    # Reshape the cyphertext back into a string
    cyphermatrix = cyphermatrix.reshape(-1, order='F')
    cyphertext = ''
    for i in range(n_ext):
        cyphertext += chr(int(cyphermatrix[i]) % 26 + ord('A'))

    return cyphertext


def decrypt(cypher_text, key='ABBA', key_inverse=None):

    if key_inverse is None:
        # Create the matrix key
        key = (4 * key)[:4]
        a = ord(key[0]) - ord('A')
        b = ord(key[1]) - ord('A')
        c = ord(key[2]) - ord('A')
        d = ord(key[3]) - ord('A')

        # Calculate inverse for decryption
        det = (a*d - b*c) % 26
        det_inv = pow(det, -1, 26)
        key_inverse = (det_inv * np.array([[d, -b], [-c, a]])) % 26

    # Reshape the cryptogram
    n = len(cypher_text)
    n_ext = n + (len(key) - (n % len(key))) if n % len(key) != 0 else n
    cypher_matrix = np.zeros(n_ext)
    for i, c in zip(range(n), cypher_text):
        cypher_matrix[i] = ord(c) - ord('A')
    cypher_matrix = cypher_matrix.reshape((2, len(cypher_matrix)//2), order='F')

    # Decrypt (mat multiply)
    plain_matrix = np.dot(key_inverse, cypher_matrix)

    # Reshape the cyphertext back into a string
    plain_matrix = plain_matrix.reshape(-1, order='F')
    plain_text = ''
    for i in range(n_ext):
        plain_text += chr(int(plain_matrix[i]) % 26 + ord('A'))

    return plain_text


def crack_hill_cipher(cipher_text):
    # Go through all keys and use frequency analysis to determine the best key

    # We can split the frequency analysis into 2 parts: odd and even (top and bottom row)
    c_even = cipher_text[0::2]
    c_odd = cipher_text[1::2]

    key_grades = np.ones((26, 26, 26, 26))

    # even (top part of key matrix)
    for ai, a in zip(range(26), alphabet):
        print(f'{ai}/26')
        for bi, b in zip(range(26), alphabet):
            for ci, c in zip(range(26), alphabet):
                for di, d in zip(range(26), alphabet):
                    try:
                        # check if invertible
                        det = (ai * di - bi * ci) % 26
                        det_inv = pow(det, -1, 26)
                        key_inverse = (det_inv * np.array([[di, -bi], [-ci, ai]])) % 26
                        # decrypt
                        plaintext = decrypt(cipher_text, f'{a}{b}{c}{d}', key_inverse)
                        # perform frequency analysis
                        dist = calculate_letter_distribution(plaintext)
                        # grade key pair
                        key_grades[ai,bi,ci,di] = compare_distributions(dist)
                    except:
                        continue

    # Best key candidate(s):
    best_key = np.argmin(key_grades)

    # keys = np.where(key_grades < (key_grades[np.unravel_index(best_key, (26, 26, 26, 26))] + 0.01))

    print("Found key")
    print(best_key)



def calculate_letter_distribution(text):
    nis = np.zeros(26)
    for i, k in zip(range(26), alphabet):
        nis[i] = text.count(k) / len(text)
    return nis


def compare_distributions(d1, d2=LETTER_FREQ):
    return sum(np.square(d1 - d2))


if __name__ == "__main__":
    # Test encryption and decryption
    # Adds as many 'A's as needed to make the length divisible by the key length
    print(encrypt("KRIPTOGRAFIJAHILL", "ZBJC"))
    print(decrypt("HUHYVRLKFKBMHODQPVAA", "ZBJC"))

    # Takes about 2 minutes to crack the cipher (Intel i5 2320@3.0Ghz, single core performance)
    # crack_hill_cipher(ASSIGNMENT_CRIPTOGRAM)

    # End result for cracking the code
    ai, bi, ci, di = np.unravel_index(16983, (26, 26, 26, 26))
    a = alphabet[ai]
    b = alphabet[bi]
    c = alphabet[ci]
    d = alphabet[di]

    # Original columns
    print(f'{ai} {bi} \n{ci} {di}')
    print(decrypt(ASSIGNMENT_CRIPTOGRAM, f'{a}{b}{c}{d}'))

    # Switched columns (correct one)
    print(f'{bi} {ai}\n{di} {ci}')
    print(decrypt(ASSIGNMENT_CRIPTOGRAM, f'{b}{a}{d}{c}'))