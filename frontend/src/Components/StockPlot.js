import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

const StockPlot = ({ ticker, filterType, period, startDate, endDate, plotType, maWindow }) => {
  const [plotData, setPlotData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchPlot = async () => {
      if (!ticker) return;

      const payload = {
        ticker,
        plot_type: plotType,
        ...(filterType === 'period' ? { period } : { start: startDate, end: endDate }),
        ...(plotType === 'moving_average' && maWindow ? { ma_window: maWindow } : {}),
      };
      try {
        const response = await fetch('http://localhost:5000/api/plot', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        if (data.error) {
          setError(data.error);
          setPlotData(null);
        } else {
          setPlotData(data.plot);
          setError(null);
        }
      } catch (err) {
        setError('Failed to fetch plot');
        setPlotData(null);
      }
    };

    fetchPlot();
  }, [ticker, filterType, period, startDate, endDate, plotType, maWindow]);

  return (
    <div className="stock-plot">
      {error && <div className="error">{error}</div>}
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
};

export default StockPlot;