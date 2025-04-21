# WSL Kali Pentest Agent

A Python-based utility for running penetration testing tools from Kali Linux through Windows Subsystem for Linux (WSL).

## Overview

This tool creates a bridge between Python applications running on Windows and security tools available in the Kali Linux WSL distribution. It exposes common penetration testing utilities as callable functions through a simple API.

## Prerequisites

- Windows 10/11 with WSL2 installed
- Kali Linux WSL distribution
- Python 3.7+
- Required Python packages: `mcp-fastmcp`

## Installation

1. Install Kali Linux on WSL:
   ```
   wsl --install -d kali-linux
   ```

2. Update Kali and install required tools:
   ```
   wsl -d kali-linux -- apt update && apt upgrade -y
   wsl -d kali-linux -- apt install -y nmap gobuster nikto exploitdb
   ```

3. Install the required Python package:
   ```
   pip install mcp-fastmcp
   ```

## Usage

Import the module and use the provided tools:

```python
from wsl_kali_pentest_agent import nmap_scan, gobuster_scan, nikto_scan, search_exploit, metasploit_stub

# Run an Nmap scan
results = nmap_scan("192.168.1.1", "-sV -p 1-1000")
print(results)

# Directory enumeration with Gobuster
dirs = gobuster_scan("http://example.com", "/usr/share/wordlists/dirb/common.txt")
print(dirs)

# Web server analysis with Nikto
vulns = nikto_scan("http://example.com")
print(vulns)

# Search for exploits
exploits = search_exploit("apache 2.4.49")
print(exploits)

# Example stub for Metasploit (to be expanded)
metasploit_stub("exploit/multi/http/apache_log4j_cve_2021_44228_rce")
```

## Available Tools

| Function | Description | Default Options |
|----------|-------------|----------------|
| `nmap_scan(target, options)` | Network scanning with Nmap | `-sV` |
| `gobuster_scan(url, wordlist)` | Directory enumeration | `/usr/share/wordlists/dirb/common.txt` |
| `nikto_scan(target)` | Web server vulnerability scanning | N/A |
| `search_exploit(query)` | Search for exploits in ExploitDB | N/A |
| `metasploit_stub(module)` | Stub for future Metasploit integration | N/A |

## Implementation Details

The agent uses the FastMCP framework to expose WSL commands as callable tools. Each function executes commands inside the Kali Linux WSL environment using the `subprocess` module.

```python
import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WSL-Kali-Pentest-Agent")

def run_kali_command(command: str) -> str:
    """Run a shell command inside WSL Kali"""
    try:
        # Uses 'wsl -d kali-linux' to run inside Kali distro
        result = subprocess.run(
            ["wsl", "-d", "kali-linux", "--", "bash", "-c", command],
            capture_output=True,
            text=True
        )
        return result.stdout if result.stdout else result.stderr
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def nmap_scan(target: str, options: str = "-sV") -> str:
    """Run Nmap inside WSL Kali"""
    return run_kali_command(f"nmap {options} {target}")

# Additional tools defined similarly...
```

## Security Considerations

- This tool executes commands in WSL with the permissions of the current user
- Be cautious when scanning targets - ensure you have permission to test them
- Consider sanitizing inputs to prevent command injection attacks

## Future Improvements

- Add more security tools from Kali Linux
- Implement proper Metasploit integration via RPC
- Add output parsers to convert tool results to structured data
- Create a web interface for easier interaction

## License

MIT License
