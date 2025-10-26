import os
from tavily import TavilyClient

def calculate_budget(city: str, attractions: str, days: int = 1) -> str:
    """
    Calculate travel budget based on city, attractions and number of days, including tickets and public transport costs.
    
    Args:
        city: City name
        attractions: Attraction names (can be multiple attractions separated by commas)
        days: Number of travel days, default is 1 day
    
    Returns:
        String containing ticket and transport cost budget
    """
    # 1. Read API key from environment variables
    api_key = os.environ.get("TAVILY_API_KEY")
    if not api_key:
        return "Error: TAVILY_API_KEY environment variable not configured."

    # 2. Initialize Tavily client
    tavily = TavilyClient(api_key=api_key)
    
    try:
        # 3. Query attraction ticket prices
        ticket_query = f"{city} {attractions} ticket prices entrance fee cost"
        ticket_response = tavily.search(query=ticket_query, search_depth="basic", include_answer=True)
        
        # 4. Query public transport costs
        transport_query = f"{city} public transport cost metro bus day pass transport card prices"
        transport_response = tavily.search(query=transport_query, search_depth="basic", include_answer=True)
        
        # 5. Integrate budget information
        budget_info = []
        budget_info.append(f"=== {city} Travel Budget Calculation ({days} day{'s' if days > 1 else ''}) ===\n")
        
        # Ticket cost information
        if ticket_response.get("answer"):
            budget_info.append("🎫 Attraction Ticket Costs:")
            budget_info.append(ticket_response["answer"])
            budget_info.append("")
        else:
            # If no comprehensive answer, use search results
            ticket_results = []
            for result in ticket_response.get("results", [])[:3]:  # Take first 3 results
                ticket_results.append(f"- {result['title']}: {result['content'][:200]}...")
            
            if ticket_results:
                budget_info.append("🎫 Attraction Ticket Costs:")
                budget_info.extend(ticket_results)
                budget_info.append("")
        
        # Transport cost information
        if transport_response.get("answer"):
            budget_info.append("🚇 Public Transport Costs:")
            budget_info.append(transport_response["answer"])
            budget_info.append("")
        else:
            # If no comprehensive answer, use search results
            transport_results = []
            for result in transport_response.get("results", [])[:3]:  # Take first 3 results
                transport_results.append(f"- {result['title']}: {result['content'][:200]}...")
            
            if transport_results:
                budget_info.append("🚇 Public Transport Costs:")
                budget_info.extend(transport_results)
                budget_info.append("")
        
        # Add budget suggestions
        budget_info.append("💡 Budget Suggestions:")
        budget_info.append(f"- Recommend reserving sufficient ticket and transport costs for {days} day{'s' if days > 1 else ''} itinerary")
        budget_info.append("- Consider purchasing attraction combo tickets or transport day passes to save costs")
        budget_info.append("- Some attractions may offer student tickets, senior tickets and other discount policies")
        
        return "\n".join(budget_info)
        
    except Exception as e:
        return f"Error: Problem occurred while querying budget information - {e}"


