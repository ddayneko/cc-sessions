#!/usr/bin/env node

/**
 * Claude Code Sessions Framework - Cross-Platform Node.js Installer
 * 
 * NPM wrapper installer providing identical functionality to the Python installer
 * with native Windows, macOS, and Linux support. Features interactive terminal
 * UI, platform-aware command detection, and cross-platform file operations.
 * 
 * Key Features:
 *   - Windows compatibility with .cmd and .ps1 script installation
 *   - Cross-platform command detection (where/which)
 *   - Platform-aware path handling and file permissions
 *   - Interactive menu system with keyboard navigation
 *   - Global daic command installation with PATH integration
 * 
 * Platform Support:
 *   - Windows 10/11 (Command Prompt, PowerShell, Git Bash)
 *   - macOS (Terminal, iTerm2 with Bash/Zsh)
 *   - Linux distributions (various terminals and shells)
 * 
 * Installation Methods:
 *   - npm install -g cc-sessions (global installation)
 *   - npx cc-sessions (temporary installation)
 * 
 * Windows Integration:
 *   - Creates %USERPROFILE%\AppData\Local\cc-sessions\bin directory
 *   - Installs both daic.cmd and daic.ps1 for shell compatibility
 *   - Uses Windows-style environment variables (%VAR%)
 *   - Platform-specific hook command generation
 * 
 * @module install
 * @requires fs
 * @requires path
 * @requires child_process
 * @requires readline
 */

const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');
const readline = require('readline');
const { promisify } = require('util');

// Colors for terminal output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  bgRed: '\x1b[41m',
  bgGreen: '\x1b[42m',
  bgYellow: '\x1b[43m',
  bgBlue: '\x1b[44m',
  bgMagenta: '\x1b[45m',
  bgCyan: '\x1b[46m'
};

// Helper to colorize output
const color = (text, colorCode) => `${colorCode}${text}${colors.reset}`;

// Icons and symbols
const icons = {
  check: '✓',
  cross: '✗',
  lock: '🔒',
  unlock: '🔓',
  info: 'ℹ',
  warning: '⚠',
  arrow: '→',
  bullet: '•',
  star: '★'
};

// Create readline interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const question = promisify(rl.question).bind(rl);

// Paths
const SCRIPT_DIR = __dirname;
let PROJECT_ROOT = process.cwd();

// Check if we're running from npx or in wrong directory
async function detectProjectDirectory() {
  // If running from node_modules or temp npx directory
  if (PROJECT_ROOT.includes('node_modules') || PROJECT_ROOT.includes('.npm')) {
    console.log(color('⚠️  Running from package directory, not project directory.', colors.yellow));
    console.log();
    const projectPath = await question('Enter the path to your project directory (or press Enter for current directory): ');
    if (projectPath) {
      PROJECT_ROOT = path.resolve(projectPath);
    } else {
      PROJECT_ROOT = process.cwd();
    }
    console.log(color(`Using project directory: ${PROJECT_ROOT}`, colors.cyan));
  }
}

// Configuration object to build
const config = {
  developer_name: "the developer",
  trigger_phrases: ["make it so", "run that", "go ahead", "yert"],
  blocked_tools: ["Edit", "Write", "MultiEdit", "NotebookEdit"],
  task_detection: { enabled: true },
  branch_enforcement: { enabled: true },
  serena_mcp: { 
    enabled: false,
    auto_activate: true 
  },
  memory_bank_mcp: {
    enabled: false,
    auto_activate: true,
    memory_bank_root: "",
    sync_files: []
  },
  github_mcp: {
    enabled: false,
    auto_activate: true,
    requires_pat: true
  },
  storybook_mcp: {
    enabled: false,
    auto_activate: true,
    storybook_url: ""
  },
  playwright_mcp: {
    enabled: false,
    auto_activate: true,
    browser_automation: true
  }
};

// Check if command exists
function commandExists(command) {
  try {
    if (process.platform === 'win32') {
      // Windows - use 'where' command
      execSync(`where ${command}`, { stdio: 'ignore' });
      return true;
    } else {
      // Unix/Mac - use 'which' command
      execSync(`which ${command}`, { stdio: 'ignore' });
      return true;
    }
  } catch {
    return false;
  }
}

// Get list of already installed MCP servers
function getInstalledMCPServers() {
  if (!commandExists('claude')) {
    return new Set();
  }
  
  try {
    const result = execSync('claude mcp list', { encoding: 'utf-8' });
    const installed = new Set();
    const lines = result.split('\n');
    
    for (const line of lines) {
      const lowerLine = line.toLowerCase();
      if (lowerLine.includes('serena:')) {
        installed.add('serena');
      } else if (lowerLine.includes('memory-bank') || lowerLine.includes('memorybank')) {
        installed.add('memory-bank');
      } else if (lowerLine.includes('github-mcp') || lowerLine.includes('github_mcp')) {
        installed.add('github');
      } else if (lowerLine.includes('storybook-mcp') || lowerLine.includes('storybook')) {
        installed.add('storybook');
      } else if (lowerLine.includes('playwright-mcp') || lowerLine.includes('playwright')) {
        installed.add('playwright');
      }
    }
    
    return installed;
  } catch {
    return new Set();
  }
}

// Check dependencies
async function checkDependencies() {
  console.log(color('Checking dependencies...', colors.cyan));
  
  // Check Python
  const hasPython = commandExists('python3') || commandExists('python');
  if (!hasPython) {
    console.log(color('❌ Python 3 is required but not installed.', colors.red));
    process.exit(1);
  }
  
  // Check pip
  const hasPip = commandExists('pip3') || commandExists('pip');
  if (!hasPip) {
    console.log(color('❌ pip is required but not installed.', colors.red));
    process.exit(1);
  }
  
  // Check Git (warning only)
  if (!commandExists('git')) {
    console.log(color('⚠️  Warning: Not in a git repository. Sessions works best with git.', colors.yellow));
    const answer = await question('Continue anyway? (y/n): ');
    if (answer.toLowerCase() !== 'y') {
      process.exit(1);
    }
  }
}

// Check for Serena MCP availability
function checkSerenaMCP() {
  const hasUv = commandExists('uv');
  const hasClaude = commandExists('claude');
  const installedServers = getInstalledMCPServers();
  
  return {
    uv: hasUv,
    claude: hasClaude,
    available: hasUv && hasClaude,
    alreadyInstalled: installedServers.has('serena')
  };
}

