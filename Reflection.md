# Auto-PPT Agent - Reflection Document

## Where did your agent fail its first attempt?
During initial testing, the agent failed in the following key areas before being refined:
1. **Tool Invocation Order**: It occasionally attempted to add slides before successfully creating a presentation, leading to a "File does not exist" error. Enforcing **Step 2 (call create_presentation)** explicitly in the System Prompt fixed this.
2. **Search Ambiguities**: When calling `search_topic` with broad keywords, the `wikipedia` library would often throw `DisambiguationError`, crashing the server and the agent loop. I had to explicitly catch the error on the MCP server side and either pick the first generic match or cleanly return a string instructing the agent to "use your own knowledge and hallucinate gracefully."
3. **Stateless Operations**: Attempting to have the MCP Server hold the active PowerPoint file in memory across multiple atomic tool calls was extremely problematic. I redesigned the functions to ensure each tool call accepts the `filename` as an argument, reads the existing `.pptx` (or creates a new one), modifying it, and immediately saving it back to disk.

## How did MCP prevent you from writing hardcoded scripts?
MCP (Model Context Protocol) forced a clean separation of concerns and purely functional execution mapping:
1. **Discoverability over Procedural Control**: Instead of writing a rigid, procedural Python script that iterates `for slide in slides`, the logic execution is completely handed over to the LangChain Agent. The Agent statically connects to the server, queries the available MCP tools (`create_presentation`, `add_slide`, `search_topic`), and dynamically plans its execution instead of following hardcoded constraints.
2. **Contract Enforcements**: The MCP server dictates strict input architectures for tools (e.g., `filename`, `title`, `bullet_points`). The agent is forced to adhere to these schemas explicitly during json generation tool calls, providing guaranteed consistency. 
3. **True Agentic Loops**: By exposing decoupled MCP tools, the agent creates a highly observable ReAct loop. It reasons about its goal ("I need to gather info"), acts (calls `search_topic`), observes the consequence ("I received star life cycle data"), and reasons again ("Now I will call `add_slide` with that specific data"). This structurally turns a deterministic code task into dynamic, autonomous problem-solving.
