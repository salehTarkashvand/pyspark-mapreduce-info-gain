import pandas as pd
import matplotlib.pyplot as plt
import os

def main():

    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'results_table.csv')
    
    if not os.path.exists(csv_path):
        print("Error: CSV file not found. Run analyze_results.py first.")
        return
        
    df = pd.read_csv(csv_path)
    

    plt.figure(figsize=(10, 6))
    plt.plot(df['Scenario'], df['Time (Seconds)'], marker='o', linestyle='-', color='b', linewidth=2)
    
    plt.title('Execution Time per Scenario')
    plt.xlabel('Scenario Number')
    plt.ylabel('Time (Seconds)')
    plt.xticks(df['Scenario'])
    plt.grid(True, linestyle='--', alpha=0.7)
    

    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output', 'execution_time_chart.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to: {output_path}")
    
    plt.show()

if __name__ == "__main__":
    main()