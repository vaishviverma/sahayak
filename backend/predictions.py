import pandas as pd
from datacleaning import df
from prophet import Prophet


def sales_forecast():
    df_daily = df.groupby("Date")["Total"].sum().reset_index()
    df_daily.columns = ["ds", "y"]
    model = Prophet()
    model.fit(df_daily)
    future = model.make_future_dataframe(periods=30)
    forecast = model.predict(future)
    forecast_dict = forecast[["ds", "yhat"]].tail(10).to_dict(orient="records")
    return forecast_dict

def peak_sales_hours():
    
    hourly_sales = df.groupby("Hour")["Total"].sum().reset_index()
    peak_hours = hourly_sales.sort_values(by="Total", ascending=False).head(5)
    
    return peak_hours.to_dict(orient="records")

def product_performance():
    product_sales = df.groupby("Product line").agg({"Total": "sum", "Quantity": "sum"}).reset_index()
    
    top_products = product_sales.sort_values(by="Total", ascending=False).head(5)
    slow_products = product_sales.sort_values(by="Total", ascending=True).head(5)
    
    return {
        "top_products": top_products.to_dict(orient="records"),
        "slow_products": slow_products.to_dict(orient="records")
    }

product_analysis = product_performance()

peak_hours = peak_sales_hours()

forecast_sales = sales_forecast
