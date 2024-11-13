import hashlib
import time

# Block header structure equivalent in Python
class Block:
    def __init__(self, index, previous_hash, data, timestamp=None, nonce=0):
        """Initialize a new block with the given parameters."""
        self.index = index
        self.previous_hash = previous_hash
        self.data = data
        self.timestamp = timestamp or int(time.time())
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculate the SHA-256 hash of the block."""
        block_string = f"{self.index}{self.previous_hash}{self.data}{self.timestamp}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        """Mine the block by finding a hash that meets the difficulty criteria."""
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()

# Blockchain structure
class Blockchain:
    def __init__(self, difficulty=2):
        """Initialize the blockchain with a genesis block and a specified difficulty."""
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        """Create the first block in the blockchain, known as the genesis block."""
        return Block(0, "0", "Genesis Block")

    def get_latest_block(self):
        """Return the latest block in the blockchain."""
        return self.chain[-1]

    def add_block(self, new_block):
        """Add a new block to the blockchain after mining it."""
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        """Check the validity of the blockchain by verifying hashes and previous hashes."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid block at index {i}: hash mismatch.")
                return False
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid block at index {i}: previous hash mismatch.")
                return False
        return True

    def print_chain(self):
        """Print the details of each block in the blockchain."""
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"  Hash: {block.hash}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Data: {block.data}")
            print(f"  Timestamp: {block.timestamp}")
            print(f"  Nonce: {block.nonce}\n")
class Transaction:
    """Represents a transaction in the blockchain."""
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __repr__(self):
        return f"Transaction({self.sender} -> {self.receiver}: {self.amount})"

    def to_dict(self):
        """Converts transaction to a dictionary for serialization."""
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount
        }

class Block:
    """Modified Block class to include transactions."""
    def __init__(self, index, previous_hash, transactions, timestamp=None, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions  # Now holds a list of Transaction objects
        self.timestamp = timestamp or int(time.time())
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculates the SHA-256 hash of the block, including transactions."""
        transactions_str = "".join([str(tx) for tx in self.transactions])
        block_string = f"{self.index}{self.previous_hash}{transactions_str}{self.timestamp}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()

# Example of creating a transaction and adding it to a block
tx1 = Transaction("Alice", "Bob", 50)
tx2 = Transaction("Bob", "Charlie", 25)
block = Block(1, "previous_hash_placeholder", [tx1, tx2])
import hashlib
import json

def hash_data(data):
    return hashlib.sha256(data.encode()).hexdigest()

class MerkleTree:
    """Merkle Tree for storing transactions and calculating the Merkle Root."""
    def __init__(self, transactions):
        self.transactions = transactions
        self.root = self.build_tree([hash_data(str(tx)) for tx in transactions])

    def build_tree(self, leaves):
        """Recursively builds the tree and returns the Merkle root."""
        if len(leaves) == 1:
            return leaves[0]
        
        # If odd number of leaves, duplicate the last hash
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1])

        # Pairwise hashing
        parent_layer = []
        for i in range(0, len(leaves), 2):
            parent_hash = hash_data(leaves[i] + leaves[i + 1])
            parent_layer.append(parent_hash)

        return self.build_tree(parent_layer)
class Block:
    def __init__(self, index, previous_hash, transactions, timestamp=None, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = timestamp or int(time.time())
        self.nonce = nonce
        self.merkle_root = MerkleTree(transactions).root  # Calculate the Merkle root
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculates the SHA-256 hash of the block, including the Merkle root."""
        block_string = f"{self.index}{self.previous_hash}{self.merkle_root}{self.timestamp}{self.nonce}".encode()
        return hashlib.sha256(block_string).hexdigest()
import json

class Blockchain:
    def __init__(self, difficulty=2, filename="blockchain.json"):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.filename = filename
        self.load_chain()

    def create_genesis_block(self):
        return Block(0, "0", [], nonce=0)

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.save_chain()

    def save_chain(self):
        """Saves the blockchain to a JSON file."""
        with open(self.filename, "w") as f:
            json.dump([self.block_to_dict(block) for block in self.chain],
