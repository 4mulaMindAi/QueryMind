import random
import csv
import os

# Query execution ka data collect karna
class DataCollector:
    def __init__(self):
        self.data = []
        self.file = "ml/query_data.csv"

    def record(self, query_type, table_size, has_where, has_index, exec_time):
        row = {
            "query_type": query_type,  # 0=SELECT, 1=INSERT
            "table_size": table_size,  # kitni rows hain
            "has_where":  has_where,   # WHERE condition hai?
            "has_index":  has_index,   # index hai?
            "exec_time":  exec_time    # kitna time laga
        }
        self.data.append(row)

    def save(self):
        with open(self.file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "query_type", "table_size", 
                "has_where", "has_index", "exec_time"
            ])
            writer.writeheader()
            writer.writerows(self.data)
        print(f"Data saved — {len(self.data)} records!")

    # fake training data generate karo
    def generate_training_data(self, samples=500):
        for _ in range(samples):
            query_type = random.randint(0, 1)
            table_size = random.randint(10, 10000)
            has_where  = random.randint(0, 1)
            has_index  = random.randint(0, 1)

            # index hai toh fast, nahi toh slow
            base_time = table_size * 0.01
            if has_index:
                base_time *= 0.1
            if has_where and not has_index:
                base_time *= 1.5

            exec_time = round(base_time + random.uniform(0, 2), 3)

            self.record(query_type, table_size, 
                       has_where, has_index, exec_time)

        self.save()
        print("Training data ready!")