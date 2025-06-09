import pandas as pd

# Load both datasets
df_fake = pd.read_csv(r"C:\Users\shama\OneDrive\Desktop\scam intern detect\fake_internship_dataset.csv")
df_real = pd.read_csv(r"C:\Users\shama\OneDrive\Desktop\scam intern detect\real_internship_dataset.csv")

# Combine
df_combined = pd.concat([df_fake, df_real], ignore_index=True)

# Shuffle the dataset (important!)
df_combined = df_combined.sample(frac=1).reset_index(drop=True)

# Save combined dataset
df_combined.to_csv("combined_internship_dataset.csv", index=False)

print("✅ Combined dataset saved as combined_internship_dataset.csv")
