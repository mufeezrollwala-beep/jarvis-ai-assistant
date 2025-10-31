#!/usr/bin/env python3
import typer
import requests
import json
import os
import asyncio
import websockets
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from jarvis_core import JarvisCore


app = typer.Typer(help="Jarvis CLI - Command-line interface for Jarvis assistant")
console = Console()


def get_api_config():
    """Get API configuration from environment or defaults"""
    return {
        'base_url': os.environ.get('JARVIS_API_URL', 'http://localhost:8000'),
        'api_key': os.environ.get('JARVIS_API_KEY', 'jarvis-secret-key-123')
    }


@app.command()
def command(
    text: str = typer.Argument(..., help="Command to send to Jarvis"),
    direct: bool = typer.Option(False, "--direct", "-d", help="Execute directly without API"),
    api_url: Optional[str] = typer.Option(None, "--api-url", help="Override API base URL"),
    api_key: Optional[str] = typer.Option(None, "--api-key", help="Override API key")
):
    """
    Send a text command to Jarvis
    
    Examples:
        jarvis-cli command "what time is it"
        jarvis-cli command "wikipedia python programming" --direct
    """
    if direct:
        console.print("[bold blue]Processing command directly...[/bold blue]")
        core = JarvisCore()
        response = core.process_command(text)
        
        if response['success']:
            console.print(f"[bold green]✓[/bold green] {response['message']}")
            if response.get('data'):
                console.print(f"\n[dim]Data:[/dim]")
                console.print_json(json.dumps(response['data'], indent=2))
        else:
            console.print(f"[bold red]✗[/bold red] {response['message']}")
    else:
        config = get_api_config()
        if api_url:
            config['base_url'] = api_url
        if api_key:
            config['api_key'] = api_key
        
        console.print(f"[bold blue]Sending command to {config['base_url']}...[/bold blue]")
        
        try:
            response = requests.post(
                f"{config['base_url']}/commands",
                json={"command": text},
                headers={"X-API-Key": config['api_key']},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    console.print(f"[bold green]✓[/bold green] {data['message']}")
                    if data.get('data'):
                        console.print(f"\n[dim]Data:[/dim]")
                        console.print_json(json.dumps(data['data'], indent=2))
                else:
                    console.print(f"[bold red]✗[/bold red] {data['message']}")
            elif response.status_code == 403:
                console.print("[bold red]Authentication failed![/bold red] Check your API key.")
            else:
                console.print(f"[bold red]Error:[/bold red] HTTP {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            console.print("[bold red]Connection failed![/bold red] Is the API server running?")
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")


@app.command()
def status(
    api_url: Optional[str] = typer.Option(None, "--api-url", help="Override API base URL"),
    api_key: Optional[str] = typer.Option(None, "--api-key", help="Override API key")
):
    """
    Get Jarvis system status
    
    Example:
        jarvis-cli status
    """
    config = get_api_config()
    if api_url:
        config['base_url'] = api_url
    if api_key:
        config['api_key'] = api_key
    
    try:
        response = requests.get(
            f"{config['base_url']}/status",
            headers={"X-API-Key": config['api_key']},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            table = Table(title="Jarvis Status")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Status", data['status'])
            table.add_row("Uptime", f"{data['uptime']:.2f}s")
            table.add_row("Commands Processed", str(data['commands_processed']))
            
            if data.get('last_command'):
                table.add_row("Last Command", data['last_command'].get('query', 'N/A'))
            
            console.print(table)
        elif response.status_code == 403:
            console.print("[bold red]Authentication failed![/bold red] Check your API key.")
        else:
            console.print(f"[bold red]Error:[/bold red] HTTP {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        console.print("[bold red]Connection failed![/bold red] Is the API server running?")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")


@app.command()
def interactive(
    direct: bool = typer.Option(False, "--direct", "-d", help="Execute directly without API"),
    api_url: Optional[str] = typer.Option(None, "--api-url", help="Override API base URL"),
    api_key: Optional[str] = typer.Option(None, "--api-key", help="Override API key")
):
    """
    Start interactive mode for continuous conversation with Jarvis
    
    Example:
        jarvis-cli interactive
        jarvis-cli interactive --direct
    """
    console.print("[bold green]Jarvis Interactive Mode[/bold green]")
    console.print("Type 'exit' or 'quit' to end the session\n")
    
    if direct:
        core = JarvisCore()
        greeting = core.get_greeting()
        console.print(f"[bold blue]Jarvis:[/bold blue] {greeting}\n")
    else:
        config = get_api_config()
        if api_url:
            config['base_url'] = api_url
        if api_key:
            config['api_key'] = api_key
        console.print(f"[dim]Connected to: {config['base_url']}[/dim]\n")
    
    while True:
        try:
            user_input = console.input("[bold yellow]You:[/bold yellow] ")
            
            if not user_input.strip():
                continue
            
            if user_input.lower() in ['exit', 'quit', 'goodbye']:
                console.print("[bold blue]Jarvis:[/bold blue] Goodbye!")
                break
            
            if direct:
                core = JarvisCore()
                response = core.process_command(user_input)
                console.print(f"[bold blue]Jarvis:[/bold blue] {response['message']}\n")
            else:
                try:
                    response = requests.post(
                        f"{config['base_url']}/commands",
                        json={"command": user_input},
                        headers={"X-API-Key": config['api_key']},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        console.print(f"[bold blue]Jarvis:[/bold blue] {data['message']}\n")
                    else:
                        console.print(f"[bold red]Error:[/bold red] HTTP {response.status_code}\n")
                except Exception as e:
                    console.print(f"[bold red]Error:[/bold red] {str(e)}\n")
                    
        except KeyboardInterrupt:
            console.print("\n[bold blue]Jarvis:[/bold blue] Goodbye!")
            break
        except EOFError:
            console.print("\n[bold blue]Jarvis:[/bold blue] Goodbye!")
            break


@app.command()
def stream(
    api_url: Optional[str] = typer.Option(None, "--api-url", help="Override API base URL"),
    api_key: Optional[str] = typer.Option(None, "--api-key", help="Override API key")
):
    """
    Connect to WebSocket stream for real-time updates
    
    Example:
        jarvis-cli stream
    """
    config = get_api_config()
    if api_url:
        config['base_url'] = api_url
    if api_key:
        config['api_key'] = api_key
    
    ws_url = config['base_url'].replace('http://', 'ws://').replace('https://', 'wss://')
    ws_url = f"{ws_url}/stream?api_key={config['api_key']}"
    
    console.print(f"[bold blue]Connecting to WebSocket stream...[/bold blue]")
    
    async def ws_client():
        try:
            async with websockets.connect(ws_url) as websocket:
                console.print("[bold green]Connected![/bold green] Listening for updates...\n")
                
                async def send_commands():
                    while True:
                        try:
                            command = await asyncio.get_event_loop().run_in_executor(
                                None, console.input, "[bold yellow]Command:[/bold yellow] "
                            )
                            
                            if command.lower() in ['exit', 'quit']:
                                break
                            
                            await websocket.send(json.dumps({
                                'type': 'command',
                                'command': command
                            }))
                        except Exception as e:
                            console.print(f"[bold red]Error sending:[/bold red] {e}")
                            break
                
                async def receive_messages():
                    async for message in websocket:
                        try:
                            data = json.loads(message)
                            msg_type = data.get('type', 'unknown')
                            
                            if msg_type == 'connection':
                                console.print(f"[dim]{data.get('message')}[/dim]")
                            elif msg_type == 'processing':
                                console.print(f"[bold blue]{data.get('message')}[/bold blue]")
                            elif msg_type == 'result':
                                response = data.get('response', {})
                                console.print(f"[bold green]Result:[/bold green] {response.get('message')}\n")
                            elif msg_type == 'command_processed':
                                console.print(f"[dim]Broadcast: Command '{data.get('command')}' processed[/dim]")
                            else:
                                console.print(f"[dim]{message}[/dim]")
                        except json.JSONDecodeError:
                            console.print(f"[dim]{message}[/dim]")
                
                await asyncio.gather(send_commands(), receive_messages())
                
        except Exception as e:
            console.print(f"[bold red]WebSocket error:[/bold red] {str(e)}")
    
    try:
        asyncio.run(ws_client())
    except KeyboardInterrupt:
        console.print("\n[bold blue]Disconnected[/bold blue]")


if __name__ == "__main__":
    app()
