import re
import os
from datetime import datetime
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType

# Import custom modules
from custom_tools import get_weather, get_attraction, calculate_budget, get_budget_summary
from utils import OutputManager
from config import (
    AGENT_SYSTEM_PROMPT, 
    MODELSCOPE_API_KEY, 
    MODELSCOPE_BASE_URL, 
    MODEL_NAME, 
    TAVILY_API_KEY
)

def main():
    # --- 1. Configure environment variables ---
    os.environ['TAVILY_API_KEY'] = TAVILY_API_KEY

    # --- 2. Initialize output manager ---
    output_manager = OutputManager()

    # --- 3. Configure LLM client ---
    llm = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
        model_type=MODEL_NAME,
        url=MODELSCOPE_BASE_URL,
        api_key=MODELSCOPE_API_KEY
    )

    llm_agent = ChatAgent(
        model=llm,
        output_language='English',
        system_message=AGENT_SYSTEM_PROMPT
    )

    # --- 4. Configure available tools ---
    available_tools = {
        "get_weather": get_weather,
        "get_attraction": get_attraction,
        "calculate_budget": calculate_budget,
        "get_budget_summary": get_budget_summary,
    }

    # --- 5. Initialize ---
    user_prompt = "Hello, please help me check the weather in Barcelona, Spain today, then recommend some suitable tourist attractions based on the weather. The attractions should be outdoors. Please list a one-day itinerary with time and budget."
    prompt_history = [f"User request: {user_prompt}"]

    print(f"User input: {user_prompt}\n" + "="*40)

    # --- 6. Run main loop ---
    for i in range(5):  # Set maximum loop count
        print(f"--- Loop {i+1} ---\n")
        
        # 5.1. Build prompt
        full_prompt = "\n".join(prompt_history)
        
        # 5.2. Call LLM for reasoning
        llm_output = llm_agent.step(full_prompt).msgs[0].content
        print(f"Model output:\n{llm_output}\n")
        prompt_history.append(llm_output)
        
        # 5.3. Parse and execute actions
        action_matches = re.findall(r"Action: ([^\n]+)", llm_output)
        if not action_matches:
            print("Parse error: No Action found in model output.")
            break
        
        # Handle the first Action (if multiple Actions exist, only handle the first one)
        action_str = action_matches[0].strip()

        if action_str.startswith("finish"):
            final_answer_match = re.search(r'finish\(answer="(.*)"\)', action_str, re.DOTALL)
            if final_answer_match:
                final_answer = final_answer_match.group(1)
            else:
                final_answer = "Task completed"
            
            print(f"Task completed, final answer: {final_answer}")
            
            # Save output results to file
            try:
                filepath = output_manager.save_travel_report(user_prompt, final_answer, prompt_history)
                print(f"\n✅ Query results saved to: {filepath}")
                
                # Verify saved file content and city name consistency
                city_from_prompt = output_manager._extract_city_from_all_content(user_prompt, final_answer, prompt_history)
                print(f"📍 Identified query city: {city_from_prompt}")
                print(f"📁 File save path: {filepath}")
                
                # Check if file was successfully created
                if os.path.exists(filepath):
                    file_size = os.path.getsize(filepath)
                    print(f"📊 File size: {file_size} bytes")
                else:
                    print("⚠️  Warning: File may not have been created successfully")
                    
            except Exception as e:
                print(f"\n❌ Error saving file: {e}")
            break
        
        # Parse tool calls
        tool_match = re.search(r"(\w+)\((.*)\)", action_str)
        if not tool_match:
            observation = f"Error: Unable to parse Action format '{action_str}'"
        else:
            tool_name = tool_match.group(1)
            args_str = tool_match.group(2)
            
            try:
                # Parse parameters
                kwargs = {}
                
                # Parse quoted string parameters
                string_params = re.findall(r'(\w+)="([^"]*)"', args_str)
                for key, value in string_params:
                    kwargs[key] = value
                
                # Parse numeric parameters (without quotes)
                number_params = re.findall(r'(\w+)=(\d+(?:\.\d+)?)', args_str)
                for key, value in number_params:
                    # Try to convert to integer, if failed then convert to float
                    try:
                        kwargs[key] = int(value)
                    except ValueError:
                        kwargs[key] = float(value)
                
                if tool_name in available_tools:
                    observation = available_tools[tool_name](**kwargs)
                else:
                    observation = f"Error: Undefined tool '{tool_name}'"
            except Exception as e:
                observation = f"Error: Problem calling tool '{tool_name}' - {e}"

        # 5.4. Record observation results
        observation_str = f"Observation: {observation}"
        print(f"{observation_str}\n" + "="*40)
        prompt_history.append(observation_str)

if __name__ == "__main__":
    main()