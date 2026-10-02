function AnalysisResult({ result, language }) {

    if (!result) {
        return null;
    }
    const isSinhala = language === "si";
    const analysis = result.analysis;
    const medicalData = result.medical_data;

    return (
        <div className="result-card">

            <h2>
                {isSinhala
                    ? "විශ්ලේෂණ ප්‍රතිඵල"
                    : "Analysis Results"}
            </h2>

            {/* Patient Information */}
            <section>

                <h3>
                    {isSinhala
                        ? "රෝගියාගේ තොරතුරු"
                        : "Patient Information"}
                </h3>

                <p>
                    <strong>
                        {isSinhala ? "නම" : "Name"}:
                    </strong>{" "}
                    {medicalData?.patient?.name || "-"}
                </p>

                <p>
                    <strong>
                        {isSinhala ? "වයස" : "Age"}:
                    </strong>{" "}
                    {medicalData?.patient?.age || "-"}
                </p>

                <p>
                    <strong>
                        {isSinhala ? "ස්ත්‍රී / පුරුෂ" : "Gender"}:
                    </strong>{" "}
                    {medicalData?.patient?.gender || "-"}
                </p>

                <p>
                    <strong>
                        {isSinhala
                            ? "වාර්තා දිනය"
                            : "Report Date"}:
                    </strong>{" "}
                    {medicalData?.report_date || "-"}
                </p>

            </section>

            {/* Summary */}
            <section>

                <h3>
                    {isSinhala
                        ? "සාරාංශය"
                        : "Summary"}
                </h3>

                <p>
                    {analysis?.summary}
                </p>

            </section>

            {/* Test Results */}
            <section>

                <h3>
                    {isSinhala
                        ? "පරීක්ෂණ ප්‍රතිඵල"
                        : "Test Results"}
                </h3>

                <div className="table-wrapper">

                    <table>

                        <thead>
                            <tr>

                                <th>
                                    {isSinhala
                                        ? "පරීක්ෂණය"
                                        : "Test"}
                                </th>

                                <th>
                                    {isSinhala
                                        ? "අගය"
                                        : "Value"}
                                </th>

                                <th>
                                    {isSinhala
                                        ? "ඒකකය"
                                        : "Unit"}
                                </th>

                                <th>
                                    {isSinhala
                                        ? "සාමාන්‍ය පරාසය"
                                        : "Reference Range"}
                                </th>

                                <th>
                                    {isSinhala
                                        ? "තත්ත්වය"
                                        : "Status"}
                                </th>

                                <th>
                                    {isSinhala
                                        ? "විස්තරය"
                                        : "Explanation"}
                                </th>

                            </tr>
                        </thead>

                        <tbody>

                            {analysis?.results?.map(
                                (test, index) => (

                                    <tr key={index}>

                                        <td>
                                            {test.name}
                                        </td>

                                        <td>
                                            {test.value}
                                        </td>

                                        <td>
                                            {test.unit}
                                        </td>

                                        <td>
                                            {test.reference_range}
                                        </td>

                                        <td>
                                            {test.status}
                                        </td>

                                        <td>
                                            {test.explanation}
                                        </td>

                                    </tr>

                                )
                            )}

                        </tbody>

                    </table>

                </div>

            </section>

            {/* Important Notes */}
            <section>

                <h3>
                    {isSinhala
                        ? "වැදගත් සටහන්"
                        : "Important Notes"}
                </h3>

                <ul>

                    {analysis?.important_notes?.map(
                        (note, index) => (
                            <li key={index}>
                                {note}
                            </li>
                        )
                    )}

                </ul>

            </section>

            {/* Disclaimer */}
            <section className="disclaimer">

                <h3>
                    {isSinhala
                        ? "වියාචනය"
                        : "Disclaimer"}
                </h3>

                <p>
                    {analysis?.disclaimer}
                </p>

            </section>

        </div>
    );
}

export default AnalysisResult;