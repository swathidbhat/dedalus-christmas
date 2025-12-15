"""Christmas Gift Finder - Sonar MCP Test"""
import csv
import json
import asyncio
from pathlib import Path
from dedalus_labs import AsyncDedalus, DedalusRunner
from dotenv import load_dotenv

load_dotenv()

client = AsyncDedalus()
runner = DedalusRunner(client)

SEARCH_MCP = "akakak/sonar"
INPUT_CSV = Path(__file__).parent / "Name,Gift Idea,Budget.csv"
OUTPUT_CSV = Path(__file__).parent / "results.csv"


async def search_best_deal(gift: str, budget: float) -> dict:
    """Search for best price using Perplexity Sonar MCP."""
    print(f"  🔍 Searching for: {gift} (budget: ${budget})")
    
    try:
        response = await runner.run(
            input=f"""Search for the best deal to buy "{gift}" online under ${budget}.
            Find a real product with actual price and purchase link.
            Return ONLY a JSON object in this exact format:
            {{"price": 29.99, "link": "https://...", "product_name": "Full Product Name"}}
            No explanation, just the JSON.""",
            model="openai/gpt-4o-mini",
            mcp_servers=[SEARCH_MCP]
        )
        
        text = response.final_output.strip()
        print(f"  📦 Raw response: {text[:150]}...")
        
        # Parse JSON from response
        if "```" in text:
            text = text.split("```")[1].replace("json", "").strip()
        
        # Find JSON object in response
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            text = text[start:end]
        
        result = json.loads(text)
        print(f"  ✅ Found: {result.get('product_name', 'Unknown')} - ${result.get('price', 'N/A')}")
        return result
        
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return {"price": "N/A", "link": "", "product_name": gift, "error": str(e)}


async def generate_riddle(gift: str, name: str) -> str:
    """Generate a Christmas riddle for the gift."""
    try:
        response = await runner.run(
            input=f"""Write a 4-line Christmas riddle for {name} about their gift "{gift}".
            Hint at what the gift is WITHOUT saying it directly.
            Make it festive and fun. Return ONLY the riddle, no intro.""",
            model="openai/gpt-4o-mini"
        )
        return response.final_output.strip()
    except Exception as e:
        return f"A special gift awaits for you, {name}!"


async def process_gifts():
    """Process all gifts from CSV and output results."""
    print(f"\n🎄 Christmas Gift Finder 🎄")
    print(f"Reading from: {INPUT_CSV}")
    
    # Read input CSV
    gifts = []
    with open(INPUT_CSV, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Name'):  # Skip empty rows
                gifts.append(row)
    
    print(f"Found {len(gifts)} recipients\n")
    
    # Process each gift
    results = []
    for i, gift in enumerate(gifts):
        name = gift['Name']
        gift_idea = gift['Gift Idea']
        budget = float(gift['Budget'])
        
        print(f"[{i+1}/{len(gifts)}] Processing {name}...")
        
        # Search for best deal
        deal = await search_best_deal(gift_idea, budget)
        
        # Generate riddle
        riddle = await generate_riddle(gift_idea, name)
        
        results.append({
            'Name': name,
            'Gift Idea': gift_idea,
            'Budget': budget,
            'Product Found': deal.get('product_name', gift_idea),
            'Price': deal.get('price', 'N/A'),
            'Link': deal.get('link', ''),
            'Riddle': riddle.replace('\n', ' | ')
        })
        
        print()
    
    # Write output CSV
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    
    print(f"✨ Results saved to: {OUTPUT_CSV}")
    print(f"Processed {len(results)} gifts!")


async def test_single():
    """Test with just one gift first."""
    print("\n🧪 Testing Sonar MCP with single gift...\n")
    
    result = await search_best_deal("Noise-cancelling headphones", 100)
    print(f"\nFull result: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        asyncio.run(test_single())
    else:
        asyncio.run(process_gifts())
