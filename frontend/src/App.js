import React, { useState } from "react";
import Plot from "react-plotly.js";
import "./App.css";

function App() {
  const [ticker, setTicker] = useState("NVDA");
  const [period, setPeriod] = useState("1mo");
  const [plotType, setPlotType] = useState("close");
  const [plotData, setPlotData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("http://localhost:5000/api/plot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker, period, plot_type: plotType }),
      });
      const result = await response.json();
      if (result.error) {
        setError(result.error);
        setPlotData(null);
      } else {
        setPlotData(result.plot);
      }
    } catch (err) {
      setError("Failed to connect to backend. Is it running?");
      setPlotData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>Stock Plotter</h1>
      <form onSubmit={handleSubmit} className="stock-form">
        <div className="form-group">
          <label>Ticker:</label>
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Period:</label>
          <input
            type="text"
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            placeholder="e.g., 1mo, 1y"
          />
        </div>
        <div className="form-group">
          <label>Plot Type:</label>
          <select value={plotType} onChange={(e) => setPlotType(e.target.value)}>
            <option value="close">Close (Candlestick)</option>
            <option value="volume">Volume</option>
          </select>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Generate Plot"}
        </button>
      </form>
      {error && <p className="error">{error}</p>}
      {plotData && (
        <Plot
          data={plotData.data}
          layout={plotData.layout}
          config={{ responsive: true }}
          style={{ width: "100%", height: "800px" }}
        />
      )}
    </div>
  );
}

export default App;