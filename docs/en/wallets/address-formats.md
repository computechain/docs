# Address Formats

ComputeChain uses **Bech32** encoding for addresses with different prefixes depending on the entity type.

## Address Types

### Accounts

**Prefix:** `cpc`

**Example:** `cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t`

**Usage:**
- Regular users
- Transaction recipients
- Validator reward addresses (`reward_address`)

**Generation:**

```python
from computechain.protocol.crypto.keys import public_key_from_private
from computechain.protocol.crypto.address import address_from_pubkey

priv_key_bytes = bytes.fromhex("...")
pub_key_bytes = public_key_from_private(priv_key_bytes)
address = address_from_pubkey(pub_key_bytes, prefix="cpc")
```

### Validators

**Prefix:** `cpcvalcons` (consensus address)

**Example:** `cpcvalcons1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t`

**Usage:**
- Validator identification in consensus
- Address in `Validator.address`
- Used in `BlockHeader.proposer_address`

**Generation:**

```python
# When staking, pub_key is specified in payload
pub_key_hex = tx.payload.get("pub_key")
val_pub_bytes = bytes.fromhex(pub_key_hex)
val_addr = address_from_pubkey(val_pub_bytes, prefix="cpcvalcons")
```

**Important:** Validator has two addresses:
- `cpcvalcons...` — for consensus (used in blockchain)
- `cpc1...` — for receiving rewards (regular account)

### Operator Address (Future)

**Prefix:** `cpcvaloper` (config: `bech32_prefix_val`)

**Status:** Reserved for future use

**Planned usage:**
- Validator operator / self-delegator address
- Separation of operator from consensus address

## Address Structure

**Bech32 format:**

```
<prefix>1<data><checksum>
```

**Components:**
- `prefix`: Prefix (cpc, cpcvalcons, cpcvaloper)
- `1`: Separator
- `data`: Encoded data (20 bytes for address)
- `checksum`: Checksum for error detection

## Usage Examples

### Creating Address from Private Key

```python
from computechain.cli.keystore import KeyStore

ks = KeyStore()
key = ks.create_key("alice")
print(f"Address: {key['address']}")  # cpc1...
print(f"Pubkey: {key['public_key']}")
```

### Getting Validator Address

```python
from computechain.protocol.crypto.address import address_from_pubkey

# From validator public key
pub_key_hex = "02a1b2c3d4e5f6..."
pub_key_bytes = bytes.fromhex(pub_key_hex)
val_addr = address_from_pubkey(pub_key_bytes, prefix="cpcvalcons")
print(f"Validator address: {val_addr}")
```

### Validating Address Format

```python
from bech32 import bech32_decode

VALID_PREFIXES = {"cpc", "cpcvalcons", "cpcvaloper"}

def is_valid_address(address: str) -> bool:
    """Checks if string is a valid ComputeChain address"""
    if not address:
        return False

    hrp, data = bech32_decode(address)
    if hrp is None or data is None:
        return False

    return hrp in VALID_PREFIXES
```

## Prefix Configuration

**Network parameters:**

```python
# protocol/config/params.py
bech32_prefix_acc: str = "cpc"           # Accounts
bech32_prefix_val: str = "cpcvaloper"    # Operators (future)
bech32_prefix_cons: str = "cpcvalcons"   # Consensus addresses
```

**Current prefixes across networks:**
- Accounts: `cpc`
- Consensus: `cpcvalcons`
- Operator: `cpcvaloper` (reserved, not used in MVP)

## Next Steps

- **[Keystore](keystore.md)** — Key management
- **[Staking](../staking/staking-basic.md)** — How to become a validator
