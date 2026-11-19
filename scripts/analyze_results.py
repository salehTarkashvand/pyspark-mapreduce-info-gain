import pickle
import pandas as pd
import os

def main():
    # مسیر فایل نتایج
    results_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'results.pkl')
    
    if not os.path.exists(results_path):
        print(f"Error: File {results_path} not found. Please run run_experiments.py first.")
        return
        
    with open(results_path, 'rb') as f:
        results = pickle.load(f)
    
    # ساخت جدول
    df = pd.DataFrame([{
        'Scenario': r['scenario'],
        'Map Tasks': r['num_map'],
        'Reduce Tasks': r['num_reduce'],
        'Chunk Size (TB)': r['chunk_size_tb'],
        'Time (Seconds)': r['time_seconds']
    } for r in results])
    
    print("\n=== Execution Times Table ===")
    print(df.to_string(index=False))
    
    # ذخیره در فایل CSV
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'results_table.csv')
    df.to_csv(csv_path, index=False)
    print(f"\nTable saved to: {csv_path}")
    
    # نمایش ویژگی‌های برتر
    print("\n=== Top 10 Features (Last Scenario) ===")
    for feat, score in results[-1]['top_100'][:10]:
        print(f"  - {feat}: {score:.4f}")

if __name__ == "__main__":
    main()