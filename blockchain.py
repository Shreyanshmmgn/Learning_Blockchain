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

    def hash(self, block):                         # Function to covert block into JSON and converting into SHA256
        encode_block = json.dumps(block, sort_keys=True).encode() # Encoding to JSON objects 
        return hashlib.sha256(encode_block).hexdigest()           # Secure hash algorithm 256 converts any data file into 64 character

    def list_valid(self, chain):                    # to check if the chain is valid or not
        # idea is to check the current node's hash with next node's previous node for the whole chain, whenver we change the data of one
        # it's hash value will change and list will be invalid for that node. 
        previous_block = chain[0]                   # First block is genisis block
        block_index = 1                             # Block index of the 2nd block
        while block_index < len(chain):             # If block_index is less then len of chain  
            block = chain[block_index]              
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()
            ).hexdigest()                           #=======================??????====================
            if hash_operation[:4] != "0000":
                return False
            previous_block = block 
            block_index += 1                        # Go to the next block
        return True
                                                    # Creating a web server                                                    
app = Flask(__name__)                               # Creating flask server object

blockChain = BlockChain()                           # Object of the Class Blockchain


@app.route("/mine_block", methods=["GET"])          # Route is used fot routing the hhtp get request of mine block 
def mine_block():                                   # Fucntion to mine an block
    previous_block = blockChain.get_previous_block() 
    previous_proof = previous_block["proof"]
    proof = blockChain.proof_of_work(previous_proof)
    previous_hash = blockChain.hash(previous_block)
    block = blockChain.create_block(proof, previous_hash)   # New block is created with nonce = proof, and previous hash
    response = {                                            # It's standerd protocol to send respose once sucessfully creation of the block to let know the user
       "message": "YOOOO Block mIneDDD",
        "index": block["index"],
        "timestamp": block["timestamp"],
        "proof": block["proof"],
        "previous_hash": block["previous_hash"],
    }
    return jsonify(response), 200                   # Sucessfull run code  - 200
                                                    # 404 - Code for not found

@app.route("/show_chain", methods = ["GET"])
def show_chain():                                   # To show the Block Chain
    response = {
        "chain":blockChain.chain,
        "length": len(blockChain.chain)
    }
    return jsonify(response), 200



@app.route("/is_valid", methods = ["GET"])
def is_valid():                                      # To check if the list is valid
    is_valid = blockChain.list_valid(blockChain.chain)
    if is_valid:
        response = { "message" : "Chain is valid hurry---"}
    else:
        response = { "message" : "Chain is not valid---"}
    return jsonify(response), 200

app.run(debug=True, port="5000")                    # Run the App flask server on port 5000
