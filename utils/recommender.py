
import pandas as pd

def recommend_charts(df):
    recommendations = []
    for col in df.columns:
        dtype = df[col].dtype
        unique_vals = df[col].nunique()

        if pd.api.types.is_numeric_dtype(dtype):
            if unique_vals < 10:
                chart = "Bar Chart"
                reason = "Few unique numeric values — good for bar comparison."
            else:
                chart = "Histogram"
                reason = "Many numeric values — histogram shows distribution well."

        elif pd.api.types.is_datetime64_any_dtype(dtype):
            chart = "Line Chart"
            reason = "Datetime column — line chart shows trends over time."

        elif pd.api.types.is_object_dtype(dtype):
            if unique_vals < 10:
                chart = "Pie Chart"
                reason = "Categorical data with few categories — pie chart works."
            else:
                chart = "Bar Chart"
                reason = "Too many categories — bar chart is better than pie."

        else:
            chart = "Not sure"
            reason = "Unsupported data type"

        recommendations.append({
            "column": col,
            "recommended_chart": chart,
            "reason": reason
        })

    return recommendations
