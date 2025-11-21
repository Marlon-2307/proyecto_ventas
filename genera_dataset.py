import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

# Ruta donde se guardará
base = "."
data_dir = os.path.join(base, "data")
os.makedirs(data_dir, exist_ok=True)
out_path = os.path.join(data_dir, "ventas.csv")

# Cantidad de registros
n = 2500

start_date = datetime(2018,1,1)
end_date = datetime(2022,12,31)
days_range = (end_date - start_date).days

regions = ['East', 'West', 'Central', 'South']
categories = ['Furniture', 'Office Supplies', 'Technology']
subcats = {
    'Furniture': ['Bookcases','Chairs','Tables','Furnishings'],
    'Office Supplies': ['Paper','Binders','Storage','Art'],
    'Technology': ['Phones','Accessories','Copiers','Computers']
}
segments = ['Consumer', 'Corporate', 'Home Office']

rows = []
for i in range(n):
    order_date = start_date + timedelta(days=random.randint(0, days_range))
    category = random.choice(categories)
    subcat = random.choice(subcats[category])

    quantity = random.randint(1, 5)
    unit_price = round(abs(np.random.normal(100, 40)), 2)
    discount = round(random.choice([0,0,0.1,0.15,0.2,0.3]), 2)
    sales = round(unit_price * quantity * (1 - discount), 2)
    profit = round(sales * (0.2 + np.random.normal(0, 0.05)), 2)

    rows.append({
        "Order ID": f"ORD{i+1}",
        "Order Date": order_date.strftime("%Y-%m-%d"),
        "Region": random.choice(regions),
        "Category": category,
        "Sub-Category": subcat,
        "Segment": random.choice(segments),
        "Quantity": quantity,
        "Unit Price": unit_price,
        "Discount": discount,
        "Sales": sales,
        "Profit": profit
    })

df = pd.DataFrame(rows)
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Year"] = df["Order Date"].dt.year
df["Month"] = df["Order Date"].dt.month

df.to_csv(out_path, index=False)
print("Dataset generado en:", out_path)
print(df.head())
