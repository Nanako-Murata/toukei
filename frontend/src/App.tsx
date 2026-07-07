import { useState } from "react";
import Spreadsheet from "react-spreadsheet";
import type { Matrix, CellBase } from "react-spreadsheet";
import "./App.css";

function App() {
  const [data, setData] = useState<Matrix<CellBase>>([
    [{ value: "" }, { value: "" }],
    [{ value: "" }, { value: "" }],
    [{ value: "" }, { value: "" }],
  ]);

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>("");
  const [selectedGraph, setSelectedGraph] = useState<"boxplot" | "scatter" | "heatmap">("boxplot");
  const [paired, setPaired] = useState(false);
  const [yColumnIndex, setYColumnIndex] = useState<number>(0);
  const rowLabels = data.map((_, i) => `R${i + 1}`);
  const [method, setMethod] = useState<
    "basic" | "ttest" | "correlation" | "regression" | "multiple_regression" | "anova" | "chisquare"
  >("basic");

  const downloadCsv = () => {
    if (!result || result.status !== "success") return;

    let csvContent = "";

    if (result.method === "basic") {
      csvContent = "群,平均,中央値,標準偏差,分散,最小,最大,n\n";
      Object.entries(result.result).forEach(([name, stats]: [string, any]) => {
        csvContent += `${name},${stats.mean},${stats.median},${stats.sd},${stats.variance},${stats.min},${stats.max},${stats.n}\n`;
      });
    } else if (result.method === "ttest") {
      csvContent = "項目,値\n";
      csvContent += `t統計量,${result.result.statistic}\n`;
      csvContent += `p値,${result.result.pValue}\n`;
      csvContent += `自由度,${result.result.degreesOfFreedom}\n`;
    } else if (result.method === "correlation") {
      const labels = result.result.labels;
      csvContent = "," + labels.map((_: string, i: number) => `#${i + 1}`).join(",") + "\n";
      labels.forEach((rowName: string, i: number) => {
        const row = labels.map((colName: string) => result.result.correlation[rowName][colName]);
        csvContent += `#${i + 1},${row.join(",")}\n`;
      });
    } else if (result.method === "regression") {
      csvContent = "項目,値\n";
      csvContent += `傾き,${result.result.slope}\n`;
      csvContent += `切片,${result.result.intercept}\n`;
      csvContent += `決定係数(R2),${result.result.rSquared}\n`;
      csvContent += `p値,${result.result.pValue}\n`;
    } else if (result.method === "multiple_regression") {
      csvContent = "項目,係数,p値\n";
      csvContent += `切片,${result.result.intercept},${result.result.interceptPValue}\n`;
      Object.entries(result.result.coefficients).forEach(([name, c]: [string, any]) => {
        csvContent += `${name},${c.coefficient},${c.pValue}\n`;
      });
    } else if (result.method === "anova") {
      csvContent = "項目,値\n";
      csvContent += `F統計量,${result.result.statistic}\n`;
      csvContent += `p値,${result.result.pValue}\n`;
    } else if (result.method === "chisquare") {
      csvContent = "観測値\n";
      csvContent += "," + result.result.observed[0].map((_: number, j: number) => `#${j + 1}`).join(",") + "\n";
      result.result.observed.forEach((row: number[], i: number) => {
        csvContent += `R${i + 1},${row.join(",")}\n`;
      });
      csvContent += `\nカイ二乗統計量,${result.result.statistic}\n`;
      csvContent += `p値,${result.result.pValue}\n`;
    }

    const bom = "\uFEFF";
    const blob = new Blob([bom + csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${result.method}_result.csv`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const downloadGraph = (base64: string, filename: string) => {
    const link = document.createElement("a");
    link.href = `data:image/png;base64,${base64}`;
    link.download = filename;
    link.click();
  };

  const addRow = () => {
    const columnCount = data[0]?.length ?? 1;
    const newRow = Array.from({ length: columnCount }, () => ({ value: "" }));
    setData([...data, newRow]);
  };

  const addColumn = () => {
    const newData = data.map((row) => [...row, { value: "" }]);
    setData(newData);
  };

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
        body: JSON.stringify({
          groups,
          method,
          options:
            method === "ttest"
              ? { paired }
              : method === "multiple_regression"
                ? { yColumnIndex }
                : {},
        }),
      });

      if (!response.ok) {
        throw new Error("解析リクエストに失敗しました");
      }

      const json = await response.json();

      if (json.status === "error") {
        setError(json.message || "解析中にエラーが発生しました");
        return;
      }

      setResult(json);
    } catch (e) {
      setError(e instanceof Error ? e.message : "不明なエラーが発生しました");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">統計解析アプリ</h1>
      <p className="app-subtitle">数値データを入力し、解析手法を選んで実行してください</p>

      <div className="section">
        <div style={{ display: "flex", gap: "8px", marginTop: "10px" }}>
          <button onClick={addRow} type="button">行を追加</button>
          <button onClick={addColumn} type="button">列を追加</button>
        </div>
        <span className="section-label">Data</span>
        <Spreadsheet
          data={data}
          onChange={handleChange}
          columnLabels={columnLabels}
          rowLabels={rowLabels}
        />
      </div>

      <div className="section">
        <span className="section-label">Method</span>
        <div className="method-row">
          <label>
            解析手法:
            <select value={method} onChange={(e) => setMethod(e.target.value as any)}>
              <option value="basic">基礎統計</option>
              <option value="ttest">t検定</option>
              <option value="correlation">相関分析</option>
              <option value="regression">単回帰分析</option>
              <option value="multiple_regression">重回帰分析</option>
              <option value="anova">ANOVA(分散分析)</option>
              <option value="chisquare">カイ二乗検定</option>
            </select>

            {method === "multiple_regression" && (
              <label style={{ marginLeft: "16px" }}>
                目的変数(Y):
                <select
                  value={yColumnIndex}
                  onChange={(e) => setYColumnIndex(Number(e.target.value))}
                  style={{ marginLeft: "6px" }}
                >
                  {columnLabels?.map((label, i) => (
                    <option key={i} value={i}>
                      {label}
                    </option>
                  ))}
                </select>
              </label>
            )}
          </label>

          {method === "ttest" && (
            <label>
              <input
                type="checkbox"
                checked={paired}
                onChange={(e) => setPaired(e.target.checked)}
              />
              対応あり(paired)
            </label>
          )}
        </div>
      </div>

      <button className="run-button" onClick={runAnalysis} disabled={loading}>
        {loading ? "解析中..." : "解析実行"}
      </button>

      {error && <p className="error-message">{error}</p>}

      {result && result.status === "success" && (
        <div className="result-section">
          <span className="result-badge">{result.method}</span>

          <div style={{ marginTop: "10px", marginBottom: "10px" }}>
            <button onClick={downloadCsv} type="button">
              結果をCSVで保存
            </button>
          </div>

          {result.method === "basic" && (
            <table className="result-table">
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
          )}

          {(result.method === "basic" || result.method === "ttest" || result.method === "anova") &&
            result.graphs && (
              <div className="graph-row">
                <img
                  src={`data:image/png;base64,${result.graphs[selectedGraph].base64}`}
                  alt={selectedGraph}
                />
                <div>
                  <select
                    value={selectedGraph}
                    onChange={(e) =>
                      setSelectedGraph(e.target.value as "boxplot" | "scatter" | "heatmap")
                    }
                  >
                    <option value="boxplot">箱ひげ図</option>
                    <option value="scatter">散布図</option>
                  </select>
                  <br />
                  <button
                    onClick={() =>
                      downloadGraph(result.graphs[selectedGraph].base64, `${selectedGraph}.png`)
                    }
                    type="button"
                    style={{ marginTop: "8px" }}
                  >
                    画像を保存
                  </button>
                </div>
              </div>
            )}

          {result.method === "correlation" && (
            <div>
              <table className="result-table">
                <thead>
                  <tr>
                    <th></th>
                    {result.result.labels.map((_: string, i: number) => (
                      <th key={i}>#{i + 1}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.result.labels.map((rowName: string, i: number) => (
                    <tr key={rowName}>
                      <th>#{i + 1}</th>
                      {result.result.labels.map((colName: string) => (
                        <td key={colName}>
                          {result.result.correlation[rowName][colName].toFixed(3)}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="graph-row">
                <img
                  src={`data:image/png;base64,${result.graphs.heatmap.base64}`}
                  alt="相関ヒートマップ"
                />
              </div>
            </div>
          )}

          {result.method === "anova" && (
            <div className="stat-summary">
              <div>
                F統計量: {result.result.statistic.toFixed(3)} ／
                p値: {result.result.pValue.toFixed(4)}
              </div>
              <div className="verdict">
                {result.result.pValue < 0.05
                  ? "→ 少なくともいずれかの群間に有意差あり(p < 0.05)"
                  : "→ 群間に有意差なし(p ≥ 0.05)"}
              </div>
            </div>
          )}

          {result.method === "regression" && (
            <div>
              <div className="stat-summary">
                <div>
                  傾き(slope): {result.result.slope.toFixed(3)} ／
                  切片(intercept): {result.result.intercept.toFixed(3)}
                </div>
                <div>
                  決定係数(R²): {result.result.rSquared.toFixed(3)} ／
                  p値: {result.result.pValue.toFixed(4)}
                </div>
                <div className="verdict">
                  回帰式: y = {result.result.slope.toFixed(3)}x + {result.result.intercept.toFixed(3)}
                </div>
              </div>

              <div className="graph-row">
                <img
                  src={`data:image/png;base64,${result.graphs.regression.base64}`}
                  alt="回帰直線"
                />
              </div>
            </div>
          )}

          {result.method === "multiple_regression" && (
            <div>
              <div className="stat-summary">
                <div>
                  切片: {result.result.intercept.toFixed(3)} (p={result.result.interceptPValue.toFixed(4)})
                </div>
                {Object.entries(result.result.coefficients).map(([name, c]: [string, any]) => (
                  <div key={name}>
                    {name}: 係数 {c.coefficient.toFixed(3)} (p={c.pValue.toFixed(4)})
                  </div>
                ))}
                <div className="verdict">
                  R² = {result.result.rSquared.toFixed(3)} ／
                  調整済みR² = {result.result.adjustedRSquared.toFixed(3)} ／
                  モデル全体のp値 = {result.result.fPValue.toFixed(4)}
                </div>
              </div>

              <div className="graph-row">
                <img
                  src={`data:image/png;base64,${result.graphs.prediction.base64}`}
                  alt="予測vs実測プロット"
                />
              </div>
            </div>
          )}

          {result.method === "chisquare" && (
            <div>
              <div className="stat-summary">
                <div>
                  カイ二乗統計量: {result.result.statistic.toFixed(3)} ／
                  p値: {result.result.pValue.toFixed(4)} ／
                  自由度: {result.result.degreesOfFreedom}
                </div>
                <div className="verdict">
                  {result.result.pValue < 0.05
                    ? "→ 関連あり(独立ではない)(p < 0.05)"
                    : "→ 関連なし(独立である)(p ≥ 0.05)"}
                </div>
              </div>

              {result.result.warning && (
                <p style={{ color: "#B8860B", fontSize: "13px", marginTop: "10px" }}>
                  ⚠ {result.result.warning}
                </p>
              )}

              {result.result.fisher && (
                <div className="stat-summary" style={{ marginTop: "10px" }}>
                  <div>
                    フィッシャーの正確確率検定(参考): p値 {result.result.fisher.pValue.toFixed(4)} ／
                    オッズ比 {result.result.fisher.oddsRatio.toFixed(3)}
                  </div>
                  <div style={{ fontSize: "12px", color: "var(--text-muted)" }}>
                    (2×2表のため、近似に頼らない正確な検定結果も参考値として表示しています)
                  </div>
                </div>
              )}

              <table className="result-table" style={{ marginTop: "16px" }}>
                <thead>
                  <tr>
                    <th>観測値(行\列)</th>
                    {result.result.observed[0].map((_: number, j: number) => (
                      <th key={j}>#{j + 1}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {result.result.observed.map((row: number[], i: number) => (
                    <tr key={i}>
                      <th>R{i + 1}</th>
                      {row.map((val, j) => (
                        <td key={j}>{val}</td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;