import { useState } from "react";
import Spreadsheet from "react-spreadsheet";
import type { Matrix, CellBase } from "react-spreadsheet";

function App() {
  const [data, setData] = useState<Matrix<CellBase>>([
    [{ value: "" }, { value: "" }],
    [{ value: "" }, { value: "" }],
    [{ value: "" }, { value: "" }],
  ]);

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const [selectedGraph, setSelectedGraph] = useState<"boxplot" | "scatter">("boxplot");

  const handleChange = (newData: Matrix<CellBase>) => {
    setData(newData);
  };

  const columnLabels = data[0]?.map((_, i) => `#${i + 1}`);

  const runAnalysis = async () => {
    setLoading(true);
    setError("");
    setResult(null);

    const columnCount = data[0]?.length ?? 0;
    const groups = Array.from({ length: columnCount }, (_, colIndex) => {
      const values = data
        .map((row) => row[colIndex]?.value)
        .filter((v) => v !== undefined && v !== "")
        .map((v) => Number(v));
      return { name: `Group${colIndex + 1}`, values };
    });

    try {
      const response = await fetch("http://localhost:8080/api/analyses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ groups, method: "basic", options: {} }),
      });

      if (!response.ok) {
        throw new Error("解析リクエストに失敗しました");
      }

      const json = await response.json();
      setResult(json);
    } catch (e) {
      setError(e instanceof Error ? e.message : "不明なエラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>統計解析アプリ</h1>

      <Spreadsheet data={data} onChange={handleChange} columnLabels={columnLabels} />

      <button onClick={runAnalysis} style={{ marginTop: "20px" }} disabled={loading}>
        {loading ? "解析中..." : "解析実行"}
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && result.status === "success" && (
        <div style={{ marginTop: "20px" }}>
          <h2>結果</h2>


         {result && result.status === "success" && (
  <div style={{ marginTop: "20px" }}>
    <h2>結果</h2>
    <div style={{ display: "flex", justifyContent: "center" }}>
      <table border={1} cellPadding={6}>

            <thead>
              <tr>
                <th>群</th>
                <th>平均</th>
                <th>中央値</th>
                <th>標準偏差</th>
                <th>分散</th>
                <th>最小</th>
                <th>最大</th>
                <th>n</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(result.result).map(([name, stats]: [string, any]) => (
                <tr key={name}>
                  <td>{name}</td>
                  <td>{stats.mean.toFixed(2)}</td>
                  <td>{stats.median.toFixed(2)}</td>
                  <td>{stats.sd.toFixed(2)}</td>
                  <td>{stats.variance.toFixed(2)}</td>
                  <td>{stats.min}</td>
                  <td>{stats.max}</td>
                  <td>{stats.n}</td>
                </tr>
              ))}
            </tbody>
            </table>
</div>

{/* タブ(プルダウン)とグラフを横並びに配置 */}
{result.graphs && (
  <div style={{ display: "flex", justifyContent: "center", alignItems: "flex-start", marginTop: "20px", gap: "16px" }}>
    <img
      src={`data:image/png;base64,${result.graphs[selectedGraph].base64}`}
      alt={selectedGraph}
      style={{ maxWidth: "600px" }}
    />

    <select
      value={selectedGraph}
      onChange={(e) => setSelectedGraph(e.target.value as "boxplot" | "scatter")}
      style={{ marginTop: "20px" }}
    >
      <option value="boxplot">箱ひげ図</option>
      <option value="scatter">散布図</option>
    </select>
  </div>
)}
  </div>
)}
        </div>
      )}
    </div>
  );
}

export default App;