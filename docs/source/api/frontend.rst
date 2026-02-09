Frontend Components
===================

This section documents the React components in the Next.js frontend application.

Technology Stack
----------------

* **Framework**: Next.js 16.0.3 with App Router
* **React**: 19.2.0
* **Language**: TypeScript 5
* **Styling**: Tailwind CSS v4
* **Fonts**: Geist Sans and Geist Mono
* **Build Tool**: Turbopack

Project Structure
-----------------

.. code-block:: text

   frontend/
   ├── src/
   │   └── app/
   │       ├── layout.tsx        # Root layout
   │       ├── page.tsx          # Home page
   │       ├── globals.css       # Global styles
   │       ├── upload/
   │       │   └── page.tsx      # Upload page
   │       ├── train/
   │       │   └── page.tsx      # Training page
   │       └── predict/
   │           └── page.tsx      # Prediction page
   ├── public/
   ├── package.json
   └── next.config.ts

Root Layout
-----------

Location: ``src/app/layout.tsx``

The root layout component that wraps all pages.

**Features:**

* Loads Geist Sans and Geist Mono fonts
* Sets up HTML metadata
* Provides consistent layout structure

**Code Structure:**

.. code-block:: typescript

   import { GeistSans } from "geist/font/sans";
   import { GeistMono } from "geist/font/mono";
   import "./globals.css";

   export default function RootLayout({
     children,
   }: Readonly<{
     children: React.ReactNode;
   }>) {
     return (
       <html lang="en">
         <body className={`${GeistSans.variable} ${GeistMono.variable}`}>
           {children}
         </body>
       </html>
     );
   }

Home Page
---------

Location: ``src/app/page.tsx``

The landing page of the application.

**Features:**

* Welcome message
* Navigation links to Upload, Train, and Predict pages
* Responsive design
* Dark mode support

Upload Page
-----------

Location: ``src/app/upload/page.tsx``

Component for uploading training and prediction datasets.

State Management
~~~~~~~~~~~~~~~~

.. code-block:: typescript

   const [datasetType, setDatasetType] = useState<'training' | 'prediction'>('training')
   const [file, setFile] = useState<File | null>(null)
   const [uploading, setUploading] = useState(false)
   const [uploadResult, setUploadResult] = useState<any>(null)
   const [error, setError] = useState<string | null>(null)

**Key States:**

* ``datasetType``: Type of dataset being uploaded
* ``file``: Selected file object
* ``uploading``: Upload in progress flag
* ``uploadResult``: Server response with dataset info
* ``error``: Error message if upload fails

Upload Process
~~~~~~~~~~~~~~

**Training Dataset:**

.. code-block:: typescript

   const handleUpload = async () => {
     const formData = new FormData()
     formData.append('file', file)

     const response = await fetch('http://localhost:8000/upload-fit-dataset/', {
       method: 'POST',
       body: formData,
     })

     const data = await response.json()
     setUploadResult(data)
   }

**Prediction Dataset:**

.. code-block:: typescript

   const response = await fetch('http://localhost:8000/upload-predict-dataset/', {
     method: 'POST',
     body: formData,
   })

**Upload Result Display:**

Shows preview of uploaded data:

* Total samples
* Data shape
* First 5 rows of data
* Proceed to next step button

Train Page
----------

Location: ``src/app/train/page.tsx``

Component for training the neural network model with configurable hyperparameters.

State Management
~~~~~~~~~~~~~~~~

.. code-block:: typescript

   const [trainingDataUploaded, setTrainingDataUploaded] = useState(false)
   const [modelTrained, setModelTrained] = useState(false)
   const [training, setTraining] = useState(false)
   const [trainResult, setTrainResult] = useState<any>(null)
   const [hyperparameters, setHyperparameters] = useState({
     hidden_layer_1: 64,
     hidden_layer_2: 32,
     hidden_layer_3: 16,
     learning_rate: 0.001,
     max_iterations: 500,
     early_stopping: true,
   })

Hyperparameter Controls
~~~~~~~~~~~~~~~~~~~~~~~

**Hidden Layer Sizes:**

.. code-block:: typescript

   // Layer 1: 8-256 neurons
   <input
     type="range"
     min="8"
     max="256"
     step="8"
     value={hyperparameters.hidden_layer_1}
     onChange={(e) => setHyperparameters({
       ...hyperparameters,
       hidden_layer_1: parseInt(e.target.value)
     })}
   />

   // Layer 2: 8-128 neurons
   // Layer 3: 4-64 neurons

**Learning Rate:**

.. code-block:: typescript

   <input
     type="range"
     min="0.0001"
     max="0.01"
     step="0.0001"
     value={hyperparameters.learning_rate}
     onChange={(e) => setHyperparameters({
       ...hyperparameters,
       learning_rate: parseFloat(e.target.value)
     })}
   />

**Max Iterations:**

.. code-block:: typescript

   <input
     type="range"
     min="100"
     max="2000"
     step="100"
     value={hyperparameters.max_iterations}
   />

**Early Stopping:**

.. code-block:: typescript

   <input
     type="checkbox"
     checked={hyperparameters.early_stopping}
     onChange={(e) => setHyperparameters({
       ...hyperparameters,
       early_stopping: e.target.checked
     })}
   />

Training Process
~~~~~~~~~~~~~~~~

.. code-block:: typescript

   const handleTrain = async () => {
     setTraining(true)
     setTrainResult(null)

     const response = await fetch('http://localhost:8000/start-training/', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ hyperparameters })
     })

     const data = await response.json()
     setTrainResult(data)
     setModelTrained(true)
     setTraining(false)
   }

Results Display
~~~~~~~~~~~~~~~

**Performance Metrics:**

