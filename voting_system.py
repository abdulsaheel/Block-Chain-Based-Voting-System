from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import hashlib
import json
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Blockchain Model
class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.Float, nullable=False)
    proof = db.Column(db.Integer, nullable=False)
    previous_hash = db.Column(db.String(64), nullable=False)
    transactions = db.Column(db.Text, nullable=False)

# Initialize database
db.create_all()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=100, previous_hash='1')  # Genesis block

    def create_block(self, proof, previous_hash):
        transactions = json.dumps(self.transactions)
        block = Block(
            index=len(self.chain) + 1,
            timestamp=time.time(),
            proof=proof,
            previous_hash=previous_hash,
            transactions=transactions
        )
        db.session.add(block)
        db.session.commit()
        self.transactions = []
        self.chain.append(block.__dict__)
        return block

    def get_previous_block(self):
        return Block.query.order_by(Block.index.desc()).first()

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self):
        previous_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, voter_id, party):
        self.transactions.append({
            'voter_id': voter_id,
            'party': party
        })
        previous_block = self.get_previous_block()
        return previous_block.index + 1

# Flask API
blockchain = Blockchain()
parties = {'BRS': 0, 'CONGRESS': 0, 'CPI': 0}

@app.route('/get_votes', methods=['GET'])
def get_votes():
    response = {
        'parties': parties
    }
    return jsonify(response), 200

@app.route('/cast_vote', methods=['POST'])
def cast_vote():
    json = request.get_json()
    required = ['name', 'party']
    if not all(k in json for k in required):
        return 'Some elements are missing', 400

    voter_name = json['name']
    party = json['party']
    
    if party not in parties:
        return 'Invalid party', 400

    # Hash the voter's details
    voter_id = hashlib.sha256(voter_name.encode()).hexdigest()
    
    # Add transaction
    index = blockchain.add_transaction(voter_id, party)
    
    # Mine a new block
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block.proof
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.create_block(proof, previous_hash)

    # Update party votes
    parties[party] += 1

    response = {
        'message': f'Vote casted for {party}. Your ID is {voter_id}.',
        'block_index': index
    }
    return jsonify(response), 201

@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid()
    if is_valid:
        response = {'message': 'The blockchain is valid.'}
    else:
        response = {'message': 'The blockchain is not valid.'}
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
