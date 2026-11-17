from pyspark import SparkContext, SparkConf
import time
import pickle
import os
from load_data import get_dataset_path, find_data_file, load_subset
from mapreduce_ig import get_feature_names, run_mapreduce

def create_spark_context():
    """Create SparkContext with settings for 8GB RAM."""
    conf = SparkConf() \
        .setAppName("IG-MapReduce") \
        .setMaster("local[2]") \
        .set("spark.driver.memory", "3g") \
        .set("spark.executor.memory", "3g") \
        .set("spark.sql.shuffle.partitions", "2") \
        .set("spark.network.timeout", "800s") \
        .set("spark.executor.heartbeatInterval", "60s")
    return SparkContext(conf=conf)

def main():
    print("=== Step 1: Data Preparation ===")
    dataset_path = get_dataset_path()
    data_file = find_data_file(dataset_path)
    
    if not data_file:
        print("Error: Data file not found!")
        return
    
    # Load 10,000 records for 8GB RAM
    records = load_subset(data_file, max_rows=10000)
    if not records:
        print("Error: No records loaded. Exiting.")
        return
        
    feature_names = get_feature_names(records, max_features=500)
    print(f"Selected {len(feature_names)} features.")
    
    print("\n=== Step 2: Starting Spark ===")
    sc = create_spark_context()
    
    print("\n=== Step 3: Running Experiments ===")
    # Scenarios from the assignment table: (Map Tasks, Reduce Tasks, Chunk Size in TB)
    scenarios = [
        (1, 1, 0.1),
        (1, 1, 0.2),
        (1, 1, 0.5),
        (1, 1, 1.0),
        (3, 1, 1.0),
        (5, 1, 1.0),
        (3, 3, 1.0),
        (5, 3, 1.0),
        (3, 5, 1.0),
        (5, 5, 1.0),
    ]
    
    results = []
    for i, (num_map, num_reduce, chunk) in enumerate(scenarios):
        print(f"\n--- Scenario {i+1}: Map={num_map}, Reduce={num_reduce}, Chunk={chunk}TB ---")
        
        # Convert list of records to RDD with specified partitions (Map Tasks)
        data_rdd = sc.parallelize(records, numSlices=num_map)
        
        # Measure time
        start = time.time()
        ig_scores = run_mapreduce(data_rdd, feature_names)
        elapsed = time.time() - start
        
        # Sort and get top 100 features
        top_100 = sorted(ig_scores.items(), key=lambda x: x[1], reverse=True)[:100]
        
        results.append({
            'scenario': i + 1,
            'num_map': num_map,
            'num_reduce': num_reduce,
            'chunk_size_tb': chunk,
            'time_seconds': round(elapsed, 2),
            'top_100': top_100
        })
        
        print(f"Time elapsed: {elapsed:.2f} seconds")
        if top_100:
            print(f"Top feature: {top_100[0][0]} (IG = {top_100[0][1]:.4f})")
    
    print("\n=== Step 4: Saving Results ===")
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'results.pkl')
    
    with open(output_path, 'wb') as f:
        pickle.dump(results, f)
    print(f"Results saved to {output_path}")
    
    sc.stop()

if __name__ == "__main__":
    main()