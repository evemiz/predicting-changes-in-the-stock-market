import pandas as pd
from datetime import timedelta
import yfinance as yf

# קריאה של קובץ ה-CSV
df = pd.read_csv('emotions_dataset.csv')

# Make sure the date column is a date and not datetime
df['date'] = pd.to_datetime(df['date']).dt.date

# Define the ticker symbol for the S&P 500 (SPY is an ETF tracking the S&P 500 index)
ticker = '^GSPC'

def get_sp500_closing_values(date):
    # Fetch data for the S&P 500 using yfinance
    sp500_data = yf.download(ticker, start=date - pd.Timedelta(days=7), end=date + pd.Timedelta(days=1))
    
    # Get closing value for the specified date, the next day, and one week after
    closing_today = sp500_data.loc[sp500_data.index.date == date, 'Close'].values
    closing_next_day = sp500_data.loc[sp500_data.index.date == (date + pd.Timedelta(days=1)), 'Close'].values
    closing_next_week = sp500_data.loc[sp500_data.index.date == (date + pd.Timedelta(days=7)), 'Close'].values
    
    # Return closing values or None if they are not available
    return {
        'sp500_close_today': closing_today[0] if len(closing_today) > 0 else None,
        'sp500_close_next_day': closing_next_day[0] if len(closing_next_day) > 0 else None,
        'sp500_close_next_week': closing_next_week[0] if len(closing_next_week) > 0 else None
    }


# Apply the function to each date in the DataFrame and create new columns
sp500_values = df['date'].apply(get_sp500_closing_values)
print(df.head())

# Convert the dictionary columns to separate columns in the DataFrame
df = pd.concat([df, pd.DataFrame(sp500_values.tolist())], axis=1)

# Display the DataFrame
print(df)


# הוספת עמודות לשינויים ליום אחרי ושבוע אחרי
df['Next_Day_Change'] = df['sp500_close_next_day'] - df['sp500_close_today']  # מחשבים את ההפרש בין סגירת היום ליום אחרי
df['Next_Week_Change'] = df['sp500_close_next_week'] - df['sp500_close_today']  # מחשבים את ההפרש בין סגירת היום לשבוע אחרי

# הוספת עמודות לסטטוס (עלייה או ירידה)
df['Next_Day_Status'] = df['Next_Day_Change'].apply(
    lambda x: 'עלייה' if x > 0 else ('ירידה' if x < 0 else 'ללא שינוי')
)
df['Next_Week_Status'] = df['Next_Week_Change'].apply(
    lambda x: 'עלייה' if x > 0 else ('ירידה' if x < 0 else 'ללא שינוי')
)

# שמירת הדאטהסט החדש לקובץ CSV
df.to_csv('updated_data.csv', index=False)

print("הדאטהסט עודכן והישמר כ- updated_data.csv")
