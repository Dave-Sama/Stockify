import React, { useState } from "react";
import Plot from "react-plotly.js";
import "./App.css";

function App() {
  const [ticker, setTicker] = useState("NVDA");
  const [filterType, setFilterType] = useState("period"); // "period" or "dates"
  const [period, setPeriod] = useState("1mo");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [plotType, setPlotType] = useState("close");
  const [plotData, setPlotData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const payload = {
        ticker,
        plot_type: plotType,
        ...(filterType === "period" ? { period } : { start: startDate, end: endDate }),
      };
      const response = await fetch("http://localhost:5000/api/plot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
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
      <header className="app-header">
        <div className="header-left">
          <img
            src="/candlestick-chart.png"
            alt="Stock Market Icon"
            className="header-icon"
          />
          <h1>Stock Plotter</h1>
        </div>
        <nav>
          <a href="/" className="nav-link">Home</a>
          <a href="/about" className="nav-link">About</a>
        </nav>
      </header>
      <main>
        <form onSubmit={handleSubmit} className="stock-form">
          <div className="form-group">
            <label>Ticker:</label>
            <input
              type="text"
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
            />
          </div>
          <div className="filter-type">
            <label>
              <input
                type="radio"
                value="period"
                checked={filterType === "period"}
                onChange={() => setFilterType("period")}
              />
              Period
            </label>
            <label>
              <input
                type="radio"
                value="dates"
                checked={filterType === "dates"}
                onChange={() => setFilterType("dates")}
              />
              Start/End Dates
            </label>
          </div>
          {filterType === "period" ? (
            <div className="form-group">
              <label>Period:</label>
              <input
                type="text"
                value={period}
                onChange={(e) => setPeriod(e.target.value)}
                placeholder="e.g., 1mo, 1y"
              />
            </div>
          ) : (
            <>
              <div className="form-group">
                <label>Start Date:</label>
                <input
                  type="date"
                  value={startDate}
                  onChange={(e) => setStartDate(e.target.value)}
                  max={endDate || new Date().toISOString().split("T")[0]} // No future dates
                />
              </div>
              <div className="form-group">
                <label>End Date:</label>
                <input
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  min={startDate}
                  max={new Date().toISOString().split("T")[0]} // No future dates
                />
              </div>
            </>
          )}
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
      </main>
    </div>
  );
}

export default App;