"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

export default function TrainPage() {
  const [training, setTraining] = useState(false);
  const [trainResult, setTrainResult] = useState<any>(null);
  const [error, setError] = useState<string>("");
  const [trainingDataUploaded, setTrainingDataUploaded] = useState(false);
  const [modelTrained, setModelTrained] = useState(false);
  const [checkingStatus, setCheckingStatus] = useState(true);
  const [resetting, setResetting] = useState(false);

  // Hyperparameter state
  const [hiddenLayer1, setHiddenLayer1] = useState(64);
  const [hiddenLayer2, setHiddenLayer2] = useState(32);
  const [hiddenLayer3, setHiddenLayer3] = useState(16);
  const [learningRate, setLearningRate] = useState(0.001);
  const [maxIterations, setMaxIterations] = useState(500);
  const [earlyStopping, setEarlyStopping] = useState(true);

  // Check if training data is uploaded and if model is already trained
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch("http://localhost:8000/status");
        const data = await response.json();
        setTrainingDataUploaded(data.training_data_uploaded);
        setModelTrained(data.model_trained);
      } catch (err) {
        console.error("Failed to check status:", err);
      } finally {
        setCheckingStatus(false);
      }
    };
    checkStatus();
  }, []);

  const handleStartTraining = async () => {
    setTraining(true);
    setError("");
    setTrainResult(null);

    try {
      const response = await fetch("http://localhost:8000/start-training/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          hyperparameters: {
            hidden_layer_1: hiddenLayer1,
            hidden_layer_2: hiddenLayer2,
            hidden_layer_3: hiddenLayer3,
            learning_rate: learningRate,
            max_iterations: maxIterations,
            early_stopping: earlyStopping,
          },
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setTrainResult(data);
        setModelTrained(true);
      } else {
        setError(data.detail || data.message || "Training failed");
      }
    } catch (err: any) {
      setError(err.message || "Failed to connect to the backend. Make sure the server is running and a dataset is uploaded.");
    } finally {
      setTraining(false);
    }
  };

  const handleReset = async () => {
    setResetting(true);
    setError("");

    try {
      const response = await fetch("http://localhost:8000/reset", {
        method: "POST",
      });

      const data = await response.json();

      if (response.ok) {
        // Reset all local state
        setTrainingDataUploaded(false);
        setModelTrained(false);
        setTrainResult(null);
        setError("");
        // Optionally redirect to upload page
        window.location.href = "/upload";
      } else {
        setError(data.detail || data.message || "Reset failed");
      }
    } catch (err: any) {
      setError(err.message || "Failed to reset. Please try again.");
    } finally {
      setResetting(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-950">
      {/* Compact Header */}
      <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-3 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 hover:opacity-80 transition-opacity">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">5D</span>
            </div>
            <div>
              <h1 className="text-lg font-bold text-gray-900 dark:text-white">5D Interpolator</h1>
              <p className="text-xs text-gray-600 dark:text-gray-400">Model Training</p>
            </div>
          </Link>
          <Link href="/" className="text-xs text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
            ← Back
          </Link>
        </div>
      </header>

      {/* Main Content - Centered */}
      <main className="flex-1 flex items-start justify-center px-6 py-8 overflow-y-auto">
        <div className="w-full max-w-5xl">
          <div className="bg-white dark:bg-gray-900 rounded-xl shadow-md p-6 border border-gray-200 dark:border-gray-800">
            <div className="grid grid-cols-3 gap-6">
              {/* Left Column - Configuration */}
              <div className="col-span-2 space-y-4">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">Hyperparameter Configuration</h2>

                {/* Neural Network Architecture */}
                <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 space-y-4">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-6 h-6 bg-blue-600 rounded flex items-center justify-center">
                      <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                      </svg>
                    </div>
                    <h3 className="font-bold text-base text-gray-900 dark:text-white">Neural Network Architecture</h3>
                  </div>

                  {/* Hidden Layer 1 */}
                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Hidden Layer 1 (neurons)</label>
                      <span className="text-sm font-bold text-blue-600">{hiddenLayer1}</span>
                    </div>
                    <input
                      type="range"
                      min="8"
                      max="256"
                      step="8"
                      value={hiddenLayer1}
                      onChange={(e) => setHiddenLayer1(Number(e.target.value))}
                      className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-blue-600"
                    />
                    <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                      <span>8</span>
                      <span>256</span>
                    </div>
                  </div>

                  {/* Hidden Layer 2 */}
                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Hidden Layer 2 (neurons)</label>
                      <span className="text-sm font-bold text-blue-600">{hiddenLayer2}</span>
                    </div>
                    <input
                      type="range"
                      min="8"
                      max="128"
                      step="8"
                      value={hiddenLayer2}
                      onChange={(e) => setHiddenLayer2(Number(e.target.value))}
                      className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-blue-600"
                    />
                    <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                      <span>8</span>
                      <span>128</span>
                    </div>
                  </div>

                  {/* Hidden Layer 3 */}
                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Hidden Layer 3 (neurons)</label>
                      <span className="text-sm font-bold text-blue-600">{hiddenLayer3}</span>
                    </div>
                    <input
                      type="range"
                      min="4"
                      max="64"
                      step="4"
                      value={hiddenLayer3}
                      onChange={(e) => setHiddenLayer3(Number(e.target.value))}
                      className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-blue-600"
                    />
                    <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                      <span>4</span>
                      <span>64</span>
                    </div>
                  </div>

                  <div className="text-sm text-gray-600 dark:text-gray-400 pt-2 border-t border-gray-300 dark:border-gray-600">
                    Architecture: [{hiddenLayer1}, {hiddenLayer2}, {hiddenLayer3}] • Activation: ReLU
                  </div>
                </div>

                {/* Training Parameters */}
                <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 space-y-4">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-6 h-6 bg-orange-600 rounded flex items-center justify-center">
                      <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                      </svg>
                    </div>
                    <h3 className="font-bold text-base text-gray-900 dark:text-white">Training Parameters</h3>
                  </div>

                  {/* Learning Rate */}
                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Learning Rate</label>
                      <span className="text-sm font-bold text-orange-600">{learningRate.toFixed(4)}</span>
                    </div>
                    <input
                      type="range"
                      min="0.0001"
                      max="0.01"
                      step="0.0001"
                      value={learningRate}
                      onChange={(e) => setLearningRate(Number(e.target.value))}
                      className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-orange-600"
                    />
                    <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                      <span>0.0001</span>
                      <span>0.01</span>
                    </div>
                  </div>

                  {/* Max Iterations */}
                  <div>
                    <div className="flex justify-between mb-2">
                      <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Max Iterations</label>
                      <span className="text-sm font-bold text-orange-600">{maxIterations}</span>
                    </div>
                    <input
                      type="range"
                      min="100"
                      max="2000"
                      step="100"
                      value={maxIterations}
                      onChange={(e) => setMaxIterations(Number(e.target.value))}
                      className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700 accent-orange-600"
                    />
                    <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
                      <span>100</span>
                      <span>2000</span>
                    </div>
                  </div>

                  {/* Early Stopping */}
                  <div className="flex items-center justify-between pt-2 border-t border-gray-300 dark:border-gray-600">
                    <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Early Stopping</label>
                    <button
                      onClick={() => setEarlyStopping(!earlyStopping)}
                      className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                        earlyStopping ? "bg-orange-600" : "bg-gray-300 dark:bg-gray-600"
                      }`}
                    >
                      <span
                        className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                          earlyStopping ? "translate-x-6" : "translate-x-1"
                        }`}
                      />
                    </button>
                  </div>

                  <div className="text-sm text-gray-600 dark:text-gray-400">
                    Optimizer: Adam • Data Split: 60/20/20
                  </div>
                </div>

                {/* Warning: No Training Data */}
                {!checkingStatus && !trainingDataUploaded && (
                  <div className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg border-2 border-orange-600">
                    <div className="flex items-start gap-2">
                      <svg className="w-5 h-5 text-orange-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      <div>
                        <p className="font-bold text-base text-orange-900 dark:text-orange-100">No Training Data</p>
                        <p className="text-sm text-orange-800 dark:text-orange-200">Please upload a training dataset first</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Info: Model Already Trained */}
                {!checkingStatus && trainingDataUploaded && modelTrained && !trainResult && (
                  <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-2 border-blue-600 space-y-3">
                    <div className="flex items-start gap-2">
                      <svg className="w-5 h-5 text-blue-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <div className="flex-1">
                        <p className="font-bold text-base text-blue-900 dark:text-blue-100">Model Already Trained</p>
                        <p className="text-sm text-blue-800 dark:text-blue-200 mt-1">
                          A model has been trained on the current dataset. To train a new model on different data, you need to reset the system first.
                        </p>
                      </div>
                    </div>
                    <button
                      onClick={handleReset}
                      disabled={resetting}
                      className={`w-full py-2 px-4 rounded-lg font-semibold transition-all ${
                        resetting
                          ? "bg-gray-300 dark:bg-gray-700 text-gray-500 cursor-not-allowed"
                          : "bg-orange-600 hover:bg-orange-700 text-white shadow-md"
                      }`}
                    >
                      {resetting ? "Resetting..." : "Reset & Train New Model"}
                    </button>
                  </div>
                )}

                {/* Error Message */}
                {error && (
                  <div className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg border-2 border-orange-600">
                    <div className="flex items-start gap-2">
                      <svg className="w-5 h-5 text-orange-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      <div>
                        <p className="font-bold text-base text-orange-900 dark:text-orange-100">Training Error</p>
                        <p className="text-sm text-orange-800 dark:text-orange-200">{error}</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Training Results */}
                {trainResult && trainResult.function_result && (
                  <div className="space-y-3">
                    <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-2 border-blue-600">
                      <div className="flex items-center gap-2 mb-3">
                        <div className="w-7 h-7 bg-blue-600 rounded-full flex items-center justify-center">
                          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                        <p className="font-bold text-base text-blue-900 dark:text-blue-100">Training Complete</p>
                      </div>
                      <div className="grid grid-cols-4 gap-2">
                        <div className="bg-white dark:bg-gray-800 p-2 rounded border-2 border-blue-600">
                          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">R² Score</div>
                          <div className="text-xl font-bold text-blue-600">{trainResult.function_result.r2?.toFixed(4)}</div>
                        </div>
                        <div className="bg-white dark:bg-gray-800 p-2 rounded border border-gray-300 dark:border-gray-700">
                          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">MSE</div>
                          <div className="text-xl font-bold text-gray-900 dark:text-white">{trainResult.function_result.mse?.toFixed(4)}</div>
                        </div>
                        <div className="bg-white dark:bg-gray-800 p-2 rounded border border-gray-300 dark:border-gray-700">
                          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">MAE</div>
                          <div className="text-xl font-bold text-gray-900 dark:text-white">{trainResult.function_result.mae?.toFixed(4)}</div>
                        </div>
                        <div className="bg-white dark:bg-gray-800 p-2 rounded border border-gray-300 dark:border-gray-700">
                          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">RMSE</div>
                          <div className="text-xl font-bold text-gray-900 dark:text-white">{trainResult.function_result.rmse?.toFixed(4)}</div>
                        </div>
                      </div>
                    </div>

                    {/* Hyperparameters Used */}
                    {trainResult.hyperparameters_used && (
                      <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-300 dark:border-gray-700">
                        <p className="font-bold text-sm text-gray-900 dark:text-white mb-2">Hyperparameters Used:</p>
                        <div className="grid grid-cols-2 gap-2 text-xs">
                          <div className="flex justify-between">
                            <span className="text-gray-600 dark:text-gray-400">Architecture:</span>
                            <span className="font-mono font-semibold text-gray-900 dark:text-white">
                              [{trainResult.hyperparameters_used.hidden_layers.join(', ')}]
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600 dark:text-gray-400">Learning Rate:</span>
                            <span className="font-mono font-semibold text-gray-900 dark:text-white">
                              {trainResult.hyperparameters_used.learning_rate.toFixed(4)}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600 dark:text-gray-400">Max Iterations:</span>
                            <span className="font-mono font-semibold text-gray-900 dark:text-white">
                              {trainResult.hyperparameters_used.max_iterations}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600 dark:text-gray-400">Early Stopping:</span>
                            <span className="font-mono font-semibold text-gray-900 dark:text-white">
                              {trainResult.hyperparameters_used.early_stopping ? 'Yes' : 'No'}
                            </span>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Start Button */}
                <button
                  onClick={handleStartTraining}
                  disabled={training || !trainingDataUploaded || checkingStatus || (trainingDataUploaded && modelTrained && !trainResult)}
                  className={`w-full py-3 rounded-lg font-bold transition-all ${
                    training || !trainingDataUploaded || checkingStatus || (trainingDataUploaded && modelTrained && !trainResult)
                      ? "bg-gray-300 dark:bg-gray-700 text-gray-500 cursor-not-allowed"
                      : "bg-orange-600 hover:bg-orange-700 text-white shadow-md"
                  }`}
                >
                  {checkingStatus
                    ? "Checking..."
                    : training
                    ? "Training..."
                    : !trainingDataUploaded
                    ? "Upload Dataset First"
                    : (trainingDataUploaded && modelTrained && !trainResult)
                    ? "Already Trained"
                    : "Start Training"}
                </button>
              </div>

              {/* Right Column - Info & Next Steps */}
              <div className="space-y-4">
                <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-2 border-blue-600">
                  <p className="font-bold text-sm text-blue-900 dark:text-blue-100 mb-2">Requirements</p>
                  <ul className="space-y-1 text-sm text-blue-800 dark:text-blue-200">
                    <li>• Dataset uploaded</li>
                    <li>• Training &lt;1 min</li>
                    <li>• Auto standardization</li>
                  </ul>
                </div>

                {trainResult && (
                  <div className="space-y-1">
                    <p className="font-bold text-base text-gray-900 dark:text-white">Next Steps</p>
                    
                    <Link
                      href="/predict"
                      className="block w-full py-2 px-3 bg-teal-600 hover:bg-teal-700 text-white rounded-lg font-semibold text-sm text-center transition-colors"
                    >
                      Make Predictions →
                    </Link>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
