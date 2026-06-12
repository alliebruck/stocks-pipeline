import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "";

function formatDate(dateString) {
  const date = new Date(`${dateString}T00:00:00`);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
  });
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload || payload.length === 0) {
    return null;
  }

  const data = payload[0].payload;

  return (
    <div className="custom-tooltip">
      <p className="tooltip-date">{formatDate(label)}</p>
      <p>
        <strong>{data.ticker}</strong>: {data.percent_change}%
      </p>
      <p>Close: ${data.closing_price}</p>
    </div>
  );
}

function App() {
  const [movers, setMovers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  

  useEffect(() => {
    async function fetchMovers() {
      try {
        if (!API_URL) {
          throw new Error("Missing VITE_API_URL");
        }

        const response = await fetch(API_URL);

        if (!response.ok) {
          throw new Error("Failed to fetch movers");
        }

        const data = await response.json();
        setMovers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    fetchMovers();
  }, []);

  const biggestMove =
    movers.length > 0
      ? movers.reduce((max, mover) =>
          Math.abs(mover.percent_change) > Math.abs(max.percent_change)
            ? mover
            : max
        )
      : null;

  const winnerCounts = movers.reduce((acc, mover) => {
    acc[mover.ticker] = (acc[mover.ticker] || 0) + 1;
    return acc;
  }, {});

  const topWinner =
    movers.length > 0
    ? Object.entries(winnerCounts).reduce(
        (best, current) => (current[1] > best[1] ? current : best),
        ["", 0]
      )
    : null;
  
    
  return (
    <main className="page">
      <section className="card">
        <h1>Top Stock Movers</h1>
        <hr />
        <p className="subtitle">
          Daily stock analytics dashboard powered by AWS.
        </p>

        {loading && <p>Loading movers...</p>}
        {error && <p className="error">{error}</p>}

        {!loading && !error && (
          <>
            {biggestMove && topWinner && (
              <div className="stats-row">
                <div className="stat-card">
                  <p className="summary-label">Biggest Move</p>
                  <h2>{biggestMove.ticker}</h2>
                  <p className={biggestMove.percent_change >= 0 ? "gain" : "loss"}>
                    {biggestMove.percent_change}% on {biggestMove.date}
                  </p>
                </div>

                <div className="stat-card">
                  <p className="summary-label">Most Frequent Mover</p>
                  <h2>{topWinner[0]}</h2>
                  <p>{topWinner[1]} appearances in {movers.length} days</p>
                </div>
              </div>
            )}

          

          <div className="chart-section">
          <h2>Last 7 Trading Days</h2>
            
          <div className="chart-wrapper">
              <ResponsiveContainer width="100%" height={180}>
                <LineChart
                  data={[...movers].reverse()}
                  margin={{
                    top: 10,
                    right: 20,
                    left: 10,
                    bottom: 10,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" tickFormatter={formatDate} />
                  <YAxis
                    axisLine={false}
                    tickLine={false}
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Line
                    type="monotone"
                    dataKey="percent_change"
                    name="% Change"
                    strokeWidth={3}
                    dot={{ r: 5 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Ticker</th>
                  <th>% Change</th>
                  <th>Closing Price</th>
                </tr>
              </thead>
              <tbody>
                {movers.map((mover) => (
                  <tr key={mover.date}>
                    <td>{mover.date}</td>
                    <td className="ticker">{mover.ticker}</td>
                    <td className={mover.percent_change >= 0 ? "gain" : "loss"}>
                      {mover.percent_change}%
                    </td>
                    <td>${mover.closing_price}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </>
        )}
      </section>
    </main>
  );
}

export default App;