// Setup Serena MCP integration
async function setupSerenaMCP() {
  const serenaStatus = checkSerenaMCP();
  
  if (serenaStatus.alreadyInstalled) {
    console.log(color('✓ Serena MCP already installed', colors.green));
    config.serena_mcp.enabled = true;
    return true;
  }
  
  if (!serenaStatus.available) {
    const missing = [];
    if (!serenaStatus.uv) missing.push('uv (Python package manager)');
    if (!serenaStatus.claude) missing.push('claude (Claude Code CLI)');
    
    console.log(color(`⚠️  Serena MCP requirements not met. Missing: ${missing.join(', ')}`, colors.yellow));
    console.log(color('   Install with: curl -LsSf https://astral.sh/uv/install.sh | sh', colors.dim));
    console.log(color('   Serena MCP features will be disabled but agents will gracefully fallback.', colors.dim));
    return false;
  }
  
  console.log(color('✓ Serena MCP requirements detected', colors.green));
  
  const installSerena = await question(color('  Install Serena MCP for enhanced code analysis? (y/n): ', colors.cyan));
  
  if (installSerena.toLowerCase() === 'y') {
    try {
      console.log(color('  Installing Serena MCP server...', colors.dim));
      
      // Add Serena MCP server to Claude Code
      execSync(`claude mcp add serena sh -c "uvx --from git+https://github.com/oraios/serena serena start-mcp-server"`, { stdio: 'inherit' });
      
      console.log(color('  ✓ Serena MCP server configured', colors.green));
      console.log(color('    Remember to activate your project: "Activate the project /path/to/project"', colors.dim));
      
      config.serena_mcp.enabled = true;
      return true;
      
    } catch (error) {
      console.log(color('  ⚠️ Serena MCP installation failed, continuing without it', colors.yellow));
      console.log(color('    You can set it up manually later with: claude mcp add serena ...', colors.dim));
      return false;
    }
  }
  
  return false;
}

// Check Memory Bank MCP requirements
function checkMemoryBankMCP() {
  const hasNpx = commandExists('npx');
  const hasClaude = commandExists('claude');
  const installedServers = getInstalledMCPServers();
  
  return {
    npx: hasNpx,
    claude: hasClaude,
    available: hasNpx && hasClaude,
    alreadyInstalled: installedServers.has('memory-bank')
  };
}

// Setup Memory Bank MCP integration
async function setupMemoryBankMCP() {
  const memoryBankStatus = checkMemoryBankMCP();
  
  if (memoryBankStatus.alreadyInstalled) {
    console.log(color('✓ Memory Bank MCP already installed', colors.green));
    config.memory_bank_mcp.enabled = true;
    return true;
  }
  
  if (!memoryBankStatus.available) {
    const missing = [];
    if (!memoryBankStatus.npx) missing.push('npx (Node.js package runner)');
    if (!memoryBankStatus.claude) missing.push('claude (Claude Code CLI)');
    
    console.log(color(`⚠️  Memory Bank MCP requirements not met. Missing: ${missing.join(', ')}`, colors.yellow));
    console.log(color('   Install Node.js to get npx: https://nodejs.org/', colors.dim));
    console.log(color('   Memory Bank MCP features will be disabled but workflow continues normally.', colors.dim));
    return false;
  }
  
  console.log(color('✓ Memory Bank MCP requirements detected', colors.green));
  
  const installMemoryBank = await question(color('  Install Memory Bank MCP for persistent context analysis? (y/n): ', colors.cyan));
  
  if (installMemoryBank.toLowerCase() === 'y') {
    try {
      console.log(color('  Installing Memory Bank MCP server...', colors.dim));
      
      // Set default memory bank root
      const memoryBankRoot = path.join(PROJECT_ROOT, 'sessions', 'memory_bank');
      await fs.mkdir(memoryBankRoot, { recursive: true });
      
      // Install Memory Bank MCP server using smithery
      execSync('npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude', { stdio: 'inherit' });
      
      console.log(color('  ✓ Memory Bank MCP server configured', colors.green));
      console.log(color(`    Memory bank root: ${memoryBankRoot}`, colors.dim));
      console.log(color('    Note: Configure MEMORY_BANK_ROOT environment variable if needed', colors.dim));
      
      config.memory_bank_mcp.enabled = true;
      config.memory_bank_mcp.memory_bank_root = memoryBankRoot;
      
      // Collect files to sync with Memory Bank
      console.log(color('\n  📄 File Synchronization Setup', colors.cyan));
      console.log(color('  Specify markdown files to sync with Memory Bank for persistent context.', colors.dim));
      console.log(color('  Examples: "README.md", "docs/architecture.md", "DESIGN.md"', colors.dim));
      console.log();
      
      while (true) {
        const filePath = await question(color('  Add markdown file to sync (Enter path relative to project root, or Enter to skip): ', colors.cyan));
        if (!filePath) {
          break;
        }
        
        // Validate file exists and is markdown
        const fullPath = path.join(PROJECT_ROOT, filePath);
        if (!fs.existsSync(fullPath)) {
          console.log(color(`  ⚠️ File not found: ${filePath}`, colors.yellow));
          continue;
        }
        if (!filePath.toLowerCase().endsWith('.md')) {
          console.log(color('  ⚠️ Only markdown files (.md) are supported', colors.yellow));
          continue;
        }
        
        // Add to sync files configuration
        const syncFile = {
          path: filePath,
          status: 'pending',
          last_synced: null
        };
        config.memory_bank_mcp.sync_files.push(syncFile);
        console.log(color(`  ✓ Added: "${filePath}"`, colors.green));
      }
      
      return true;
      
    } catch (error) {
      console.log(color('  ⚠️ Memory Bank MCP installation failed, continuing without it', colors.yellow));
      console.log(color('    You can set it up manually later with: npx -y @smithery/cli install @alioshr/memory-bank-mcp --client claude', colors.dim));
      return false;
    }
  }
  
  return false;
}

// Check for GitHub MCP availability
function checkGitHubMCP() {
  const hasDocker = commandExists('docker');
  const hasClaude = commandExists('claude');
  const installedServers = getInstalledMCPServers();
  
  return {
    docker: hasDocker,
    claude: hasClaude,
    available: hasDocker && hasClaude,
    alreadyInstalled: installedServers.has('github')
  };
}

// Setup GitHub MCP integration
async function setupGitHubMCP() {
  const githubStatus = checkGitHubMCP();
  
  if (githubStatus.alreadyInstalled) {
    console.log(color('✓ GitHub MCP already installed', colors.green));
    config.github_mcp.enabled = true;
    return true;
  }
  
  if (!githubStatus.available) {
    const missing = [];
    if (!githubStatus.docker) missing.push('docker (container runtime)');
    if (!githubStatus.claude) missing.push('claude (Claude Code CLI)');
    
    console.log(color(`⚠️  GitHub MCP requirements not met. Missing: ${missing.join(', ')}`, colors.yellow));
    console.log(color('   Install Docker: https://docs.docker.com/get-docker/', colors.dim));
    console.log(color('   GitHub MCP features will be disabled but workflow continues normally.', colors.dim));
    return false;
  }
  
  console.log(color('✓ GitHub MCP requirements detected', colors.green));
  
  const installGitHub = await question(color('  Install GitHub MCP for repository management and automation? (y/n): ', colors.cyan));
  
  if (installGitHub.toLowerCase() === 'y') {
    try {
      console.log(color('  Installing GitHub MCP server...', colors.dim));
      console.log(color('  Note: You will need a GitHub Personal Access Token to use this server', colors.yellow));
      console.log(color('  Create one at: https://github.com/settings/tokens', colors.dim));
      console.log(color('  Recommended scopes: repo, read:packages, read:org', colors.dim));
      
      // Add GitHub MCP server to Claude Code using Docker
      execSync(`claude mcp add github docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server`, { stdio: 'inherit' });
      
      console.log(color('  ✓ GitHub MCP server configured', colors.green));
      console.log(color('    Remember to set GITHUB_PERSONAL_ACCESS_TOKEN environment variable', colors.dim));
      
      config.github_mcp.enabled = true;
      return true;
      
    } catch (error) {
      console.log(color('  ⚠️ GitHub MCP installation failed, continuing without it', colors.yellow));
      console.log(color('    You can set it up manually later with Docker', colors.dim));
      return false;
    }
  }
  
  return false;
}

