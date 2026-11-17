import math
from collections import defaultdict

def get_feature_names(records, max_features=500):
    """Extract feature names (limit to 500 for 8GB RAM)."""
    if not records:
        return []
    # The parquet dataset might store features differently. 
    # We need to check the first record to see its structure.
    first_record = records[0]
    
    # Usually, EMBER parquet features are stored in a specific column
    # If it's a dictionary, we extract keys
    if 'features' in first_record and isinstance(first_record['features'], dict):
        features = list(first_record['features'].keys())
    else:
        # If features are flat columns, we exclude 'label' and 'sha256'
        features = [k for k in first_record.keys() if k not in ['label', 'sha256', 'appeared', 'weekofyear']]
        
    return features[:max_features]

def map_contingency(record, feature_names):
    """Map step: generate key-value pairs for each feature."""
    label = record.get('label', 0)
    features = record.get('features', record) # Fallback if features are flat
    
    output = []
    for fid, fname in enumerate(feature_names):
        value = features.get(fname, 0)
        # Simple discretization for float values
        if isinstance(value, float):
            value_bin = round(value * 10)
        else:
            value_bin = value
        output.append(((fid, value_bin, label), 1))
    return output

def reduce_contingency(count1, count2):
    """Reduce step: sum the counts."""
    return count1 + count2

def compute_information_gain(contingency_dict, feature_names):
    """Calculate Information Gain from aggregated contingency tables."""
    feature_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    label_totals = defaultdict(int)
    
    for (fid, val_bin, label), count in contingency_dict.items():
        feature_counts[fid][val_bin][label] += count
        label_totals[label] += count
    
    total_samples = sum(label_totals.values())
    if total_samples == 0:
        return {}
    
    # Calculate H(Y): Total Entropy
    h_y = 0.0
    for label, count in label_totals.items():
        p = count / total_samples
        if p > 0:
            h_y -= p * math.log2(p)
    
    # Calculate IG for each feature
    ig_scores = {}
    for fid, val_dist in feature_counts.items():
        h_y_given_x = 0.0
        for val_bin, label_counts in val_dist.items():
            val_total = sum(label_counts.values())
            p_val = val_total / total_samples
            
            h_bin = 0.0
            for label, count in label_counts.items():
                p_label = count / val_total
                if p_label > 0:
                    h_bin -= p_label * math.log2(p_label)
            
            h_y_given_x += p_val * h_bin
        
        ig = h_y - h_y_given_x
        if fid < len(feature_names):
            ig_scores[feature_names[fid]] = ig
    
    return ig_scores

def run_mapreduce(data_rdd, feature_names):
    """Run the full MapReduce pipeline."""
    # Map step
    mapped = data_rdd.flatMap(lambda rec: map_contingency(rec, feature_names))
    
    # Reduce step (aggregation)
    reduced = mapped.reduceByKey(reduce_contingency)
    
    # Collect results
    contingency_list = reduced.collect()
    contingency_dict = dict(contingency_list)
    
    # Calculate Information Gain
    ig_scores = compute_information_gain(contingency_dict, feature_names)
    return ig_scores