"""
Carbon emission calculation service with standard emission factors.
All factors are global averages in kg CO2 equivalent.
"""

# Emission factors (kg CO2e per unit)
EMISSION_FACTORS = {
    "transport": {
        "car": 0.21,  # per km
        "electric_car": 0.08,  # per km
        "bus": 0.06,  # per km
        "train": 0.04,  # per km
        "flight": 0.25,  # per km
        "motorcycle": 0.09,  # per km
    },
    "energy": {
        "electricity": 0.385,  # per kWh (global average)
        "natural_gas": 0.20,  # per kWh
        "heating_oil": 0.268,  # per kWh
    },
    "food": {
        "beef": 27.0,  # per meal/serving
        "pork": 4.0,  # per meal/serving
        "chicken": 2.5,  # per meal/serving
        "fish": 3.5,  # per meal/serving
        "dairy": 5.0,  # per meal/serving (cheese, yogurt, milk)
        "plant_based": 1.0,  # per meal/serving (vegetarian/vegan)
    }
}

def calculate_emissions(
    category: str,
    subcategory: str,
    quantity: float,
    unit: str = None
) -> float:
    """
    Calculate CO2 emissions for a given activity.
    
    Args:
        category: "transport", "energy", or "food"
        subcategory: specific activity type
        quantity: amount of activity
        unit: optional unit (auto-detected from category if not provided)
    
    Returns:
        CO2 equivalent in kg
    """
    category_lower = category.lower()
    subcategory_lower = subcategory.lower()
    
    if category_lower not in EMISSION_FACTORS:
        raise ValueError(f"Unknown category: {category}")
    
    if subcategory_lower not in EMISSION_FACTORS[category_lower]:
        raise ValueError(f"Unknown subcategory: {subcategory} for {category}")
    
    # Get emission factor
    factor = EMISSION_FACTORS[category_lower][subcategory_lower]
    
    # Calculate CO2
    co2 = factor * quantity
    
    return round(co2, 2)

def get_available_subcategories(category: str) -> list:
    """Get list of available subcategories for a category."""
    category_lower = category.lower()
    if category_lower in EMISSION_FACTORS:
        return list(EMISSION_FACTORS[category_lower].keys())
    return []

def get_emission_factor(category: str, subcategory: str) -> float:
    """Get emission factor for a category/subcategory pair."""
    category_lower = category.lower()
    subcategory_lower = subcategory.lower()
    
    if category_lower in EMISSION_FACTORS:
        if subcategory_lower in EMISSION_FACTORS[category_lower]:
            return EMISSION_FACTORS[category_lower][subcategory_lower]
    
    return 0.0