def get_budget_summary(city: str, total_budget: float) -> str:
    """
    Provide budget allocation suggestions based on total budget
    
    Args:
        city: City name
        total_budget: Total budget amount (local currency)
    
    Returns:
        Budget allocation suggestion string
    """
    if total_budget <= 0:
        return "Error: Budget amount must be greater than 0"
    
    # Get currency information based on city
    currency_info = _get_currency_info(city)
    currency_symbol = currency_info["symbol"]
    currency_name = currency_info["name"]
    
    # Budget allocation ratios (can be adjusted based on different cities)
    transport_ratio = 0.2  # Transport 20%
    tickets_ratio = 0.3    # Tickets 30%
    food_ratio = 0.3       # Food 30%
    other_ratio = 0.2      # Other 20%
    
    transport_budget = total_budget * transport_ratio
    tickets_budget = total_budget * tickets_ratio
    food_budget = total_budget * food_ratio
    other_budget = total_budget * other_ratio
    
    summary = []
    summary.append(f"=== {city} Budget Allocation Suggestions (Total Budget: {currency_symbol}{total_budget:.0f} {currency_name}) ===\n")
    summary.append(f"🚇 Transport Costs: {currency_symbol}{transport_budget:.0f} ({transport_ratio*100:.0f}%)")
    summary.append(f"🎫 Ticket Costs: {currency_symbol}{tickets_budget:.0f} ({tickets_ratio*100:.0f}%)")
    summary.append(f"🍽️ Food Costs: {currency_symbol}{food_budget:.0f} ({food_ratio*100:.0f}%)")
    summary.append(f"🛍️ Other Costs: {currency_symbol}{other_budget:.0f} ({other_ratio*100:.0f}%)")
    summary.append("")
    summary.append("💡 Friendly Tips:")
    summary.append("- Above allocation is for reference only, can be adjusted based on personal preferences")
    summary.append("- Recommend reserving 10-20% emergency funds")
    summary.append("- Can save costs through group buying, coupons and other methods")
    
    return "\n".join(summary)