// Check for Storybook MCP availability
function checkStorybookMCP() {
  const hasNpx = commandExists('npx');
  const hasClaude = commandExists('claude');
  const installedServers = getInstalledMCPServers();
  
  return {
    npx: hasNpx,
    claude: hasClaude,
    available: hasNpx && hasClaude,
    alreadyInstalled: installedServers.has('storybook')
  };
}

// Check if package.json exists in project root
function checkPackageJsonExists() {
  try {
    const packageJsonPath = path.join(PROJECT_ROOT, 'package.json');
    fs.accessSync(packageJsonPath);
    return true;
  } catch {
    return false;
  }
}

// Check if a package is installed by looking in package.json
function checkPackageInstalled(packageName) {
  if (!checkPackageJsonExists()) {
    return false;
  }
  
  try {
    const packageJsonPath = path.join(PROJECT_ROOT, 'package.json');
    const packageData = JSON.parse(require('fs').readFileSync(packageJsonPath, 'utf-8'));
    
    // Check both dependencies and devDependencies
    const deps = packageData.dependencies || {};
    const devDeps = packageData.devDependencies || {};
    
    // Support wildcard matching for packages like @storybook/*
    if (packageName.includes('*')) {
      const prefix = packageName.replace('*', '');
      return Object.keys(deps).concat(Object.keys(devDeps)).some(pkg => pkg.startsWith(prefix));
    } else {
      return packageName in deps || packageName in devDeps;
    }
  } catch {
    return false;
  }
}

// Install an npm package
function installNpmPackage(packageName, dev = true) {
  try {
    const cmd = ['npm', 'install'];
    if (dev) {
      cmd.push('--save-dev');
    }
    cmd.push(packageName);
    
    console.log(color(`  Installing ${packageName}...`, colors.dim));
    execSync(cmd.join(' '), { cwd: PROJECT_ROOT, stdio: 'inherit' });
    console.log(color(`  ✓ Installed ${packageName}`, colors.green));
    return true;
  } catch {
    console.log(color(`  ⚠️ Failed to install ${packageName}`, colors.yellow));
    return false;
  }
}

// Check if Storybook is running on the specified port
function checkStorybookRunning(port = 6006) {
  try {
    const net = require('net');
    const client = new net.Socket();
    client.setTimeout(1000);
    
    return new Promise((resolve) => {
      client.connect(port, 'localhost', () => {
        client.destroy();
        resolve(true);
      });
      
      client.on('error', () => {
        resolve(false);
      });
      
      client.on('timeout', () => {
        client.destroy();
        resolve(false);
      });
    });
  } catch {
    return Promise.resolve(false);
  }
}

// Start Storybook in the background
async function startStorybook() {
  try {
    console.log(color('  Starting Storybook...', colors.dim));
    const { spawn } = require('child_process');
    
    // Start Storybook in background - don't wait for completion
    const storybookProcess = spawn('npm', ['run', 'storybook'], {
      cwd: PROJECT_ROOT,
      detached: true,
      stdio: 'ignore'
    });
    
    storybookProcess.unref();
    
    // Wait a moment for startup, then check if it's running
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    const isRunning = await checkStorybookRunning();
    if (isRunning) {
      console.log(color('  ✓ Storybook started successfully', colors.green));
      return true;
    } else {
      console.log(color('  ⚠️ Storybook may still be starting up', colors.yellow));
      return true; // Return true anyway as it was started
    }
  } catch {
    console.log(color('  ⚠️ Failed to start Storybook', colors.yellow));
    console.log(color('    Make sure you have a \'storybook\' script in package.json', colors.dim));
    return false;
  }
}

// Setup Storybook MCP integration
async function setupStorybookMCP() {
  const storybookStatus = checkStorybookMCP();
  
  if (storybookStatus.alreadyInstalled) {
    console.log(color('✓ Storybook MCP already installed', colors.green));
    config.storybook_mcp.enabled = true;
    return true;
  }
  
  if (!storybookStatus.available) {
    const missing = [];
    if (!storybookStatus.npx) missing.push('npx (Node.js package runner)');
    if (!storybookStatus.claude) missing.push('claude (Claude Code CLI)');
    
    console.log(color(`⚠️  Storybook MCP requirements not met. Missing: ${missing.join(', ')}`, colors.yellow));
    console.log(color('   Install Node.js to get npx: https://nodejs.org/', colors.dim));
    console.log(color('   Storybook MCP features will be disabled but workflow continues normally.', colors.dim));
    return false;
  }
  
  console.log(color('✓ Storybook MCP requirements detected', colors.green));
  
  const installStorybook = await question(color('  Install Storybook MCP for component development workflows? (requires package installation) (y/n): ', colors.cyan));
  
  if (installStorybook.toLowerCase() === 'y') {
    try {
      // Check if this is a Node.js project
      if (!checkPackageJsonExists()) {
        console.log(color('  ⚠️ No package.json found. Storybook MCP requires a Node.js project.', colors.yellow));
        console.log(color('    Initialize with: npm init', colors.dim));
        return false;
      }
      
      // Check if Storybook packages are installed
      const storybookInstalled = checkPackageInstalled('@storybook/*');
      
      if (!storybookInstalled) {
        console.log(color('  Storybook packages not found, installing...', colors.dim));
        // Install basic Storybook packages
        const success = (
          installNpmPackage('@storybook/react', true) &&
          installNpmPackage('@storybook/react-webpack5', true) &&
          installNpmPackage('storybook', true)
        );
        if (!success) {
          console.log(color('  ⚠️ Failed to install Storybook packages', colors.yellow));
          return false;
        }
      } else {
        console.log(color('  ✓ Storybook packages already installed', colors.green));
      }
      
      // Check if Storybook is running
      const isRunning = await checkStorybookRunning();
      if (!isRunning) {
        console.log(color('  Storybook not running, attempting to start...', colors.dim));
        const started = await startStorybook();
        if (!started) {
          console.log(color('  ⚠️ Could not start Storybook automatically', colors.yellow));
          console.log(color('    Start manually with: npm run storybook', colors.dim));
        }
      } else {
        console.log(color('  ✓ Storybook is already running', colors.green));
      }
      
      console.log(color('  Installing Storybook MCP server...', colors.dim));
      
      // Add Storybook MCP server to Claude Code
      execSync('claude mcp add storybook npx -y storybook-mcp', { stdio: 'inherit' });
      
      console.log(color('  ✓ Storybook MCP server configured', colors.green));
      console.log(color('    Storybook URL: http://localhost:6006/index.json', colors.green));
      
      config.storybook_mcp.enabled = true;
      config.storybook_mcp.storybook_url = 'http://localhost:6006/index.json';
      return true;
      
    } catch (error) {
      console.log(color('  ⚠️ Storybook MCP installation failed, continuing without it', colors.yellow));
      console.log(color('    You can set it up manually later with: npx storybook-mcp', colors.dim));
      return false;
    }
  }
  
  return false;
}

