import pandas as pd

def read_data():
    df = pd.read_csv("./data_modified.csv")

    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')

    df = df.dropna(subset=["Date"])

    return df

def gross_income():
    
    df=read_data()
    df['Week'] = df['Date'].dt.isocalendar().week
    weekly_income = df.groupby("Week")["gross income"].sum().reset_index()

    percentage_change = (
        ((weekly_income["gross income"].iloc[-1] - weekly_income["gross income"].iloc[-2])
         / weekly_income["gross income"].iloc[-2]) * 100
        if len(weekly_income) > 1 else 0
    )

    return {
        "second": weekly_income["Week"].tolist(),
        "third": weekly_income["gross income"].tolist(),
        "first": weekly_income["gross income"].sum(),
        "fourth": round(percentage_change, 2),
    }



def total_sales():
    df=read_data()
    df["Week"] = df["Date"].dt.isocalendar().week
    weekly_sales = df.groupby("Week")["Total"].sum().reset_index()

    percentage_change = (
        ((weekly_sales["Total"].iloc[-1] - weekly_sales["Total"].iloc[-2])
         / weekly_sales["Total"].iloc[-2]) * 100
        if len(weekly_sales) > 1 else 0
    )

    return {
        "second": weekly_sales["Week"].tolist(),
        "third": weekly_sales["Total"].tolist(),
        "first": weekly_sales["Total"].sum(),
        "fourth": round(percentage_change, 2),
    }



def peak_hour():
    df=read_data()
    df["Week"] = df["Date"].dt.isocalendar().week
    
    weekly_gross_margin = df.groupby("Week")["Hour"].mean().reset_index()

    percentage_change = (
        ((weekly_gross_margin["Hour"].iloc[-1] - weekly_gross_margin["Hour"].iloc[-2])
         / weekly_gross_margin["Hour"].iloc[-2]) * 100
        if len(weekly_gross_margin) > 1 else 0
    )

    return {
        "second": weekly_gross_margin["Week"].tolist(),
        "third": weekly_gross_margin["Hour"].round(2).tolist(),
        "first": int(round(df["Hour"].mean(), 2)),
        "fourth": round(percentage_change, 2),
    }



def weekly_transactions():
    df = read_data()
    df["Week"] = df["Date"].dt.isocalendar().week

    weekly_transactions = df.groupby("Week")["Invoice ID"].nunique().reset_index()

    weeks = weekly_transactions["Week"].astype(int).tolist()
    total_transactions = weekly_transactions["Invoice ID"].astype(int).tolist()
    overall_total_transactions = sum(total_transactions)  
    percentage_change = (
        ((total_transactions[-1] - total_transactions[-2]) / total_transactions[-2]) * 100
        if len(total_transactions) > 1 else 0
    )

    return {
        "second": weeks,  
        "third": total_transactions,  
        "first": overall_total_transactions, 
        "fourth": round(percentage_change, 2), 
    }

def product_distribution(metric: str = "Total"):
    df = read_data()

    if metric not in ["Total", "Quantity"]:
        return {"error": "Invalid metric. Choose 'Total' or 'Quantity'."}

    distribution = df.groupby("Product line")[metric].sum().reset_index()
    distribution = distribution.sort_values(by=metric, ascending=False)

    top_3 = distribution.head(3).to_dict(orient="records")

    others_value = distribution[metric].iloc[3:].sum()
    if others_value > 0:
        top_3.append({"Product line": "Others", metric: others_value})

    formatted_data = [{"label": row["Product line"], "value": row[metric]} for row in top_3]
    return {"series": formatted_data}
    
# print(gross_income())
# print(weekly_transactions())
# print(weekly_gross_margin())
# print(total_sales())