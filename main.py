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

@mcp.tool()
def gobuster_scan(url: str, wordlist: str = "/usr/share/wordlists/dirb/common.txt") -> str:
    """Run Gobuster inside WSL Kali"""
    return run_kali_command(f"gobuster dir -u {url} -w {wordlist}")

@mcp.tool()
def nikto_scan(target: str) -> str:
    """Run Nikto inside WSL Kali"""
    return run_kali_command(f"nikto -h {target}")

@mcp.tool()
def search_exploit(query: str) -> str:
    """Searchsploit inside WSL Kali"""
    return run_kali_command(f"searchsploit {query}")

@mcp.tool()
def metasploit_stub(module: str) -> str:
    """Metasploit stub (you can later integrate msfconsole RPC)"""
    return f"[Stub] Would run {module} in msfconsole via script"
