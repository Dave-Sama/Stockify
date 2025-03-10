import React, { useState } from "react";
import Header from "./Components/Header/Header";
import StockPlot from "./Components/StockPlot";

import FilterForm from "./Components/Form/FilterForm";
import StockInsights from "./Components/StockInsights";

import "./App.css";

function App() {
  const [ticker, setTicker] = useState("");
  const [filterType, setFilterType] = useState("period");
  const [period, setPeriod] = useState("1mo");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [plotType, setPlotType] = useState("close");
  const [showPlot, setShowPlot] = useState(false);
  const [maWindow, setMaWindow] = useState(20);

  const handleSubmit = (e) => {
    e.preventDefault();
    setShowPlot(true); // Trigger plot display
  };

  return (
    <div className="App">
      <Header />
      <FilterForm
        ticker={ticker}
        setTicker={setTicker}
        filterType={filterType}
        setFilterType={setFilterType}
        period={period}
        setPeriod={setPeriod}
        startDate={startDate}
        setStartDate={setStartDate}
        endDate={endDate}
        setEndDate={setEndDate}
        plotType={plotType}
        showPlot={showPlot}
        setPlotType={setPlotType}
        handleSubmit={handleSubmit}
        maWindow={maWindow}
        setMaWindow={setMaWindow}
      />
      {showPlot && (
        <StockPlot
          ticker={ticker}
          filterType={filterType}
          period={period}
          startDate={startDate}
          endDate={endDate}
          plotType={plotType}
          maWindow={plotType === "moving_average" ? maWindow : undefined}
        />
      )}
      {showPlot && (
        <StockInsights
          ticker={ticker}
          filterType={filterType}
          period={period}
          startDate={startDate}
          endDate={endDate}
        />
      )}
    </div>
  );
}

export default App;
