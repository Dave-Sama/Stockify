import React, { useState } from 'react';
import Header from './Components/Header/Header'
import StockPlot from './Components/StockPlot'
import './App.css';
import FilterForm from './Components/Form/FilterForm';

function App() {

  const [ticker, setTicker] = useState("");
  const [filterType, setFilterType] = useState("period");
  const [period, setPeriod] = useState("1mo");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [plotType, setPlotType] = useState("close");
  const [showPlot, setShowPlot] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(startDate)
    console.log(endDate)
    setShowPlot(true); // Trigger plot display
  };

  return (
    <div className="App">
     <Header />
      <FilterForm ticker={ticker} setTicker={setTicker} filterType={filterType} setFilterType={setFilterType} period={period} setPeriod={setPeriod} startDate={startDate} setStartDate={setStartDate} endDate={endDate} setEndDate={setEndDate} plotType={plotType} showPlot={showPlot} setPlotType={setPlotType} handleSubmit={handleSubmit}/>
      {showPlot && (
      <StockPlot
        ticker={ticker}
        filterType={filterType}
        period={period}
        startDate={startDate}
        endDate={endDate}
        plotType={plotType}
      />
    )}
    </div>
  );
}

export default App;