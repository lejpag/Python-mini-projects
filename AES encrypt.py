"""The purpose of this code is encrypt a plain text using AES-256

Standard documentation :
https://nvlpubs.nist.gov/nistpubs/fips/nist.fips.197.pdf

The above publication will be refered to as "the standard" throughout this code.

The code follows the notations and naming conventions of the standard.

start date 21.10.2022
end date 27.10.2022
"""
# VARIABLES

# Nk is the number of 32-bit words (or column) of the cipher key, in our case 256 = 8 x 32.
Nk = 8

# Nb is the number of 32-bit words (or column) of the AES blocks, which are 128-bit blocks.
Nb = 4

# Nr is the number of rounds, that can be 10, 12 and 14, in our case (AES-256) Nr = 14
Nr = 14

# S-Box is the substitution table used in SubBytes() method
# It works as follow, substitution of {53} is equal to SBOX[5][3]

SBOX = [
[0x63,0x7c,0x77,0x7b,0xf2,0x6b,0x6f,0xc5,0x30,0x01,0x67,0x2b,0xfe,0xd7,0xab,0x76],
[0xca,0x82,0xc9,0x7d,0xfa,0x59,0x47,0xf0,0xad,0xd4,0xa2,0xaf,0x9c,0xa4,0x72,0xc0],
[0xb7,0xfd,0x93,0x26,0x36,0x3f,0xf7,0xcc,0x34,0xa5,0xe5,0xf1,0x71,0xd8,0x31,0x15],
[0x04,0xc7,0x23,0xc3,0x18,0x96,0x05,0x9a,0x07,0x12,0x80,0xe2,0xeb,0x27,0xb2,0x75],
[0x09,0x83,0x2c,0x1a,0x1b,0x6e,0x5a,0xa0,0x52,0x3b,0xd6,0xb3,0x29,0xe3,0x2f,0x84],
[0x53,0xd1,0x00,0xed,0x20,0xfc,0xb1,0x5b,0x6a,0xcb,0xbe,0x39,0x4a,0x4c,0x58,0xcf],
[0xd0,0xef,0xaa,0xfb,0x43,0x4d,0x33,0x85,0x45,0xf9,0x02,0x7f,0x50,0x3c,0x9f,0xa8],
[0x51,0xa3,0x40,0x8f,0x92,0x9d,0x38,0xf5,0xbc,0xb6,0xda,0x21,0x10,0xff,0xf3,0xd2],
[0xcd,0x0c,0x13,0xec,0x5f,0x97,0x44,0x17,0xc4,0xa7,0x7e,0x3d,0x64,0x5d,0x19,0x73],
[0x60,0x81,0x4f,0xdc,0x22,0x2a,0x90,0x88,0x46,0xee,0xb8,0x14,0xde,0x5e,0x0b,0xdb],
[0xe0,0x32,0x3a,0x0a,0x49,0x06,0x24,0x5c,0xc2,0xd3,0xac,0x62,0x91,0x95,0xe4,0x79],
[0xe7,0xc8,0x37,0x6d,0x8d,0xd5,0x4e,0xa9,0x6c,0x56,0xf4,0xea,0x65,0x7a,0xae,0x08],
[0xba,0x78,0x25,0x2e,0x1c,0xa6,0xb4,0xc6,0xe8,0xdd,0x74,0x1f,0x4b,0xbd,0x8b,0x8a],
[0x70,0x3e,0xb5,0x66,0x48,0x03,0xf6,0x0e,0x61,0x35,0x57,0xb9,0x86,0xc1,0x1d,0x9e],
[0xe1,0xf8,0x98,0x11,0x69,0xd9,0x8e,0x94,0x9b,0x1e,0x87,0xe9,0xce,0x55,0x28,0xdf],
[0x8c,0xa1,0x89,0x0d,0xbf,0xe6,0x42,0x68,0x41,0x99,0x2d,0x0f,0xb0,0x54,0xbb,0x16]
]

Rcon = ["",0x01000000,0x02000000,0x04000000,0x08000000,0x10000000,0x20000000,0x40000000]

ans1 = input("Please enter plain text in hex or skip:")
if ans1 : 
    print("Thanks, the below value will be used as plain text:")
    print(ans1)
    PLAINTEXT = int("0x"+ans1,16)
else :
    print("The below default value will be used as plain text:") 
    PLAINTEXT = 0x00112233445566778899aabbccddeeff
    print(hex(PLAINTEXT)[2:])

ans2 = input("Please enter key in hex (256-bit) or skip:")
if ans2 :
    KEY = ans2
else :
    print("The below default value will be used as key:")
    KEY = 0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
    print(hex(KEY)[2:])


state = [["" for j in range(Nb)] for i in range(Nb)]

# Filling the state variable with initial content

