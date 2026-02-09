import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-950">
      {/* Header */}
      <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">5D</span>
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white">5D Interpolator</h1>
              <p className="text-sm text-gray-600 dark:text-gray-400">Neural Network Platform</p>
            </div>
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">Cambridge DIS • bamk3</div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex items-center justify-center px-6 py-12">
        <div className="w-full max-w-6xl">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h2 className="text-4xl md:text-5xl font-bold mb-3 text-gray-900 dark:text-white">
              Professional 5D Function Interpolation
            </h2>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              Advanced neural network • Fast CPU training • Research-grade accuracy
            </p>
          </div>

          {/* Feature Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            {/* Upload Card */}
            <Link href="/upload">
              <div className="group bg-white dark:bg-gray-900 rounded-2xl p-8 shadow-md hover:shadow-xl transition-all cursor-pointer border-2 border-gray-200 dark:border-gray-800 hover:border-blue-600 dark:hover:border-blue-500 h-full">
                <div className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 bg-blue-600 rounded-xl flex items-center justify-center mb-4 group-hover:scale-105 transition-transform shadow-lg">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
                    </svg>
                  </div>
                  <span className="inline-block px-3 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-sm font-semibold rounded-full mb-3">
                    STEP 1
                  </span>
                  <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-white">Data Upload</h3>
                  <p className="text-base text-gray-700 dark:text-gray-300">Upload .pkl datasets for training and prediction workflows</p>
                </div>
              </div>
            </Link>

            {/* Train Card */}
            <Link href="/train">
              <div className="group bg-white dark:bg-gray-900 rounded-2xl p-8 shadow-md hover:shadow-xl transition-all cursor-pointer border-2 border-gray-200 dark:border-gray-800 hover:border-orange-600 dark:hover:border-orange-500 h-full">
                <div className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 bg-orange-600 rounded-xl flex items-center justify-center mb-4 group-hover:scale-105 transition-transform shadow-lg">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                    </svg>
                  </div>
                  <span className="inline-block px-3 py-1 bg-orange-100 dark:bg-orange-900/30 text-orange-700 dark:text-orange-300 text-sm font-semibold rounded-full mb-3">
                    STEP 2
                  </span>
                  <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-white">Model Training</h3>
                  <p className="text-base text-gray-700 dark:text-gray-300">Train neural network with optimized hyperparameters</p>
                </div>
              </div>
            </Link>

            {/* Predict Card */}
            <Link href="/predict">
              <div className="group bg-white dark:bg-gray-900 rounded-2xl p-8 shadow-md hover:shadow-xl transition-all cursor-pointer border-2 border-gray-200 dark:border-gray-800 hover:border-teal-600 dark:hover:border-teal-500 h-full">
                <div className="flex flex-col items-center text-center">
                  <div className="w-16 h-16 bg-teal-600 rounded-xl flex items-center justify-center mb-4 group-hover:scale-105 transition-transform shadow-lg">
                    <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  </div>
                  <span className="inline-block px-3 py-1 bg-teal-100 dark:bg-teal-900/30 text-teal-700 dark:text-teal-300 text-sm font-semibold rounded-full mb-3">
                    STEP 3
                  </span>
                  <h3 className="text-2xl font-bold mb-3 text-gray-900 dark:text-white">Generate Predictions</h3>
                  <p className="text-base text-gray-700 dark:text-gray-300">Deploy model for accurate prediction generation</p>
                </div>
              </div>
            </Link>
          </div>

          {/* Technical Specs */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-gray-900 rounded-xl p-6 shadow-md border border-gray-200 dark:border-gray-800">
              <h3 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Technical Specifications</h3>
              <div className="grid grid-cols-4 gap-4 text-center">
                <div>
                  <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">&lt;1min</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">Training</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-orange-600 dark:text-orange-400">&gt;95%</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">R² Score</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-teal-600 dark:text-teal-400">5D</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">Features</div>
                </div>
                <div>
                  <div className="text-3xl font-bold text-gray-900 dark:text-white">CPU</div>
                  <div className="text-sm text-gray-600 dark:text-gray-400 mt-1">Optimized</div>
                </div>
              </div>
            </div>

            <div className="bg-white dark:bg-gray-900 rounded-xl p-6 shadow-md border border-gray-200 dark:border-gray-800">
              <h3 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Architecture Overview</h3>
              <div className="grid grid-cols-3 gap-3 text-sm">
                <div className="text-center">
                  <div className="w-3 h-3 bg-blue-600 rounded-full mx-auto mb-2"></div>
                  <div className="font-semibold text-gray-900 dark:text-white">Layers</div>
                  <div className="text-gray-600 dark:text-gray-400">[64,32,16]</div>
                </div>
                <div className="text-center">
                  <div className="w-3 h-3 bg-orange-600 rounded-full mx-auto mb-2"></div>
                  <div className="font-semibold text-gray-900 dark:text-white">Optimizer</div>
                  <div className="text-gray-600 dark:text-gray-400">Adam</div>
                </div>
                <div className="text-center">
                  <div className="w-3 h-3 bg-teal-600 rounded-full mx-auto mb-2"></div>
                  <div className="font-semibold text-gray-900 dark:text-white">Split</div>
                  <div className="text-gray-600 dark:text-gray-400">60/20/20</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 py-4">
        <div className="max-w-6xl mx-auto px-6 text-center text-sm text-gray-600 dark:text-gray-400">
          <p>Developed by Makimona Kiakisolako (bamk3) • University of Cambridge DIS Course 2025</p>
        </div>
      </footer>
    </div>
  );
}
