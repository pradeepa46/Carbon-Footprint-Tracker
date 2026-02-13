"""
Recommendation engine for carbon footprint reduction.
Provides personalized suggestions based on user's emission patterns.
"""

from typing import List, Dict, Tuple
from sqlmodel import Session, select
from app.models import EmissionEntry
from uuid import UUID
from datetime import datetime, timedelta

# Recommendation rules: (condition_function, action, savings, priority, difficulty)
RECOMMENDATIONS = [
    {
        "id": "transit_switch",
        "category": "transport",
        "action": "Switch 2 car trips/week to public transit",
        "description": "Using buses or trains instead of driving reduces your emissions significantly",
        "savings": 1.5,  # kg CO2 per week
        "priority": "high",
        "difficulty": "easy",
        "condition": lambda user_transport: user_transport > 40  # kg/month
    },
    {
        "id": "carpool",
        "category": "transport",
        "action": "Try carpooling for 1 trip per week",
        "description": "Sharing rides reduces per-person emissions",
        "savings": 0.8,  # kg CO2 per week
        "priority": "medium",
        "difficulty": "medium",
        "condition": lambda user_transport: user_transport > 30  # kg/month
    },
    {
        "id": "electric_vehicle",
        "category": "transport",
        "action": "Consider an electric vehicle for your next car",
        "description": "Electric cars produce 60% less emissions than petrol cars",
        "savings": 10.0,  # kg CO2 per week estimate
        "priority": "high",
        "difficulty": "hard",
        "condition": lambda user_transport: user_transport > 50  # kg/month
    },
    {
        "id": "reduce_flights",
        "category": "transport",
        "action": "Reduce flights by 1-2 per year",
        "description": "Flying is the highest-emission activity. Consider alternatives or fewer trips",
        "savings": 200.0,  # kg CO2 per flight avoided
        "priority": "high",
        "difficulty": "hard",
        "condition": lambda user_transport: user_transport > 100  # Very high transport emissions
    },
    {
        "id": "thermostat_adjust",
        "category": "energy",
        "action": "Reduce heating/cooling by 2°C",
        "description": "Small temperature adjustments can significantly reduce energy use",
        "savings": 2.3,  # kg CO2 per week
        "priority": "medium",
        "difficulty": "easy",
        "condition": lambda user_energy: user_energy > 400  # kWh/month
    },
    {
        "id": "led_lighting",
        "category": "energy",
        "action": "Switch to LED lighting throughout your home",
        "description": "LEDs use 75% less energy than incandescent bulbs",
        "savings": 1.5,  # kg CO2 per week
        "priority": "medium",
        "difficulty": "easy",
        "condition": lambda user_energy: user_energy > 300  # kWh/month
    },
    {
        "id": "renewable_energy",
        "category": "energy",
        "action": "Switch to renewable energy provider",
        "description": "Your utility may offer renewable energy plans",
        "savings": 5.0,  # kg CO2 per week (depends on grid mix)
        "priority": "high",
        "difficulty": "medium",
        "condition": lambda user_energy: user_energy > 200  # kWh/month
    },
    {
        "id": "beef_reduction",
        "category": "food",
        "action": "Replace 1 beef meal/week with chicken",
        "description": "Beef has 10x higher emissions than chicken",
        "savings": 1.2,  # kg CO2 per week
        "priority": "high",
        "difficulty": "easy",
        "condition": lambda user_food: user_food > 50  # kg/month (high meat consumption)
    },
    {
        "id": "meatless_monday",
        "category": "food",
        "action": "Adopt one meatless day per week",
        "description": "Plant-based meals have 5-10x lower emissions than meat",
        "savings": 4.0,  # kg CO2 per week
        "priority": "high",
        "difficulty": "medium",
        "condition": lambda user_food: user_food > 40  # kg/month
    },
    {
        "id": "vegan_transition",
        "category": "food",
        "action": "Try a vegan diet",
        "description": "Plant-based eating has the lowest carbon footprint",
        "savings": 20.0,  # kg CO2 per week estimate
        "priority": "high",
        "difficulty": "hard",
        "condition": lambda user_food: user_food > 100  # kg/month
    },
    {
        "id": "local_food",
        "category": "food",
        "action": "Buy local, seasonal produce",
        "description": "Reduces transportation and storage emissions",
        "savings": 0.5,  # kg CO2 per week
        "priority": "low",
        "difficulty": "easy",
        "condition": lambda user_food: user_food > 30  # kg/month
    },
]

def get_recommendations(
    session: Session,
    user_id: UUID,
    limit: int = 5
) -> Tuple[List[Dict], float]:
    """
    Generate personalized recommendations based on user's emission history.
    
    Args:
        session: Database session
        user_id: User ID
        limit: Maximum number of recommendations to return
    
    Returns:
        Tuple of (list of recommendations, total potential savings in kg CO2/week)
    """
    
    # Get last 30 days of emissions for user
    thirty_days_ago = (datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    query = select(EmissionEntry).where(
        (EmissionEntry.user_id == user_id) &
        (EmissionEntry.date >= thirty_days_ago)
    )
    entries = session.exec(query).all()
    
    # Calculate totals by category
    category_totals = {
        "transport": 0,
        "energy": 0,
        "food": 0
    }
    
    for entry in entries:
        if entry.category in category_totals:
            category_totals[entry.category] += entry.co2_equivalent
    
    # Evaluate recommendations
    applicable_recommendations = []
    
    for rec in RECOMMENDATIONS:
        try:
            if rec["category"] == "transport":
                if rec["condition"](category_totals["transport"]):
                    applicable_recommendations.append(rec)
            elif rec["category"] == "energy":
                if rec["condition"](category_totals["energy"]):
                    applicable_recommendations.append(rec)
            elif rec["category"] == "food":
                if rec["condition"](category_totals["food"]):
                    applicable_recommendations.append(rec)
        except (TypeError, ValueError):
            # Skip if condition evaluation fails
            continue
    
    # Sort by priority (high > medium > low) then by savings
    priority_order = {"high": 0, "medium": 1, "low": 2}
    applicable_recommendations.sort(
        key=lambda x: (
            priority_order.get(x["priority"], 3),
            -x["savings"]
        )
    )
    
    # Limit results
    recommendations = applicable_recommendations[:limit]
    
    # Calculate total potential savings
    total_savings = sum(rec["savings"] for rec in recommendations)
    
    return recommendations, total_savings

def get_all_recommendations(limit: int = 10) -> List[Dict]:
    """Get all available recommendations (for reference)."""
    sorted_recs = sorted(
        RECOMMENDATIONS,
        key=lambda x: (-EMISSION_FACTORS.get(x["category"], {}).get(x["id"], 0), x["id"])
    )
    return sorted_recs[:limit]

EMISSION_FACTORS = {
    "transport": {"transit_switch": 1.5, "carpool": 0.8, "electric_vehicle": 10.0, "reduce_flights": 200.0},
    "energy": {"thermostat_adjust": 2.3, "led_lighting": 1.5, "renewable_energy": 5.0},
    "food": {"beef_reduction": 1.2, "meatless_monday": 4.0, "vegan_transition": 20.0, "local_food": 0.5},
}