def Input(plaintext):
    plaintext = hex(plaintext)[2:]
    plaintext = "0" * (32 - len(plaintext)) + plaintext
    for j in range(Nb):
        for i in range(Nb):
            state[i][j] = int(plaintext[2 * i + 8 * j : 2 * (i + 1) + 8 * j],16)

Input(PLAINTEXT)

# Output fonction to print the state in a hex string

def Output(state):
    output=""
    for j in range(Nb):
        for i in range(Nb):
            val = state[i][j]
            val = hex(val)[2:]
            if len(val) == 1 : val = "0" + val
            output = output + val
    print(output)

# Cipher Round function methods

# SubBytes

def SubBytes(state): #method not tested
    for i in range(Nb):
        for j in range(Nb):
            val = state[i][j]
            val = hex(val)[2:]
            if len(val) == 1: val = "0" + val
            x,y = int(val[0],16),int(val[1],16)
            state[i][j] = SBOX[x][y]

# ShiftRows

def ShiftRows(state):
    state[1] = [state[1][1],state[1][2],state[1][3],state[1][0]]
    state[2] = [state[2][2],state[2][3],state[2][0],state[2][1]]
    state[3] = [state[3][3],state[3][0],state[3][1],state[3][2]]

# xtime is a byte level operating function described in the Standard

def xtime(byte):
    # string conversion to manipulate bits
    byte = bin(byte)[2:]
    byte = "0" * (8 - len(byte)) + byte
    first_bit = byte[0]
    # left shift
    byte = byte[1:] + "0"
    # and now back to number format
    byte = int(byte,2)
    # conditionnal XOR with {1b}
    if first_bit == "1" :
        byte = byte ^ 0x1b
    return byte

# MixColums operates on columns of the state (32-bit words)
# Formulas are derived from the standard
# provided that {03}.s = s + xtime(s)
# s being a byte, . being the multiplication in GF(2^8), and + the XOR operator

def MixColumns(state):
    state_buffer = state.copy()
    for c in range(Nb):
        A,B,C,D = state_buffer[0][c],state_buffer[1][c],state_buffer[2][c],state_buffer[3][c]
        state[0][c] = xtime(A) ^ B ^ xtime(B) ^ C ^ D
        state[1][c] = A ^ xtime(B) ^ C ^ xtime(C) ^ D
        state[2][c] = A ^ B ^ xtime(C) ^ D ^ xtime(D)
        state[3][c] = A ^ xtime(A) ^ B ^ C ^ xtime(D)

# AddRoundKey()

def AddRoundKey(state,round_key): # method not tested
    for j in range(Nb):
        wround = round_key[j]
        wround = hex(wround)[2:]
        wround = "0" * (8 - len(wround)) + wround
        state[0][j] = state[0][j] ^ int(wround[0:2],16)
        state[1][j] = state[1][j] ^ int(wround[2:4],16)
        state[2][j] = state[2][j] ^ int(wround[4:6],16)
        state[3][j] = state[3][j] ^ int(wround[6:8],16)

# Key Expansion methods

# SubWord() substitutes all Nb(=4) bytes of a word according to SBOX 

def SubWord(word):
    word = hex(word)[2:]
    word = "0" * (8 - len(word)) + word
    subword =""
    for i in range(Nb):
        x,y = int(word[2*i],16),int(word[2*i+1],16)
        newval = hex(SBOX[x][y])[2:]
        if len(newval) == 1: newval = "0" + newval
        subword = subword + newval
    subword = int(subword,16)
    return subword

# RotWord() performs a cyclic permutation on 32-bit words

def RotWord(word):
    word = hex(word)[2:]
    word = "0" * (8 - len(word)) + word
    word = word[2:] + word[:2]
    word = int(word,16)
    return word

# Key Expansion

# initial values 
key = KEY
key = hex(key)[2:]
key = "0" * (Nk * 8 - len(key)) + key
key_exp = []
for i in range(Nk):
    key_exp.append(int(key[8 * i:8 * (i + 1)],16))

# computation of the next values
for i in range(8,Nb*(Nr+1)):
    temp = key_exp[i-1]
    if i % Nk == 0:
        temp = RotWord(temp)
        temp = SubWord(temp)
        temp = temp ^ Rcon[int(i/Nk)]
    if i % Nk == 4:
        temp = SubWord(temp)
    key_exp.append(temp ^ key_exp[i-Nk])

print("LET'S ENCRYPT !")
# Cipher
AddRoundKey(state,key_exp[0:4])
for i in range(1,Nr):
    SubBytes(state)
    ShiftRows(state)
    MixColumns(state)
    AddRoundKey(state,key_exp[i * Nb:(i + 1) * Nb])

    

SubBytes(state)
ShiftRows(state)
AddRoundKey(state,key_exp[Nr * Nb:(Nr + 1) * Nb])

print("Your AES-256 encryption is:")
Output(state)