* R² Score (coefficient of determination)
* MSE (Mean Squared Error)
* MAE (Mean Absolute Error)
* RMSE (Root Mean Squared Error)

**Hyperparameters Used:**

Displays the actual configuration used for training.

Button Logic
~~~~~~~~~~~~

The training button is disabled when:

* Training is in progress
* No training data uploaded
* Status is being checked
* Model already trained on current dataset

.. code-block:: typescript

   disabled={
     training ||
     !trainingDataUploaded ||
     checkingStatus ||
     (trainingDataUploaded && modelTrained && !trainResult)
   }

Predict Page
------------

Location: ``src/app/predict/page.tsx``

Component for making predictions using the trained model.

State Management
~~~~~~~~~~~~~~~~

.. code-block:: typescript

   const [predictionMode, setPredictionMode] = useState<'batch' | 'single'>('batch')
   const [predictionDataUploaded, setPredictionDataUploaded] = useState(false)
   const [batchPredictionDone, setBatchPredictionDone] = useState(false)
   const [modelTrained, setModelTrained] = useState(false)
   const [predicting, setPredicting] = useState(false)
   const [predictionResult, setPredictionResult] = useState<any>(null)
   const [singleInput, setSingleInput] = useState<number[]>([0, 0, 0, 0, 0])
   const [singlePrediction, setSinglePrediction] = useState<number | null>(null)

Batch Prediction
~~~~~~~~~~~~~~~~

**Process:**

.. code-block:: typescript

   const handleBatchPrediction = async () => {
     setPredicting(true)
     setPredictionResult(null)

     const response = await fetch('http://localhost:8000/start-predict/', {
       method: 'POST'
     })

     const data = await response.json()
     setPredictionResult(data)
     setBatchPredictionDone(true)
     setPredicting(false)
   }

**Results Display:**

* Total predictions made
* First 5 predictions preview
* Download button for full results

**Button Disabled When:**

* Prediction in progress
* No prediction data uploaded
* Model not trained
* Batch prediction already done on current dataset

Single Prediction
~~~~~~~~~~~~~~~~~

**Input Interface:**

.. code-block:: typescript

   {[0, 1, 2, 3, 4].map((i) => (
     <div key={i}>
       <label>Feature {i + 1}</label>
       <input
         type="number"
         step="0.0001"
         value={singleInput[i]}
         onChange={(e) => {
           const newInput = [...singleInput]
           newInput[i] = parseFloat(e.target.value) || 0
           setSingleInput(newInput)
         }}
       />
     </div>
   ))}

**Prediction Request:**

.. code-block:: typescript

   const handleSinglePrediction = async () => {
     setPredicting(true)

     const response = await fetch('http://localhost:8000/predict-single/', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ features: singleInput })
     })

     const data = await response.json()
     setSinglePrediction(data.prediction)
     setPredicting(false)
   }

**Result Display:**

Shows input features and predicted value in a clean layout.

Styling
-------

Global Styles
~~~~~~~~~~~~~

Location: ``src/app/globals.css``

Uses Tailwind CSS v4 with custom theme configuration:

.. code-block:: css

   @import "tailwindcss";

   @theme {
     --font-family-sans: var(--font-geist-sans);
     --font-family-mono: var(--font-geist-mono);
   }

Common Patterns
~~~~~~~~~~~~~~~

**Container Layout:**

.. code-block:: typescript

   <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-950">
     <header className="...sticky top-0 z-10">
       {/* Header content */}
     </header>
     <main className="flex-1 flex items-start justify-center px-6 py-8 overflow-y-auto">
       {/* Page content */}
     </main>
   </div>

**Cards:**

.. code-block:: typescript

   <div className="bg-white dark:bg-gray-900 shadow-lg rounded-lg p-6">
     {/* Card content */}
   </div>

**Buttons:**

.. code-block:: typescript

   // Primary button
   <button className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
     {buttonText}
   </button>

   // Disabled button
   <button
     disabled={isDisabled}
     className="...disabled:opacity-50 disabled:cursor-not-allowed"
   >
     {buttonText}
   </button>

**Form Inputs:**

.. code-block:: typescript

   <input
     type="number"
     className="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
   />

Error Handling
--------------

All components implement consistent error handling:

.. code-block:: typescript

   try {
     const response = await fetch(url, options)

     if (!response.ok) {
       throw new Error(`HTTP error! status: ${response.status}`)
     }

     const data = await response.json()
     // Handle success
   } catch (error) {
     console.error('Error:', error)
     setError(error.message)
   }

Error messages are displayed to users in red alert boxes:

.. code-block:: typescript

   {error && (
     <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
       <p className="text-red-800">{error}</p>
     </div>
   )}

Responsive Design
-----------------

All components are responsive and work on mobile devices:

* Flexible layouts using flexbox
* Responsive padding and margins
* Mobile-friendly form controls
* Readable font sizes on all screens

Dark Mode
---------

Full dark mode support using Tailwind's dark variant:

.. code-block:: typescript

   <div className="bg-white dark:bg-gray-900">
     <p className="text-gray-900 dark:text-gray-100">Content</p>
   </div>

Best Practices
--------------

The frontend follows these practices:

* TypeScript for type safety
* React hooks for state management
* Async/await for API calls
* Loading states for better UX
* Error handling and display
* Responsive design
* Dark mode support
* Accessible form controls
* Clean code organization

Development
-----------

**Start Dev Server:**

.. code-block:: bash

   cd frontend
   npm run dev

**Build for Production:**

.. code-block:: bash

   npm run build
   npm start

**Linting:**

.. code-block:: bash

   npm run lint

Next Steps
----------

* :doc:`backend` - Backend API reference
* :doc:`neural_network` - Neural network module
* :doc:`../usage` - Usage guide
