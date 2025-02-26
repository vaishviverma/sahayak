import pandas as pd
from prophet import Prophet
from .analysis import read_data

def sales_forecast():
    df = read_data()
    df_daily = df.groupby("Date")["Total"].sum().reset_index()
    df_daily.columns = ["ds", "y"]
    model = Prophet()
    model.fit(df_daily)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    forecast_dict = forecast[["ds", "yhat"]].tail(10).to_dict(orient="records")
    return forecast_dict

def predict_demand(product_line: str, date: str) -> int:
    
    filtered_data = df[(df["Product line"] == product_line)]
    demand_trends = filtered_data.groupby("Date")["Quantity"].sum().rolling(3).mean()

    target_date = pd.to_datetime(date)
    past_data = demand_trends[demand_trends.index <= target_date]
    
    return int(past_data.iloc[-1]) if not past_data.empty else 0