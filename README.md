# E.F.A.F-Tool
Simple program that encrypts files or texts into images - Other encryption methods may be added later.

## Before Using:
#### Make sure you have both Pillow and Cryptography libraries
**How to install:**
```
$ pip install Pillow
$ pip install cryptography
```
## Usage
### Note:
**Whenever asked for a key, a 32 characters key is always recommended to be able to use the best encryption method.**
###  Encrpytion:

##### Encrypting text into an image:
```
E.F.A.F: encrypt textToImg
Text: [The text you want to encrypt]
Input Image Name: [The name of the file you want your text to be encrypted in]
Output Image Name: [The name of the output file that will be create with your encrypted text on it]
Key: [Encryption Key]
```

### Decryption: 

##### Decrypting text from an image:

```
E.F.A.F: decrypt textFromImg
Input Image Name: [The name of the file which has encrypted text in it]
Key: [Decrpytion Key]
```