// Check for Playwright MCP availability
function checkPlaywrightMCP() {
  const hasNpx = commandExists('npx');
  const hasClaude = commandExists('claude');
  const installedServers = getInstalledMCPServers();
  
  return {
    npx: hasNpx,
    claude: hasClaude,
    available: hasNpx && hasClaude,
    alreadyInstalled: installedServers.has('playwright')
  };
}

// Setup Playwright MCP integration
async function setupPlaywrightMCP() {
  const playwrightStatus = checkPlaywrightMCP();
  
  if (playwrightStatus.alreadyInstalled) {
    console.log(color('✓ Playwright MCP already installed', colors.green));
    config.playwright_mcp.enabled = true;
    return true;
  }
  
  if (!playwrightStatus.available) {
    const missing = [];
    if (!playwrightStatus.npx) missing.push('npx (Node.js package runner)');
    if (!playwrightStatus.claude) missing.push('claude (Claude Code CLI)');
    
    console.log(color(`⚠️  Playwright MCP requirements not met. Missing: ${missing.join(', ')}`, colors.yellow));
    console.log(color('   Install Node.js to get npx: https://nodejs.org/', colors.dim));
    console.log(color('   Playwright MCP features will be disabled but workflow continues normally.', colors.dim));
    return false;
  }
  
  console.log(color('✓ Playwright MCP requirements detected', colors.green));
  
  const installPlaywright = await question(color('  Install Playwright MCP for browser automation and testing? (requires package installation) (y/n): ', colors.cyan));
  
  if (installPlaywright.toLowerCase() === 'y') {
    try {
      // Check if this is a Node.js project
      if (!checkPackageJsonExists()) {
        console.log(color('  ⚠️ No package.json found. Playwright MCP requires a Node.js project.', colors.yellow));
        console.log(color('    Initialize with: npm init', colors.dim));
        return false;
      }
      
      // Check if Playwright packages are installed
      const playwrightInstalled = checkPackageInstalled('@playwright/test');
      
      if (!playwrightInstalled) {
        console.log(color('  Playwright packages not found, installing...', colors.dim));
        // Install Playwright test package
        const success = installNpmPackage('@playwright/test', true);
        if (!success) {
          console.log(color('  ⚠️ Failed to install Playwright packages', colors.yellow));
          return false;
        }
      } else {
        console.log(color('  ✓ Playwright packages already installed', colors.green));
      }
      
      // Install Playwright browser binaries
      console.log(color('  Installing Playwright browser binaries...', colors.dim));
      try {
        execSync('npx playwright install', { 
          cwd: PROJECT_ROOT, 
          stdio: 'inherit' 
        });
        console.log(color('  ✓ Playwright browser binaries installed', colors.green));
      } catch {
        console.log(color('  ⚠️ Failed to install Playwright browser binaries', colors.yellow));
        console.log(color('    You can install them manually with: npx playwright install', colors.dim));
      }
      
      console.log(color('  Installing Playwright MCP server...', colors.dim));
      
      // Add Playwright MCP server to Claude Code
      execSync('claude mcp add playwright npx @playwright/mcp@latest', { stdio: 'inherit' });
      
      console.log(color('  ✓ Playwright MCP server configured', colors.green));
      console.log(color('    Provides browser automation and web page interaction capabilities', colors.green));
      
      config.playwright_mcp.enabled = true;
      return true;
      
    } catch (error) {
      console.log(color('  ⚠️ Playwright MCP installation failed, continuing without it', colors.yellow));
      console.log(color('    You can set it up manually later with: npx @playwright/mcp@latest', colors.dim));
      return false;
    }
  }
  
  return false;
}

// Create directory structure
async function createDirectories() {
  console.log(color('Creating directory structure...', colors.cyan));
  
  const dirs = [
    '.claude/hooks',
    '.claude/state',
    '.claude/agents',
    '.claude/commands',
    'sessions/tasks/done',
    'sessions/protocols',
    'sessions/knowledge'
  ];
  
  for (const dir of dirs) {
    await fs.mkdir(path.join(PROJECT_ROOT, dir), { recursive: true });
  }
}

// Install Python dependencies
async function installPythonDeps() {
  console.log(color('Installing Python dependencies...', colors.cyan));
  try {
    const pipCommand = commandExists('pip3') ? 'pip3' : 'pip';
    execSync(`${pipCommand} install tiktoken --quiet`, { stdio: 'inherit' });
  } catch (error) {
    console.log(color('⚠️  Could not install tiktoken. You may need to install it manually.', colors.yellow));
  }
}

