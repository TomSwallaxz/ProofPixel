import tkinter as tk
from tkinter import messagebox
import time
import hashlib
import rsa


class Block:
    def __init__(self, data, previous_hash, private_key=None):
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
        self.signature = self.sign_block(private_key) if private_key else None

    def calculate_hash(self):
        data_to_hash = f"{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(data_to_hash.encode()).hexdigest()

    def sign_block(self, private_key):
        return rsa.sign(self.hash.encode(), private_key, "SHA-256")


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block("Genesis Block", "0")

    def add_block(self, data, private_key):
        previous_hash = self.chain[-1].hash
        block = Block(data, previous_hash, private_key)
        self.chain.append(block)

    def is_valid(self, public_key):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.previous_hash != previous.hash:
                return False

            try:
                rsa.verify(current.hash.encode(), current.signature, public_key)
            except rsa.VerificationError:
                return False
        return True


# GUI Implementation
class BlockchainGUI:
    def __init__(self, root, blockchain, public_key, private_key):
        self.root = root
        self.blockchain = blockchain
        self.public_key = public_key
        self.private_key = private_key

        self.root.title("Blockchain GUI")
        self.root.geometry("600x400")

        # Add block section
        self.add_block_label = tk.Label(root, text="Add a Block:")
        self.add_block_label.pack()

        self.block_data_entry = tk.Entry(root, width=50)
        self.block_data_entry.pack()

        self.add_block_button = tk.Button(
            root, text="Add Block", command=self.add_block
        )
        self.add_block_button.pack()

        # Display chain section
        self.display_button = tk.Button(
            root, text="Display Blockchain", command=self.display_blockchain
        )
        self.display_button.pack()

        # Validate chain section
        self.validate_button = tk.Button(
            root, text="Validate Blockchain", command=self.validate_blockchain
        )
        self.validate_button.pack()

        self.text_area = tk.Text(root, height=15, width=70)
        self.text_area.pack()

    def add_block(self):
        data = self.block_data_entry.get()
        if data:
            self.blockchain.add_block(data, self.private_key)
            messagebox.showinfo("Success", "Block added successfully!")
            self.block_data_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Block data cannot be empty!")

    def display_blockchain(self):
        self.text_area.delete("1.0", tk.END)
        for block in self.blockchain.chain:
            block_info = (
                f"Block Hash: {block.hash}\n"
                f"Block Data: {block.data}\n"
                f"Previous Block Hash: {block.previous_hash}\n"
                f"Timestamp: {block.timestamp}\n"
                f"Signature: {block.signature}\n"
                "-----\n"
            )
            self.text_area.insert(tk.END, block_info)

    def validate_blockchain(self):
        if self.blockchain.is_valid(self.public_key):
            messagebox.showinfo("Blockchain Validation", "Blockchain is valid!")
        else:
            messagebox.showerror("Blockchain Validation", "Blockchain is invalid!")


# Initialize blockchain and keys
(public_key, private_key) = rsa.newkeys(512)
blockchain = Blockchain()

# Run GUI
root = tk.Tk()
gui = BlockchainGUI(root, blockchain, public_key, private_key)
root.mainloop()
