import json
import os
from google import genai
client=genai.Client(api_key="AQ.Ab8RN6IuPvOm9QI0bss3Y-xqpxFOIq3CyEGcR8JWbbWrvH8M9w")
from utils import check_stockout_risk

# Initialize the Gemini client (reads GEMINI_API_KEY from environment variables)
client = genai.Client(api_key="AQ.Ab8RN6IuPvOm9QI0bss3Y-xqpxFOIq3CyEGcR8JWbbWrvH8M9w")

def run_supply_chain_agent():
    print("===========================================")
    print("   SupplyChainIQ: Autonomous Agent v1.0    ")
    print("===========================================\n")
    
    with open("data.json", "r") as f:
        inventory = json.load(f)

    for item in inventory:
        print(f"📦 Agent inspecting: {item['product_name']}")
        
        # Step 1: Tool Execution (Math calculation)
        analysis = check_stockout_risk(item)
        
        # Step 2: Agent Reasoning & Decision Making (LLM Call)
        prompt = f"""
        You are an autonomous supply chain agent. 
        Product: {item['product_name']}
        Current Stock: {item['current_stock']} units
        Daily Demand: {item['daily_demand']} units/day
        Supplier Lead Time: {item['lead_time_days']} days
        Calculated Days Until Stockout: {analysis['days_until_stockout']}
        Is Stockout Imminent: {analysis['is_at_risk']}

        As an AI agent, analyze this situation. If a stockout is imminent, generate a professional, step-by-step reasoning chain and a final procurement recommendation specifying how many units to reorder from {item['supplier']}. If stable, state why no action is needed.
        """

        print("   🤖 Agent is reasoning...")
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        print("\n--- Agent Execution Output ---")
        print(response.text)
        print("-" * 42 + "\n")

if __name__ == "__main__":
    run_supply_chain_agent()
