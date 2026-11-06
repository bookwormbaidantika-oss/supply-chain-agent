def check_stockout_risk(item):
    stock = item["current_stock"]
    demand = item["daily_demand"]
    lead_time = item["lead_time_days"]
    
    # Calculate how many units will sell while waiting for a new shipment
    demand_during_lead_time = demand * lead_time
    days_until_stockout = stock / demand if demand > 0 else float('inf')
    
    # If current stock is less than what we need during delivery, it's at risk
    is_at_risk = stock < demand_during_lead_time
    
    return {
        "demand_during_lead_time": demand_during_lead_time,
        "days_until_stockout": round(days_until_stockout, 1),
        "is_at_risk": is_at_risk
    }
