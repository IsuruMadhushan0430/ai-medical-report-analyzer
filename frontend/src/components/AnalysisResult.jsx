function AnalysisResult({ result }) {
    if (!result) {
        return null;
    }

    const analysis = result.analysis;
    const medicalData = result.medical_data;

    return (
        <div className="results-container">

            <div className="result-card">
                <h2>Patient Information</h2>

                <div className="patient-info">
                    <p>
                        <strong>Name:</strong>{" "}
                        {medicalData?.patient?.name || "Not available"}
                    </p>

                    <p>
                        <strong>Age:</strong>{" "}
                        {medicalData?.patient?.age || "Not available"}
                    </p>

                    <p>
                        <strong>Gender:</strong>{" "}
                        {medicalData?.patient?.gender || "Not available"}
                    </p>

                    <p>
                        <strong>Report Date:</strong>{" "}
                        {medicalData?.report_date || "Not available"}
                    </p>
                </div>
            </div>

            <div className="result-card">
                <h2>Summary</h2>

                <p>
                    {analysis?.summary || "No summary available."}
                </p>
            </div>

            <div className="result-card">
                <h2>Test Results</h2>

                {analysis?.results?.length > 0 ? (
                    <div className="table-wrapper">
                        <table>
                            <thead>
                                <tr>
                                    <th>Test</th>
                                    <th>Value</th>
                                    <th>Unit</th>
                                    <th>Reference Range</th>
                                    <th>Status</th>
                                    <th>Explanation</th>
                                </tr>
                            </thead>

                            <tbody>
                                {analysis.results.map((test, index) => (
                                    <tr key={index}>
                                        <td>{test.name}</td>
                                        <td>{test.value ?? "N/A"}</td>
                                        <td>{test.unit || "N/A"}</td>
                                        <td>
                                            {test.reference_range || "N/A"}
                                        </td>
                                        <td>
                                            {test.status || "Unknown"}
                                        </td>
                                        <td>
                                            {test.explanation || "N/A"}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ) : (
                    <p>No test results available.</p>
                )}
            </div>

            <div className="result-card">
                <h2>Important Notes</h2>

                {analysis?.important_notes?.length > 0 ? (
                    <ul>
                        {analysis.important_notes.map(
                            (note, index) => (
                                <li key={index}>{note}</li>
                            )
                        )}
                    </ul>
                ) : (
                    <p>No additional notes.</p>
                )}
            </div>

            <div className="disclaimer">
                <strong>Disclaimer:</strong>{" "}
                {analysis?.disclaimer ||
                    "This application provides educational information and is not a medical diagnosis."}
            </div>

        </div>
    );
}

export default AnalysisResult;