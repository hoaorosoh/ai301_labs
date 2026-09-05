import pandas as pd

def clean_text_columns(df):
    """
    Cleans string/object columns to prevent SQL import errors by:
    1. Removing newlines, carriage returns, and tabs.
    2. Removing hidden/invisible zero-width characters.
    3. Stripping leading and trailing whitespaces.
    """
    str_cols = df.select_dtypes(include=['object', 'string']).columns
    for col in str_cols:
        # Replace newlines, carriage returns, and tabs with a single space
        df[col] = df[col].str.replace(r'[\r\n\t]+', ' ', regex=True)
        # Remove zero-width spaces and byte order marks (invisible weird characters)
        df[col] = df[col].str.replace(r'[\u200B-\u200D\uFEFF]', '', regex=True)
        # Strip trailing and leading whitespace
        df[col] = df[col].str.strip()
    return df

def clean_football_data():
    # -----------------------------------------
    # 1. Clean results.csv
    # -----------------------------------------
    print("Cleaning results.csv...")
    df_results = pd.read_csv("database/downloads/results.csv")
    
    # Clean weird characters from text columns
    df_results = clean_text_columns(df_results)
    
    # Format date for SQL (YYYY-MM-DD)
    df_results['date'] = pd.to_datetime(df_results['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    
    # Ensure scores are integers (fill any missing scores with 0 before converting)
    df_results['home_score'] = pd.to_numeric(df_results['home_score'], errors='coerce').fillna(0).astype(int)
    df_results['away_score'] = pd.to_numeric(df_results['away_score'], errors='coerce').fillna(0).astype(int)
    
    # Convert True/False 'neutral' column to 1/0 for SQL compatibility
    if 'neutral' in df_results.columns:
        df_results['neutral'] = df_results['neutral'].astype(int, errors='ignore')
        
    df_results.to_csv("database/results_cleaned.csv", index=False, na_rep='NULL')

    # -----------------------------------------
    # 2. Clean shootouts.csv
    # -----------------------------------------
    print("Cleaning shootouts.csv...")
    df_shootouts = pd.read_csv("database/downloads/shootouts.csv")
    
    # Clean weird characters
    df_shootouts = clean_text_columns(df_shootouts)
    
    df_shootouts['date'] = pd.to_datetime(df_shootouts['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    
    # Fill missing string values with 'Unknown' to prevent SQL import errors
    df_shootouts.fillna({'winner': 'Unknown', 'first_shooter': 'Unknown'}, inplace=True)
    
    df_shootouts.to_csv("database/shootouts_cleaned.csv", index=False, na_rep='NULL')

    # -----------------------------------------
    # 3. Clean goalscorers.csv
    # -----------------------------------------
    print("Cleaning goalscorers.csv...")
    df_goals = pd.read_csv("database/downloads/goalscorers.csv")
    
    # Clean weird characters
    df_goals = clean_text_columns(df_goals)
    
    df_goals['date'] = pd.to_datetime(df_goals['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    
    # Convert True/False columns to 1/0 for SQL
    if 'own_goal' in df_goals.columns:
        df_goals['own_goal'] = df_goals['own_goal'].fillna(False).astype(int, errors='ignore')
    if 'penalty' in df_goals.columns:
        df_goals['penalty'] = df_goals['penalty'].fillna(False).astype(int, errors='ignore')
        
    df_goals.to_csv("database/goalscorers_cleaned.csv", index=False, na_rep='NULL')

    # -----------------------------------------
    # 4. Clean former_names.csv
    # -----------------------------------------
    print("Cleaning former_names.csv...")
    df_former = pd.read_csv("database/downloads/former_names.csv")
    
    # Clean weird characters
    df_former = clean_text_columns(df_former)
    
    # Format start and end dates
    df_former['start_date'] = pd.to_datetime(df_former['start_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    df_former['end_date'] = pd.to_datetime(df_former['end_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    
    df_former.to_csv("database/former_names_cleaned.csv", index=False, na_rep='NULL')
    
    print("Data cleaning complete! The _cleaned.csv files are ready to be imported into SQL Workbench.")

if __name__ == "__main__":
    clean_football_data()