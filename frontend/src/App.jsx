import { useState } from "react";
import UploadForm from "./components/UploadForm";
import AnalysisResult from "./components/AnalysisResult";

function App() {
    const [result, setResult] = useState(null);

    return (
        <div className="app">

            <header className="header">
                <div className="container">
                    <h1>AI Medical Report Analyzer</h1>

                    <p>
                        Upload a medical report and receive
                        AI-powered educational explanations.
                    </p>
                </div>
            </header>

            <main className="container">

                <UploadForm onResult={setResult} />

                {result && (
                    <AnalysisResult result={result} />
                )}

            </main>

            <footer className="footer">
                <p>
                    AI Medical Report Analyzer © 2026
                </p>

                <p>
                    For educational purposes only. Not a substitute
                    for professional medical advice.
                </p>
            </footer>

        </div>
    );
}

export default App;