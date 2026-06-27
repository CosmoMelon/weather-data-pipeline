from extract import extract_weather_data
from transform import transform_data
from load import load_data

def run_pipeline():
    print("Starting Weather Data Pipeline...")
    raw_data = extract_weather_data()
    dim_city, fact_weather = transform_data(raw_data)
    load_data(dim_city, fact_weather)
    print("Pipeline execution finished successfully.")

if __name__ == "__main__":
    run_pipeline()