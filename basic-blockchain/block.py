# import hashlib

# class Block:
#     def __init__(self, index, timestamp, data, previous_hash):
#         self.index = index
#         self.timestamp = timestamp
#         self.data = data
#         self.previous_hash = previous_hash
#         self.hash = self.calculate_hash()

#     def calculate_hash(self):
#         hash_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
#         return hashlib.sha256(hash_string.encode()).hexdigest()


# ---------- V:00.2

# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import serialization
# from cryptography.hazmat.primitives.asymmetric import padding

# class Block:
#     def __init__(self, index, timestamp, data, previous_hash, private_key):
#         self.index = index
#         self.timestamp = timestamp
#         self.data = data
#         self.previous_hash = previous_hash
#         self.hash = self.calculate_hash()
#         self.signature = self.sign_block(private_key)

#     def calculate_hash(self):
#         hash_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
#         return hashlib.sha256(hash_string.encode()).hexdigest()

#     def sign_block(self, private_key):
#         """חיתום הבלוק בעזרת מפתח פרטי"""
#         message = self.hash.encode()
#         signature = private_key.sign(
#             message,
#             padding.PKCS1v15(),
#             hashes.SHA256()
#         )
#         return signature

# # Create a private key 
# private_key = rsa.generate_private_key(
#     public_exponent=65537,
#     key_size=2048,
# )

# # Example of a block with a digital signature
# block = Block(1, "03/01/2025", "Data for Block 1", "458aaf24b304c85edb1637eda158944ffae7987bfd31e3c19dc83226c6b3f52e", private_key)
# print(f"Block Hash: {block.hash}")
# print(f"Block Signature: {block.signature}")


# ---------- V:00.2.5 


# import hashlib
# from cryptography.hazmat.primitives.asymmetric import rsa
# from cryptography.hazmat.primitives import padding
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.asymmetric import padding

# # יצירת מחלקה לבלוק
# class Block:
#     def __init__(self, index, timestamp, data, previous_hash, private_key):
#         self.index = index
#         self.timestamp = timestamp
#         self.data = data
#         self.previous_hash = previous_hash
#         self.hash = self.calculate_hash()
#         self.signature = self.sign_block(private_key)

#     # חישוב Hash עבור הבלוק
#     def calculate_hash(self):
#         hash_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
#         return hashlib.sha256(hash_string.encode()).hexdigest()

#     # חיתום הבלוק עם המפתח הפרטי
#     def sign_block(self, private_key):
#         message = self.hash.encode()
#         signature = private_key.sign(
#             message,
#             padding.PKCS1v15(),
#             hashes.SHA256()
#         )
#         return signature

# # יצירת מפתח פרטי
# private_key = rsa.generate_private_key(
#     public_exponent=65537,
#     key_size=2048,
# )

# # יצירת בלוק עם חתימה דיגיטלית
# block = Block(1, "03/01/2025", "Data for Block 1", "458aaf24b304c85edb1637eda158944ffae7987bfd31e3c19dc83226c6b3f52e", private_key)

# # הדפסת ה-Hash והחתימה
# print(f"Block Hash: {block.hash}")
# print(f"Block Signature: {block.signature}")



# ---------- V:00.3.0


import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization

class Block:
    def __init__(self, index, timestamp, data, previous_hash, private_key):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.signature = self.sign_block(private_key)

    # חישוב ה-Hash עבור הבלוק
    def calculate_hash(self):
        hash_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(hash_string.encode()).hexdigest()

    # חיתום הבלוק עם המפתח הפרטי
    def sign_block(self, private_key):
        message = self.hash.encode()
        signature = private_key.sign(
            message,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return signature

    # אימות החתימה בעזרת המפתח הציבורי
    def verify_signature(self, public_key):
        message = self.hash.encode()
        try:
            public_key.verify(
                self.signature,
                message,
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            print("Signature is valid.")
            return True
        except:
            print("Signature is invalid.")
            return False

# יצירת מפתח פרטי וציבורי
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
public_key = private_key.public_key()

# יצירת בלוק עם חתימה דיגיטלית
block = Block(1, "03/01/2025", "Data for Block 1", "458aaf24b304c85edb1637eda158944ffae7987bfd31e3c19dc83226c6b3f52e", private_key)

# הדפסת ה-Hash, החתימה והאימות
print(f"Block Hash: {block.hash}")
print(f"Block Signature: {block.signature}")
block.verify_signature(public_key)
