import csv
import math

# Simple ML Model — Decision Tree logic
class QueryOptimizer:
    def __init__(self):
        self.data    = []
        self.trained = False

    def load_data(self):
        with open("ml/query_data.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.data.append({
                    "query_type": int(row["query_type"]),
                    "table_size": int(row["table_size"]),
                    "has_where":  int(row["has_where"]),
                    "has_index":  int(row["has_index"]),
                    "exec_time":  float(row["exec_time"])
                })
        print(f"Loaded {len(self.data)} training records!")

    def train(self):
        self.load_data()

        # average execution time calculate karo
        # index hai vs nahi
        with_index    = [r["exec_time"] for r in self.data if r["has_index"] == 1]
        without_index = [r["exec_time"] for r in self.data if r["has_index"] == 0]

        self.avg_with_index    = sum(with_index) / len(with_index)
        self.avg_without_index = sum(without_index) / len(without_index)

        # table size threshold
        sizes     = [r["table_size"] for r in self.data]
        self.avg_size = sum(sizes) / len(sizes)

        self.trained = True
        print(f"\n--- Model Trained ---")
        print(f"Avg time with index    : {self.avg_with_index:.3f}ms")
        print(f"Avg time without index : {self.avg_without_index:.3f}ms")
        print(f"Avg table size         : {self.avg_size:.0f} rows")

    def predict(self, table_size, has_where, has_index):
        if not self.trained:
            print("Model train nahi hua!")
            return

        # recommendation
        print(f"\n--- Query Optimizer ---")
        print(f"Table size : {table_size}")
        print(f"Has WHERE  : {bool(has_where)}")
        print(f"Has Index  : {bool(has_index)}")

        if table_size > self.avg_size and has_where and not has_index:
            print("⚠️  Recommendation: INDEX banao — query slow hogi!")
            est_time = table_size * 0.01 * 1.5
        elif has_index:
            print("✅ Index hai — query fast rahegi!")
            est_time = table_size * 0.001
        else:
            print("ℹ️  Table chhoti hai — index zaroori nahi")
            est_time = table_size * 0.01

        print(f"Estimated time : {est_time:.3f}ms")

if __name__ == "__main__":
    from data_collector import DataCollector

    # data generate karo
    collector = DataCollector()
    collector.generate_training_data(500)

    # model train karo
    optimizer = QueryOptimizer()
    optimizer.train()

    # predictions karo
    print("\n--- Test Cases ---")
    optimizer.predict(table_size=5000, has_where=1, has_index=0)
    optimizer.predict(table_size=5000, has_where=1, has_index=1)
    optimizer.predict(table_size=100,  has_where=0, has_index=0)