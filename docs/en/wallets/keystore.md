# Key Management (Keystore)

ComputeChain CLI (`cpc-cli`) provides tools for key management through keystore.

## Key Location

**Directory:** `~/.computechain/keys/` (default CLI location)

**Structure:**

```
~/.computechain/keys/
├── alice.json
├── bob.json
└── faucet.json
```

**Key File Format:**

```json
{
  "name": "alice",
  "address": "cpc1...",
  "public_key": "02a1b2c3...",
  "private_key": "4f3edf98..."   // 32-byte secp256k1 key in hex
}
```

**⚠️ Important:** In MVP, keys are stored **unencrypted**. Do not share key files!

## CLI Commands

### Create New Key

```bash
./cpc-cli keys add <NAME>
```

**Example:**

```bash
./cpc-cli keys add alice
```

**Output:**

```
Key 'alice' created.
Address: cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
Pubkey:  02a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6
Important: Private key saved unencrypted (MVP). Do not share!
```

### Import Existing Key

```bash
./cpc-cli keys import <NAME> --private-key <HEX_PRIVATE_KEY>
```

**Example:**

```bash
./cpc-cli keys import faucet --private-key 4f3edf982522b4e51b7e8b5f2f9c4d1d7a9e5f8c2b6d4e1a3c5b7d9e0f1a2b3c
```

**Usage:**
- Import faucet key from Node A to CLI
- Restore key from backup

### List Keys

```bash
./cpc-cli keys list
```

**Output:**

```
Name            Address                                          
------------------------------------------------------------
alice           cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t
faucet          cpc1f1a2u3c4e5t6k7e8y9a0b1c2d3e4f5g6h7i8j9k0
```

### Show Key Details

```bash
./cpc-cli keys show <NAME>
```

**Example:**

```bash
./cpc-cli keys show alice
```

**Output:**

```json
{
  "name": "alice",
  "address": "cpc1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t",
  "public_key": "02a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6"
}
```

**Note:** Private key is not shown in output for security.

## Programmatic Access

### Using KeyStore in Python

```python
from computechain.cli.keystore import KeyStore

# Create instance
ks = KeyStore()

# Create new key
key = ks.create_key("alice")
print(f"Address: {key['address']}")

# Get existing key
alice_key = ks.get_key("alice")
if alice_key:
    print(f"Address: {alice_key['address']}")
    print(f"Pubkey: {alice_key['public_key']}")
    # ⚠️ Private key available in alice_key['private_key']

# Import key
imported_key = ks.import_key("bob", "4f3edf982522b4e51b7e8b5f2f9c4d1d7a9e5f8c2b6d4e1a3c5b7d9e0f1a2b3c")

# List all keys
all_keys = ks.list_keys()
for k in all_keys:
    print(f"{k['name']}: {k['address']}")
```

## Security

### Current Limitations (MVP)

**⚠️ Keys stored unencrypted:**

- Files in `~/.computechain/keys/` contain private keys in plain text
- Do not share these files
- Do not commit them to Git
- Make backups in secure location

### Recommendations

1. **Backups:**
   ```bash
   # Save private keys in secure location
   cat ~/.computechain/keys/alice.json | jq -r '.private_key' > alice_privkey_backup.txt
   # Store backup in encrypted storage (e.g., password manager)
   ```

2. **File Permissions:**
   ```bash
   # Restrict access to key directory
   chmod 700 ~/.computechain/keys/
   ```

3. **Different Keys for Different Purposes:**
   - Separate key for validator
   - Separate key for regular transactions
   - Do not use faucet key for production

### Future Improvements

**Planned:**
- Password encryption for keys
- Hardware wallet support
- Multi-signature wallets

## Node Integration

### Using Validator Key

**Node A (Genesis):**

```bash
# Validator key located in:
.node_a/validator_key.hex
```

**Node B:**

```bash
# Validator key exported from CLI (dev/testing only):
python3 -c "from computechain.cli.keystore import KeyStore; print(KeyStore().get_key('alice')['private_key'])" > .node_b/validator_key.hex
```

> ⚠️ In production, generate and store validator keys securely on the node. Exporting private keys from CLI is convenient for devnet, but not recommended for mainnet.

### Using Faucet Key

**Node A:**

```bash
# Faucet key located in:
.node_a/faucet_key.hex
```

**Import to CLI:**

```bash
./cpc-cli keys import faucet --private-key $(cat .node_a/faucet_key.hex)
```

## Usage Examples

### Scenario: Creating Validator

```bash
# 1. Create Alice key
./cpc-cli keys add alice

# 2. Get Alice address
ALICE_ADDR=$(./cpc-cli keys show alice | grep address | awk '{print $2}' | tr -d '",')

# 3. Fund Alice (from faucet)
./cpc-cli tx send $ALICE_ADDR 2000 --from faucet --node http://localhost:8000

# 4. Stake Alice
./cpc-cli tx stake 1500 --from alice --node http://localhost:8000

# 5. Export key for node
python3 -c "from computechain.cli.keystore import KeyStore; print(KeyStore().get_key('alice')['private_key'])" > validator_key.hex
```

## Next Steps

- **[Address Formats](address-formats.md)** — Address formats
- **[Staking](../staking/staking-basic.md)** — How to become a validator
- **[CLI Guide](../cli/cpc-cli.md)** — Complete CLI command list
