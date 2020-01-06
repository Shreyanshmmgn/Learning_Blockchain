# Module 1 - Create a Blockchain

# To be installed:
# Flask==0.12.2: pip install Flask==0.12.2
# Postman HTTP Client: https://www.getpostman.com/

# Importing the libraries
import datetime
import hashlib
import json

import requests
from urllib.parse import urlparse
from uuid import uuid4

from flask import Flask, jsonify, request


# Part 1 - Building a Blockchain
# Day 3 - 1: transactions
#         2: Decentilization
#         3: Consenses - Longest chain wins


class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash="0")
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
            "transactions": self.transactions,
        }
        self.chain.append(block)
        self.transactions = []
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()
            if hash_operation[:4] == "0000":
                print(hash_operation)
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transactions(self, sender, reciver, amount):
        self.transactions.append(
            {"Sender": sender, "Reciver": reciver, "Amount": amount}
        )
        previous_block = self.get_previous_block()
        return previous_block["index"] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f"http://{node}/get_chain")
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False


# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

node_address = str(uuid4()).replace("-", "")


# Creating a Blockchain
blockchain = Blockchain()

# Mining a new block
@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transactions(
        sender=node_address, reciver="Shreyansh Rocks", amount=1
    )
    block = blockchain.create_block(proof, previous_hash)
    response = {
        "message": "Congratulations, you just mined a block!",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
        "transactions": block["transactions"],
    }
    return jsonify(response), 200


# Getting the full Blockchain
@app.route("/get_chain", methods=["GET"])
def get_chain():
    response = {"chain": blockchain.chain, "length": len(blockchain.chain)}
    return jsonify(response), 200


# Checking if the Blockchain is valid
@app.route("/is_valid", methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {"message": "The Blockchain is valid."}
    else:
        response = {"message": "The blockchain has been compromised"}
    return jsonify(response), 200


@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    json = request.get_json()  # Flask wali requests
    transactions_keys = ["sender", "reciver", "amount"]
    if not all(key in json for key in transactions_keys):
        return "Some of the keys are missing", 400
    index = blockchain.add_transactions(json["sender"], json["reciver"], json["amount"])
    response = {"message ": f"This transaction will be added in block {index}"}
    return jsonify(response), 201


@app.route("/connect_nodes", methods=["POST"])
def connect_nodes():
    json = request.get_json()
    nodes = json.get("nodes")
    if nodes is None:
        return "No node", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        "message": "ALl nodes are noe connectd, NCucoin has the following nodes",
        "total_nodes": list(blockchain.nodes),
    }
    return jsonify(response), 201


# Running the app


@app.route("/replace_chain", methods=["GET"])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {
            "Message": "the nodes have different chain so the node was replced",
            "new_chain": blockchain.chain,
        }
    else:
        response = {"MEssage": "All good your chain is the largest one", "new_Chain": blockchain.chain}
    return jsonify(response), 200

app.run(debug=True, port=5000)
