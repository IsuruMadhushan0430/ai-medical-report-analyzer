import { useState } from "react";

function UploadForm({ onResult }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];

        if (!selectedFile) {
            return;
        }

        if (selectedFile.type !== "application/pdf") {
            setError("Please select a PDF file.");
            setFile(null);
            return;
        }

        if (selectedFile.size > 10 * 1024 * 1024) {
            setError("File size must be less than 10 MB.");
            setFile(null);
            return;
        }

        setError("");
        setFile(selectedFile);
    };

    const handleUpload = async () => {
        if (!file) {
            setError("Please select a PDF file.");
            return;
        }

        setLoading(true);
        setError("");

        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/upload",
                {
                    method: "POST",
                    body: formData,
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Upload failed.");
            }

            onResult(data);
        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-card">
            <h2>Upload Medical Report</h2>

            <p className="upload-description">
                Upload a medical report in PDF format for educational
                analysis and explanation.
            </p>

            <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
            />

            {file && (
                <p className="selected-file">
                    Selected: {file.name}
                </p>
            )}

            {error && (
                <div className="error-message">
                    {error}
                </div>
            )}

            <button
                onClick={handleUpload}
                disabled={loading}
            >
                {loading ? "Analyzing..." : "Analyze Report"}
            </button>
        </div>
    );
}

export default UploadForm;