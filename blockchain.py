import datetime                                    # Python library to access computer's current date
import hashlib                                     # Python library to make hash code - 256 bit code and 64 character
import json                                        # Python library to make JSON file, JSON structure
from flask import Flask, jsonify                   # Python library for creating local server


class BlockChain:                                  # Class named blockchain
    def __init__(self):                            # Initializer wakes up on creation of object
        self.chain = []                            # An array which will contain the BLOCK
        self.create_block(
            proof=1, previous_hash=0
        )                                          # Proof = nonce , Previous hash = Unicode code
                                                   # previous block which will get checked with previous block
    def create_block(self, proof, previous_hash):  # A function to create a new block
        block = {                                  # Dictionary to store information
            "index": len(self.chain) + 1,          # Index is no. of each block
            "proof": proof,                        # Nonce - Is a code which will change the hash
                                                   # such that it will stasisfy our parameter
            "timestamp": str(
                datetime.datetime.now()
            ),                                     # Timestamp  to get time at which the block was created
            "previous_hash": previous_hash,
                                                   # Previous block which will get checked with previous block
        }
        self.chain.append(block)                   # Adding the block to the chain if created
        return block                               # Return the block

    def get_previous_block(self):                  # To get the previous block
        return self.chain[-1]

    def proof_of_work(
        self, previous_hash
    ):                                             # A function to check if the new added block stisfies our protocol
        new_proof = 1                              # Proof of firrst element
        check_proof = False                        # Currrent block proof stauts
        while check_proof is False:                # check until nonce satisfy our protocol
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_hash ** 2).encode()
            ).hexdigest()                          # convert no. genrated from our algo of nonce into hexadecimal
            if hash_operation[:4] == "0000":       # Our protocol is if the first 4 digits are 0000 then approve
                print(hash_operation)
                check_proof = True
            else:
                new_proof += 1                     # Go to nect nonce
            return new_proof            

    def hash(self, block):                         # Function to covert block into JSON and convertinv into SHA256
        encode_block = json.dumps(block, sort_keys=True).encode() # Encoding to JSON objects 
        return hashlib.sha256(encode_block).hexdigest()           # Secure hash algorithm 256 converts any data file into 64 character

    def list_valid(self, chain):
        previous_block = chain[0]  # first block is genisis block
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
            block = previous_block
            block_index += 1


# creating a web server
# creating flask server object
app = Flask(__name__)

blockChain = BlockChain()


@app.route("/mine_block", methods=["GET"])
def mine_block():
    previous_block = blockChain.get_previous_block()
    previous_proof = previous_block["proof"]
    proof = blockChain.proof_of_work(previous_proof)
    previous_hash = blockChain.hash(previous_block)
    block = blockChain.create_block(proof, previous_hash)
    response = {
        "message": "YOOOO Block mIneDDD",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }
    return jsonify(response), 200  # Sucessfull run code


app.run(debug=True, port="5000")

