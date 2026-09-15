import hashlib, json, time

def sha256(b): return hashlib.sha256(b).hexdigest()
def hstr(s): return sha256(s.encode())

class MerkleTree:
    def __init__(self, leaves):
        self.leaves = [hstr(x) for x in leaves]
        self.levels = [self.leaves] if self.leaves else []
        self.build()

    def build(self):
        cur = self.leaves[:]
        while len(cur) > 1:
            cur = [sha256(bytes.fromhex(cur[i]) +
                    bytes.fromhex(cur[i+1] if i+1 < len(cur) else cur[i]))
                    for i in range(0, len(cur), 2)]
            self.levels.append(cur)

    def root(self):
        return self.levels[-1][0] if self.levels else ''

    def proof(self, idx):
        p, i = [], idx
        for lvl in self.levels[:-1]:
            s = i + 1 if i % 2 == 0 else i - 1
            if s >= len(lvl): s = i
            p.append((lvl[s], 'right' if i % 2 == 0 else 'left'))
            i //= 2
        return p

    @staticmethod
    def verify(leaf, proof, root):
        cur = hstr(leaf)
        for s, pos in proof:
            cur = sha256(bytes.fromhex(cur) + bytes.fromhex(s)) if pos == 'right' \
                  else sha256(bytes.fromhex(s) + bytes.fromhex(cur))
        return cur == root


class Block:
    def __init__(self, idx, txs, prev, diff=2):
        self.idx, self.txs, self.prev, self.diff = idx, txs[:], prev, diff
        self.ts, self.nonce = time.time(), 0
        self.merkle = MerkleTree(txs).root()
        self.hash = self._hash()

    def _hash(self):
        x = {'idx': self.idx, 'ts': self.ts, 'prev': self.prev,
             'nonce': self.nonce, 'merkle': self.merkle, 'cnt': len(self.txs)}
        return sha256(json.dumps(x, sort_keys=True).encode())

    def mine(self):
        while True:
            self.hash = self._hash()
            if self.hash.startswith('0' * self.diff): break
            self.nonce += 1


class Blockchain:
    def __init__(self, diff=2):
        self.diff, self.chain = diff, []
        g = Block(0, ['genesis'], '0' * 64, diff)
        g.mine()
        self.chain.append(g)

    def add(self, txs):
        b = Block(len(self.chain), txs, self.chain[-1].hash, self.diff)
        b.mine()
        self.chain.append(b)
        return b

    def valid(self):
        for i in range(1, len(self.chain)):
            b, p = self.chain[i], self.chain[i-1]
            if b.prev != p.hash or not b.hash.startswith('0' * b.diff):
                return False
            if MerkleTree(b.txs).root() != b.merkle or b._hash() != b.hash:
                return False
        return True


if __name__ == '__main__':
    bc = Blockchain(diff=3)

    b1 = bc.add(["Alice->Bob:5", "Carol->Dave:2", "Eve->Frank:7"])
    print("Block", b1.idx, "hash", b1.hash, "merkle", b1.merkle)

    b2 = bc.add(["Ivy->John:3", "Alice->Carol:1"])
    print("Block", b2.idx, "hash", b2.hash)

    print("Chain valid?", bc.valid())

    proof = MerkleTree(b1.txs).proof(1)
    print("Proof for tx:", b1.txs[1])
    print(proof)
    print("Verify:", MerkleTree.verify(b1.txs[1], proof, b1.merkle))