// Copy files with proper permissions
async function copyFiles() {
  console.log(color('Installing hooks...', colors.cyan));
  const hookFiles = await fs.readdir(path.join(SCRIPT_DIR, 'cc_sessions/hooks'));
  for (const file of hookFiles) {
    if (file.endsWith('.py')) {
      await fs.copyFile(
        path.join(SCRIPT_DIR, 'cc_sessions/hooks', file),
        path.join(PROJECT_ROOT, '.claude/hooks', file)
      );
      if (process.platform !== 'win32') {
        await fs.chmod(path.join(PROJECT_ROOT, '.claude/hooks', file), 0o755);
      }
    }
  }
  
  console.log(color('Installing protocols...', colors.cyan));
  const protocolFiles = await fs.readdir(path.join(SCRIPT_DIR, 'cc_sessions/protocols'));
  for (const file of protocolFiles) {
    if (file.endsWith('.md')) {
      await fs.copyFile(
        path.join(SCRIPT_DIR, 'cc_sessions/protocols', file),
        path.join(PROJECT_ROOT, 'sessions/protocols', file)
      );
    }
  }
  
  console.log(color('Installing agent definitions...', colors.cyan));
  const agentFiles = await fs.readdir(path.join(SCRIPT_DIR, 'cc_sessions/agents'));
  for (const file of agentFiles) {
    if (file.endsWith('.md')) {
      await fs.copyFile(
        path.join(SCRIPT_DIR, 'cc_sessions/agents', file),
        path.join(PROJECT_ROOT, '.claude/agents', file)
      );
    }
  }
  
  console.log(color('Installing templates...', colors.cyan));
  const templateFiles = await fs.readdir(path.join(SCRIPT_DIR, 'cc_sessions/templates'));
  for (const file of templateFiles) {
    if (file.endsWith('.md')) {
      let destPath;
      if (file === 'TEMPLATE.md') {
        // Task template goes to sessions/tasks/
        destPath = path.join(PROJECT_ROOT, 'sessions/tasks/TEMPLATE.md');
      } else if (file === 'BUILD_PROJECT_TEMPLATE.md') {
        // Build project template goes to sessions/ for easier access
        destPath = path.join(PROJECT_ROOT, 'sessions', file);
      } else {
        // Other templates go to sessions/ directory
        destPath = path.join(PROJECT_ROOT, 'sessions', file);
      }
      await fs.copyFile(
        path.join(SCRIPT_DIR, 'cc_sessions/templates', file),
        destPath
      );
    }
  }
  
  console.log(color('Installing commands...', colors.cyan));
  const commandFiles = await fs.readdir(path.join(SCRIPT_DIR, 'cc_sessions/commands'));
  for (const file of commandFiles) {
    if (file.endsWith('.md')) {
      await fs.copyFile(
        path.join(SCRIPT_DIR, 'cc_sessions/commands', file),
        path.join(PROJECT_ROOT, '.claude/commands', file)
      );
    }
    // Copy Python command scripts
    if (file.endsWith('.py')) {
      await fs.copyFile(
        path.join(SCRIPT_DIR, 'cc_sessions/commands', file),
        path.join(PROJECT_ROOT, '.claude/commands', file)
      );
      if (process.platform !== 'win32') {
        await fs.chmod(path.join(PROJECT_ROOT, '.claude/commands', file), 0o755);
      }
    }
  }
  
  // Copy knowledge files if they exist
  const knowledgePath = path.join(SCRIPT_DIR, 'cc_sessions/knowledge/claude-code');
  try {
    await fs.access(knowledgePath);
    console.log(color('Installing Claude Code knowledge base...', colors.cyan));
    await copyDir(knowledgePath, path.join(PROJECT_ROOT, 'sessions/knowledge/claude-code'));
  } catch {
    // Knowledge files don't exist, skip
  }
}

// Recursive directory copy
async function copyDir(src, dest) {
  await fs.mkdir(dest, { recursive: true });
  const entries = await fs.readdir(src, { withFileTypes: true });
  
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    
    if (entry.isDirectory()) {
      await copyDir(srcPath, destPath);
    } else {
      await fs.copyFile(srcPath, destPath);
    }
  }
}

// Install daic command
async function installDaicCommand() {
  console.log(color('Installing daic command...', colors.cyan));
  
  if (process.platform === 'win32') {
    // Windows installation
    const daicCmdSource = path.join(SCRIPT_DIR, 'cc_sessions/scripts/daic.cmd');
    const daicPs1Source = path.join(SCRIPT_DIR, 'cc_sessions/scripts/daic.ps1');
    
    // Install to user's local directory
    const localBin = path.join(process.env.USERPROFILE || process.env.HOME, 'AppData', 'Local', 'cc-sessions', 'bin');
    await fs.mkdir(localBin, { recursive: true });
    
    try {
      // Copy .cmd script
      await fs.access(daicCmdSource);
      const daicCmdDest = path.join(localBin, 'daic.cmd');
      await fs.copyFile(daicCmdSource, daicCmdDest);
      console.log(color(`  ✓ Installed daic.cmd to ${localBin}`, colors.green));
    } catch {
      console.log(color('  ⚠️ daic.cmd script not found', colors.yellow));
    }
    
    try {
      // Copy .ps1 script
      await fs.access(daicPs1Source);
      const daicPs1Dest = path.join(localBin, 'daic.ps1');
      await fs.copyFile(daicPs1Source, daicPs1Dest);
      console.log(color(`  ✓ Installed daic.ps1 to ${localBin}`, colors.green));
    } catch {
      console.log(color('  ⚠️ daic.ps1 script not found', colors.yellow));
    }
    
    console.log(color(`  ℹ Add ${localBin} to your PATH to use 'daic' command`, colors.yellow));
  } else {
    // Unix/Mac installation
    const daicSource = path.join(SCRIPT_DIR, 'cc_sessions/scripts/daic');
    const daicDest = '/usr/local/bin/daic';
    
    try {
      await fs.copyFile(daicSource, daicDest);
      await fs.chmod(daicDest, 0o755);
    } catch (error) {
      if (error.code === 'EACCES') {
        console.log(color('⚠️  Cannot write to /usr/local/bin. Trying with sudo...', colors.yellow));
        try {
          execSync(`sudo cp ${daicSource} ${daicDest}`, { stdio: 'inherit' });
          execSync(`sudo chmod +x ${daicDest}`, { stdio: 'inherit' });
        } catch {
          console.log(color('⚠️  Could not install daic command globally. You can run it locally from .claude/scripts/', colors.yellow));
        }
      }
    }
  }
}

// Interactive menu with keyboard navigation
async function interactiveMenu(items, options = {}) {
  const {
    title = 'Select an option',
    multiSelect = false,
    selectedItems = new Set(),
    formatItem = (item, selected) => item
  } = options;
  
  let currentIndex = 0;
  let selected = new Set(selectedItems);
  let done = false;
  
  // Hide cursor
  process.stdout.write('\x1B[?25l');
  
  const renderMenu = () => {
    // Clear previous menu
    console.clear();
    
    // Render title
    if (title) {
      console.log(title);
    }
    
    // Render items
    items.forEach((item, index) => {
      const isSelected = selected.has(item);
      const isCurrent = index === currentIndex;
      
      let prefix = '  ';
      if (isCurrent) {
        prefix = color('▶ ', colors.cyan);
      }
      
      console.log(prefix + formatItem(item, isSelected, isCurrent));
    });
  };
  
  return new Promise((resolve) => {
    renderMenu();
    
    // Set raw mode for key input
    readline.emitKeypressEvents(process.stdin);
    if (process.stdin.setRawMode) {
      process.stdin.setRawMode(true);
    }
    process.stdin.resume();
    
    const keyHandler = (str, key) => {
      if (key) {
        if (key.name === 'up') {
          currentIndex = (currentIndex - 1 + items.length) % items.length;
          renderMenu();
        } else if (key.name === 'down') {
          currentIndex = (currentIndex + 1) % items.length;
          renderMenu();
        } else if (key.name === 'space' && multiSelect) {
          const item = items[currentIndex];
          if (selected.has(item)) {
            selected.delete(item);
          } else {
            selected.add(item);
          }
          renderMenu();
        } else if (key.name === 'return') {
          done = true;
          // Restore terminal
          if (process.stdin.setRawMode) {
            process.stdin.setRawMode(false);
          }
          process.stdin.removeListener('keypress', keyHandler);
          process.stdout.write('\x1B[?25h'); // Show cursor
          console.clear();
          
          // Resume stdin for subsequent prompts (don't pause!)
          process.stdin.resume();
          
          if (multiSelect) {
            resolve(selected);
          } else {
            resolve(items[currentIndex]);
          }
        } else if (key.ctrl && key.name === 'c') {
          // Handle Ctrl+C
          if (process.stdin.setRawMode) {
            process.stdin.setRawMode(false);
          }
          process.stdin.pause();
          process.stdout.write('\x1B[?25h'); // Show cursor
          process.exit(0);
        }
      }
    };
    
    process.stdin.on('keypress', keyHandler);
  });
}