def _get_currency_info(city: str) -> dict:
    """
    Get local currency information based on city name
    
    Args:
        city: City name
    
    Returns:
        Dictionary containing currency symbol and name
    """
    # City to currency mapping
    city_currency_map = {
        # European cities - Euro
        "Granada": {"symbol": "€", "name": "Euro"},
        "Madrid": {"symbol": "€", "name": "Euro"},
        "Barcelona": {"symbol": "€", "name": "Euro"},
        "Valencia": {"symbol": "€", "name": "Euro"},
        "Seville": {"symbol": "€", "name": "Euro"},
        "Bilbao": {"symbol": "€", "name": "Euro"},
        "Zaragoza": {"symbol": "€", "name": "Euro"},
        "Malaga": {"symbol": "€", "name": "Euro"},
        "Murcia": {"symbol": "€", "name": "Euro"},
        "Palma": {"symbol": "€", "name": "Euro"},
        "Cordoba": {"symbol": "€", "name": "Euro"},
        "Alicante": {"symbol": "€", "name": "Euro"},
        "Toledo": {"symbol": "€", "name": "Euro"},
        "Salamanca": {"symbol": "€", "name": "Euro"},
        "Burgos": {"symbol": "€", "name": "Euro"},
        "Leon": {"symbol": "€", "name": "Euro"},
        "Valladolid": {"symbol": "€", "name": "Euro"},
        "Logrono": {"symbol": "€", "name": "Euro"},
        "Pamplona": {"symbol": "€", "name": "Euro"},
        "San Sebastian": {"symbol": "€", "name": "Euro"},
        "Vitoria": {"symbol": "€", "name": "Euro"},
        "Ronda": {"symbol": "€", "name": "Euro"},
        "Sevilla": {"symbol": "€", "name": "Euro"},
        
        # Other European cities
        "Paris": {"symbol": "€", "name": "Euro"},
        "Berlin": {"symbol": "€", "name": "Euro"},
        "Munich": {"symbol": "€", "name": "Euro"},
        "Amsterdam": {"symbol": "€", "name": "Euro"},
        "Brussels": {"symbol": "€", "name": "Euro"},
        "Rome": {"symbol": "€", "name": "Euro"},
        "Milan": {"symbol": "€", "name": "Euro"},
        
        # UK
        "London": {"symbol": "£", "name": "Pound"},
        
        # USA
        "New York": {"symbol": "$", "name": "Dollar"},
        "NYC": {"symbol": "$", "name": "Dollar"},
        "Los Angeles": {"symbol": "$", "name": "Dollar"},
        "LA": {"symbol": "$", "name": "Dollar"},
        "San Francisco": {"symbol": "$", "name": "Dollar"},
        "SF": {"symbol": "$", "name": "Dollar"},
        "Chicago": {"symbol": "$", "name": "Dollar"},
        "Washington": {"symbol": "$", "name": "Dollar"},
        "DC": {"symbol": "$", "name": "Dollar"},
        "Boston": {"symbol": "$", "name": "Dollar"},
        "Seattle": {"symbol": "$", "name": "Dollar"},
        "Miami": {"symbol": "$", "name": "Dollar"},
        "Las Vegas": {"symbol": "$", "name": "Dollar"},
        
        # Canada
        "Toronto": {"symbol": "C$", "name": "Canadian Dollar"},
        "Vancouver": {"symbol": "C$", "name": "Canadian Dollar"},
        
        # Australia
        "Sydney": {"symbol": "A$", "name": "Australian Dollar"},
        "Melbourne": {"symbol": "A$", "name": "Australian Dollar"},
        "Brisbane": {"symbol": "A$", "name": "Australian Dollar"},
        
        # Japan
        "Tokyo": {"symbol": "¥", "name": "Yen"},
        
        # South Korea
        "Seoul": {"symbol": "₩", "name": "Won"},
        
        # Singapore
        "Singapore": {"symbol": "S$", "name": "Singapore Dollar"},
        
        # Malaysia
        "Kuala Lumpur": {"symbol": "RM", "name": "Ringgit"},
        "KL": {"symbol": "RM", "name": "Ringgit"},
        
        # Thailand
        "Bangkok": {"symbol": "฿", "name": "Baht"},
        
        # Russia
        "Moscow": {"symbol": "₽", "name": "Ruble"},
        "Saint Petersburg": {"symbol": "₽", "name": "Ruble"},
        
        # UAE
        "Dubai": {"symbol": "AED", "name": "Dirham"},
        
        # Chinese cities - RMB
        "Beijing": {"symbol": "¥", "name": "RMB"},
        "Shanghai": {"symbol": "¥", "name": "RMB"},
        "Guangzhou": {"symbol": "¥", "name": "RMB"},
        "Shenzhen": {"symbol": "¥", "name": "RMB"},
        "Hangzhou": {"symbol": "¥", "name": "RMB"},
        "Nanjing": {"symbol": "¥", "name": "RMB"},
        "Suzhou": {"symbol": "¥", "name": "RMB"},
        "Chengdu": {"symbol": "¥", "name": "RMB"},
        "Chongqing": {"symbol": "¥", "name": "RMB"},
        "Xian": {"symbol": "¥", "name": "RMB"},
        "Wuhan": {"symbol": "¥", "name": "RMB"},
        "Tianjin": {"symbol": "¥", "name": "RMB"},
        
        # Hong Kong, Macau, Taiwan
        "Hong Kong": {"symbol": "HK$", "name": "Hong Kong Dollar"},
        "HK": {"symbol": "HK$", "name": "Hong Kong Dollar"},
        "Macau": {"symbol": "MOP", "name": "Pataca"},
        "Macao": {"symbol": "MOP", "name": "Pataca"},
        "Taipei": {"symbol": "NT$", "name": "New Taiwan Dollar"},
    }
    
    # Find currency information corresponding to the city
    if city in city_currency_map:
        return city_currency_map[city]
    
    # If specific city not found, try to infer country/region based on city name
    city_lower = city.lower()
    
    # Spanish cities general matching
    spanish_keywords = ["spain", "spanish"]
    if any(keyword in city_lower for keyword in spanish_keywords):
        return {"symbol": "€", "name": "Euro"}
    
    # Other European countries
    european_keywords = ["france", "germany", "italy", "netherlands", "belgium", "austria", "portugal"]
    if any(keyword in city_lower for keyword in european_keywords):
        return {"symbol": "€", "name": "Euro"}
    
    # USA
    us_keywords = ["usa", "united states", "america"]
    if any(keyword in city_lower for keyword in us_keywords):
        return {"symbol": "$", "name": "Dollar"}
    
    # UK
    uk_keywords = ["uk", "united kingdom", "britain", "england"]
    if any(keyword in city_lower for keyword in uk_keywords):
        return {"symbol": "£", "name": "Pound"}
    
    # Default return Euro (since most queries might be European cities)
    return {"symbol": "€", "name": "Euro"}