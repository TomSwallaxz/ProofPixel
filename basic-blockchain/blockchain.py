# from block import Block
# from datetime import datetime

# class Blockchain:
#     def __init__(self):
#         self.chain = [self.create_genesis_block()]

#     def create_genesis_block(self):
#         return Block(0, "01/01/2025", "Genesis Block", "0")

#     def add_block(self, data):
#         previous_block = self.chain[-1]
#         new_block = Block(len(self.chain), self.get_timestamp(), data, previous_block.hash)
#         self.chain.append(new_block)

#     def is_chain_valid(self):
#         for i in range(1, len(self.chain)):
#             current_block = self.chain[i]
#             previous_block = self.chain[i - 1]

#             # Validate hash
#             if current_block.hash != current_block.calculate_hash():
#                 return False

#             # Validate previous hash
#             if current_block.previous_hash != previous_block.hash:
#                 return False

#         return True

#     def get_timestamp(self):
#         return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    


# ---------- V:00.2 



# import hashlib
# import time
# import rsa 
# from block import Block

# class Blockchain:
#     def __init__(self):
#         self.chain = []
#         self.create_genesis_block()

#     # יצירת בלוק הגנזיס (הבלוק הראשון)
#     def create_genesis_block(self):
#         genesis_block = Block(0, "01/01/2025", "Genesis Block", "0", private_key)
#         self.chain.append(genesis_block)

#     # הוספת בלוק חדש לשרשרת
#     def add_block(self, data, private_key):
#         last_block = self.chain[-1]
#         new_block = Block(len(self.chain), time.strftime("%d/%m/%Y %H:%M:%S"), data, last_block.hash, private_key)
#         self.chain.append(new_block)

#     # אימות השרשרת (בדיקה שכל הבלוקים תקינים)
#     def is_chain_valid(self):
#         for i in range(1, len(self.chain)):
#             current_block = self.chain[i]
#             previous_block = self.chain[i-1]

#             # אם ה-Hash של הבלוק לא נכון
#             if current_block.hash != current_block.calculate_hash():
#                 print(f"Block {i} has an invalid hash")
#                 return False

#             # אם החתימה לא תקינה
#             if not current_block.verify_signature(public_key):
#                 print(f"Block {i} has an invalid signature")
#                 return False

#             # אם ה-Hash של הבלוק הקודם לא תואם
#             if current_block.previous_hash != previous_block.hash:
#                 print(f"Block {i} has an invalid previous hash")
#                 return False

#         print("Blockchain is valid")
#         return True

# # יצירת מפתח פרטי וציבורי (אם לא כבר עשינו זאת)
# private_key = rsa.generate_private_key(
#     public_exponent=65537,
#     key_size=2048,
# )
# public_key = private_key.public_key()

# # יצירת Blockchain והוספת בלוקים
# blockchain = Blockchain()
# blockchain.add_block("Data for Block 1", private_key)
# blockchain.add_block("Data for Block 2", private_key)

# # הדפסת ה-Hash של כל הבלוקים בשרשרת
# for block in blockchain.chain:
#     print(f"Index: {block.index}, Timestamp: {block.timestamp}, Data: {block.data}, Hash: {block.hash}")
#     print(f"Block Signature: {block.signature}")

# # בדיקת תקינות השרשרת
# blockchain.is_chain_valid()

# ---------- V:00.3 


# import hashlib
# import json
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import padding
# from cryptography.hazmat.primitives import hashes

# class Block:
#     def __init__(self, index, previous_hash, timestamp, data, hash=None):
#         self.index = index
#         self.previous_hash = previous_hash
#         self.timestamp = timestamp
#         self.data = data
#         self.hash = hash or self.calculate_hash()

#     def calculate_hash(self):
#         block_string = json.dumps(self.__dict__, sort_keys=True)
#         return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

#     def sign_block(self, private_key):
#         """
#         Method to sign the block using a private key.
#         """
#         block_string = json.dumps(self.__dict__, sort_keys=True).encode('utf-8')
#         signature = private_key.sign(
#             block_string,
#             padding.PKCS1v15(),
#             hashes.SHA256()
#         )
#         return signature

#     def verify_signature(self, signature, public_key):
#         """
#         Method to verify the signature of the block using the public key.
#         """
#         block_string = json.dumps(self.__dict__, sort_keys=True).encode('utf-8')
#         try:
#             public_key.verify(
#                 signature,
#                 block_string,
#                 padding.PKCS1v15(),
#                 hashes.SHA256()
#             )
#             return True
#         except:
#             return False

# # Function to create a new RSA private-public key pair
# def create_keys():
#     private_key = rsa.generate_private_key(
#         public_exponent=65537,
#         key_size=2048,
#     )
#     public_key = private_key.public_key()

#     # Save private key
#     with open("private_key.pem", "wb") as private_key_file:
#         private_key_file.write(private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.TraditionalOpenSSL,
#             encryption_algorithm=serialization.NoEncryption()
#         ))

#     # Save public key
#     with open("public_key.pem", "wb") as public_key_file:
#         public_key_file.write(public_key.public_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PublicFormat.SubjectPublicKeyInfo
#         ))

#     return private_key, public_key

# # Create keys
# private_key, public_key = create_keys()

# # Create a new block
# block = Block(1, "0", 1622547800, {"amount": 10})

# # Sign the block
# signature = block.sign_block(private_key)

# # Verify the block's signature
# is_valid = block.verify_signature(signature, public_key)

# # Output the results
# print(f"Block Hash: {block.hash}")
# print(f"Block Signature: {signature}")
# print(f"Signature is valid: {is_valid}")


# ---------- V:00.4

import hashlib
import rsa
import time

class Block:
    def __init__(self, previous_hash, data, signature):
        self.previous_hash = previous_hash
        self.data = data
        self.signature = signature
        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(f'{self.previous_hash}{self.data}{self.timestamp}'.encode('utf-8')).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        # יצירת בלוק גזירה ראשוני (ה-blok הראשון)
        self.create_genesis_block()

    def create_genesis_block(self):
        # יצירת בלוק גזירה, עם hash הקודם כ-"0" (כי אין בלוק קודם)
        genesis_block = Block("0", "Genesis Block", b"")
        self.chain.append(genesis_block)

    def add_block(self, data, signature):
        # הוספת בלוק חדש
        previous_block = self.chain[-1]
        new_block = Block(previous_block.hash, data, signature)
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print(f"Block Hash: {block.hash}")
            print(f"Block Data: {block.data}")
            print(f"Block Signature: {block.signature}")
            print(f"Previous Block Hash: {block.previous_hash}")
            print(f"Timestamp: {block.timestamp}")
            print("-----")


if __name__ == "__main__":
    blockchain = Blockchain()
    
    # יצירת private ו public keys
    (public_key, private_key) = rsa.newkeys(2048)
    
    # חתימת בלוק ראשון
    block_data = "This is the first block"
    signature = rsa.sign(block_data.encode('utf-8'), private_key, 'SHA-256')
    
    blockchain.add_block(block_data, signature)
    
    # חתימת בלוק שני
    block_data_2 = "This is the second block"
    signature_2 = rsa.sign(block_data_2.encode('utf-8'), private_key, 'SHA-256')
    
    blockchain.add_block(block_data_2, signature_2)
    
    # הדפסת השרשרת
    blockchain.print_chain()
