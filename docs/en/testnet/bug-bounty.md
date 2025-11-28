# Bug Bounty Program

Reward program for discovering vulnerabilities and bugs in ComputeChain.

## Program Goals

- Improve network security
- Discover critical vulnerabilities before mainnet
- Improve code quality
- Build community

## Reward Policy

Rewards are discretionary and discussed individually (paid in CPC testnet/mainnet tokens or fiat) depending on severity, impact, and quality of the report.

## Severity Levels

### Critical

**Description:** Vulnerabilities that can lead to:
- Loss of user funds
- Consensus compromise
- Complete network shutdown

**Examples:**
- Double spending
- Transaction validation bypass
- Block forgery
- Private key leakage

**Reward:** By agreement (case-by-case discussion)

### High

**Description:** Vulnerabilities that can lead to:
- Partial functionality loss
- DoS attacks
- Incorrect reward calculation

**Examples:**
- DoS via mempool
- Incorrect stake calculation
- Synchronization issues

**Reward:** By agreement

### Medium

**Description:** Vulnerabilities that can lead to:
- Usage inconvenience
- Incorrect behavior in edge cases

**Examples:**
- Gas calculation issues
- Incorrect error handling
- UI/UX issues

**Reward:** By agreement

### Low

**Description:** Minor bugs and improvements

**Examples:**
- Documentation typos
- Performance improvements
- UX improvements

**Reward:** Recognition in documentation

## How to Report a Bug

### Step 1: Prepare Report

**Report template:**

```markdown
## Problem Description

Brief description of the problem.

## Reproduction Steps

1. Step 1
2. Step 2
3. Step 3

## Expected Behavior

What should have happened.

## Actual Behavior

What actually happened.

## Version

- ComputeChain version: X.Y.Z
- Python version: X.Y.Z
- OS: Linux/macOS/Windows

## Logs

```
Insert logs here
```

## Additional Information

Any additional information.
```

### Step 2: Submit Report

**Options:**

1. **GitHub Issues:**
   - Create issue in repository
   - Use "Bug Report" template
   - Do not publish exploit details publicly

2. **Email (for critical vulnerabilities, planned):**
   - security@computechain.ru
   - Use PGP encryption (if available)

3. **Telegram/Discord (planned community channels):**
   - Contact team directly
   - Only for non-critical issues

### Step 3: Wait for Response

**Timeframes:**

- Critical: Within 24 hours
- High: Within 48 hours
- Medium: Within 1 week
- Low: Within 2 weeks

## Rules

### Do's

- ✅ Report issues responsibly
- ✅ Provide detailed information
- ✅ Do not use vulnerabilities for personal gain
- ✅ Give team time to fix before publishing

### Don'ts

- ❌ Do not attack network without permission
- ❌ Do not publish exploit details before fix (coordinate public disclosure with team)
- ❌ Do not attempt to access others' funds
- ❌ Do not spam reports

## Fix Process

### 1. Confirmation

- Team confirms problem
- Assesses severity level
- Determines fix priority

### 2. Fix

- Develop patch
- Testing
- Deploy to testnet

### 3. Reward

- After fix and verification
- Payment in CPC tokens or fiat
- Recognition in documentation

## Good Report Examples

### Example 1: Critical Vulnerability

```markdown
## Problem Description

Discovered possibility of double spending via race condition in mempool.

## Reproduction Steps

1. Send transaction A with nonce N
2. Quickly send transaction B with same nonce N and higher gas price
3. Both transactions included in different blocks

## Expected Behavior

Second transaction should be rejected due to nonce duplication.

## Actual Behavior

Both transactions included in blocks, leading to double spending.

## Version

- ComputeChain version: 0.4.0
- Python version: 3.12.0
- OS: Linux

## Logs

[Logs attached]
```

### Example 2: Medium Issue

```markdown
## Problem Description

Gas price not considered in fee calculation in some cases.

## Reproduction Steps

1. Send transaction with --gas-price 5000
2. Check actual fee in block
3. Fee calculated with gas_price=1000 instead of 5000

## Version

- ComputeChain version: 0.4.0
```

## Acknowledgments

List of security researchers who helped improve ComputeChain:

- (Will be updated as reports are received)

## Next Steps

- **[Known Issues](known-issues.md)** — Known issues
- **[Join Testnet](join.md)** — Connect to testnet
- **[Security](../understand/overview.md)** — Network security
