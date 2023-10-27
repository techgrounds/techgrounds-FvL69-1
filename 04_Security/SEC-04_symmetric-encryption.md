## SYMMETRIC ENCRYPTION:

**Cryptography has the main objective of securing data from being accessed by unauthorized entities.**  

Symmetric cryptography uses a unique key to both encrypt and decrypt data. In such a way, the entities  
that encrypt and decrypt data must access the same key to communicate.  

Examples of popular symmetric-key algorithms include Twofish, Serpent, AES (Rijndael algorithm) and many more.  

## KEY-TERMS:

* Encryption = A technique that transforms data into a code hard to decipher without the proper key.
* Symmetric Encryption = uses a unique key to encrypt and decrypt data

## ASSIGNMENT:

* Find one more historic cipher besides the Caesar cipher.
* Find two digital ciphers that are being used today.
* Send a symmetrically encrypted message to one of your peers via the public Slack channel. They should be able  
  to decrypt the message using a key you share with them. Try to think of a way to share this encryption key without  
  revealing it to everyone. You are not allowed to use any private messages or other communication channels besides the  
  public Slack channel. Analyse the shortcomings of symmetric encryption for sending messages.  


## USED RESOURCES:

[symmetric-cryptography](https://www.baeldung.com/cs/symmetric-cryptography)

[Diffie-Hellman-protocol](https://www.comparitech.com/blog/information-security/diffie-hellman-key-exchange/)

[historic-ciphers](https://interestingengineering.com/innovation/11-cryptographic-methods-that-marked-history-from-the-caesar-cipher-to-enigma-code-and-beyond)  

[AES-generator](https://encode-decode.com/aes256-encrypt-online/)  



## DIFFICULTIES:

Diffie-Helman protocol took some figuring out. 

## RESULT:

### Another historic cipher besides ceasar cipher:

* _Steganography_ is a method of hiding messages 'in plain sight' by camouflaging it as something else.  
  The earliest recorded use of this form of 'encryption' was described by Herodotus in his Histories.  

### Two commonly used digital ciphers today are:  

    Advanced Encryption Standard (AES): AES is a symmetric encryption algorithm that has become the de facto standard for encrypting sensitive information.  
    It is   widely used in various applications, including secure communication protocols, file encryption, and data protection.  
    AES supports key sizes of 128, 192, and 256 bits and operates on fixed-size blocks of data.  

    RSA (Rivest-Shamir-Adleman): RSA is an asymmetric encryption algorithm widely used for secure communication, digital signatures,  
    and key exchange. It is based on the mathematical complexity of factoring large prime numbers. RSA utilizes a public-private key pair,  
    where the encryption key is public, and the decryption key is kept private. The security of RSA is based on the difficulty of factoring  
    large numbers into their prime factors.  

These ciphers provide secure encryption and play a crucial role in safeguarding sensitive information in various digital systems and communication channels.  


![symmetric-key](../00_includes/SCREENSHOTS/Security/SEC-03_symm-key.png)

## Try to think of a way to share an encryption key.

### In the Diffie-Hellman protocol, two entities agree on using two values: the first value (p) is a prime number consisting of the modulo of a multiplicative group of integers, and the second value (g) is a primitive root modulo of the first value. Using a big prime number secures the sharing of the key to encrypt and decrypt.   

### Question: give an example of a prime number consisting of the modulo of a multiplicative group of integers  

Answer ChatGPT:  
Certainly! Let's consider the multiplicative group of integers modulo 7, denoted as Z₇*.  

The elements of Z₇* are {1, 2, 3, 4, 5, 6}, excluding 0. To find a prime number consisting of the modulo of this group, we need to look for a number that satisfies the   following conditions:  

    It is a prime number.  
    It is an element of Z₇*.  

Let's check the prime numbers within Z₇*:  

1 is not prime.  
2 is prime.  
3 is prime.  
4 is not prime.  
5 is prime.  
6 is not prime.  

Therefore, we have three prime numbers in Z₇*: 2, 3, and 5.  
So, an example of a prime number consisting of the modulo of a multiplicative group of integers is 5, which is an element of Z₇*.  
Note that Z₇* does not contain all prime numbers; it only consists of the numbers that are coprime to 7.  

### Question: explain a primitive root modulo of value 5
ChatGPT

A primitive root modulo of a given value is an integer that generates all the numbers in the multiplicative group modulo that value. Let's consider the primitive root modulo 5.

The multiplicative group modulo 5, denoted as Z₅*, consists of the elements {1, 2, 3, 4}. To find a primitive root modulo 5, we need to find an integer that, when raised to different powers, generates all the elements of Z₅*.

Let's examine the powers of different integers modulo 5:

For 1, the powers are: 1¹ ≡ 1 (mod 5), 1² ≡ 1 (mod 5), 1³ ≡ 1 (mod 5), ...

For 2, the powers are: 2¹ ≡ 2 (mod 5), 2² ≡ 4 (mod 5), 2³ ≡ 3 (mod 5), 2⁴ ≡ 1 (mod 5), ...

For 3, the powers are: 3¹ ≡ 3 (mod 5), 3² ≡ 4 (mod 5), 3³ ≡ 2 (mod 5), 3⁴ ≡ 1 (mod 5), ...

For 4, the powers are: 4¹ ≡ 4 (mod 5), 4² ≡ 1 (mod 5), ...

From the above calculations, we observe that only the integer 2 generates all the elements of Z₅*. It satisfies the property of being a primitive root modulo 5 because raising it to different powers yields all the elements {1, 2, 3, 4} in some order.

Hence, 2 is a primitive root modulo 5.  

### Each entity then chooses a secret value (let’s call them sv_1 and sv_2) and compute a number executing the following equation : g^{sv_n} mod p. Thus, each entity have as result the values we call S_1 and S_2.

### Finally, the entities exchange S_1 and S_2 and derivate a common key using their own secret value and the received S value: S_2^{sv_1} mod p and S_1^{sv_2} mod p.  

### In this example i use small numbers for clarity but normally one would use a big prime number to make reverse calculation by a hacker too expensive in regard to time and compute power.  

Let's take number 5 as P, 5 is one of the prime elements of 7. So P=5  
The primitive root of 5 is 2, so G=2

Now P and G are agreed upon by Alice and Bob.  
They both choose a secret value (sv_1 and sv_2), Alice: 9 and Bob: 7. 

Then they both use the formula: **G^sv mod P** to calculate the number they're gonna share.(SN)

for Alice: **SN: 2^9 mod 5 = 2**  
for Bob: **SN: 2^7 mod 5 = 3**  

Now they share the outcomes with eachother over an open (unsafe) line.  

Next, they both use the formula: **SN^sv mod P** to calculate the common key. (CK)    

for Alice: **CK = 3^9 mod 5 = 19.683 mod 5 = 3**  
for Bob: **CK = 2^7 mod 5 = 128 mod 5 = 3**  

### The common key (CK) they can use for their symmetric encryption is: **3**  

## Send a symmetrically encrypted message to one of your peers.
![encrypt-decrypt_with_Zev](../00_includes/SCREENSHOTS/Security/SEC-04_symm-encrypt.png)

## Disadvantages of Symmetric Cryptography  

It is not possible to create digital signatures that cannot be revoked. The message's origin and validity cannot be guaranteed.  
Messages cannot be proven to have originated from a specific person because both the sender and the recipient use the same key.  


