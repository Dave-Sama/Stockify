import React from "react";

function FilterForm({
  ticker,
  setTicker,
  filterType,
  setFilterType,
  period,
  setPeriod,
  startDate,
  setStartDate,
  endDate,
  setEndDate,
  plotType,
  setPlotType,
  handleSubmit,
}) {
  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Ticker:</label>
        <input
          type="text"
          value={ticker}
          onChange={(e) => setTicker(e.target.value.toUpperCase())}
          placeholder="e.g., NVDA"
          required
        />
      </div>
      <div className="form-group">
        <label>Filter Type:</label>
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
        >
          <option value="period">Period</option>
          <option value="dates">Start/End Dates</option>
        </select>
      </div>
      {filterType === "period" ? (
        <div className="form-group">
          <label>Period:</label>
          <select value={period} onChange={(e) => setPeriod(e.target.value)}>
            <option value="1mo">1 Month</option>
            <option value="3mo">3 Months</option>
            <option value="6mo">6 Months</option>
            <option value="1y">1 Year</option>
          </select>
        </div>
      ) : (
        <>
          <div className="form-group">
            <label>Start Date:</label>
            <input
              type="date"
              value={startDate}
              onChange={(e) => setStartDate(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label>End Date:</label>
            <input
              type="date"
              value={endDate}
              onChange={(e) => setEndDate(e.target.value)}
              required
            />
          </div>
        </>
      )}
      <div className="form-group">
        <label>Plot Type:</label>
        <select value={plotType} onChange={(e) => setPlotType(e.target.value)}>
          <option value="close">Close (Candlestick)</option>
          <option value="volume">Volume</option>
          <option value="moving_average">Moving Average</option>
          <option value="volume_weighted">Volume-Weighted Price</option>
        </select>
      </div>
      <button type="submit" disabled={!ticker}>
        Generate Plot
      </button>
    </form>
  );
}

export default FilterForm;
