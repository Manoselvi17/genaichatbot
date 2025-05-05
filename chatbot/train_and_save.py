from model import load_and_prepare_data, build_and_save_model

print("🔍 Starting training...")

df = load_and_prepare_data("traveldetail.csv")
print("📊 Data loaded!")

build_and_save_model(df)
print("✅ Model and scaler saved successfully!")
