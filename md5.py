# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 15:36:57 2022

@author: JAndreG

The aim of this code is to compute MD5 hashes
"""

#let's first create some functions doing bitwise boolean operations
#I know such functions already exist in Python, mines perform the same operations on strings of bits

def and_bits(a,b):
    if len(a) != len(b):
        print("Warning: bits do not have the same length !")
        print("a = ",a)
        print("b = ",b)
    result=""
    for i in range(len(a)):
        result = result + str(int(a[i]) & int(b[i]))
    return result
    
def or_bits(a,b):
    if len(a) != len(b):
        print("Warning: bits do not have the same length !")
        print("a = ",a)
        print("b = ",b)
    result=""
    for i in range(len(a)):
        result = result + str(int(a[i]) | int(b[i]))
    return result
    
def xor_bits(a,b):
    if len(a) != len(b):
        print("Warning: bits do not have the same length !")
        print("a = ",a)
        print("b = ",b)    
    result=""
    for i in range(len(a)):
        result = result + str(int(a[i]) ^ int(b[i]))
    return result

def shift_bits(bits,shift):
    return bits[shift % len(bits):]+bits[:shift % len(bits)]

def not_bits(bits):
    result = ""
    for bit in bits: result = result + ( "0" if bit == "1" else "1" )
    return result

def int_to_32bits(integer):
    #this function returns a 32-bit string representation of an integer
    result = bin(integer)[2:]
    
    #the below line is equivalent to take the 2^32 modulo
    if len(result) > 32: result = result[len(result)-32:]
    
    #the lenght of the output is fixed to 32, some leading zeros might be added
    result = (32-len(result))*"0" + result
    
    return result

"""
based on the conventions in RFC1321:
   -------------------------------------------------------------------
   A "word" is a 32-bit quantity and a "byte" is an
   eight-bit quantity. A sequence of bits can be interpreted in a
   natural manner as a sequence of bytes, where each consecutive group
   of eight bits is interpreted as a byte with the high-order (most
   significant) bit of each byte listed first. Similarly, a sequence of
   bytes can be interpreted as a sequence of 32-bit words, where each
   consecutive group of four bytes is interpreted as a word with the
   low-order (least significant) byte given first.
   -------------------------------------------------------------------
hence we defined the below function to reorder the bytes little endian style
"""

def little_endian(bits):
    #take a string of bits and reverse the order of octets
    if len(bits) % 8 != 0: print("WARNING: input bits are not a set of octets")
    n = len(bits) // 8
    result = ""
    
    #building the result reading the octets backwards 
    for i in range(n,0,-1):
        result = result + bits[8*i-8:8*i]
      
    return result
  

#let us define the constants K, the rotation array R and the initial buffer values

from math import sin

K=[abs(int(2**32*sin(i+1))) for i in range(64)]

R = [7,12,17,22]*4 + [5,9,14,20]*4 + [4,11,16,23]*4 + [6,10,15,21]*4


#intiial values for buffers

h0 = bin(0x01234567)[2:]
h1 = bin(0x89abcdef)[2:]
h2 = bin(0xfedcba98)[2:]
h3 = bin(0x76543210)[2:]

#0 padding to get 32-bit words

h0 = "0000000" + h0
h3 = "0" + h3

#initial values were provided in little-endian in RFC 1321
#hence converting to big endian (applying the above little_endian function)

h0,h1,h2,h3 = little_endian(h0),little_endian(h1),little_endian(h2),little_endian(h3)

"""
RFC 1321
We then define four auxiliary functions that each take as input
   three 32-bit words and produce as output one 32-bit word.

          F(X,Y,Z) = XY v not(X) Z
          G(X,Y,Z) = XZ v Y not(Z)
          H(X,Y,Z) = X xor Y xor Z
          I(X,Y,Z) = Y xor (X v not(Z))
"""

def F(X,Y,Z):
    return or_bits(and_bits(X,Y),and_bits(not_bits(X),Z))

def G(X,Y,Z):
    return or_bits(and_bits(X,Z),and_bits(Y,not_bits(Z)))

def H(X,Y,Z):
    return xor_bits(X,xor_bits(Y,Z))

def I(X,Y,Z):
    return xor_bits(Y,or_bits(X,not_bits(Z)))

"""PREPARING THE MESSAGE"""

raw_message = input("Enter message : ")

#8 bits are required to encode each character, hence:
length_message = len(raw_message) * 8

#modulo 2^64 as length will be encoded on 64 bits
length_message = length_message % 2**64

#conversion to a string of bits
length_message = bin(length_message)[2:]

#0-padding
length_message = (64 - len(length_message))*"0" + length_message


#Conversion of the message to binaries (Unicode)
message = ""
for char in raw_message:
    octet = format(ord(char), 'b')
    octet = (8-len(octet))*"0" + octet
    message = message + octet

#padding of the message to the next multiple of 512 - 64

message = message + "1"

while len(message) % 512 != 448:
    message = message + "0"
    
#adding the little-endianed length to the padded message
message = message + little_endian(length_message)

#message formatting is now complete, it is a sequence 512 bits blocks

#now forming the list of 512-bit blocks
blocks = []
n = len(message) // 512
for i in range(n):
    blocks.append(message[512*i:512*(i+1)])
    
#Let us begin hash !

for block in blocks:
    #splitting each 512-bit block in 16 32-bit words
    words = []
    for i in range(16):
        words.append(block[32*i:32*(i+1)])
    #applying little-endian on each word
    for i in range(16):
        words[i] = little_endian(words[i])
    #initializing buffers
    a,b,c,d = h0,h1,h2,h3
    #main loop
    for i in range(64):
        
        if i<=15:
            f = F(b,c,d)
            g = i
        elif i>=15 and i<=31:
            f = G(b,c,d)
            g = (5*i + 1) % 16
        elif i>=32 and i<=47:
            f = H(b,c,d)
            g = (3*i + 5) % 16          
        elif i>=48:
            f = I(b,c,d)
            g = 7*i % 16        
        
        temp = d
        
        d = c
        
        c = b
        
        addition = int(a,2) + int(f,2) + K[i] + int(words[g],2)
        
        addition_in_bits = int_to_32bits(addition)
        
        addition_in_bits_shifted = shift_bits(addition_in_bits, R[i])
        
        final_addition = int(addition_in_bits_shifted,2) +int(b,2)
        
        b = int_to_32bits(final_addition)
        
        a = temp
        
    #adding buffers to the initial values    
    h0 = int_to_32bits(int(h0,2) + int(a,2))
    h1 = int_to_32bits(int(h1,2) + int(b,2))
    h2 = int_to_32bits(int(h2,2) + int(c,2))
    h3 = int_to_32bits(int(h3,2) + int(d,2))

#now formatting the final hash
h = [h0,h1,h2,h3]
for i in range(len(h)):
    h[i] = little_endian(h[i])
    #hexadecimal conversion
    h[i] = hex(int(h[i],2))[2:]
    #0-padding possibly needed
    h[i] = "0"*(8-len(h[i])) + h[i]

h = ''.join(h)


print("{:>15}{:^40}".format("My MD5 result :",h))

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    