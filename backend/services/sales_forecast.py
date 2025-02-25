import random

def predict_sales(days: int):
    return [{"day": i, "predicted_sales": round(random.uniform(500, 1500), 2)} for i in range(1, days + 1)]
