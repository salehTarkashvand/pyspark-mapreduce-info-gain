بفرمایید. این هم کل متن فایل `README.md` به صورت یکجا. فقط کافی است کل این کد را کپی کنید و در فایل `README.md` قرار دهید.

```markdown
# PySpark MapReduce: Information Gain for Feature Selection

This project implements a distributed feature selection algorithm using the **MapReduce** paradigm with **Apache Spark (PySpark)**. It calculates the **Information Gain (IG)** score for features in the EMBER 2018 dataset to identify the most predictive features for malware detection.

## 📌 Project Overview

The goal is to compute the Information Gain for hundreds of features across a large dataset. Since the dataset is large, the computation is distributed across multiple Map tasks. 
- **Map Phase:** Each Mapper calculates a local contingency table (counts of feature values vs. labels).
- **Reduce Phase:** The Reducers aggregate these local counts.
- **Final Step:** The Information Gain is computed from the globally aggregated contingency table.

## 📂 Repository Structure

```text
ember-mapreduce/
├── data/                   # Place the EMBER parquet files here
│   ├── test_ember_2018_v2_features.parquet
│   └── train_ember_2018_v2_features.parquet
├── output/                 # Generated results, tables, and charts
├── scripts/
│   ├── load_data.py        # Loads local parquet files
│   ├── mapreduce_ig.py     # Core MapReduce and IG logic
│   ├── run_experiments.py  # Runs the 10 scenarios (Map/Reduce/Chunk sizes)
│   ├── analyze_results.py  # Generates the CSV results table
│   └── plot_results.py     # Plots the execution time chart
├── environment.yml         # Conda environment setup
├── requirements.txt        # Python dependencies
└── README.md
```

## ⚙️ Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/pyspark-mapreduce-info-gain.git
   cd pyspark-mapreduce-info-gain
   ```

2. **Create and activate the Conda environment:**
   ```bash
   conda env create -f environment.yml
   conda activate ember_env
   ```

3. **Download the Dataset:**
   Download the EMBER 2018 v2 features dataset from Kaggle and place the `.parquet` files inside the `data/` directory.

## 🚀 Usage

1. **Run the MapReduce experiments:**
   ```bash
   cd scripts
   python run_experiments.py
   ```
   *This will run 10 different scenarios varying the number of Map tasks, Reduce tasks, and Chunk sizes.*

2. **Analyze the results:**
   ```bash
   python analyze_results.py
   ```
   *This generates a summary table and saves it as `output/results_table.csv`.*

3. **Generate the execution time chart:**
   ```bash
   python plot_results.py
   ```

## 📊 Results Summary

The experiments demonstrate the impact of parallelization in the Map phase. Increasing the number of Map tasks generally reduces execution time due to parallel processing. However, on a machine with limited RAM (e.g., 8GB), increasing the number of tasks beyond a certain threshold (e.g., >5) can lead to network buffer errors (`No buffer space available`), highlighting the trade-off between parallelism and hardware constraints.

## 🏗️ System Architecture

The following diagram illustrates the data flow and the MapReduce pipeline implemented in this project:

```mermaid
‍‍‍‍‍‍
graph TD
    %% Styling
    classDef data fill:#f9f9f9,stroke:#333,stroke-width:2px;
    classDef process fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef storage fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef output fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;

    %% Data Ingestion
    A[(EMBER 2018 Dataset\nParquet Files)]:::data -->|Load Data| B(Pandas DataFrame):::process
    B -->|Sample 10,000 rows| C(Python List of Dictionaries):::process
    C -->|sc.parallelize| D{RDD Partitioning}:::process

    %% MapReduce Phase
    D -->|Split by Map Tasks| E[Map Phase: Local Contingency\nFeature ID, Value Bin, Label]:::process
    E -->|Shuffle & Sort| F[Reduce Phase: Aggregate Counts\nSum of Frequencies]:::process

    %% Aggregation & Calculation
    F -->|Collect to Driver| G(Aggregated Contingency Table):::storage
    G -->|Calculate H(Y)| H[Global Label Entropy]:::process
    G -->|Calculate H(Y|X)| I[Conditional Entropy per Feature]:::process
    
    H --> J{Information Gain Calculation}:::process
    I --> J
    J -->|IG = H(Y) - H(Y|X)| K[Feature Ranking]:::process

    %% Output
    K --> L[Top 100 Features]:::output
    K --> M[Execution Time Metrics\nScenario 1 to 10]:::output
    L --> N[(output/results.pkl)]:::storage
    M --> N
    M --> O[(output/results_table.csv)]:::storage

##👨‍💻 Author
**Saleh Torkashvand** - *Master's Student in Artificial Intelligence*
