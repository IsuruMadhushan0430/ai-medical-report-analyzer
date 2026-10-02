import { useState } from "react";

function UploadForm({ setResult, language, setLanguage }) {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleFileChange = (event) => {
        const selectedFile = event.target.files[0];

        if (!selectedFile) {
            return;
        }

        const allowedTypes = [
            "application/pdf",
            "image/jpeg",
            "image/png"
        ];

        if (!allowedTypes.includes(selectedFile.type)) {
            setError("Only PDF, JPG, JPEG, and PNG files are allowed.");
            setFile(null);
            return;
        }

        setFile(selectedFile);
        setError("");
        setResult(null);
    };

    const handleUpload = async (event) => {
        event.preventDefault();

        if (!file) {
            setError(
                language === "si"
                    ? "කරුණාකර වාර්තාවක් තෝරන්න."
                    : "Please select a medical report."
            );
            return;
        }

        setLoading(true);
        setError("");
        setResult(null);

        const formData = new FormData();

        formData.append("file", file);
        formData.append("language", language);

        try {
            const response = await fetch(
                "http://127.0.0.1:8000/upload",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(
                    data.detail || "Something went wrong."
                );
            }

            setResult(data);

        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="upload-card">

            <h2>
                {language === "si"
                    ? "වෛද්‍ය වාර්තාව විශ්ලේෂණය"
                    : "Medical Report Analysis"}
            </h2>

            {/* Language Selector */}
            <div className="form-group">
                <label>
                    {language === "si"
                        ? "භාෂාව"
                        : "Language"}
                </label>

                <select
                    value={language}
                    onChange={(e) => {
                        setLanguage(e.target.value);
                        setError("");
                    }}
                >
                    <option value="en">English</option>
                    <option value="si">සිංහල</option>
                </select>
            </div>

            {/* File Upload */}
            <div className="form-group">

                <label>
                    {language === "si"
                        ? "වෛද්‍ය වාර්තාව තෝරන්න"
                        : "Select Medical Report"}
                </label>

                <input
                    type="file"
                    accept=".pdf,.jpg,.jpeg,.png"
                    onChange={handleFileChange}
                />

            </div>

            {/* Selected File */}
            {file && (
                <p className="selected-file">
                    {language === "si"
                        ? `තෝරාගත් ගොනුව: ${file.name}`
                        : `Selected file: ${file.name}`}
                </p>
            )}

            {/* Error */}
            {error && (
                <p className="error-message">
                    {error}
                </p>
            )}

            {/* Submit */}
            <button
                type="button"
                onClick={handleUpload}
                disabled={loading}
            >
                {loading
                    ? language === "si"
                        ? "විශ්ලේෂණය කරමින්..."
                        : "Analyzing..."
                    : language === "si"
                        ? "වාර්තාව විශ්ලේෂණය කරන්න"
                        : "Analyze Report"}
            </button>

        </div>
    );
}

export default UploadForm;