// Tool blocking menu
async function configureToolBlocking() {
  const allTools = [
    { name: 'Edit', description: 'Edit existing files', defaultBlocked: true },
    { name: 'Write', description: 'Create new files', defaultBlocked: true },
    { name: 'MultiEdit', description: 'Multiple edits in one operation', defaultBlocked: true },
    { name: 'NotebookEdit', description: 'Edit Jupyter notebooks', defaultBlocked: true },
    { name: 'Bash', description: 'Run shell commands', defaultBlocked: false },
    { name: 'Read', description: 'Read file contents', defaultBlocked: false },
    { name: 'Grep', description: 'Search file contents', defaultBlocked: false },
    { name: 'Glob', description: 'Find files by pattern', defaultBlocked: false },
    { name: 'LS', description: 'List directory contents', defaultBlocked: false },
    { name: 'WebSearch', description: 'Search the web', defaultBlocked: false },
    { name: 'WebFetch', description: 'Fetch web content', defaultBlocked: false },
    { name: 'Task', description: 'Launch specialized agents', defaultBlocked: false }
  ];
  
  // Initialize blocked tools
  const initialBlocked = new Set(config.blocked_tools.map(name => 
    allTools.find(t => t.name === name)
  ).filter(Boolean));
  
  const title = `${color('╭───────────────────────────────────────────────────────────────╮', colors.cyan)}
${color('│              Tool Blocking Configuration                      │', colors.cyan)}
${color('├───────────────────────────────────────────────────────────────┤', colors.cyan)}
${color('│   ↑/↓: Navigate   SPACE: Toggle   ENTER: Save & Continue      │', colors.dim)}
${color('│     Tools marked with 🔒 are blocked in discussion mode       │', colors.dim)}
${color('╰───────────────────────────────────────────────────────────────╯', colors.cyan)}
`;
  
  const formatItem = (tool, isBlocked, isCurrent) => {
    const icon = isBlocked ? icons.lock : icons.unlock;
    const status = isBlocked ? color('[BLOCKED]', colors.red) : color('[ALLOWED]', colors.green);
    const toolColor = isCurrent ? colors.bright : (isBlocked ? colors.yellow : colors.white);
    
    return `${icon} ${color(tool.name.padEnd(15), toolColor)} - ${tool.description.padEnd(30)} ${status}`;
  };
  
  const selectedTools = await interactiveMenu(allTools, {
    title,
    multiSelect: true,
    selectedItems: initialBlocked,
    formatItem
  });
  
  config.blocked_tools = Array.from(selectedTools).map(t => t.name);
  console.log(color(`\n  ${icons.check} Tool blocking configuration saved`, colors.green));
}

// Interactive configuration
async function configure() {
  console.log();
  console.log(color('╔═══════════════════════════════════════════════════════════════╗', colors.bright + colors.cyan));
  console.log(color('║                    CONFIGURATION SETUP                        ║', colors.bright + colors.cyan));
  console.log(color('╚═══════════════════════════════════════════════════════════════╝', colors.bright + colors.cyan));
  console.log();
  
  let statuslineInstalled = false;
  
  // Developer name section
  console.log(color(`\n${icons.star} DEVELOPER IDENTITY`, colors.bright + colors.magenta));
  console.log(color('─'.repeat(60), colors.dim));
  console.log(color('  Claude will use this name when addressing you in sessions', colors.dim));
  console.log();
  
  const name = await question(color('  Your name: ', colors.cyan));
  if (name) {
    config.developer_name = name;
    console.log(color(`  ${icons.check} Hello, ${name}!`, colors.green));
  }
  
  // Statusline installation section
  console.log(color(`\n\n${icons.star} STATUSLINE INSTALLATION`, colors.bright + colors.magenta));
  console.log(color('─'.repeat(60), colors.dim));
  console.log(color('  Real-time status display in Claude Code showing:', colors.white));
  console.log(color(`    ${icons.bullet} Current task and DAIC mode`, colors.cyan));
  console.log(color(`    ${icons.bullet} Token usage with visual progress bar`, colors.cyan));
  console.log(color(`    ${icons.bullet} Modified file counts`, colors.cyan));
  console.log(color(`    ${icons.bullet} Open task count`, colors.cyan));
  console.log();
  
  const installStatusline = await question(color('  Install statusline? (y/n): ', colors.cyan));
  
  if (installStatusline.toLowerCase() === 'y') {
    const statuslineSource = path.join(SCRIPT_DIR, 'cc_sessions/scripts/statusline-script.sh');
    try {
      await fs.access(statuslineSource);
      console.log(color('  Installing statusline script...', colors.dim));
      await fs.copyFile(statuslineSource, path.join(PROJECT_ROOT, '.claude/statusline-script.sh'));
      await fs.chmod(path.join(PROJECT_ROOT, '.claude/statusline-script.sh'), 0o755);
      statuslineInstalled = true;
      console.log(color(`  ${icons.check} Statusline installed successfully`, colors.green));
    } catch {
      console.log(color(`  ${icons.warning} Statusline script not found in package`, colors.yellow));
    }
  }
  
  // DAIC trigger phrases section
  console.log(color(`\n\n${icons.star} DAIC WORKFLOW CONFIGURATION`, colors.bright + colors.magenta));
  console.log(color('─'.repeat(60), colors.dim));
  console.log(color('  The DAIC system enforces discussion before implementation.', colors.white));
  console.log(color('  Trigger phrases tell Claude when you\'re ready to proceed.', colors.white));
  console.log();
  console.log(color('  Default triggers:', colors.cyan));
  config.trigger_phrases.forEach(phrase => {
    console.log(color(`    ${icons.arrow} "${phrase}"`, colors.green));
  });
  console.log();
  console.log(color('  Hint: Common additions: "implement it", "do it", "proceed"', colors.dim));
  console.log();
  
  // Allow adding multiple custom trigger phrases
  let addingTriggers = true;
  while (addingTriggers) {
    const customTrigger = await question(color('  Add custom trigger phrase (Enter to skip): ', colors.cyan));
    if (customTrigger) {
      config.trigger_phrases.push(customTrigger);
      console.log(color(`  ${icons.check} Added: "${customTrigger}"`, colors.green));
    } else {
      addingTriggers = false;
    }
  }
  
  // API Mode configuration
  console.log(color(`\n\n${icons.star} THINKING BUDGET CONFIGURATION`, colors.bright + colors.magenta));
  console.log(color('─'.repeat(60), colors.dim));
  console.log(color('  Token usage is not much of a concern with Claude Code Max', colors.white));
  console.log(color('  plans, especially the $200 tier. But API users are often', colors.white));
  console.log(color('  budget-conscious and want manual control.', colors.white));
  console.log();
  console.log(color('  Sessions was built to preserve tokens across context windows', colors.cyan));
  console.log(color('  but uses saved tokens to enable \'ultrathink\' - Claude\'s', colors.cyan));
  console.log(color('  maximum thinking budget - on every interaction for best results.', colors.cyan));
  console.log();
  console.log(color('  • Max users (recommended): Automatic ultrathink every message', colors.dim));
  console.log(color('  • API users: Manual control with [[ ultrathink ]] when needed', colors.dim));
  console.log();
  console.log(color('  You can toggle this anytime with: /api-mode', colors.dim));
  console.log();
  
  const enableUltrathink = await question(color('  Enable automatic ultrathink for best performance? (y/n): ', colors.cyan));
  if (enableUltrathink.toLowerCase() === 'y' || enableUltrathink.toLowerCase() === 'yes') {
    config.api_mode = false;
    console.log(color(`  ${icons.check} Max mode - ultrathink enabled for best performance`, colors.green));
  } else {
    config.api_mode = true;
    console.log(color(`  ${icons.check} API mode - manual ultrathink control (use [[ ultrathink ]])`, colors.green));
  }
  
  // Advanced configuration
  console.log(color(`\n\n${icons.star} ADVANCED OPTIONS`, colors.bright + colors.magenta));
  console.log(color('─'.repeat(60), colors.dim));
  console.log(color('  Configure tool blocking, task prefixes, and more', colors.white));
  console.log();
  
  const advanced = await question(color('  Configure advanced options? (y/n): ', colors.cyan));
  
  if (advanced.toLowerCase() === 'y') {
    await configureToolBlocking();
    
    // Task prefix configuration
    console.log(color(`\n\n${icons.star} TASK PREFIX CONFIGURATION`, colors.bright + colors.magenta));
    console.log(color('─'.repeat(60), colors.dim));
    console.log(color('  Task prefixes organize work by priority and type', colors.white));
    console.log();
    console.log(color('  Current prefixes:', colors.cyan));
    console.log(color(`    ${icons.arrow} h- (high priority)`, colors.white));
    console.log(color(`    ${icons.arrow} m- (medium priority)`, colors.white));
    console.log(color(`    ${icons.arrow} l- (low priority)`, colors.white));
    console.log(color(`    ${icons.arrow} ?- (investigate/research)`, colors.white));
    console.log();
    
    const customizePrefixes = await question(color('  Customize task prefixes? (y/n): ', colors.cyan));
    if (customizePrefixes.toLowerCase() === 'y') {
      const high = await question(color('  High priority prefix [h-]: ', colors.cyan)) || 'h-';
      const med = await question(color('  Medium priority prefix [m-]: ', colors.cyan)) || 'm-';
      const low = await question(color('  Low priority prefix [l-]: ', colors.cyan)) || 'l-';
      const inv = await question(color('  Investigate prefix [?-]: ', colors.cyan)) || '?-';
      
      config.task_prefixes = {
        priority: [high, med, low, inv]
      };
      
      console.log(color(`  ${icons.check} Task prefixes updated`, colors.green));
    }
  }
  
  return { statuslineInstalled };
}

