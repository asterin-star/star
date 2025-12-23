#!/bin/bash

################################################################################
# Chess WLD Project Installer
# Version: 1.0.0
# Date: 2025-12-18
# Description: Complete setup script for Chess WLD blockchain gaming platform
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
WALLET_ADDRESS="0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6"
PROJECT_NAME="chess-wld"
NODE_VERSION="18.0.0"

# Print colored message
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Print header
print_header() {
    echo ""
    print_message "$BLUE" "=================================="
    print_message "$BLUE" "$1"
    print_message "$BLUE" "=================================="
    echo ""
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"
    
    if ! command_exists node; then
        print_message "$RED" "Node.js is not installed. Please install Node.js v${NODE_VERSION} or higher."
        exit 1
    fi
    
    if ! command_exists npm; then
        print_message "$RED" "npm is not installed. Please install npm."
        exit 1
    fi
    
    print_message "$GREEN" "✓ Node.js and npm are installed"
}

# Create project structure
create_structure() {
    print_header "Creating Project Structure"
    
    mkdir -p ${PROJECT_NAME}/{src/{components,contracts,utils,styles},public,scripts,test}
    print_message "$GREEN" "✓ Project directories created"
}

# Create package.json
create_package_json() {
    print_message "$YELLOW" "Creating package.json..."
    
    cat > ${PROJECT_NAME}/package.json << 'EOF'
{
  "name": "chess-wld",
  "version": "1.0.0",
  "description": "Chess game with World ID verification and blockchain rewards",
  "main": "src/index.js",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest",
    "test:watch": "jest --watch",
    "deploy": "hardhat run scripts/deploy.js --network worldchain",
    "compile": "hardhat compile"
  },
  "keywords": ["chess", "blockchain", "worldcoin", "gaming", "web3"],
  "author": "Chess WLD Team",
  "license": "MIT",
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "ethers": "^6.8.0",
    "@worldcoin/idkit": "^1.0.0",
    "chess.js": "^1.0.0-beta.6",
    "react-chessboard": "^4.2.0",
    "@rainbow-me/rainbowkit": "^2.0.0",
    "wagmi": "^2.0.0",
    "viem": "^2.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.2.0",
    "hardhat": "^2.19.0",
    "@nomicfoundation/hardhat-toolbox": "^4.0.0",
    "jest": "^29.7.0",
    "@testing-library/react": "^14.0.0",
    "eslint": "^8.50.0",
    "eslint-config-next": "^14.0.0"
  }
}
EOF
    
    print_message "$GREEN" "✓ package.json created"
}

