from blockchain import Blockchain

# יצירת בלוקצ'יין
my_blockchain = Blockchain()

# הוספת בלוקים חדשים
my_blockchain.add_block("Data for Block 1")
my_blockchain.add_block("Data for Block 2")

# בדיקת שלמות השרשרת
print("Is blockchain valid?", my_blockchain.is_chain_valid())

# הצגת השרשרת
for block in my_blockchain.chain:
    print(f"Index: {block.index}, Timestamp: {block.timestamp}, Data: {block.data}, Hash: {block.hash}")
