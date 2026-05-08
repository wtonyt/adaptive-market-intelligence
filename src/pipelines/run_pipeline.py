import subprocess


def run_pipeline():
    try:
        # Run full pipeline in order
        subprocess.run(["python", "src/ingestion/market_data.py"], check=True)
        subprocess.run(["python", "src/features/bronze.py"], check=True)
        subprocess.run(["python", "src/features/silver.py"], check=True)
        subprocess.run(["python", "src/features/gold.py"], check=True)
        subprocess.run(["python", "src/models/train.py"], check=True)

        return {"status": "success"}

    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": str(e)}