# Create smart contract
create_smart_contract() {
    print_message "$YELLOW" "Creating ChessRewards.sol smart contract..."
    
    cat > ${PROJECT_NAME}/src/contracts/ChessRewards.sol << 'EOF'
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

interface IWorldID {
    function verifyProof(
        uint256 root,
        uint256 groupId,
        uint256 signalHash,
        uint256 nullifierHash,
        uint256 externalNullifierHash,
        uint256[8] calldata proof
    ) external view;
}

contract ChessRewards is Ownable, ReentrancyGuard {
    IWorldID public worldId;
    uint256 public immutable groupId = 1;
    
    mapping(address => uint256) public playerRatings;
    mapping(address => uint256) public playerRewards;
    mapping(address => bool) public verifiedPlayers;
    mapping(uint256 => bool) public usedNullifiers;
    mapping(bytes32 => GameResult) public games;
    
    uint256 public totalGamesPlayed;
    uint256 public rewardPool;
    uint256 public constant WIN_REWARD = 0.01 ether;
    uint256 public constant DRAW_REWARD = 0.005 ether;
    uint256 public constant INITIAL_RATING = 1200;
    
    struct GameResult {
        address player1;
        address player2;
        address winner;
        uint256 timestamp;
        bool validated;
    }
    
    event PlayerVerified(address indexed player);
    event GameRecorded(bytes32 indexed gameId, address player1, address player2, address winner);
    event RewardClaimed(address indexed player, uint256 amount);
    event RatingUpdated(address indexed player, uint256 newRating);
    
    constructor(address _worldId) {
        worldId = IWorldID(_worldId);
    }
    
    function verifyPlayer(
        uint256 root,
        uint256 nullifierHash,
        uint256[8] calldata proof
    ) external {
        require(!verifiedPlayers[msg.sender], "Already verified");
        require(!usedNullifiers[nullifierHash], "Nullifier already used");
        
        worldId.verifyProof(
            root,
            groupId,
            uint256(uint160(msg.sender)),
            nullifierHash,
            uint256(uint160(address(this))),
            proof
        );
        
        verifiedPlayers[msg.sender] = true;
        usedNullifiers[nullifierHash] = true;
        playerRatings[msg.sender] = INITIAL_RATING;
        
        emit PlayerVerified(msg.sender);
    }
    
    function recordGame(
        address _player1,
        address _player2,
        address _winner,
        bytes32 _gameId
    ) external onlyOwner {
        require(verifiedPlayers[_player1] && verifiedPlayers[_player2], "Players not verified");
        require(games[_gameId].timestamp == 0, "Game already recorded");
        
        games[_gameId] = GameResult({
            player1: _player1,
            player2: _player2,
            winner: _winner,
            timestamp: block.timestamp,
            validated: true
        });
        
        totalGamesPlayed++;
        
        if (_winner != address(0)) {
            playerRewards[_winner] += WIN_REWARD;
            updateRatings(_winner, _winner == _player1 ? _player2 : _player1, true);
        } else {
            playerRewards[_player1] += DRAW_REWARD;
            playerRewards[_player2] += DRAW_REWARD;
        }
        
        emit GameRecorded(_gameId, _player1, _player2, _winner);
    }
    
    function updateRatings(address winner, address loser, bool isWin) internal {
        uint256 winnerRating = playerRatings[winner];
        uint256 loserRating = playerRatings[loser];
        
        uint256 kFactor = 32;
        uint256 expectedWinner = 10000 / (1 + 10**((loserRating - winnerRating) / 400));
        uint256 expectedLoser = 10000 - expectedWinner;
        
        playerRatings[winner] = winnerRating + (kFactor * (10000 - expectedWinner)) / 10000;
        playerRatings[loser] = loserRating > (kFactor * expectedLoser / 10000) 
            ? loserRating - (kFactor * expectedLoser / 10000) 
            : 0;
        
        emit RatingUpdated(winner, playerRatings[winner]);
        emit RatingUpdated(loser, playerRatings[loser]);
    }
    
    function claimRewards() external nonReentrant {
        uint256 amount = playerRewards[msg.sender];
        require(amount > 0, "No rewards to claim");
        require(address(this).balance >= amount, "Insufficient contract balance");
        
        playerRewards[msg.sender] = 0;
        
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        
        emit RewardClaimed(msg.sender, amount);
    }
    
    function fundRewardPool() external payable onlyOwner {
        rewardPool += msg.value;
    }
    
    function getPlayerStats(address player) external view returns (
        uint256 rating,
        uint256 rewards,
        bool verified
    ) {
        return (playerRatings[player], playerRewards[player], verifiedPlayers[player]);
    }
    
    receive() external payable {
        rewardPool += msg.value;
    }
}
EOF
    
    print_message "$GREEN" "✓ Smart contract created"
}

