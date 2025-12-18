# Chess WLD Project Installer

A comprehensive, cross-platform installer script for the Chess WLD blockchain gaming platform. This installer automates the complete setup process, creating a production-ready chess game with World ID verification and crypto rewards.

## Features

✨ **Enhanced Functionality:**
- 🔍 Automatic dependency detection (Node.js, npm, Git)
- 🎯 Interactive configuration mode
- 🚩 Multiple command-line flags for automation
- 🎨 Color-coded output for better readability
- 📊 Progress tracking with step-by-step feedback
- ⏱️ Execution time tracking
- 🔄 Automatic rollback on errors
- 📝 Comprehensive logging
- ✅ Input validation (wallet address, project name, disk space)
- 🌍 Cross-platform support (Linux, macOS, Windows Git Bash)

## Prerequisites

Before running the installer, ensure you have:

- **Node.js** v18.0.0 or higher ([Download](https://nodejs.org/))
- **npm** (comes with Node.js)
- **Git** (optional, for version control) ([Download](https://git-scm.com/))
- At least **500MB** of free disk space

## Quick Start

### Basic Installation

```bash
cd chess-wld-installer
chmod +x install.sh
./install.sh
```

This will create a new project called `chess-wld` with the default wallet address.

## Usage

### Interactive Mode

Run the installer in interactive mode to customize your configuration:

```bash
./install.sh --interactive
```

You'll be prompted to configure:
- Project name
- Wallet address
- Whether to install dependencies automatically
- Whether to initialize a git repository

### Command-Line Flags

```bash
./install.sh [OPTIONS]
```

#### Available Options

| Flag | Description |
|------|-------------|
| `-h, --help` | Show help message and exit |
| `-w, --wallet ADDRESS` | Specify custom wallet address |
| `-p, --project NAME` | Specify custom project name |
| `-i, --interactive` | Enable interactive configuration mode |
| `--no-git` | Skip git repository initialization |
| `--no-install` | Skip npm dependencies installation |
| `-v, --verbose` | Enable verbose mode with detailed logging |

### Examples

#### Custom Wallet and Project Name

```bash
./install.sh --wallet 0xYourWalletAddress --project my-chess-game
```

#### Verbose Mode with Custom Configuration

```bash
./install.sh --wallet 0xABC123... --project custom-chess --verbose
```

#### Skip Dependency Installation (for CI/CD)

```bash
./install.sh --no-install --verbose
```

#### Full Interactive Setup

```bash
./install.sh --interactive --verbose
```

## What Gets Installed

The installer creates a complete project structure:

```
chess-wld/
├── src/
│   ├── components/         # React components (ChessBoard, WorldID, etc.)
│   ├── contracts/          # Solidity smart contracts
│   ├── pages/             # Next.js pages
│   ├── utils/             # Utility functions
│   └── styles/            # CSS stylesheets
├── scripts/               # Deployment scripts
├── test/                  # Test files
├── public/               # Static assets
├── package.json          # Dependencies and scripts
├── hardhat.config.js     # Hardhat configuration
├── next.config.js        # Next.js configuration
├── .env.local           # Environment variables
└── README.md            # Project documentation
```

## Output Format

The installer provides clear, color-coded feedback:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ♟️  Chess WLD Project Installer v2.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Node.js v18.17.0 detected
✓ npm v9.6.7 detected
✓ Git v2.39.0 detected

📦 Project Configuration
   Name: chess-wld
   Wallet: 0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6
   Location: ./chess-wld

[1/8] Creating project structure...        ✓ Done (0.2s)
[2/8] Generating configuration files...    ✓ Done (0.5s)
[3/8] Creating React components...         ✓ Done (1.1s)
[4/8] Creating smart contracts...          ✓ Done (0.8s)
[5/8] Setting up styles...                 ✓ Done (0.3s)
[6/8] Initializing Git repository...       ✓ Done (0.2s)
[7/8] Installing dependencies...           ✓ Done (45.3s)
[8/8] Running post-install checks...       ✓ Done (0.4s)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Installation Complete! (48.8s)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 Project: ./chess-wld
💰 Wallet: 0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6
⏱️  Total time: 48s

Next steps:
  1. cd chess-wld
  2. Update .env.local with your World App ID
  3. npm run dev
  4. Open http://localhost:3000

📖 Documentation: ./chess-wld/README.md
🔧 Configuration: ./chess-wld/.env.local
📝 Full log: ./install.log
```

## Post-Installation

After the installer completes:

1. **Navigate to your project:**
   ```bash
   cd chess-wld
   ```

2. **Update environment variables** in `.env.local`:
   - Add your World App ID from [Worldcoin Developer Portal](https://developer.worldcoin.org/)
   - Add your WalletConnect Project ID from [WalletConnect Cloud](https://cloud.walletconnect.com/)

3. **Start the development server:**
   ```bash
   npm run dev
   ```

4. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Validation

The installer performs several validation checks:

- ✅ Node.js version (minimum v18.0.0)
- ✅ npm installation
- ✅ Git installation (optional)
- ✅ Wallet address format (must be valid Ethereum address)
- ✅ Project name (alphanumeric, hyphens, underscores only)
- ✅ Disk space availability (minimum 500MB)
- ✅ Directory existence (prompts before overwriting)

## Error Handling

The installer includes robust error handling:

- **Automatic rollback:** If installation fails, the script automatically cleans up partial installations
- **Detailed logging:** All operations are logged to `install.log`
- **Clear error messages:** Each error includes actionable steps to resolve it
- **Exit codes:** Non-zero exit codes indicate failure for CI/CD integration

## Troubleshooting

### Common Issues

#### 1. Permission Denied

**Problem:** `./install.sh: Permission denied`

**Solution:**
```bash
chmod +x install.sh
./install.sh
```

#### 2. Node.js Version Too Old

**Problem:** `Node.js v16.x.x is too old`

**Solution:** Update Node.js to v18.0.0 or higher:
```bash
# Using nvm
nvm install 18
nvm use 18

# Or download from https://nodejs.org/
```

#### 3. Git Not Found

**Problem:** `Git is not installed (optional)`

**Solution:** Install Git or use `--no-git` flag:
```bash
# Install Git
# Ubuntu/Debian: sudo apt install git
# macOS: brew install git
# Windows: Download from https://git-scm.com/

# Or skip git
./install.sh --no-git
```

#### 4. Invalid Wallet Address

**Problem:** `Invalid wallet address format`

**Solution:** Ensure your wallet address:
- Starts with `0x`
- Contains exactly 40 hexadecimal characters
- Example: `0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6`

#### 5. Directory Already Exists

**Problem:** `Directory 'chess-wld' already exists!`

**Solution:** 
- Remove the existing directory: `rm -rf chess-wld`
- Or use a different project name: `./install.sh --project chess-wld-2`

#### 6. Network/npm Install Failures

**Problem:** Dependencies fail to install

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Try again with verbose output
./install.sh --verbose

# Or install dependencies manually later
./install.sh --no-install
cd chess-wld
npm install
```

#### 7. Insufficient Disk Space

**Problem:** `Insufficient disk space`

**Solution:** Free up at least 500MB of disk space before running the installer.

### Checking Logs

If you encounter issues, check the detailed log file:

```bash
cat install.log
```

Or view it in real-time during installation:

```bash
./install.sh --verbose
```

## Platform-Specific Notes

### Linux

- Works on all major distributions (Ubuntu, Debian, Fedora, Arch, etc.)
- Make sure you have build tools: `sudo apt install build-essential`

### macOS

- Requires Xcode Command Line Tools: `xcode-select --install`
- Homebrew recommended for installing dependencies

### Windows (Git Bash)

- Install [Git for Windows](https://git-scm.com/download/win) which includes Git Bash
- Run the script from Git Bash, not Command Prompt or PowerShell
- Node.js installer for Windows available at [nodejs.org](https://nodejs.org/)

## FAQ

### Q: Can I use this installer multiple times?

**A:** Yes! Use different project names with the `--project` flag to create multiple installations.

### Q: What if I want to use a different blockchain network?

**A:** Edit the `.env.local` file in your project and update the `WORLDCHAIN_RPC_URL` to your desired network.

### Q: Can I skip the dependency installation and install later?

**A:** Yes! Use the `--no-install` flag, then run `npm install` manually in your project directory.

### Q: Is the installer safe to use in CI/CD pipelines?

**A:** Yes! The installer supports automation with flags like `--no-install`, `--no-git`, and `--verbose`. It also provides proper exit codes.

### Q: How do I update my installed project?

**A:** The installer creates a fresh project. To update an existing project, manually pull updates from the repository or run `npm update` in your project directory.

### Q: Where can I find the smart contract address?

**A:** The smart contract address is set during installation and can be found in:
- `.env.local` file
- `src/utils/blockchain.js`
- Installation output and logs

### Q: What versions of dependencies are installed?

**A:** Check the `package.json` file in your generated project for exact versions. The installer uses current stable versions at the time of generation.

## Advanced Usage

### Custom Configuration File

Create a `.install-config` file in the same directory as the script to set custom defaults:

```bash
PROJECT_NAME="my-default-project"
WALLET_ADDRESS="0xYourDefaultWallet"
SKIP_GIT=false
SKIP_INSTALL=false
```

### Scripted/Automated Installation

For automated deployments:

```bash
#!/bin/bash

# Automated installation script
./install.sh \
  --project "production-chess" \
  --wallet "0xProductionWallet" \
  --no-install \
  --verbose

# Continue with custom setup
cd production-chess
npm install --production
npm run build
```

## Support

- **Issues:** Report bugs at [GitHub Issues](https://github.com/asterin-star/star/issues)
- **Documentation:** [Main Repository](https://github.com/asterin-star/star)
- **Discord:** [Join our community](https://discord.gg/worldcoin)

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly on all platforms
5. Submit a pull request

## License

MIT License - see the main repository for details.

## Credits

Built with ❤️ for World Chain

- Chess Engine: [chess.js](https://github.com/jhlywa/chess.js)
- UI Components: [react-chessboard](https://github.com/Clariity/react-chessboard)
- Identity Verification: [Worldcoin](https://worldcoin.org/)
- Smart Contracts: [Hardhat](https://hardhat.org/)

---

**Version:** 2.0.0  
**Last Updated:** 2025-12-18  
**Compatibility:** Linux, macOS, Windows (Git Bash)
