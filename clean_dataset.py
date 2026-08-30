import pandas as pd
import unicodedata

df = pd.read_csv("./database/downloads/shootouts.csv")

def remove_accents(text):
    if not isinstance(text, str):
        return text
    
    # Strip standard accents
    nfkd = unicodedata.normalize('NFKD', text)
    ascii_text = "".join([c for c in nfkd if not unicodedata.combining(c)])
    
    # Force strict ASCII formatting, dropping stubborn letters like 'Đ'
    return ascii_text.encode('ascii', 'ignore').decode('ascii')

# Include 'str' to silence the Pandas warning
for col in df.select_dtypes(include=['object', 'str']).columns:
    df[col] = df[col].apply(remove_accents)

# Save to your database folder
df.to_csv("./database/shootouts_clean.csv", index=False, encoding='ascii')
print("Dataset strictly cleaned and saved locally!")