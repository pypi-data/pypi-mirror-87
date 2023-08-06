import numpy as np
import math
from sympy import Matrix
from des import DesKey
import os
from .aes import AES
import hashlib
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256

class CNS_ALGO():
    '''
        Cryptography Algorithm Instance to use algorithms and so on.
    '''
    def __init__(self):
        pass

    def caesar(self, text:str, offset:int):
        """
            Function to perform Caesar Cipher on a given Plain Text and Offset.

            Args:
            Text:str - Plain Text to encrypt
            Offset:int - Offset to encrypt plain text

            Returns: None
        """
        print("Simulating Caesar Cipher")
        def encode(string, offset):
            res=[]
            for i in string:
                if(i.isalpha()):
                    if(i.isupper()):
                        res.append(chr(ord('A')+(ord(i)-ord('A')+offset)%26))
                    else:
                        res.append(chr(ord('a')+(ord(i)-ord('a')+offset)%26))
                else:
                    res.append(i)
            return "".join(res)
        
        ciph = encode(text, offset)
        print("Cipher Text:", ciph)
        print("Plain Text:", encode(ciph, 26-offset))
        

    def playfair(self, key:str, text:str):
        """
            Function to simulate Playfair Cipher

            Args:
            key:str - Key to encrypt Plain text
            text:str - Plain text to be encrypted

            Returns: None
        """
        key = key
        key = key.replace(" ", "")
        key = key.upper()

        result=list()
        for c in key: #storing key
            if c not in result:
                if c=='J':
                    result.append('I')
                else:
                    result.append(c)

        flag=0
        for i in range(65,91): #storing other character
            if chr(i) not in result:
                if i==73 and chr(74) not in result:
                    result.append("I")
                    flag=1
                elif flag==0 and i==73 or i==74:
                    pass    
                else:
                    result.append(chr(i))
        k = 0
        my_matrix = [[0 for i in range(5)] for j in range(5)] #initialize matrix
        for i in range(0,5): #making matrix
            for j in range(0,5):
                my_matrix[i][j]=result[k]
                k+=1

        def locindex(c): #get location of each character
            loc=list()
            if c=='J':
                c='I'
            for i ,j in enumerate(my_matrix):
                for k,l in enumerate(j):
                    if c==l:
                        loc.append(i)
                        loc.append(k)
                        return loc
        def encrypt(message):  #Encryption
            msg= message
            msg=msg.upper()
            msg=msg.replace(" ", "")             
            i=0
            for s in range(0,len(msg)+1,2):
                if s<len(msg)-1:
                    if msg[s] == msg[s+1]:
                        msg=msg[:s+1]+'X'+msg[s+1:]
            if len(msg)%2!=0:
                msg=msg[:]+'X'

            r = ''
            while i<len(msg):
                loc=list()
                loc=locindex(msg[i])
                loc1=list()
                loc1=locindex(msg[i+1])
                if loc[1]==loc1[1]:
                    r += "{}{}".format(my_matrix[(loc[0]+1)%5][loc[1]],my_matrix[(loc1[0]+1)%5][loc1[1]])
                elif loc[0]==loc1[0]:
                    r += "{}{}".format(my_matrix[loc[0]][(loc[1]+1)%5],my_matrix[loc1[0]][(loc1[1]+1)%5])
                else:
                    r+= "{}{}".format(my_matrix[loc[0]][loc1[1]],my_matrix[loc1[0]][loc[1]])   
                i=i+2

            return r        
                
        def decrypt(message):  #decryption
            msg= message
            msg = msg.upper()
            msg = msg.replace(" ", "")

            i = 0
            r = " "
            while i<len(msg):
                loc=list()
                loc=locindex(msg[i])
                loc1=list()
                loc1=locindex(msg[i+1])
                if loc[1]==loc1[1]:
                    r += "{}{}".format(my_matrix[(loc[0]-1)%5][loc[1]],my_matrix[(loc1[0]-1)%5][loc1[1]])
                elif loc[0]==loc1[0]:
                    r += "{}{}".format(my_matrix[loc[0]][(loc[1]-1)%5],my_matrix[loc1[0]][(loc1[1]-1)%5])
                else:
                    r += "{}{}".format(my_matrix[loc[0]][loc1[1]],my_matrix[loc1[0]][loc[1]])  
                i=i+2

            return r

        print("Simulating Playfair Cipher")
        print("Encryption")
        enc = encrypt(text)
        print("Cipher Text:", *enc,sep="")
        print("Decryption")
        dec = decrypt(enc)
        print("Plain Text: ",*dec,sep="")

    def hill_cipher(self, text:str, key:str):
        '''
            Program to perform Hill Cipher.

            Plain text length must be 3
            Key length must be 9
        '''
        np.keyMatrix = [[0] * 3 for i in range(3)]
        messageVector = [[0] for i in range(3)]
        cipherMatrix = [[0] for i in range(3)]
        plainMatrix = [[0] for i in range(3)]
        np.inverseKeyMatrix = [[0] * 3 for i in range(3)]

        def getKeyMatrix(key):
            k = 0
            for i in range(3):
                for j in range(3):
                    np.keyMatrix[i][j] = ord(key[k]) % 65
                    k += 1

        def encrypt(messageVector):
            for i in range(3):
                for j in range(1):
                    cipherMatrix[i][j] = 0
                    for x in range(3):
                        cipherMatrix[i][j] += (np.keyMatrix[i][x] * messageVector[x][j])
                        cipherMatrix[i][j] = cipherMatrix[i][j] % 26

        def HillCipher1(message, key):
            getKeyMatrix(key)
            for i in range(3):
                messageVector[i][0] = ord(message[i]) % 65
            encrypt(messageVector)
            CipherText = []
            for i in range(3):
                CipherText.append(chr(cipherMatrix[i][0] + 65))
            return "".join(CipherText)

        def getInverseKeyMatrix(key):
            getKeyMatrix(key)
            keyMatrix=np.keyMatrix
            inverseKeyMatrix = Matrix(keyMatrix).inv_mod(26)
            np.inverseKeyMatrix = np.array(inverseKeyMatrix)

        def HillCipher2(message, key):
            getInverseKeyMatrix(key)
            for i in range(3):
                messageVector[i][0] = ord(message[i]) % 65
            decrypt(messageVector)
            PlainText = []
            for i in range(3):
                PlainText.append(chr(int(round(plainMatrix[i][0]) + 65)))
            return "".join(PlainText)

        def decrypt(messageVector):
            for i in range(3):
                for j in range(1):
                    plainMatrix[i][j] = 0
                    for x in range(3):
                        plainMatrix[i][j] = plainMatrix[i][j] % 26
                        plainMatrix[i][j] += (np.inverseKeyMatrix[i][x] * messageVector[x][j])
                    plainMatrix[i][j] = plainMatrix[i][j] % 26

        print("Simulating Hill Cipher")
        message = text.upper()
        key = key.upper()
        cipher = HillCipher1(message, key)
        print("Cipher Text:", cipher)
        plain = HillCipher2(cipher, key)
        print("Plain Text:", plain)

    def vigenere(self, text:str, key:str):
        def generateKey(string, key): 
            key = list(key) 
            if len(string) == len(key): 
                return(key) 
            else: 
                for i in range(len(string) - len(key)): 
                    key.append(key[i % len(key)]) 
            return("" . join(key)) 


        def cipherText(string, key): 
            cipher_text = [] 
            for i in range(len(string)): 
                x = (ord(string[i]) +
                    ord(key[i])) % 26
                x += ord('A') 
                cipher_text.append(chr(x)) 
            return("" . join(cipher_text)) 
            
            
        def originalText(cipher_text, key): 
            orig_text = [] 
            for i in range(len(cipher_text)): 
                x = (ord(cipher_text[i]) -
                    ord(key[i]) + 26) % 26
                x += ord('A') 
                orig_text.append(chr(x)) 
            return("" . join(orig_text))

        print("Simulating Vigenere Cipher")	
        key = generateKey(text, key) 
        cipher_text = cipherText(text, key) 
        print("Cipher Text :", cipher_text) 
        print("Plain Text :", originalText(cipher_text, key)) 

    def rail_fence(self, text:str, key:int):
        def encryptRailFence(text, key): 
            rail = [['\n' for i in range(len(text))] 
                        for j in range(key)] 
            
            dir_down = False
            row, col = 0, 0
            
            for i in range(len(text)): 
                if (row == 0) or (row == key - 1): 
                    dir_down = not dir_down 
                
                # fill the corresponding alphabet 
                rail[row][col] = text[i] 
                col += 1
                
                # find the next row using 
                # direction flag 
                if dir_down: 
                    row += 1
                else: 
                    row -= 1

            result = [] 
            for i in range(key): 
                for j in range(len(text)): 
                    if rail[i][j] != '\n': 
                        result.append(rail[i][j]) 
            return("" . join(result)) 
    

        def decryptRailFence(cipher, key): 
            rail = [['\n' for i in range(len(cipher))]  
                        for j in range(key)] 
            
            dir_down = None
            row, col = 0, 0
                
            for i in range(len(cipher)): 
                if row == 0: 
                    dir_down = True
                if row == key - 1: 
                    dir_down = False
                
                rail[row][col] = '*'
                col += 1
                
                if dir_down: 
                    row += 1
                else: 
                    row -= 1
                    
            index = 0
            for i in range(key): 
                for j in range(len(cipher)): 
                    if ((rail[i][j] == '*') and
                    (index < len(cipher))): 
                        rail[i][j] = cipher[index] 
                        index += 1
                    
            result = [] 
            row, col = 0, 0
            for i in range(len(cipher)):  
                if row == 0: 
                    dir_down = True
                if row == key-1: 
                    dir_down = False
                        
                if (rail[row][col] != '*'): 
                    result.append(rail[row][col]) 
                    col += 1

                if dir_down: 
                    row += 1
                else: 
                    row -= 1
            return("".join(result))            

        print("Simulating Rail Fence Algorithm")
        cipher = encryptRailFence(text, key)
        print("Cipher Text:", cipher)
        plain = decryptRailFence(cipher, key)
        print("Plain Text:", plain)

    def row_column_transposition(self, text:str, key:str):
        key = key

        def encryptMessage(msg): 
            cipher = "" 

            k_indx = 0

            msg_len = float(len(msg)) 
            msg_lst = list(msg) 
            key_lst = sorted(list(key)) 

            col = len(key) 
            
            row = int(math.ceil(msg_len / col)) 

            fill_null = int((row * col) - msg_len) 
            msg_lst.extend('_' * fill_null) 

            matrix = [msg_lst[i: i + col] 
                    for i in range(0, len(msg_lst), col)] 

            for _ in range(col): 
                curr_idx = key.index(key_lst[k_indx]) 
                cipher += ''.join([row[curr_idx] 
                                for row in matrix]) 
                k_indx += 1

            return cipher 

        def decryptMessage(cipher): 
            msg = "" 

            k_indx = 0

            msg_indx = 0
            msg_len = float(len(cipher)) 
            msg_lst = list(cipher) 

            col = len(key) 
                
            row = int(math.ceil(msg_len / col)) 

            key_lst = sorted(list(key)) 

            dec_cipher = [] 
            for _ in range(row): 
                dec_cipher += [[None] * col] 

            for _ in range(col): 
                curr_idx = key.index(key_lst[k_indx]) 

                for j in range(row): 
                    dec_cipher[j][curr_idx] = msg_lst[msg_indx] 
                    msg_indx += 1
                k_indx += 1

            try: 
                msg = ''.join(sum(dec_cipher, [])) 
            except TypeError: 
                raise TypeError("This program cannot", 
                                "handle repeating words.") 

            null_count = msg.count('_') 

            if null_count > 0: 
                return msg[: -null_count] 

            return msg 

        print("Row Column Transposition Simulation")
        cipher = encryptMessage(text) 
        print("Cipher Text: {}". 
                    format(cipher)) 

        print("Plain Text: {}". 
            format(decryptMessage(cipher)))

    def des_algo(self, text:str, key:str):
        d_key = DesKey(bytes(key, 'utf-8'))

        cipher = d_key.encrypt(bytes(text, 'utf-8'), padding=True) 

        print("Cipher Text:", cipher)

        plain = d_key.decrypt(cipher, padding=True)

        print("Plain Text:", plain.decode('utf-8'))

    def aes_algo(self, url:str):
        key = os.urandom(16)
        iv = os.urandom(16)

        encrypted = AES(key).encrypt_ctr(bytes(url, 'utf-8'), iv)
        print("Encrypted URL:", encrypted)
        plain = AES(key).decrypt_ctr(encrypted, iv)
        print("Decrypted URL:", str(plain, 'utf-8'))

    def rsa(self):
        html = '''
        <html>

        <head>
            <title>RSA Encryption</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>

        <body>
            <center>
                <h1>RSA Algorithm</h1>
                <h2>Implemented Using HTML & Javascript</h2>
                <hr>
                <table>
                    <tr>
                        <td>Enter First Prime Number:</td>
                        <td><input type="number" value="53" id="p"></td>
                    </tr>
                    <tr>
                        <td>Enter Second Prime Number:</td>
                        <td><input type="number" value="59" id="q"></p>
                        </td>
                    </tr>
                    <tr>
                        <td>Enter the Message(cipher text):<br>[A=1, B=2,...]</td>
                        <td><input type="number" value="89" id="msg"></p>
                        </td>
                    </tr>
                    <tr>
                        <td>Public Key:</td>
                        <td>
                            <p id="publickey"></p>
                        </td>
                    </tr>
                    <tr>
                        <td>Exponent:</td>
                        <td>
                            <p id="exponent"></p>
                        </td>
                    </tr>
                    <tr>
                        <td>Private Key:</td>
                        <td>
                            <p id="privatekey"></p>
                        </td>
                    </tr>
                    <tr>
                        <td>Cipher Text:</td>
                        <td>
                            <p id="ciphertext"></p>
                        </td>
                    </tr>
                    <tr>
                        <td><button onclick="RSA();">Apply RSA</button></td>
                    </tr>
                </table>
            </center>
        </body>
        <script type="text/javascript">
            function RSA() {
                var gcd, p, q, no, n, t, e, i, x;
                gcd = function (a, b) { return (!b) ? a : gcd(b, a % b); };
                p = document.getElementById('p').value;
                q = document.getElementById('q').value;
                no = document.getElementById('msg').value;
                n = p * q;
                t = (p - 1) * (q - 1);

                for (e = 2; e < t; e++) {
                    if (gcd(e, t) == 1) {
                        break;
                    }
                }

                for (i = 0; i < 10; i++) {
                    x = 1 + i * t
                    if (x % e == 0) {
                        d = x / e;
                        break;
                    }
                }

                ctt = Math.pow(no, e).toFixed(0);
                ct = ctt % n;

                dtt = Math.pow(ct, d).toFixed(0);
                dt = dtt % n;

                document.getElementById('publickey').innerHTML = n;
                document.getElementById('exponent').innerHTML = e;
                document.getElementById('privatekey').innerHTML = d;
                document.getElementById('ciphertext').innerHTML = ct;
            }
        </script>
        </html>
        '''
        file = open("rsa.html","w")
        file.write(html)
        file.close()
        print("File is written successfully")

    def diffie_hellman(self, p:int, q:int):
        print('The Value of P is :%d'%(p))
        print('The Value of G is :%d'%(q))
        
        a = int(input("Enter Alice Private Key:")) #Alice Private key
        b = int(input("Enter Bob Private Key:")) #Bob Private Key
        
        x = int(pow(q, a, p))
        
        y = int(pow(q, b, p)) 
        print('The Private Key a for Alice is :%d'%(a))
        
        ka = int(pow(y, a, p)) 
        
        
        print('The Private Key b for Bob is :%d'%(b))
        
        kb = int(pow(x,b,p))
        
        if ka == kb:
            print("Secret key is correct, it is", ka)

        else:
            print("Secret key is incorrect")

    def sha1_algo(self, text:str):
        result = hashlib.sha1(text.encode()) 

        print("The hexadecimal equivalent in SHA1 is : ") 
        print(result.hexdigest())

    def dss_algo(self, text:str):
        key = DSA.generate(2048)

        hash_obj = SHA256.new(text.encode("utf-8"))
        signer = DSS.new(key, 'fips-186-3')
        signature = signer.sign(hash_obj)

        print("Digital Signature:", signature)