// Save configuration
async function saveConfig(installStatusline = false) {
  console.log(color('Creating configuration...', colors.cyan));
  
  await fs.writeFile(
    path.join(PROJECT_ROOT, 'sessions/sessions-config.json'),
    JSON.stringify(config, null, 2)
  );
  
  // Create or update .claude/settings.json with hooks configuration
  const settingsPath = path.join(PROJECT_ROOT, '.claude/settings.json');
  let settings = {};
  
  // Check if settings.json already exists
  try {
    const existingSettings = await fs.readFile(settingsPath, 'utf-8');
    settings = JSON.parse(existingSettings);
    console.log(color('Found existing settings.json, merging sessions hooks...', colors.cyan));
  } catch {
    console.log(color('Creating new settings.json with sessions hooks...', colors.cyan));
  }
  
  // Define the sessions hooks
  const sessionsHooks = {
    UserPromptSubmit: [
      {
        hooks: [
          {
            type: "command",
            command: process.platform === 'win32' ? "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\user-messages.py\"" : "$CLAUDE_PROJECT_DIR/.claude/hooks/user-messages.py"
          }
        ]
      }
    ],
    PreToolUse: [
      {
        matcher: "Write|Edit|MultiEdit|Task|Bash",
        hooks: [
          {
            type: "command",
            command: process.platform === 'win32' ? "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\sessions-enforce.py\"" : "$CLAUDE_PROJECT_DIR/.claude/hooks/sessions-enforce.py"
          }
        ]
      },
      {
        matcher: "Task",
        hooks: [
          {
            type: "command",
            command: process.platform === 'win32' ? "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\task-transcript-link.py\"" : "$CLAUDE_PROJECT_DIR/.claude/hooks/task-transcript-link.py"
          }
        ]
      }
    ],
    PostToolUse: [
      {
        hooks: [
          {
            type: "command",
            command: process.platform === 'win32' ? "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\post-tool-use.py\"" : "$CLAUDE_PROJECT_DIR/.claude/hooks/post-tool-use.py"
          }
        ]
      }
    ],
    SessionStart: [
      {
        matcher: "startup|clear",
        hooks: [
          {
            type: "command",
            command: process.platform === 'win32' ? "python \"%CLAUDE_PROJECT_DIR%\\.claude\\hooks\\session-start.py\"" : "$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.py"
          }
        ]
      }
    ]
  };
  
  // Merge hooks (sessions hooks take precedence)
  if (!settings.hooks) {
    settings.hooks = {};
  }
  
  // Merge each hook type
  for (const [hookType, hookConfig] of Object.entries(sessionsHooks)) {
    if (!settings.hooks[hookType]) {
      settings.hooks[hookType] = hookConfig;
    } else {
      // Append sessions hooks to existing ones
      settings.hooks[hookType] = [...settings.hooks[hookType], ...hookConfig];
    }
  }
  
  // Add statusline if requested
  if (installStatusline) {
    settings.statusLine = {
      type: "command",
      command: process.platform === 'win32' ? "%CLAUDE_PROJECT_DIR%\\.claude\\statusline-script.sh" : "$CLAUDE_PROJECT_DIR/.claude/statusline-script.sh",
      padding: 0
    };
  }
  
  // Save the updated settings
  await fs.writeFile(settingsPath, JSON.stringify(settings, null, 2));
  console.log(color('✅ Sessions hooks configured in settings.json', colors.green));
  
  // Initialize DAIC state
  await fs.writeFile(
    path.join(PROJECT_ROOT, '.claude/state/daic-mode.json'),
    JSON.stringify({ mode: "discussion" }, null, 2)
  );
  
  // Create initial task state
  const currentDate = new Date().toISOString().split('T')[0];
  await fs.writeFile(
    path.join(PROJECT_ROOT, '.claude/state/current_task.json'),
    JSON.stringify({
      task: null,
      branch: null,
      services: [],
      updated: currentDate
    }, null, 2)
  );
}

