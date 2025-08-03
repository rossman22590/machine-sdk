"""
machine SDK for machine AI Agent Platform

A Python SDK for creating and managing AI agents with thread execution capabilities.
"""

__version__ = "0.1.0"

from .machine.machine import Machine
from .machine.tools import AgentPressTools, MCPTools

__all__ = ["Machine", "AgentPressTools", "MCPTools"]