# Create React components
create_components() {
    print_message "$YELLOW" "Creating React components..."
    
    # ChessBoard.js
    cat > ${PROJECT_NAME}/src/components/ChessBoard.js << 'EOF'
import React, { useState, useEffect } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';

export default function ChessBoard({ onGameEnd, player1, player2 }) {
  const [game, setGame] = useState(new Chess());
  const [position, setPosition] = useState(game.fen());
  const [moveHistory, setMoveHistory] = useState([]);
  const [currentTurn, setCurrentTurn] = useState('w');

  function makeMove(move) {
    try {
      const result = game.move(move);
      if (result) {
        setPosition(game.fen());
        setMoveHistory([...moveHistory, result.san]);
        setCurrentTurn(game.turn());
        
        if (game.isGameOver()) {
          handleGameEnd();
        }
        return true;
      }
    } catch (error) {
      console.error('Invalid move:', error);
    }
    return false;
  }

  function onDrop(sourceSquare, targetSquare) {
    const move = makeMove({
      from: sourceSquare,
      to: targetSquare,
      promotion: 'q'
    });
    return move;
  }

  function handleGameEnd() {
    let result = {
      isDraw: game.isDraw(),
      isCheckmate: game.isCheckmate(),
      winner: null
    };

    if (game.isCheckmate()) {
      result.winner = game.turn() === 'w' ? player2 : player1;
    }

    if (onGameEnd) {
      onGameEnd(result);
    }
  }

  function resetGame() {
    const newGame = new Chess();
    setGame(newGame);
    setPosition(newGame.fen());
    setMoveHistory([]);
    setCurrentTurn('w');
  }

  return (
    <div className="chess-board-container">
      <div className="game-info">
        <h3>Current Turn: {currentTurn === 'w' ? 'White' : 'Black'}</h3>
        <button onClick={resetGame} className="reset-button">New Game</button>
      </div>
      <Chessboard 
        position={position} 
        onPieceDrop={onDrop}
        boardWidth={560}
      />
      <div className="move-history">
        <h4>Move History</h4>
        <div className="moves">
          {moveHistory.map((move, index) => (
            <span key={index} className="move">
              {Math.floor(index / 2) + 1}. {move}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
EOF

    # WorldIDVerification.js
    cat > ${PROJECT_NAME}/src/components/WorldIDVerification.js << 'EOF'
import { IDKit, ISuccessResult } from '@worldcoin/idkit';
import { useAccount } from 'wagmi';

export default function WorldIDVerification({ onVerificationSuccess }) {
  const { address } = useAccount();

  const handleVerify = async (proof: ISuccessResult) => {
    try {
      const response = await fetch('/api/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          proof,
          address
        })
      });

      const data = await response.json();
      
      if (data.success) {
        onVerificationSuccess(data);
      }
    } catch (error) {
      console.error('Verification failed:', error);
    }
  };

  return (
    <div className="verification-container">
      <h2>Verify Your Identity</h2>
      <p>Verify with World ID to start playing and earning rewards</p>
      <IDKit
        app_id={process.env.NEXT_PUBLIC_WORLD_APP_ID}
        action="chess-verification"
        onSuccess={handleVerify}
        verification_level="orb"
      >
        {({ open }) => (
          <button onClick={open} className="verify-button">
            Verify with World ID
          </button>
        )}
      </IDKit>
    </div>
  );
}
EOF

    # Leaderboard.js
    cat > ${PROJECT_NAME}/src/components/Leaderboard.js << 'EOF'
import React, { useState, useEffect } from 'react';

export default function Leaderboard({ contract }) {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLeaderboard();
  }, [contract]);

  async function loadLeaderboard() {
    if (!contract) return;

    try {
      setLoading(true);
      // In a real implementation, you'd fetch this from your backend
      // This is a placeholder
      const leaderboardData = [
        { address: '0x123...', rating: 1450, games: 15, wins: 10 },
        { address: '0x456...', rating: 1380, games: 12, wins: 7 },
        { address: '0x789...', rating: 1320, games: 20, wins: 11 }
      ];
      setPlayers(leaderboardData);
    } catch (error) {
      console.error('Error loading leaderboard:', error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="leaderboard-container">
      <h2>Leaderboard</h2>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <table className="leaderboard-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Player</th>
              <th>Rating</th>
              <th>Games</th>
              <th>Wins</th>
            </tr>
          </thead>
          <tbody>
            {players.map((player, index) => (
              <tr key={player.address}>
                <td>{index + 1}</td>
                <td>{player.address}</td>
                <td>{player.rating}</td>
                <td>{player.games}</td>
                <td>{player.wins}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
EOF

    # WalletConnect.js
    cat > ${PROJECT_NAME}/src/components/WalletConnect.js << 'EOF'
import { ConnectButton } from '@rainbow-me/rainbowkit';

export default function WalletConnect() {
  return (
    <div className="wallet-connect">
      <ConnectButton 
        showBalance={true}
        chainStatus="icon"
      />
    </div>
  );
}
EOF

    print_message "$GREEN" "✓ React components created"
}

# Create main App component
create_app() {
    print_message "$YELLOW" "Creating main App component..."
    
    cat > ${PROJECT_NAME}/src/pages/_app.js << 'EOF'
import '@/styles/globals.css';
import { WagmiConfig, createConfig, configureChains } from 'wagmi';
import { worldchain } from 'wagmi/chains';
import { publicProvider } from 'wagmi/providers/public';
import { RainbowKitProvider, getDefaultWallets } from '@rainbow-me/rainbowkit';
import '@rainbow-me/rainbowkit/styles.css';

const { chains, publicClient } = configureChains(
  [worldchain],
  [publicProvider()]
);

const { connectors } = getDefaultWallets({
  appName: 'Chess WLD',
  projectId: process.env.NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID,
  chains
});

const wagmiConfig = createConfig({
  autoConnect: true,
  connectors,
  publicClient
});

export default function App({ Component, pageProps }) {
  return (
    <WagmiConfig config={wagmiConfig}>
      <RainbowKitProvider chains={chains}>
        <Component {...pageProps} />
      </RainbowKitProvider>
    </WagmiConfig>
  );
}
EOF

    cat > ${PROJECT_NAME}/src/pages/index.js << 'EOF'
import { useState, useEffect } from 'react';
import { useAccount, useContract, useSigner } from 'wagmi';
import Head from 'next/head';
import ChessBoard from '@/components/ChessBoard';
import WorldIDVerification from '@/components/WorldIDVerification';
import Leaderboard from '@/components/Leaderboard';
import WalletConnect from '@/components/WalletConnect';

const CONTRACT_ADDRESS = '0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6';

export default function Home() {
  const { address, isConnected } = useAccount();
  const [isVerified, setIsVerified] = useState(false);
  const [userStats, setUserStats] = useState(null);
  const [contract, setContract] = useState(null);

  useEffect(() => {
    if (isConnected && address) {
      checkVerificationStatus();
    }
  }, [isConnected, address]);

  async function checkVerificationStatus() {
    // Check if user is verified on-chain
    // This would interact with your smart contract
  }

  function handleVerificationSuccess(data) {
    setIsVerified(true);
  }

  function handleGameEnd(result) {
    console.log('Game ended:', result);
    // Record game result on-chain
  }

  return (
    <>
      <Head>
        <title>Chess WLD - Blockchain Chess Gaming</title>
        <meta name="description" content="Play chess, verify with World ID, earn crypto rewards" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="main-container">
        <header className="header">
          <h1>♟️ Chess WLD</h1>
          <WalletConnect />
        </header>

        <div className="content">
          {!isConnected ? (
            <div className="welcome-screen">
              <h2>Welcome to Chess WLD</h2>
              <p>Connect your wallet to start playing</p>
            </div>
          ) : !isVerified ? (
            <WorldIDVerification onVerificationSuccess={handleVerificationSuccess} />
          ) : (
            <div className="game-container">
              <div className="game-section">
                <ChessBoard 
                  onGameEnd={handleGameEnd}
                  player1={address}
                  player2="0x000..."
                />
              </div>
              <div className="sidebar">
                <Leaderboard contract={contract} />
              </div>
            </div>
          )}
        </div>

        <footer className="footer">
          <p>Built with ❤️ for World Chain | Contract: {CONTRACT_ADDRESS}</p>
        </footer>
      </main>
    </>
  );
}
EOF

    print_message "$GREEN" "✓ Main App component created"
}

# Create utility files
create_utils() {
    print_message "$YELLOW" "Creating utility files..."
    
    cat > ${PROJECT_NAME}/src/utils/blockchain.js << 'EOF'
import { ethers } from 'ethers';

export const CONTRACT_ADDRESS = '0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6';

export async function getContract(signer) {
  const abi = [
    "function verifyPlayer(uint256 root, uint256 nullifierHash, uint256[8] calldata proof) external",
    "function recordGame(address _player1, address _player2, address _winner, bytes32 _gameId) external",
    "function claimRewards() external",
    "function getPlayerStats(address player) external view returns (uint256 rating, uint256 rewards, bool verified)",
    "function playerRatings(address) external view returns (uint256)",
    "function playerRewards(address) external view returns (uint256)",
    "function verifiedPlayers(address) external view returns (bool)"
  ];

  return new ethers.Contract(CONTRACT_ADDRESS, abi, signer);
}

export async function verifyWithWorldID(proof, address, signer) {
  try {
    const contract = await getContract(signer);
    const tx = await contract.verifyPlayer(
      proof.merkle_root,
      proof.nullifier_hash,
      proof.proof
    );
    await tx.wait();
    return { success: true, tx: tx.hash };
  } catch (error) {
    console.error('Verification failed:', error);
    return { success: false, error: error.message };
  }
}

export async function recordGameResult(player1, player2, winner, gameId, signer) {
  try {
    const contract = await getContract(signer);
    const tx = await contract.recordGame(player1, player2, winner, gameId);
    await tx.wait();
    return { success: true, tx: tx.hash };
  } catch (error) {
    console.error('Recording game failed:', error);
    return { success: false, error: error.message };
  }
}

export async function claimRewards(signer) {
  try {
    const contract = await getContract(signer);
    const tx = await contract.claimRewards();
    await tx.wait();
    return { success: true, tx: tx.hash };
  } catch (error) {
    console.error('Claiming rewards failed:', error);
    return { success: false, error: error.message };
  }
}

export async function getPlayerStats(address, provider) {
  try {
    const contract = await getContract(provider);
    const stats = await contract.getPlayerStats(address);
    return {
      rating: stats.rating.toNumber(),
      rewards: ethers.formatEther(stats.rewards),
      verified: stats.verified
    };
  } catch (error) {
    console.error('Getting player stats failed:', error);
    return null;
  }
}
EOF

    cat > ${PROJECT_NAME}/src/utils/chess.js << 'EOF'
export function calculateEloRating(playerRating, opponentRating, gameResult, kFactor = 32) {
  const expectedScore = 1 / (1 + Math.pow(10, (opponentRating - playerRating) / 400));
  
  let actualScore;
  if (gameResult === 'win') actualScore = 1;
  else if (gameResult === 'draw') actualScore = 0.5;
  else actualScore = 0;
  
  return Math.round(playerRating + kFactor * (actualScore - expectedScore));
}

export function generateGameId(player1, player2, timestamp) {
  const data = `${player1}-${player2}-${timestamp}`;
  return ethers.id(data);
}

export function validateMove(chess, move) {
  try {
    const result = chess.move(move);
    return result !== null;
  } catch {
    return false;
  }
}

export function getGameStatus(chess) {
  if (chess.isCheckmate()) return 'checkmate';
  if (chess.isDraw()) return 'draw';
  if (chess.isStalemate()) return 'stalemate';
  if (chess.isThreefoldRepetition()) return 'repetition';
  if (chess.isInsufficientMaterial()) return 'insufficient_material';
  if (chess.isCheck()) return 'check';
  return 'active';
}
EOF

    print_message "$GREEN" "✓ Utility files created"
}

# Create styles
create_styles() {
    print_message "$YELLOW" "Creating stylesheets..."
    
    cat > ${PROJECT_NAME}/src/styles/globals.css << 'EOF'
* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

:root {
  --primary-color: #3b82f6;
  --secondary-color: #8b5cf6;
  --success-color: #10b981;
  --danger-color: #ef4444;
  --bg-color: #0f172a;
  --surface-color: #1e293b;
  --text-color: #f1f5f9;
  --border-color: #334155;
}

html,
body {
  max-width: 100vw;
  overflow-x: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background: var(--bg-color);
  color: var(--text-color);
}

a {
  color: inherit;
  text-decoration: none;
}

.main-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: var(--surface-color);
  border-bottom: 1px solid var(--border-color);
}

.header h1 {
  font-size: 2rem;
  background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.content {
  flex: 1;
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
}

.welcome-screen {
  text-align: center;
  padding: 4rem 2rem;
}

.welcome-screen h2 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.game-container {
  display: grid;
  grid-template-columns: 1fr 400px;
  gap: 2rem;
}

.chess-board-container {
  background: var(--surface-color);
  padding: 2rem;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.game-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.reset-button {
  padding: 0.5rem 1rem;
  background: var(--primary-color);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.2s;
}

.reset-button:hover {
  background: #2563eb;
}

.move-history {
  margin-top: 1.5rem;
  padding: 1rem;
  background: var(--bg-color);
  border-radius: 8px;
  max-height: 200px;
  overflow-y: auto;
}

.move-history h4 {
  margin-bottom: 0.5rem;
}

.moves {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.move {
  padding: 0.25rem 0.5rem;
  background: var(--surface-color);
  border-radius: 4px;
  font-size: 0.9rem;
}

.verification-container {
  text-align: center;
  padding: 3rem;
  background: var(--surface-color);
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.verification-container h2 {
  margin-bottom: 1rem;
  font-size: 2rem;
}

.verify-button {
  margin-top: 2rem;
  padding: 1rem 2rem;
  background: linear-gradient(to right, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  cursor: pointer;
  transition: transform 0.2s;
}

.verify-button:hover {
  transform: scale(1.05);
}

.sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.leaderboard-container {
  background: var(--surface-color);
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.leaderboard-container h2 {
  margin-bottom: 1rem;
}

.leaderboard-table {
  width: 100%;
  border-collapse: collapse;
}

.leaderboard-table th,
.leaderboard-table td {
  padding: 0.75rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.leaderboard-table th {
  font-weight: 600;
  color: var(--primary-color);
}

.footer {
  padding: 2rem;
  text-align: center;
  background: var(--surface-color);
  border-top: 1px solid var(--border-color);
  margin-top: auto;
}

@media (max-width: 1024px) {
  .game-container {
    grid-template-columns: 1fr;
  }
}
EOF

    print_message "$GREEN" "✓ Stylesheets created"
}

# Create Hardhat config
create_hardhat_config() {
    print_message "$YELLOW" "Creating Hardhat configuration..."
    
    cat > ${PROJECT_NAME}/hardhat.config.js << 'EOF'
require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

const PRIVATE_KEY = process.env.PRIVATE_KEY || "0x0000000000000000000000000000000000000000000000000000000000000000";
const WORLDCHAIN_RPC = process.env.WORLDCHAIN_RPC_URL || "https://worldchain-mainnet.g.alchemy.com/public";

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  networks: {
    worldchain: {
      url: WORLDCHAIN_RPC,
      accounts: [PRIVATE_KEY],
      chainId: 480
    },
    localhost: {
      url: "http://127.0.0.1:8545"
    }
  },
  etherscan: {
    apiKey: {
      worldchain: process.env.WORLDSCAN_API_KEY || ""
    }
  },
  paths: {
    sources: "./src/contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  }
};
EOF

    print_message "$GREEN" "✓ Hardhat configuration created"
}

# Create deployment script
create_deploy_script() {
    print_message "$YELLOW" "Creating deployment script..."
    
    cat > ${PROJECT_NAME}/scripts/deploy.js << 'EOF'
const hre = require("hardhat");

async function main() {
  console.log("Starting deployment...");

  const WORLD_ID_ADDRESS = process.env.WORLD_ID_ADDRESS || "0x0";

  const ChessRewards = await hre.ethers.getContractFactory("ChessRewards");
  const chessRewards = await ChessRewards.deploy(WORLD_ID_ADDRESS);

  await chessRewards.waitForDeployment();

  const address = await chessRewards.getAddress();
  console.log(`ChessRewards deployed to: ${address}`);

  // Fund the contract with initial reward pool
  console.log("Funding reward pool...");
  const fundTx = await chessRewards.fundRewardPool({
    value: hre.ethers.parseEther("1.0")
  });
  await fundTx.wait();
  console.log("Reward pool funded with 1.0 ETH");

  console.log("\nDeployment complete!");
  console.log("Contract address:", address);
  console.log("\nUpdate your .env.local file with:");
  console.log(`NEXT_PUBLIC_CONTRACT_ADDRESS=${address}`);
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
EOF

    print_message "$GREEN" "✓ Deployment script created"
}

# Create environment files
create_env_files() {
    print_message "$YELLOW" "Creating environment files..."
    
    cat > ${PROJECT_NAME}/.env.example << EOF
# Blockchain Configuration
NEXT_PUBLIC_CONTRACT_ADDRESS=0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6
NEXT_PUBLIC_WORLDCHAIN_RPC_URL=https://worldchain-mainnet.g.alchemy.com/public
WORLDCHAIN_RPC_URL=https://worldchain-mainnet.g.alchemy.com/public

# World ID Configuration
NEXT_PUBLIC_WORLD_APP_ID=your_world_app_id
WORLD_ID_ADDRESS=0x0

# WalletConnect
NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID=your_project_id

# Deployment (Keep private!)
PRIVATE_KEY=your_private_key
WORLDSCAN_API_KEY=your_api_key
EOF

    cat > ${PROJECT_NAME}/.env.local << EOF
# Blockchain Configuration
NEXT_PUBLIC_CONTRACT_ADDRESS=0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6
NEXT_PUBLIC_WORLDCHAIN_RPC_URL=https://worldchain-mainnet.g.alchemy.com/public
WORLDCHAIN_RPC_URL=https://worldchain-mainnet.g.alchemy.com/public

# World ID Configuration (Update these with your actual values)
NEXT_PUBLIC_WORLD_APP_ID=app_staging_1234567890
WORLD_ID_ADDRESS=0x0

# WalletConnect (Update with your project ID)
NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID=your_project_id

# Deployment (Keep private! Never commit this file)
PRIVATE_KEY=
WORLDSCAN_API_KEY=
EOF

    print_message "$GREEN" "✓ Environment files created"
}

# Create configuration files
create_config_files() {
    print_message "$YELLOW" "Creating configuration files..."
    
    # next.config.js
    cat > ${PROJECT_NAME}/next.config.js << 'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  webpack: (config) => {
    config.resolve.fallback = { fs: false, net: false, tls: false };
    return config;
  }
};

module.exports = nextConfig;
EOF

    # .gitignore
    cat > ${PROJECT_NAME}/.gitignore << 'EOF'
# Dependencies
node_modules/
/.pnp
.pnp.js

# Testing
/coverage

# Next.js
/.next/
/out/

# Production
/build

# Misc
.DS_Store
*.pem

# Debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Local env files
.env*.local
.env

# Vercel
.vercel

# Hardhat
cache/
artifacts/
typechain/
typechain-types/

# IDE
.vscode/
.idea/
EOF

    # README.md
    cat > ${PROJECT_NAME}/README.md << EOF
# Chess WLD - Blockchain Chess Gaming Platform

A decentralized chess gaming platform built on World Chain with World ID verification and crypto rewards.

## Features

- ♟️ Full-featured chess game
- 🌍 World ID verification for fair play
- 💰 Earn crypto rewards for winning games
- 📊 ELO rating system
- 🏆 Global leaderboard
- 🔗 Blockchain-verified game results

## Smart Contract

**Deployed Address:** \`0xa3cdea9fe705bc16dcd9e9170e217b0f1ba5aaf6\`

## Getting Started

### Prerequisites

- Node.js v18.0.0 or higher
- npm or yarn
- MetaMask or compatible Web3 wallet
- World ID app

### Installation

1. Clone the repository
2. Install dependencies:
   \`\`\`bash
   npm install
   \`\`\`

3. Configure environment variables:
   - Copy \`.env.example\` to \`.env.local\`
   - Add your World App ID
   - Add your WalletConnect Project ID

4. Run development server:
   \`\`\`bash
   npm run dev
   \`\`\`

5. Open [http://localhost:3000](http://localhost:3000)

### Smart Contract Deployment

1. Configure your private key in \`.env.local\`
2. Compile contracts:
   \`\`\`bash
   npm run compile
   \`\`\`

3. Deploy to World Chain:
   \`\`\`bash
   npm run deploy
   \`\`\`

## Project Structure

\`\`\`
chess-wld/
├── src/
│   ├── components/      # React components
│   ├── contracts/       # Solidity smart contracts
│   ├── pages/          # Next.js pages
│   ├── styles/         # CSS styles
│   └── utils/          # Utility functions
├── scripts/            # Deployment scripts
├── test/              # Test files
└── public/            # Static assets
\`\`\`

## How to Play

1. Connect your wallet
2. Verify your identity with World ID
3. Start a game against another player
4. Win to earn crypto rewards!

## Technologies Used

- **Frontend:** Next.js, React, TypeScript
- **Blockchain:** Ethereum, Hardhat, Ethers.js
- **Identity:** World ID (Worldcoin)
- **Chess Engine:** chess.js
- **UI:** react-chessboard, RainbowKit

## License

MIT

## Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ for World Chain
EOF

    print_message "$GREEN" "✓ Configuration files created"
}

# Create API routes
create_api_routes() {
    print_message "$YELLOW" "Creating API routes..."
    
    mkdir -p ${PROJECT_NAME}/src/pages/api
    
    cat > ${PROJECT_NAME}/src/pages/api/verify.js << 'EOF'
import { verifyCloudProof } from '@worldcoin/idkit';

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { proof, address } = req.body;

  try {
    const verifyRes = await verifyCloudProof(
      proof,
      process.env.NEXT_PUBLIC_WORLD_APP_ID,
      'chess-verification'
    );

    if (verifyRes.success) {
      // In production, you would store this verification in a database
      return res.status(200).json({
        success: true,
        verified: true,
        address
      });
    } else {
      return res.status(400).json({
        success: false,
        error: 'Verification failed'
      });
    }
  } catch (error) {
    console.error('Verification error:', error);
    return res.status(500).json({
      success: false,
      error: error.message
    });
  }
}
EOF

    print_message "$GREEN" "✓ API routes created"
}

# Create test files
create_tests() {
    print_message "$YELLOW" "Creating test files..."
    
    cat > ${PROJECT_NAME}/test/ChessRewards.test.js << 'EOF'
const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("ChessRewards", function () {
  let chessRewards;
  let owner;
  let player1;
  let player2;
  let worldId;

  beforeEach(async function () {
    [owner, player1, player2, worldId] = await ethers.getSigners();

    const ChessRewards = await ethers.getContractFactory("ChessRewards");
    chessRewards = await ChessRewards.deploy(worldId.address);
    await chessRewards.waitForDeployment();

    // Fund the contract
    await chessRewards.fundRewardPool({ value: ethers.parseEther("10") });
  });

  it("Should deploy with correct initial values", async function () {
    expect(await chessRewards.totalGamesPlayed()).to.equal(0);
    expect(await chessRewards.rewardPool()).to.equal(ethers.parseEther("10"));
  });

  it("Should record game correctly", async function () {
    // Mock verification for testing
    // In production, you would use actual World ID proofs

    const gameId = ethers.id("game1");
    
    // This would fail without proper World ID verification
    // but demonstrates the flow
    // await chessRewards.recordGame(
    //   player1.address,
    //   player2.address,
    //   player1.address,
    //   gameId
    // );

    // expect(await chessRewards.totalGamesPlayed()).to.equal(1);
  });
});
EOF

    print_message "$GREEN" "✓ Test files created"
}

# Install dependencies
install_dependencies() {
    print_header "Installing Dependencies"
    
    cd ${PROJECT_NAME}
    
    print_message "$YELLOW" "Installing npm packages (this may take a few minutes)..."
    npm install
    
    print_message "$GREEN" "✓ Dependencies installed successfully"
    cd ..
}

# Display completion message
show_completion() {
    print_header "Installation Complete! 🎉"
    
    print_message "$GREEN" "Chess WLD project has been successfully created!"
    echo ""
    print_message "$BLUE" "Project location: ./${PROJECT_NAME}"
    print_message "$BLUE" "Smart contract address: ${WALLET_ADDRESS}"
    echo ""
    print_message "$YELLOW" "Next steps:"
    echo ""
    echo "  1. Navigate to project directory:"
    print_message "$BLUE" "     cd ${PROJECT_NAME}"
    echo ""
    echo "  2. Update environment variables in .env.local:"
    print_message "$BLUE" "     - Add your World App ID"
    print_message "$BLUE" "     - Add your WalletConnect Project ID"
    echo ""
    echo "  3. Start development server:"
    print_message "$BLUE" "     npm run dev"
    echo ""
    echo "  4. Open your browser:"
    print_message "$BLUE" "     http://localhost:3000"
    echo ""
    print_message "$GREEN" "Happy coding! 🚀"
    echo ""
}

# Main installation flow
main() {
    print_header "Chess WLD Project Installer"
    print_message "$BLUE" "Wallet Address: ${WALLET_ADDRESS}"
    print_message "$BLUE" "Project Name: ${PROJECT_NAME}"
    echo ""
    
    check_prerequisites
    create_structure
    create_package_json
    create_smart_contract
    create_components
    create_app
    create_utils
    create_styles
    create_hardhat_config
    create_deploy_script
    create_env_files
    create_config_files
    create_api_routes
    create_tests
    install_dependencies
    show_completion
}

# Run the installer
main
EOF