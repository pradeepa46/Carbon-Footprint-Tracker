export interface User {
  id: string;
  email: string;
  full_name: string;
  region: string;
  created_at: string;
}

export interface EmissionEntry {
  id: string;
  user_id: string;
  category: 'transport' | 'energy' | 'food';
  subcategory: string;
  quantity: number;
  unit: string;
  co2_equivalent: number;
  date: string;
  notes?: string;
  created_at: string;
}

export interface UserProfile {
  user: User;
  household_size: number;
  vehicle_type: string;
  energy_source: string;
}

export interface EmissionBreakdown {
  transport: number;
  energy: number;
  food: number;
  total: number;
}

export interface EmissionBreakdownResponse {
  period: string;
  year: number;
  month: number;
  summary: {
    total_co2_kg: number;
    daily_average: number;
    trend: number;
  };
  breakdown: EmissionBreakdown;
  entries: EmissionEntry[];
}

export interface Recommendation {
  id: string;
  category: string;
  action: string;
  description: string;
  potential_savings: number;
  priority: 'high' | 'medium' | 'low';
  difficulty: 'easy' | 'medium' | 'hard';
}

export interface RecommendationsResponse {
  recommendations: Recommendation[];
  total_potential_savings: number;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  user_id: string;
}

export interface TransportEntry {
  subcategory: 'car' | 'electric_car' | 'bus' | 'train' | 'flight' | 'motorcycle';
  quantity: number;
  date: string;
}

export interface EnergyEntry {
  subcategory: 'electricity' | 'natural_gas' | 'heating_oil';
  quantity: number;
  date: string;
}

export interface FoodEntry {
  subcategory: 'beef' | 'pork' | 'chicken' | 'fish' | 'dairy' | 'plant_based';
  quantity: number;
  date: string;
}
