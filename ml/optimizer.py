import csv
import random
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

class QueryOptimizer:
    def __init__(self):
        self.model   = RandomForestRegressor(n_estimators=100, random_state=42)
        self.trained = False

    def load_data(self):
        df = pd.read_csv("ml/query_data.csv")
        print(f"Loaded {len(df)} training records!")
        return df

    def train(self):
        df = self.load_data()

        # features aur target
        X = df[["query_type", "table_size", "has_where", "has_index"]]
        y = df["exec_time"]

        # train/test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        # model train karo
        self.model.fit(X_train, y_train)

        # accuracy check karo
        predictions = self.model.predict(X_test)
        mae = mean_absolute_error(y_test, predictions)

        self.trained = True
        print(f"\n--- Random Forest Model Trained ---")
        print(f"Training samples : {len(X_train)}")
        print(f"Testing samples  : {len(X_test)}")
        print(f"Mean Abs Error   : {mae:.3f}ms")

        # feature importance
        features = ["query_type", "table_size", "has_where", "has_index"]
        importance = self.model.feature_importances_
        print(f"\n--- Feature Importance ---")
        for f, i in zip(features, importance):
            print(f"{f:15} : {i:.3f}")

    def predict(self, query_type, table_size, has_where, has_index):
        if not self.trained:
            print("Pehle train karo!")
            return

        features = np.array([[query_type, table_size, has_where, has_index]])
        est_time  = self.model.predict(features)[0]

        print(f"\n--- Query Optimizer Prediction ---")
        print(f"Table size : {table_size}")
        print(f"Has WHERE  : {bool(has_where)}")
        print(f"Has Index  : {bool(has_index)}")
        print(f"Estimated execution time : {est_time:.3f}ms")

        if has_where and not has_index and table_size > 1000:
            print("⚠️  Recommendation: INDEX banao!")
        elif has_index:
            print("✅ Query optimized hai!")
        else:
            print("ℹ️  Query theek hai!")

if __name__ == "__main__":
    from data_collector import DataCollector

    # data generate karo
    collector = DataCollector()
    collector.generate_training_data(1000)

    # model train karo
    optimizer = QueryOptimizer()
    optimizer.train()

    # predictions
    print("\n--- Test Cases ---")
    optimizer.predict(0, 5000, 1, 0)   # SELECT, large, WHERE, no index
    optimizer.predict(0, 5000, 1, 1)   # SELECT, large, WHERE, with index
    optimizer.predict(1, 100,  0, 0)   # INSERT, small, no WHERE