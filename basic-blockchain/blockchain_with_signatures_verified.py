import hashlib
import rsa
import time


class Block:
    def __init__(self, previous_hash, data, signature, public_key):
        self.previous_hash = previous_hash
        self.data = data
        self.signature = signature
        self.public_key = public_key
        self.timestamp = time.time()
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        return hashlib.sha256(f'{self.previous_hash}{self.data}{self.timestamp}'.encode('utf-8')).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block("0", "Genesis Block", b"", None)
        self.chain.append(genesis_block)

    def add_block(self, data, signature, public_key):
        previous_block = self.chain[-1]
        new_block = Block(previous_block.hash, data, signature, public_key)
        self.chain.append(new_block)
        print("Block added successfully!")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            try:
                # וולידציה של חתימה
                rsa.verify(current_block.data.encode('utf-8'), current_block.signature, current_block.public_key)
            except rsa.VerificationError:
                print(f"Block {i} has an invalid signature!")
                return False

            # בדיקה שה-hash הקודם תואם
            if current_block.previous_hash != self.chain[i - 1].hash:
                print(f"Block {i} has an invalid previous hash!")
                return False

        print("Blockchain is valid!")
        return True

    def print_chain(self):
        for block in self.chain:
            print(f"Block Hash: {block.hash}")
            print(f"Block Data: {block.data}")
            print(f"Block Signature: {block.signature}")
            print(f"Public Key: {block.public_key}")
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
    blockchain.add_block(block_data, signature, public_key)
    
    # חתימת בלוק שני
    block_data_2 = "This is the second block"
    signature_2 = rsa.sign(block_data_2.encode('utf-8'), private_key, 'SHA-256')
    blockchain.add_block(block_data_2, signature_2, public_key)
    
    # הדפסת השרשרת
    blockchain.print_chain()
    
    # וולידציה של השרשרת
    blockchain.is_chain_valid()
