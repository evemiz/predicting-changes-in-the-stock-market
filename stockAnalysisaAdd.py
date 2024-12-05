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
    sp500_data = yf.download(ticker, start=date - pd.Timedelta(days=8), end=date + pd.Timedelta(days=8))
    
    # Ensure data index is in the correct date format
    sp500_data['Date'] = sp500_data.index.date

    # Get closing value for the specified date, the next day, and one week after
    closing_today = sp500_data.loc[sp500_data['Date'] == date, 'Close'].values
    closing_next_day = sp500_data.loc[sp500_data['Date'] == (date + pd.Timedelta(days=1)), 'Close'].values
    closing_next_week = sp500_data.loc[sp500_data['Date'] == (date + pd.Timedelta(days=7)), 'Close'].values
    
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

# Check for any missing values in the 'sp500_close_next_day' and 'sp500_close_next_week'
missing_next_day = df[df['sp500_close_next_day'].isna()]
missing_next_week = df[df['sp500_close_next_week'].isna()]
print(f"Missing next day data: {len(missing_next_day)}")
print(f"Missing next week data: {len(missing_next_week)}")

# Add columns for changes between today and the next day/week
df['Next_Day_Change'] = df['sp500_close_next_day'] - df['sp500_close_today']  # Difference between today and next day
df['Next_Week_Change'] = df['sp500_close_next_week'] - df['sp500_close_today']  # Difference between today and next week

# Add columns for status (increase, decrease, or no change)
df['Next_Day_Status'] = df['Next_Day_Change'].apply(
    lambda x: 'עלייה' if x > 0 else ('ירידה' if x < 0 else 'ללא שינוי')
)
df['Next_Week_Status'] = df['Next_Week_Change'].apply(
    lambda x: 'עלייה' if x > 0 else ('ירידה' if x < 0 else 'ללא שינוי')
)

# Save the updated DataFrame to a new CSV
df.to_csv('updated_data.csv', index=False)

print("הדאטהסט עודכן והישמר כ- updated_data.csv")




# קריאה של קובץ ה-CSV
df = pd.read_csv('updated_data.csv')

# שלב 1: יצירת תנאי "ירידה" בעמודות Next_Day_Status ו-Next_Week_Status
condition_status = (df['Next_Day_Status'] == 'ירידה') | (df['Next_Week_Status'] == 'ירידה')

# שלב 2: יצירת תנאי שהעמודות Economic Security, Joy, Trust, Optimism מכילות לפחות שלוש ערכים של 1
columns_to_check = ['Economic Security', 'Joy', 'Trust', 'Optimism']
condition_values = df[columns_to_check].eq(1).sum(axis=1) >= 3

# שלב 3: סינון השורות שעומדות בתנאים
final_condition = condition_status & condition_values

# הצגת מספר השורות שעומדות בתנאים
count = final_condition.sum()
print(f"מספר השורות בהן יש 'ירידה' בעמודות הסטטוס ולפחות שלוש עמודות עם ערך 1: {count}")



# שלב 1: יצירת תנאי "עלייה" בעמודות Next_Day_Status ו-Next_Week_Status
condition_status = (df['Next_Day_Status'] == 'עלייה') | (df['Next_Week_Status'] == 'עלייה')

# שלב 2: יצירת תנאי שהעמודות Fear, Anger, Despair, Uncertainty, Fear for the future מכילות לפחות שלוש ערכים של 1
columns_to_check = ['Fear', 'Anger', 'Despair', 'Uncertainty', 'Fear for the future']
condition_values = df[columns_to_check].eq(1).sum(axis=1) >= 3

# שלב 3: סינון השורות שעומדות בתנאים
final_condition = condition_status & condition_values

# הצגת מספר השורות שעומדות בתנאים
count = final_condition.sum()
print(f"מספר השורות בהן יש 'עלייה' בעמודות הסטטוס ולפחות שלוש עמודות עם ערך 1: {count}")