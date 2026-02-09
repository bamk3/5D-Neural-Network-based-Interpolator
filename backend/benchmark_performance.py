#!/usr/bin/env python3
"""
Comprehensive Performance Benchmarking Script
Analyzes training time, memory usage, and accuracy metrics
across different dataset sizes.
"""

import numpy as np
import pickle
import time
import tracemalloc
import json
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fivedreg.base_fivedreg import FastNeuralNetwork
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


class PerformanceBenchmark:
    """Comprehensive performance benchmarking for the neural network."""

    def __init__(self, output_dir: str = "benchmark_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.results = {
            "dataset_sizes": [],
            "training_times": [],
            "peak_memory_training": [],
            "peak_memory_prediction": [],
            "r2_scores": [],
            "mse_scores": [],
            "mae_scores": [],
            "rmse_scores": [],
            "samples_per_second": [],
            "model_sizes": [],
            "iterations_completed": []
        }

    def generate_dataset(self, n_samples: int, seed: int = 42) -> tuple:
        """
        Generate synthetic dataset for benchmarking.

        Target function: f(x) = sum(x^2) + noise
        This provides a non-trivial but learnable pattern.
        """
        np.random.seed(seed)

        # Generate 5D features
        X = np.random.randn(n_samples, 5)

        # Target: sum of squares with some noise
        y = np.sum(X**2, axis=1) + 0.1 * np.random.randn(n_samples)

        return X, y

    def measure_model_size(self, model: FastNeuralNetwork) -> int:
        """Estimate model size in bytes."""
        # Save model to temporary pickle and measure size
        temp_file = self.output_dir / "temp_model.pkl"
        with open(temp_file, 'wb') as f:
            pickle.dump(model, f)
        size = temp_file.stat().st_size
        temp_file.unlink()  # Delete temp file
        return size

    def benchmark_training(self, n_samples: int) -> dict:
        """
        Benchmark training performance for a given dataset size.

        Returns metrics including time, memory, and accuracy.
        """
        print(f"\n{'='*60}")
        print(f"Benchmarking with {n_samples:,} samples")
        print(f"{'='*60}")

        # Generate dataset
        print("Generating dataset...")
        X, y = self.generate_dataset(n_samples)

        # Split data (60% train, 20% val, 20% test)
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=0.25, random_state=42
        )

        # Standardize features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_val_scaled = scaler.transform(X_val)
        X_test_scaled = scaler.transform(X_test)

        print(f"  Train samples: {len(X_train):,}")
        print(f"  Val samples: {len(X_val):,}")
        print(f"  Test samples: {len(X_test):,}")

        # Initialize model with standard configuration
        model = FastNeuralNetwork(
            hidden_layers=(64, 32, 16),
            learning_rate=0.001,
            max_iterations=500,
            early_stopping=True
        )

        # Measure training time and memory
        print("\nTraining model...")
        tracemalloc.start()
        start_time = time.time()

        # Train model
        model.model.fit(X_train_scaled, y_train)

        training_time = time.time() - start_time
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        peak_memory_mb = peak / 1024 / 1024

        print(f"  Training time: {training_time:.2f}s")
        print(f"  Peak memory: {peak_memory_mb:.2f} MB")
        print(f"  Samples/second: {n_samples/training_time:.0f}")

        # Get number of iterations completed
        iterations = model.model.n_iter_
        print(f"  Iterations completed: {iterations}")

        # Measure prediction time and memory
        print("\nMeasuring prediction performance...")
        tracemalloc.start()

        y_pred = model.model.predict(X_test_scaled)

        pred_current, pred_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        pred_peak_mb = pred_peak / 1024 / 1024

        # Calculate metrics
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mse)

        print(f"\nAccuracy Metrics:")
        print(f"  R² Score: {r2:.6f}")
        print(f"  MSE: {mse:.6f}")
        print(f"  MAE: {mae:.6f}")
        print(f"  RMSE: {rmse:.6f}")

        # Measure model size
        model_size = self.measure_model_size(model)
        model_size_kb = model_size / 1024

        print(f"\nModel size: {model_size_kb:.2f} KB")

        return {
            "n_samples": n_samples,
            "training_time": training_time,
            "peak_memory_training_mb": peak_memory_mb,
            "peak_memory_prediction_mb": pred_peak_mb,
            "r2_score": r2,
            "mse": mse,
            "mae": mae,
            "rmse": rmse,
            "samples_per_second": n_samples / training_time,
            "model_size_kb": model_size_kb,
            "iterations": iterations
        }

    def run_benchmarks(self, dataset_sizes: list = None):
        """
        Run benchmarks across multiple dataset sizes.
        """
        if dataset_sizes is None:
            dataset_sizes = [1000, 5000, 10000]

        print("\n" + "="*60)
        print("PERFORMANCE BENCHMARKING SUITE")
        print("="*60)
        print(f"\nDataset sizes to test: {dataset_sizes}")
        print(f"Output directory: {self.output_dir}")

        all_results = []

        for n_samples in dataset_sizes:
            result = self.benchmark_training(n_samples)
            all_results.append(result)

            # Store in aggregate results
            self.results["dataset_sizes"].append(n_samples)
            self.results["training_times"].append(result["training_time"])
            self.results["peak_memory_training"].append(result["peak_memory_training_mb"])
            self.results["peak_memory_prediction"].append(result["peak_memory_prediction_mb"])
            self.results["r2_scores"].append(result["r2_score"])
            self.results["mse_scores"].append(result["mse"])
            self.results["mae_scores"].append(result["mae"])
            self.results["rmse_scores"].append(result["rmse"])
            self.results["samples_per_second"].append(result["samples_per_second"])
            self.results["model_sizes"].append(result["model_size_kb"])
            self.results["iterations_completed"].append(result["iterations"])

        # Save results
        self.save_results(all_results)
        self.print_summary()

        return all_results

    def save_results(self, results: list):
        """Save benchmark results to JSON file."""
        output_file = self.output_dir / "benchmark_results.json"

        with open(output_file, 'w') as f:
            json.dump({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                "configuration": {
                    "hidden_layers": [64, 32, 16],
                    "learning_rate": 0.001,
                    "max_iterations": 500,
                    "early_stopping": True
                },
                "individual_results": results,
                "aggregate_results": self.results
            }, f, indent=2)

        print(f"\nResults saved to: {output_file}")

    def print_summary(self):
        """Print summary of benchmark results."""
        print("\n" + "="*60)
        print("BENCHMARK SUMMARY")
        print("="*60)

        print("\nScaling Analysis:")
        print(f"{'Size':<10} {'Time (s)':<12} {'Memory (MB)':<15} {'R² Score':<12} {'Samples/s':<12}")
        print("-" * 60)

        for i, size in enumerate(self.results["dataset_sizes"]):
            print(f"{size:<10,} {self.results['training_times'][i]:<12.2f} "
                  f"{self.results['peak_memory_training'][i]:<15.2f} "
                  f"{self.results['r2_scores'][i]:<12.6f} "
                  f"{self.results['samples_per_second'][i]:<12.0f}")

        # Calculate scaling factor
        if len(self.results["dataset_sizes"]) >= 2:
            size_ratio = self.results["dataset_sizes"][-1] / self.results["dataset_sizes"][0]
            time_ratio = self.results["training_times"][-1] / self.results["training_times"][0]
            memory_ratio = self.results["peak_memory_training"][-1] / self.results["peak_memory_training"][0]

            print(f"\nScaling from {self.results['dataset_sizes'][0]:,} to "
                  f"{self.results['dataset_sizes'][-1]:,} samples:")
            print(f"  Dataset size increased: {size_ratio:.1f}x")
            print(f"  Training time increased: {time_ratio:.2f}x")
            print(f"  Memory usage increased: {memory_ratio:.2f}x")
            print(f"  Time complexity: O(n^{np.log(time_ratio)/np.log(size_ratio):.2f})")

        print("\nAccuracy Consistency:")
        r2_mean = np.mean(self.results["r2_scores"])
        r2_std = np.std(self.results["r2_scores"])
        print(f"  R² Score: {r2_mean:.6f} ± {r2_std:.6f}")
        print(f"  Range: [{min(self.results['r2_scores']):.6f}, "
              f"{max(self.results['r2_scores']):.6f}]")

        print("\nMemory Efficiency:")
        print(f"  Training memory: {min(self.results['peak_memory_training']):.2f} MB - "
              f"{max(self.results['peak_memory_training']):.2f} MB")
        print(f"  Prediction memory: {min(self.results['peak_memory_prediction']):.2f} MB - "
              f"{max(self.results['peak_memory_prediction']):.2f} MB")

        print("\nThroughput:")
        avg_throughput = np.mean(self.results["samples_per_second"])
        print(f"  Average: {avg_throughput:.0f} samples/second")

        print(f"\nModel size: {self.results['model_sizes'][0]:.2f} KB")
        print(f"  (consistent across dataset sizes)")


def main():
    """Main benchmarking entry point."""
    benchmark = PerformanceBenchmark()

    # Run benchmarks with 1K, 5K, and 10K samples
    results = benchmark.run_benchmarks([1000, 5000, 10000])

    print("\n" + "="*60)
    print("BENCHMARKING COMPLETE")
    print("="*60)
    print(f"\nResults available in: {benchmark.output_dir}/benchmark_results.json")


if __name__ == "__main__":
    main()