// CLAUDE.md integration
async function setupClaudeMd() {
  console.log();
  console.log(color('═══════════════════════════════════════════', colors.bright));
  console.log(color('         CLAUDE.md Integration', colors.bright));
  console.log(color('═══════════════════════════════════════════', colors.bright));
  console.log();
  
  // Check for existing CLAUDE.md
  try {
    await fs.access(path.join(PROJECT_ROOT, 'CLAUDE.md'));
    
    // File exists, preserve it and add sessions as separate file
    console.log(color('CLAUDE.md already exists, preserving your project-specific rules...', colors.cyan));
    
    // Copy CLAUDE.sessions.md as separate file
    await fs.copyFile(
      path.join(SCRIPT_DIR, 'cc_sessions/templates/CLAUDE.sessions.md'),
      path.join(PROJECT_ROOT, 'CLAUDE.sessions.md')
    );
    
    // Check if it already includes sessions
    const content = await fs.readFile(path.join(PROJECT_ROOT, 'CLAUDE.md'), 'utf-8');
    if (!content.includes('@CLAUDE.sessions.md')) {
      console.log(color('Adding sessions include to existing CLAUDE.md...', colors.cyan));
      
      const addition = '\n## Sessions System Behaviors\n\n@CLAUDE.sessions.md\n';
      await fs.appendFile(path.join(PROJECT_ROOT, 'CLAUDE.md'), addition);
      
      console.log(color('✅ Added @CLAUDE.sessions.md include to your CLAUDE.md', colors.green));
    } else {
      console.log(color('✅ CLAUDE.md already includes sessions behaviors', colors.green));
    }
  } catch {
    // File doesn't exist, use sessions as CLAUDE.md
    console.log(color('No existing CLAUDE.md found, installing sessions as your CLAUDE.md...', colors.cyan));
    await fs.copyFile(
      path.join(SCRIPT_DIR, 'cc_sessions/templates/CLAUDE.sessions.md'),
      path.join(PROJECT_ROOT, 'CLAUDE.md')
    );
    console.log(color('✅ CLAUDE.md created with complete sessions behaviors', colors.green));
  }
}

// Main installation function
async function install() {
  console.log(color('╔════════════════════════════════════════════╗', colors.bright));
  console.log(color('║            cc-sessions Installer           ║', colors.bright));
  console.log(color('╚════════════════════════════════════════════╝', colors.bright));
  console.log();
  
  // Detect correct project directory
  await detectProjectDirectory();
  
  // Check CLAUDE_PROJECT_DIR
  if (!process.env.CLAUDE_PROJECT_DIR) {
    console.log(color(`⚠️  CLAUDE_PROJECT_DIR not set. Setting it to ${PROJECT_ROOT}`, colors.yellow));
    console.log('   To make this permanent, add to your shell profile:');
    console.log(`   export CLAUDE_PROJECT_DIR="${PROJECT_ROOT}"`);
    console.log();
  }
  
  try {
    await checkDependencies();
    await createDirectories();
    await installPythonDeps();
    await copyFiles();
    await installDaicCommand();
    const serenaMCPInstalled = await setupSerenaMCP();
    const memoryBankMCPInstalled = await setupMemoryBankMCP();
    const githubMCPInstalled = await setupGitHubMCP();
    const storybookMCPInstalled = await setupStorybookMCP();
    const playwrightMCPInstalled = await setupPlaywrightMCP();
    const { statuslineInstalled } = await configure();
    await saveConfig(statuslineInstalled);
    await setupClaudeMd();
    
    // Success message
    console.log();
    console.log();
    console.log(color('╔═══════════════════════════════════════════════════════════════╗', colors.bright + colors.green));
    console.log(color('║                 🎉 INSTALLATION COMPLETE! 🎉                  ║', colors.bright + colors.green));
    console.log(color('╚═══════════════════════════════════════════════════════════════╝', colors.bright + colors.green));
    console.log();
    
    console.log(color('  Installation Summary:', colors.bright + colors.cyan));
    console.log(color('  ─────────────────────', colors.dim));
    console.log(color(`  ${icons.check} Directory structure created`, colors.green));
    console.log(color(`  ${icons.check} Hooks installed and configured`, colors.green));
    console.log(color(`  ${icons.check} Protocols and agents deployed`, colors.green));
    console.log(color(`  ${icons.check} daic command available globally`, colors.green));
    console.log(color(`  ${icons.check} Configuration saved`, colors.green));
    console.log(color(`  ${icons.check} DAIC state initialized (Discussion mode)`, colors.green));
    
    if (statuslineInstalled) {
      console.log(color(`  ${icons.check} Statusline configured`, colors.green));
    }
    
    console.log();
    
    // Test daic command
    if (commandExists('daic')) {
      console.log(color(`  ${icons.check} daic command verified and working`, colors.green));
    } else {
      console.log(color(`  ${icons.warning} daic command not in PATH`, colors.yellow));
      console.log(color('       Add /usr/local/bin to your PATH', colors.dim));
    }
    
    console.log();
    console.log(color(`  ${icons.star} NEXT STEPS`, colors.bright + colors.magenta));
    console.log(color('  ─────────────', colors.dim));
    console.log();
    console.log(color('  1. Restart Claude Code to activate the sessions hooks', colors.white));
    console.log(color('     ' + icons.arrow + ' Close and reopen Claude Code', colors.dim));
    console.log();
    console.log(color('  2. Create your first task:', colors.white));
    console.log(color('     ' + icons.arrow + ' Tell Claude: "Create a new task"', colors.cyan));
    console.log(color('     ' + icons.arrow + ' Or: "Create a task for implementing feature X"', colors.cyan));
    console.log();
    console.log(color('  3. Start working with the DAIC workflow:', colors.white));
    console.log(color('     ' + icons.arrow + ' Discuss approach first', colors.dim));
    console.log(color('     ' + icons.arrow + ' Say "make it so" to implement', colors.dim));
    console.log(color('     ' + icons.arrow + ' Run "daic" to return to discussion', colors.dim));
    console.log();
    console.log(color('  ──────────────────────────────────────────────────────', colors.dim));
    console.log();
    console.log(color(`  Welcome aboard, ${config.developer_name}! 🚀`, colors.bright + colors.cyan));
    
  } catch (error) {
    console.error(color(`❌ Installation failed: ${error.message}`, colors.red));
    process.exit(1);
  } finally {
    rl.close();
  }
}

// Run installation
if (require.main === module) {
  install().catch(error => {
    console.error(color(`❌ Fatal error: ${error}`, colors.red));
    process.exit(1);
  });
}

module.exports = { install };
