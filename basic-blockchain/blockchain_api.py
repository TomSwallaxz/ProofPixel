from flask import Flask, jsonify, request
from blockchain_with_signatures_verified import Blockchain, Block
import json

app = Flask(__name__)

# יצירת אובייקט Blockchain
blockchain = Blockchain()

@app.route('/blocks', methods=['GET'])
def get_blocks():
    """מחזיר את כל הבלוקים בבלוקצ'יין"""
    blocks = []
    for block in blockchain.chain:
        blocks.append({
            'block_hash': block.block_hash,
            'data': block.data,
            'signature': block.signature.hex(),
            'public_key': block.public_key,
            'previous_block_hash': block.previous_block_hash,
            'timestamp': block.timestamp
        })
    return jsonify(blocks)

@app.route('/add_block', methods=['POST'])
def add_block():
    """הוספת בלוק חדש לבלוקצ'יין"""
    data = request.json.get('data')
    if not data:
        return jsonify({"error": "Missing block data"}), 400
    
    # יצירת בלוק חדש
    blockchain.add_block(data)
    
    return jsonify({"message": "Block added successfully!"}), 201

@app.route('/validate', methods=['GET'])
def validate_blockchain():
    """בדיקת תקינות הבלוקצ'יין"""
    if blockchain.is_valid():
        return jsonify({"message": "Blockchain is valid!"}), 200
    else:
        return jsonify({"message": "Blockchain is invalid!"}), 400

if __name__ == '__main__':
    app.run(debug=True)


import requests

# שליחה של בקשה ל-API שלך כדי לקבל את כל הבלוקים
response = requests.get("http://127.0.0.1:5000/blocks")

# אם הבקשה הצליחה (קוד סטטוס 200), הצג את התגובה
if response.status_code == 200:
    blocks = response.json()
    print(blocks)
else:
    print(f"Error: {response.status_code}")