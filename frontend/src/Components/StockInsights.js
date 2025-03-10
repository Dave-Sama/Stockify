import React, { useState, useEffect } from 'react';

const StockInsights = ({ ticker, filterType, period, startDate, endDate }) => {
  const [insights, setInsights] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchInsights = async () => {
      if (!ticker) return;

      const query = filterType === 'period' ? `period=${period}` : `start=${startDate}&end=${endDate}`;
      try {
        const response = await fetch(`http://localhost:5000/api/insights/${ticker}?${query}`);
        const data = await response.json();
        if (data.error) {
          setError(data.error);
          setInsights(null);
        } else {
          setInsights(data);
          setError(null);
        }
      } catch (err) {
        setError('Failed to fetch insights');
        setInsights(null);
      }
    };

    fetchInsights();
  }, [ticker, filterType, period, startDate, endDate]);

  return (
    <div className="stock-insights">
      {error && <div className="error">{error}</div>}
      {insights && (
        <div>
          <h2>Insights for {insights.ticker}</h2>
          <div>
            <h3>Volatility</h3>
            <p>{insights.volatility.annualized_volatility_percent}%</p>
            <p>{insights.volatility.description}</p>
          </div>
          <div>
            <h3>Trend</h3>
            <p>{insights.trend.direction}</p>
            <p>{insights.trend.description}</p>
          </div>
          <div>
            <h3>Anomalies</h3>
            <p>High Volume Dates: {insights.anomalies.high_volume_dates.join(', ') || 'None'}</p>
            <p>{insights.anomalies.description}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default StockInsights;