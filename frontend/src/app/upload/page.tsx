"use client";

import { useState } from "react";
import Link from "next/link";

type UploadType = "fit" | "predict";

export default function UploadPage() {
  const [uploadType, setUploadType] = useState<UploadType>("fit");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [error, setError] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.name.endsWith(".pkl")) {
        setError("Only .pkl files are accepted");
        setSelectedFile(null);
        return;
      }
      setSelectedFile(file);
      setError("");
      setUploadResult(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError("Please select a file first");
      return;
    }

    setUploading(true);
    setError("");
    setUploadResult(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const endpoint =
        uploadType === "fit"
          ? "http://localhost:8000/upload-fit-dataset/"
          : "http://localhost:8000/upload-predict-dataset/";

      console.log("Uploading to:", endpoint);
      console.log("File:", selectedFile.name, "Size:", selectedFile.size, "bytes");

      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
      });

      console.log("Response status:", response.status);
      console.log("Response headers:", Object.fromEntries(response.headers.entries()));

      const data = await response.json();
      console.log("Response data:", data);

      if (response.ok) {
        setUploadResult(data);
      } else {
        setError(data.detail || data.message || "Upload failed");
      }
    } catch (err: any) {
      console.error("Upload error:", err);
      const errorMessage = err.message || "Failed to connect to the backend. Make sure the server is running.";
      setError(`${errorMessage} (Check browser console for details)`);
    } finally {
      setUploading(false);
    }
  };

  const resetUpload = () => {
    setSelectedFile(null);
    setUploadResult(null);
    setError("");
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
              <p className="text-xs text-gray-600 dark:text-gray-400">Data Upload</p>
            </div>
          </Link>
          <Link href="/" className="text-xs text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors">
            ← Back
          </Link>
        </div>
      </header>

      {/* Main Content - Centered */}
      <main className="flex-1 flex items-start justify-center px-6 py-8 overflow-y-auto">
        <div className="w-full max-w-4xl mb-8">
          <div className="bg-white dark:bg-gray-900 rounded-xl shadow-md p-6 border border-gray-200 dark:border-gray-800">
            <div className="grid grid-cols-2 gap-6">
              {/* Left Column - Controls */}
              <div className="space-y-4">
                {/* Upload Type Selection */}
                <div>
                  <label className="block text-base font-bold text-gray-900 dark:text-white mb-2">
                    Dataset Type
                  </label>
                  <div className="grid grid-cols-1 gap-2">
                    <button
                      onClick={() => setUploadType("fit")}
                      className={`p-3 rounded-lg border-2 transition-all ${
                        uploadType === "fit"
                          ? "border-blue-600 bg-blue-50 dark:bg-blue-900/20"
                          : "border-gray-300 dark:border-gray-700 hover:border-gray-400"
                      }`}
                    >
                      <div className="font-bold text-base text-gray-900 dark:text-white">Training</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Model training</div>
                    </button>
                
                  </div>
                </div>

                {/* File Upload Area */}
                <div>
                  <label className="block text-base font-bold text-gray-900 dark:text-white mb-2">
                    Select File
                  </label>
                  <input
                    type="file"
                    accept=".pkl"
                    onChange={handleFileChange}
                    className="hidden"
                    id="file-upload"
                  />
                  <label
                    htmlFor="file-upload"
                    className="flex flex-col items-center justify-center h-40 border-2 border-dashed border-gray-300 dark:border-gray-700 rounded-lg cursor-pointer hover:border-blue-600 transition-all bg-gray-50 dark:bg-gray-900/50"
                  >
                    <svg className="w-10 h-10 text-gray-400 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                    <p className="text-base font-semibold text-gray-700 dark:text-gray-300">Click to upload</p>
                    <p className="text-sm text-gray-500 dark:text-gray-400">.pkl files only</p>
                  </label>
                </div>

                {/* Selected File */}
                {selectedFile && (
                  <div className="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-2 border-blue-600">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2 flex-1 min-w-0">
                        <svg className="w-5 h-5 text-blue-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <div className="min-w-0 flex-1">
                          <p className="font-semibold text-base text-gray-900 dark:text-white truncate">{selectedFile.name}</p>
                          <p className="text-sm text-gray-600 dark:text-gray-400">{(selectedFile.size / 1024).toFixed(2)} KB</p>
                        </div>
                      </div>
                      <button onClick={resetUpload} className="text-gray-400 hover:text-gray-600 ml-2">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                      </button>
                    </div>
                  </div>
                )}

                {/* Upload Button */}
                <button
                  onClick={handleUpload}
                  disabled={!selectedFile || uploading}
                  className={`w-full py-3 rounded-lg font-bold transition-all ${
                    !selectedFile || uploading
                      ? "bg-gray-300 dark:bg-gray-700 text-gray-500 cursor-not-allowed"
                      : "bg-blue-600 hover:bg-blue-700 text-white shadow-md"
                  }`}
                >
                  {uploading ? "Uploading..." : "Upload Dataset"}
                </button>
              </div>

              {/* Right Column - Status & Info */}
              <div className="space-y-4">
                {/* Error Message */}
                {error && (
                  <div className="p-3 bg-orange-50 dark:bg-orange-900/20 rounded-lg border-2 border-orange-600">
                    <div className="flex items-start gap-2">
                      <svg className="w-5 h-5 text-orange-600 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                      </svg>
                      <div>
                        <p className="font-bold text-base text-orange-900 dark:text-orange-100">Error</p>
                        <p className="text-sm text-orange-800 dark:text-orange-200">{error}</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Success Message */}
                {uploadResult && uploadResult.valid && (
                  <div className="space-y-3">
                    <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border-2 border-blue-600">
                      <div className="flex items-start gap-2 mb-3">
                        <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center flex-shrink-0">
                          <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
                          </svg>
                        </div>
                        <div>
                          <p className="font-bold text-base text-blue-900 dark:text-blue-100">Upload Successful</p>
                          <p className="text-sm text-blue-700 dark:text-blue-300 mt-1">{uploadResult.filename}</p>
                        </div>
                      </div>

                      {/* Data Preview */}
                      {uploadResult.preview && (
                        <div className="mt-3 p-3 bg-white dark:bg-gray-800 rounded-lg border border-blue-200 dark:border-blue-800">
                          <p className="font-bold text-sm text-gray-900 dark:text-white mb-2">Data Preview</p>
                          <div className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                            Total samples: {uploadResult.preview.total_samples} | Shape: {uploadType === "fit" ? `X${JSON.stringify(uploadResult.preview.X_shape)}, y${JSON.stringify(uploadResult.preview.y_shape)}` : JSON.stringify(uploadResult.preview.X_shape)}
                          </div>
                          <div className="bg-gray-50 dark:bg-gray-900 rounded p-2 max-h-32 overflow-auto">
                            <pre className="font-mono text-xs text-gray-900 dark:text-gray-100">
                              {uploadType === "fit"
                                ? `X (first ${uploadResult.preview.X_preview.length} rows):\n${JSON.stringify(uploadResult.preview.X_preview, null, 2)}\n\ny (first ${uploadResult.preview.y_preview.length} values):\n${JSON.stringify(uploadResult.preview.y_preview, null, 2)}`
                                : `X (first ${uploadResult.preview.X_preview.length} rows):\n${JSON.stringify(uploadResult.preview.X_preview, null, 2)}`
                              }
                            </pre>
                          </div>
                        </div>
                      )}

                      <Link
                        href={uploadType === "fit" ? "/train" : "/predict"}
                        className="block w-full py-2 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold text-base text-center transition-colors mt-3"
                      >
                        {uploadType === "fit" ? "Proceed to Training →" : "Proceed to Prediction →"}
                      </Link>
                    </div>
                  </div>
                )}

                {/* Requirements */}
                {!error && !uploadResult && (
                  <div className="p-4 bg-gray-50 dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
                    <h4 className="font-bold text-base text-gray-900 dark:text-white mb-2">Requirements</h4>
                    <ul className="space-y-1 text-sm text-gray-700 dark:text-gray-300">
                      <li className="flex items-start gap-2">
                        <svg className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Python pickle (.pkl) format</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <svg className="w-4 h-4 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                        </svg>
                        <span>Training: Dict with 'X' (n,5) and 'y' (n,)</span>
                      </li>
                    </ul>
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
