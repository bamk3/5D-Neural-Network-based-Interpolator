"use client";

import { useState, useEffect } from "react";
import Link from "next/link";

type PredictionMode = "single"  | "batch" ;

export default function PredictPage() {

  // Single prediction input fields
  const [predictionMode, setPredictionMode] = useState<PredictionMode>("single");
  const [feature1, setFeature1] = useState("");
  const [feature2, setFeature2] = useState("");
  const [feature3, setFeature3] = useState("");
  const [feature4, setFeature4] = useState("");
  const [feature5, setFeature5] = useState("");

    //Batch prediction input field

  //const [predictionMode, setPredictionMode] = useState<PredictionMode>("batch");
  const [predicting, setPredicting] = useState(false);
  const [predictionResult, setPredictionResult] = useState<any>(null);
  const [error, setError] = useState<string>("");
  const [modelTrained, setModelTrained] = useState(false);
  const [predictionDataUploaded, setPredictionDataUploaded] = useState(false);
  const [checkingStatus, setCheckingStatus] = useState(true);
  const [batchPredictionDone, setBatchPredictionDone] = useState(false);

  

  // Check if model is trained and prediction data is uploaded
  useEffect(() => {
    const checkStatus = async () => {
      try {
        const response = await fetch("http://localhost:8000/status");
        const data = await response.json();
        setModelTrained(data.model_trained);
        setPredictionDataUploaded(data.prediction_data_uploaded);
      } catch (err) {
        console.error("Failed to check status:", err);
      } finally {
        setCheckingStatus(false);
      }
    };
    checkStatus();
  }, []);

  const handleSinglePrediction = async () => {
    // Validate inputs
    const features = [feature1, feature2, feature3, feature4, feature5];
    if (features.some(f => f === "" || isNaN(parseFloat(f)))) {
      setError("All 5 feature fields must be filled with valid numbers");
      return;
    }

    setPredicting(true);
    setError("");
    setPredictionResult(null);

    try {
      const response = await fetch("http://localhost:8000/predict-single/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          features: features.map(f => parseFloat(f))
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setPredictionResult(data);
      } else {
        setError(data.detail || data.message || "Single prediction failed");
      }
    } catch (err: any) {
      setError(err.message || "Failed to connect to the backend. Make sure the server is running and a model is trained.");
    } finally {
      setPredicting(false);
    }
  };


  const handleBatchPrediction = async () => {
    setPredicting(true);
    setError("");
    setPredictionResult(null);

    try {
      const response = await fetch("http://localhost:8000/start-predict/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      const data = await response.json();

      if (response.ok) {
        setPredictionResult(data);
        setBatchPredictionDone(true);
      } else {
        setError(data.detail || data.message || "Batch prediction failed");
      }
    } catch (err: any) {
      setError(err.message || "Failed to connect to the backend. Make sure the server is running, a model is trained, and prediction data is uploaded.");
    } finally {
      setPredicting(false);
    }
  };

  
  const handlePredict = () => {
    if (predictionMode === "single") {
      handleSinglePrediction();
    } else {
      handleBatchPrediction();
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
              <p className="text-xs text-gray-600 dark:text-gray-400">Generate Predictions</p>
            </div>
          </Link>
          <Link href="/" className="text-xs text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
            ← Back
          </Link>
        </div>
      </header>

      {/* Main Content - Centered */}
      <main className="flex-1 flex items-start justify-center px-6 py-8 overflow-y-auto">
        <div className="w-full max-w-5xl mb-8">
          <div className="bg-white dark:bg-gray-900 rounded-xl shadow-md p-6 border border-gray-200 dark:border-gray-800">
            <div className="grid grid-cols-3 gap-6">
              {/* Left Column - Workflow */}
              <div className="col-span-2 space-y-4">
                <h2 className="text-xl font-bold text-gray-900 dark:text-white">Prediction Workflow</h2>

                {/* Mode Selection */}
                <div>
                  <label className="block text-base font-bold text-gray-900 dark:text-white mb-2">
                    Prediction Mode
                  </label>
                  <div className="grid grid-cols-1 gap-2">
                    <button
                      onClick={() => {
                        setPredictionMode("single");
                        setError("");
                        setPredictionResult(null);
                      }}
                      className={`p-3 rounded-lg border-2 transition-all ${
                        predictionMode === "single"
                          ? "border-teal-600 bg-teal-50 dark:bg-teal-900/20"
                          : "border-gray-300 dark:border-gray-700 hover:border-gray-400"
                      }`}
                    >
                      <div className="font-bold text-base text-gray-900 dark:text-white">Single Prediction</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Interactive form</div>
                    </button>
                    
                    
                  </div>
                </div>


                {/* Single Mode Input Form */}
                {predictionMode === "single" && (
                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                    <h4 className="font-bold text-base text-gray-900 dark:text-white mb-3">Input Features</h4>
                    <div className="grid grid-cols-5 gap-3">
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Feature 1</label>
                        <input
                          type="number"
                          step="any"
                          value={feature1}
                          onChange={(e) => setFeature1(e.target.value)}
                          placeholder="0.0"
                          className="w-full px-3 py-2 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-teal-600 focus:border-transparent"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Feature 2</label>
                        <input
                          type="number"
                          step="any"
                          value={feature2}
                          onChange={(e) => setFeature2(e.target.value)}
                          placeholder="0.0"
                          className="w-full px-3 py-2 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-teal-600 focus:border-transparent"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Feature 3</label>
                        <input
                          type="number"
                          step="any"
                          value={feature3}
                          onChange={(e) => setFeature3(e.target.value)}
                          placeholder="0.0"
                          className="w-full px-3 py-2 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-teal-600 focus:border-transparent"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Feature 4</label>
                        <input
                          type="number"
                          step="any"
                          value={feature4}
                          onChange={(e) => setFeature4(e.target.value)}
                          placeholder="0.0"
                          className="w-full px-3 py-2 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-teal-600 focus:border-transparent"
                        />
                      </div>
                      <div>
                        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-1">Feature 5</label>
                        <input
                          type="number"
                          step="any"
                          value={feature5}
                          onChange={(e) => setFeature5(e.target.value)}
                          placeholder="0.0"
                          className="w-full px-3 py-2 bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-lg text-gray-900 dark:text-white text-sm focus:ring-2 focus:ring-teal-600 focus:border-transparent"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* Batch Mode Workflow */}
                {predictionMode === "batch" && (
                  <div className="space-y-3">
                    <div className="flex items-start gap-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                      <div className="w-8 h-8 bg-blue-600 rounded flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
                        1
                      </div>
                      <div className="flex-1 min-w-0">
                        <h4 className="font-bold text-base text-gray-900 dark:text-white mb-1">Upload Prediction Dataset</h4>
                        <p className="text-sm text-gray-700 dark:text-gray-300 mb-2">Navigate to Upload page and select prediction dataset (.pkl)</p>
                        <Link
                          href="/upload"
                          className="inline-block px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold rounded transition-colors"
                        >
                          Go to Upload
                        </Link>
                      </div>
                    </div>

                    <div className="flex items-start gap-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                      <div className="w-8 h-8 bg-teal-600 rounded flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
                        2
                      </div>
                      <div className="flex-1">
                        <h4 className="font-bold text-base text-gray-900 dark:text-white mb-1">Generate Predictions</h4>
                        <p className="text-sm text-gray-700 dark:text-gray-300">Click button below to run predictions on uploaded dataset</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Warning: Requirements Not Met */}
                {!checkingStatus && predictionMode === "batch" && (!modelTrained || !predictionDataUploaded) && (
                  <div className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg border-2 border-orange-600">
                    <div className="flex items-start gap-2">
                      <svg className="w-5 h-5 text-orange-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      <div>
                        <p className="font-bold text-base text-orange-900 dark:text-orange-100">Requirements Not Met</p>
                        <ul className="text-sm text-orange-800 dark:text-orange-200 mt-1 list-disc list-inside">
                          {!modelTrained && <li>Model needs to be trained first</li>}
                          {!predictionDataUploaded && <li>Prediction dataset needs to be uploaded</li>}
                        </ul>
                      </div>
                    </div>
                  </div>
                )}

                {/* Warning: Model Not Trained (Single Mode) */}
                {!checkingStatus && predictionMode === "single" && !modelTrained && (
                  <div className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg border-2 border-orange-600">
                    <div className="flex items-start gap-2">
                      <svg className="w-5 h-5 text-orange-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      <div>
                        <p className="font-bold text-base text-orange-900 dark:text-orange-100">Model Not Trained</p>
                        <p className="text-sm text-orange-800 dark:text-orange-200">Please train a model first before making predictions</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Info: Batch Prediction Already Done */}
                {!checkingStatus && predictionMode === "batch" && predictionDataUploaded && batchPredictionDone && !predictionResult && (
                  <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-2 border-blue-600">
                    <div className="flex items-start gap-2">
                      <svg className="w-5 h-5 text-blue-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <div>
                        <p className="font-bold text-base text-blue-900 dark:text-blue-100">Predictions Already Generated</p>
                        <p className="text-sm text-blue-800 dark:text-blue-200">Batch predictions generated for the current dataset.</p>
                        <p className="text-sm text-blue-800 dark:text-blue-200"> If not seeing the results, click on back, step 3 and then "Generate batch predictions" to regenerate.</p>
                      </div>
                    </div>
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
                        <p className="font-bold text-base text-orange-900 dark:text-orange-100">Prediction Error</p>
                        <p className="text-sm text-orange-800 dark:text-orange-200">{error}</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Prediction Results */}
                {predictionResult && (
                  <div>
                    <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-2 border-blue-600 mb-3">
                      <div className="flex items-center gap-2">
                        <div className="w-7 h-7 bg-blue-600 rounded-full flex items-center justify-center">
                          <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                        <p className="font-bold text-base text-blue-900 dark:text-blue-100">
                          {predictionResult.prediction_type === "single" ? "Prediction Complete" : "Predictions Generated"}
                        </p>
                      </div>
                    </div>

                    {/* Single Prediction Result */}
                    {predictionResult.prediction_type === "single" && (
                      <div className="bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
                        <div className="space-y-3">
                          <div>
                            <h4 className="font-bold text-sm text-gray-900 dark:text-white mb-2">Input Features</h4>
                            <div className="bg-white dark:bg-gray-900 rounded p-3 border border-gray-200 dark:border-gray-700">
                              <div className="grid grid-cols-5 gap-2 text-xs">
                                {predictionResult.input_features.map((feat: number, idx: number) => (
                                  <div key={idx} className="text-center">
                                    <div className="text-gray-600 dark:text-gray-400 mb-1">F{idx + 1}</div>
                                    <div className="font-semibold text-gray-900 dark:text-white">{feat.toFixed(4)}</div>
                                  </div>
                                ))}
                              </div>
                            </div>
                          </div>
                          <div>
                            <h4 className="font-bold text-sm text-gray-900 dark:text-white mb-2">Prediction Result</h4>
                            <div className="bg-teal-50 dark:bg-teal-900/20 rounded p-4 border-2 border-teal-600 flex items-center justify-center">
                              <div className="text-center">
                                <div className="text-2xl font-bold text-teal-600">{predictionResult.prediction.toFixed(6)}</div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Batch Prediction Result */}
                    {predictionResult.prediction_type === "batch" && (
                      <div className="bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4">
                        <h4 className="font-bold text-base text-gray-900 dark:text-white mb-2 flex items-center gap-2">
                          <svg className="w-4 h-4 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
                          </svg>
                          Batch Results
                        </h4>
                        <div className="bg-white dark:bg-gray-900 rounded p-3 border border-gray-200 dark:border-gray-700 max-h-40 overflow-y-auto">
                          <pre className="font-mono text-sm text-gray-900 dark:text-gray-100 whitespace-pre-wrap break-words">
                            {predictionResult.function_result}
                          </pre>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* Start Button */}
                <button
                  onClick={handlePredict}
                  disabled={
                    predicting ||
                    !modelTrained ||
                    checkingStatus ||
                    (predictionMode === "batch" && !predictionDataUploaded) ||
                    (predictionMode === "batch" && predictionDataUploaded && batchPredictionDone && !predictionResult)
                  }
                  className={`w-full py-3 rounded-lg font-bold transition-all ${
                    predicting ||
                    !modelTrained ||
                    checkingStatus ||
                    (predictionMode === "batch" && !predictionDataUploaded) ||
                    (predictionMode === "batch" && predictionDataUploaded && batchPredictionDone && !predictionResult)
                      ? "bg-gray-300 dark:bg-gray-700 text-gray-500 cursor-not-allowed"
                      : "bg-teal-600 hover:bg-teal-700 text-white shadow-md"
                  }`}
                >
                  {checkingStatus
                    ? "Checking..."
                    : predicting
                    ? "Generating..."
                    : !modelTrained
                    ? "Train Model First"
                    : predictionMode === "batch" && !predictionDataUploaded
                    ? "Upload Dataset First"
                    : predictionMode === "batch" && predictionDataUploaded && batchPredictionDone && !predictionResult
                    ? "Already Predicted"
                    : predictionMode === "batch"
                    ? "Generate Batch Predictions"
                    : "Predict"}
                </button>
              </div>

              {/* Right Column - Requirements & Info */}
              <div className="space-y-4">
                <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-2 border-blue-600">
                  <p className="font-bold text-sm text-blue-900 dark:text-blue-100 mb-2">Requirements</p>
                  <ul className="space-y-1 text-sm text-blue-800 dark:text-blue-200">
                    <li>• Trained model ready</li>
                    {predictionMode === "batch" ? (
                      <>
                        <li>• Dataset uploaded</li>
                        <li>• 5D feature vectors</li>
                      </>
                    ) : (
                      <li>• 5 input features</li>
                    )}
                  </ul>
                </div>

                {predictionMode === "batch" && (
                  <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                    <p className="font-bold text-sm text-gray-900 dark:text-white mb-2">Dataset Format</p>
                    <ul className="space-y-1 text-sm text-gray-700 dark:text-gray-300">
                      <li className="flex items-start gap-1">
                        <svg className="w-3 h-3 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span>.pkl format</span>
                      </li>
                      <li className="flex items-start gap-1">
                        <svg className="w-3 h-3 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Array shape (n,5)</span>
                      </li>
                      <li className="flex items-start gap-1">
                        <svg className="w-3 h-3 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Auto standardized</span>
                      </li>
                    </ul>
                  </div>
                )}

                {predictionMode === "single" && (
                  <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                    <p className="font-bold text-sm text-gray-900 dark:text-white mb-2">Input Guidelines</p>
                    <ul className="space-y-1 text-sm text-gray-700 dark:text-gray-300">
                      <li className="flex items-start gap-1">
                        <svg className="w-3 h-3 text-teal-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span>All 5 fields required</span>
                      </li>
                      <li className="flex items-start gap-1">
                        <svg className="w-3 h-3 text-teal-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Numeric values only</span>
                      </li>
                      <li className="flex items-start gap-1">
                        <svg className="w-3 h-3 text-teal-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Real-time prediction</span>
                      </li>
                    </ul>
                  </div>
                )}

                <div className="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                  <p className="font-bold text-sm text-gray-900 dark:text-white mb-2">Process Steps</p>
                  <div className="space-y-2 text-sm">
                    <div className="flex items-center gap-2">
                      <div className="w-5 h-5 bg-blue-600 rounded flex items-center justify-center text-white text-xs font-bold flex-shrink-0">1</div>
                      <span className="text-gray-700 dark:text-gray-300">Load data</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-5 h-5 bg-orange-600 rounded flex items-center justify-center text-white text-xs font-bold flex-shrink-0">2</div>
                      <span className="text-gray-700 dark:text-gray-300">Model inference</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-5 h-5 bg-teal-600 rounded flex items-center justify-center text-white text-xs font-bold flex-shrink-0">3</div>
                      <span className="text-gray-700 dark:text-gray-300">Return results</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
