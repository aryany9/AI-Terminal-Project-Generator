import json
import os
import requests
from termcolor import colored
from utils.tools import tools

def process_query(llm_client, user_query, system_prompt):
    """
    Processes the user query using the chosen LLM client.
    
    Args:
        llm_client: The LLM client to use for processing.
        user_query (str): The user's query.
        system_prompt (str): The system prompt to use.
        
    Returns:
        str: The final output from the LLM.
    """
    # Create output directory if it doesn't exist
    if not os.path.exists('output'):
        os.makedirs('output')
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.append({"role": "user", "content": user_query})
    
    # Track current working directory
    original_cwd = os.getcwd()
    
    try:
        while True:
            # Get response from LLM
            try:
                response = llm_client.run_query(messages)
                parsed_output = json.loads(response)
            except json.JSONDecodeError:
                print(colored("Error: LLM response was not valid JSON. Retrying...", "red"))
                continue
            except Exception as e:
                print(colored(f"Error with LLM query: {str(e)}", "red"))
                return "Error: Failed to get a proper response from the AI assistant."
            
            # Add response to message history
            messages.append({"role": "assistant", "content": json.dumps(parsed_output)})
            print(colored(f"🤖 LLM Response: {parsed_output}", "green"))
            # Handle different step types
            if parsed_output.get("step") == "plan":
                print(colored(f"🧠 Planning: {parsed_output.get('content')}", "yellow"))
                continue
                
            elif parsed_output.get("step") == "input":
                query = input(colored(f"🔍 Input needed: {parsed_output.get('content')}: ", "cyan"))
                messages.append({
                    "role": "user",
                    "content": query
                })
                continue
                
            elif parsed_output.get("step") == "action":
                tool_name = parsed_output.get("function")
                tool_input = parsed_output.get("input")
                
                print(colored(f"🔨 Action: {tool_name} with input: {tool_input}", "blue"))
                
                if tool_name in tools:
                    fn = tools[tool_name]["fn"]
                    try:
                        # Execute the tool function with appropriate parameters
                        if isinstance(tool_input, dict):
                            output = fn(**tool_input)  # Unpack keyword arguments
                        elif isinstance(tool_input, (list, tuple)):
                            output = fn(*tool_input)   # Unpack positional arguments
                        elif tool_input is None:
                            output = fn() # No arguments
                        else:
                            output = fn(tool_input)    # Single argument
                            
                        # Format output feedback based on status
                        if isinstance(output, dict) and "status" in output:
                            status = output["status"]
                            message = output.get("message", "")
                            
                            if status == "success":
                                print(colored(f"✅ Success: {message}", "green"))
                            elif status == "error":
                                print(colored(f"❌ Error: {message}", "red"))
                            elif status == "partial":
                                print(colored(f"⚠️ Partial: {message}", "yellow"))
                        
                    except Exception as e:
                        output = {"status": "error", "message": str(e)}
                        print(colored(f"❌ Tool error: {str(e)}", "red"))
                    
                    # Add observation to message history
                    messages.append({
                        "role": "assistant",
                        "content": json.dumps({"step": "observe", "content": output})
                    })
                    continue
                else:
                    print(colored(f"❌ Unknown tool: {tool_name}", "red"))
                    messages.append({
                        "role": "assistant",
                        "content": json.dumps({
                            "step": "observe", 
                            "content": {
                                "status": "error", 
                                "message": f"Unknown tool: {tool_name}"
                            }
                        })
                    })
                    continue
                    
            elif parsed_output.get("step") == "output":
                print(colored(f"🎉 Complete: {parsed_output.get('content')}", "green"))
                return parsed_output.get('content')
                
            elif parsed_output.get("step") == "observe":
                print(colored(f"👁️ Observation: {parsed_output.get('content')}", "magenta"))
                continue
                
            else:
                print(colored(f"❓ Unknown step: {parsed_output.get('step')}", "red"))
                messages.append({
                    "role": "assistant",
                    "content": json.dumps({
                        "step": "observe", 
                        "content": {
                            "status": "error", 
                            "message": f"Unknown step: {parsed_output.get('step')}"
                        }
                    })
                })
                continue
    
    finally:
        # Ensure we return to the original directory
        os.chdir(original_cwd)