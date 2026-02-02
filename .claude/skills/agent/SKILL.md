---
name: agent
description: Create and configure AI agents for the Periscope platform
delegates-to: agent-manager
---

# /agent - Create and Manage AI Agents

Use this skill to create, configure, and execute PydanticAI agents in the Periscope platform.

## What You Can Do

1. **Create agents** - Design new AI agents with specific capabilities
2. **Configure prompts** - Craft effective system prompts
3. **Execute agents** - Run agents with prompts
4. **Manage MCP servers** - Connect agents to external tools
5. **Monitor performance** - Track agent statistics

## How to Use

Describe the AI agent you want to create:

- "Create a document analysis agent"
- "Build an agent that can classify customer support tickets"
- "Design an agent for extracting data from invoices"
- "Execute the risk assessment agent with this data"

## Agent Design Steps

1. **Define Purpose**
   - What should the agent do?
   - What type of tasks will it handle?

2. **Choose Model**
   - OpenAI: gpt-4o, gpt-4o-mini
   - Anthropic: claude-3-5-sonnet, claude-3-5-haiku
   - Google: gemini-2.0-flash, gemini-1.5-pro

3. **Craft Prompt**
   - Clear role definition
   - Specific instructions
   - Output format requirements

4. **Assign Capabilities**
   - document_analysis
   - data_extraction
   - classification
   - communication
   - decision_making

5. **Configure MCP Servers** (optional)
   - External tool access
   - Database connections
   - API integrations

## Agent Configuration Example

```json
{
  "name": "invoice-processor",
  "description": "Extracts key fields from invoices",
  "model_provider": "openai",
  "model_name": "gpt-4o",
  "system_prompt": "You are an invoice processing specialist...",
  "capabilities": ["document_analysis", "data_extraction"],
  "temperature": 0.2,
  "max_tokens": 2000
}
```

## Reference Documentation

- [MCP Tools Reference](../../../docs/mcp-tools-reference.md) - Available MCP servers and tools

## Delegated Agent

This skill delegates to the **agent-manager** agent which has access to:
- `periscope-agents-core-dev` MCP server (15 tools)
- `periscope-mcp-servers-dev` MCP server (13 tools)
- `periscope-context-dev` MCP server (5 tools)

## Output

Your agent configuration will be saved to:
```
workspace/agents/<agent-name>.json
```
