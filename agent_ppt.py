import asyncio
import os
import sys
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_huggingface import HuggingFaceEndpoint

# Loading your locally cached HuggingFace Token to permanently evade Google's rate limits!
os.environ["HUGGINGFACEHUB_API_TOKEN"] = "YOUR_HUGGINGFACE_API_KEY_HERE"

async def run_ppt_agent(user_request: str):
    server_params = StdioServerParameters(command="python", args=["mcp_server.py"])
    
    print("[Agent] Integrating with MCP Subprocess...")
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("[Agent] Connected to MCP Server smoothly.")
            
            async def call_create_presentation(filename: str) -> str:
                res = await session.call_tool("create_presentation", arguments={"filename": filename})
                return res.content[0].text

            async def call_add_slide(filename: str, title: str, bullet_points: list[str]) -> str:
                res = await session.call_tool("add_slide", arguments={"filename": filename, "title": title, "bullet_points": bullet_points})
                return res.content[0].text

            async def call_search_topic(query: str) -> str:
                res = await session.call_tool("search_topic", arguments={"query": query})
                return res.content[0].text

            # Initializing completely UNMETERED HuggingFace Model!
            llm = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2", temperature=0.1)

            print("\n[Agent] Starting Agentic Reasoning Loop...\n")

            history = f"User Request: {user_request}\n"
            steps = 0
            
            while steps < 15:
                steps += 1
                prompt = f"""
You are a Presentation Agent. Your job is to create a presentation.
You have the following tools available:
- create_presentation(filename: string): Initializes a new presentation. ALWAYS DO THIS FIRST.
- search_topic(query: string): Searches wikipedia for facts.
- add_slide(filename: string, title: string, bullet_points: array of strings): Adds a strictly formatted slide. Ensure 3-5 bullet points.

Your response must be a SINGLE RAW JSON object with exactly these keys:
- "thought": A string explaining your reasoning for your next action.
- "action": Either a tool name ("create_presentation", "search_topic", "add_slide") OR "finish" if the presentation is completely 100% built.
- "args": A dictionary of arguments for the tool (e.g. {{"filename": "pres.pptx", "title": "Intro", "bullet_points": ["A", "B", "C"], "query": "Star"}}). If action is "finish", this can be empty.

Do not output ANY code blocks, markdown formatting, or text outside the JSON object! ONLY JSON.

History of actions so far:
{history}

Next action (JSON only):
"""
                try:
                    res = await llm.ainvoke(prompt)
                    await asyncio.sleep(2) # Polite pacing
                    
                    output_text = res.replace("```json", "").replace("```", "").strip()
                    
                    # Robust parsing to strip out conversational padding HuggingFace models love to add
                    if not (output_text.startswith("{") and output_text.endswith("}")):
                        start_idx = output_text.find('{')
                        end_idx = output_text.rfind('}')
                        if start_idx != -1 and end_idx != -1:
                            output_text = output_text[start_idx:end_idx+1]

                    action_data = json.loads(output_text)
                except Exception as e:
                    print(f"  [!] Recovering from parsing error... (HuggingFace Retry)")
                    history += f"System: Error: {str(e)}. Please format STRICTLY as JSON object without extra text.\n"
                    await asyncio.sleep(2)
                    steps -= 1
                    continue
                
                thought = action_data.get("thought", "")
                action = action_data.get("action", "")
                args = action_data.get("args", {})
                
                print(f"[Thought] {thought}")
                
                if action == "finish":
                    print("\n[✔] Finished successfully!")
                    break
                    
                print(f"  --> [Tool Call] {action}({args})")
                
                tool_res = ""
                try:
                    if action == "create_presentation":
                        tool_res = await call_create_presentation(args.get("filename", "presentation.pptx"))
                    elif action == "add_slide":
                        tool_res = await call_add_slide(
                            args.get("filename", "presentation.pptx"),
                            args.get("title", ""),
                            args.get("bullet_points", [])
                        )
                    elif action == "search_topic":
                        tool_res = await call_search_topic(args.get("query", ""))
                    else:
                        tool_res = f"Unknown tool: {action}"
                except Exception as e:
                    tool_res = f"Error executing tool: {str(e)}"
                    
                history += f"\nAgent took action: {action} with args {args}\nObservation: {tool_res}\n"
                print()
            
            return "Success"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = "Create a 5-slide presentation on The Wonders of the Deep Ocean for a middle school science class"
    
    print(f"Presentation Goal: {query}\n")
    asyncio.run(run_ppt_agent(query))
