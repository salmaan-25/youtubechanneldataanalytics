import pandas as pd

# Step 1: Load your existing CSV file
df = pd.read_csv('video_data(mrwhosetheboss).csv')  # Change filename if needed

# Step 2: Convert numeric-looking columns (with commas) into real numeric values
df['Views'] = df['Views'].astype(str).str.replace(',', '', regex=False).astype(float)
df['Likes'] = df['Likes'].astype(str).str.replace(',', '', regex=False).astype(float)
df['Dislikes'] = df['Dislikes'].astype(str).str.replace(',', '', regex=False).astype(float)
df['Comments'] = df['Comments'].astype(str).str.replace(',', '', regex=False).astype(float)

# Step 3: Save cleaned data back to a new CSV
df.to_csv('youtube_channel_data_clean.csv', index=False)

print("✅ Cleaned data saved to youtube_channel_data_clean.csv")
