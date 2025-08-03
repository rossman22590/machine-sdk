# Run with `PYTHONPATH=$(pwd) uv run example/example.py`

import asyncio
import os

from kortix import kortix
from kortix.utils import print_stream


from kv import kv
from mcp_server import mcp


async def main():
    """
    Please ignore the asyncio.exceptions.CancelledError that is thrown when the MCP server is stopped. I couldn't fix it.
    """
    try:
        # Start the MCP server in the background
        server_task = asyncio.create_task(
            mcp.run_http_async(
                show_banner=False, 
                log_level="info", 
                host="0.0.0.0", 
                port=4000
            )
        )
        
        # Give the server a moment to start
        await asyncio.sleep(1)

        # Create the MCP tools client
        mcp_tools = kortix.MCPTools(
            "http://localhost:4000/mcp/",
            "Kortix",
            allowed_tools=["get_wind_direction"],
        )
        
        # Initialize the MCP tools
        try:
            await mcp_tools.initialize()
            print("MCP tools initialized successfully")
        except Exception as e:
            print(f"Failed to initialize MCP tools: {e}")
            return

        # Initialize the Kortix client
        try:
            kortix_client = kortix.Kortix(
                os.getenv("KORTIX_API_KEY"),
                "https://the-machine-api-v9-2-production.up.railway.app/api",
            )
            print("Kortix client initialized successfully")
        except Exception as e:
            print(f"Failed to initialize Kortix client: {e}")
            return

        # Setup the agent
        agent = None
        agent_id = kv.get("agent_id")
        
        if agent_id:
            try:
                agent = await kortix_client.Agent.get(agent_id)
                print(f"Using existing agent with ID: {agent._agent_id}")
            except Exception as e:
                print(f"Agent not found, will create a new one: {e}")
                agent_id = None
        
        if not agent_id:
            try:
                agent = await kortix_client.Agent.create(
                    name="Ross API Agent",
                    system_prompt="You are a generic agent. You can use the tools provided to you to answer questions.",
                    mcp_tools=[mcp_tools],
                    allowed_tools=["get_weather"],
                )
                kv.set("agent_id", agent._agent_id)
                print(f"Created new agent with ID: {agent._agent_id}")
            except Exception as e:
                print(f"Failed to create agent: {e}")
                return

        # Setup the thread
        thread_id = kv.get("thread_id")
        if not thread_id:
            try:
                thread = await kortix_client.Thread.create()
                kv.set("thread_id", thread._thread_id)
                print(f"Created new thread with ID: {thread._thread_id}")
            except Exception as e:
                print(f"Failed to create thread: {e}")
                return
        else:
            try:
                thread = await kortix_client.Thread.get(thread_id)
                print(f"Using existing thread with ID: {thread_id}")
            except Exception as e:
                print(f"Failed to get thread: {e}")
                return

        # Run the agent
        try:
            print("Running agent...")
            agent_run = await agent.run("What is the wind direction in Bangalore?", thread)
            stream = await agent_run.get_stream()
            await print_stream(stream)
        except Exception as e:
            print(f"Error running agent: {e}")

        # Keep the server running
        print("\nMCP server is running at http://localhost:4000/mcp/")
        print("Press Ctrl+C to stop the server")
        
        # Keep the script running
        while True:
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        print("\nShutting down...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        # Cleanup - MCPTools doesn't have a shutdown method, so we just cancel the server task
        if 'server_task' in locals():
            server_task.cancel()
            try:
                await server_task
            except asyncio.CancelledError:
                pass


if __name__ == "__main__":
    asyncio.run(main())
