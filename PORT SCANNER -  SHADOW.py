import socket
from rich.console import Console
from rich.progress import track
from rich.table import Table

console = Console()

target = input("Enter target IP address: ")
ports = range(20, 1025)

console.print(f"[bold cyan]Scanning {target}...[/bold cyan]")

open_ports = []

for port in track(ports, description="Scanning ports..."):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target, port))
    if result == 0:
        open_ports.append(port)
    sock.close()

table = Table(title=f"Open Ports on {target}")
table.add_column("Port", justify="center", style="green", no_wrap=True)

for port in open_ports:
    table.add_row(str(port))

if open_ports:
    console.print(table)
else:
    console.print("[bold red]No open ports found.[/bold red]")
