# Machine SDK

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)

A Python SDK that enables you to create, manage, and interact with AI agents on [Suna](https://suna.so).

## 📦 Installation

Install directly from the GitHub repository:

```bash
pip install "machine-sdk @ git+https://github.com/rossman22590/machine-sdk.git@main#subdirectory=sdk"
```

Or using uv:

```bash
uv add "machine-sdk @ git+https://github.com/rossman22590/machine-sdk.git@main#subdirectory=sdk"
```

## 🔧 Quick Start

```python
import asyncio
from Machine import Machine

async def main():
    mcp_tools = Machine.MCPTools(
        "http://localhost:4000/mcp/",  # Point to any HTTP MCP server
        "Machine",
    )
    await mcp_tools.initialize()

    # Initialize the client
    client = Machine.Machine(api_key="your-api-key")

    # Create an agent
    agent = await client.Agent.create(
        name="My Assistant",
        system_prompt="You are a helpful AI assistant.",
        mcp_tools=[mcp_tools],
        allowed_tools=["get_wind_direction"],
    )

    # Create a conversation thread
    thread = await client.Thread.create()

    # Run the agent
    run = await agent.run("Hello, how are you?", thread)

    # Stream the response
    stream = await run.get_stream()
    async for chunk in stream:
        print(chunk, end="")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🔑 Environment Setup

Get your API key from [https://machine.myapps.ai/settings/api-keys](https://machine.myapps.ai/settings/api-keys)

## 🧪 Running Examples

```bash
# Install dependencies
uv sync

# Run the main example
PYTHONPATH=$(pwd) uv run example/example.py
```
