import { useState } from "react";
import UploadForm from "./components/UploadForm";
import AnalysisResult from "./components/AnalysisResult";

function App() {
    const [result, setResult] = useState(null);
    const [language, setLanguage] = useState("en");

    return (
        <div className="app">

            <header className="header">
                <h1>
                    {language === "si"
                        ? "AI වෛද්‍ය වාර්තා විශ්ලේෂකය"
                        : "AI Medical Report Analyzer"}
                </h1>

                <p>
                    {language === "si"
                        ? "කෘත්‍රිම බුද්ධිය භාවිතයෙන් වෛද්‍ය වාර්තා විශ්ලේෂණය"
                        : "AI-powered medical report analysis"}
                </p>
            </header>

            <main className="container">

                <UploadForm
                    setResult={setResult}
                    language={language}
                    setLanguage={setLanguage}
                />

                {result && (
                    <AnalysisResult
                        result={result}
                        language={language}
                    />
                )}

            </main>

            <footer>
                <p>
                    {language === "si"
                        ? "අධ්‍යාපනික අරමුණු සඳහා පමණි. මෙය වෛද්‍ය රෝග විනිශ්චයක් නොවේ."
                        : "For educational purposes only. This is not a medical diagnosis."}
                </p>
            </footer>

        </div>
    );
}

export default App;