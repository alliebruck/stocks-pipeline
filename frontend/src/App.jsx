import { useEffect, useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "";

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

  return (
    <main className="page">
      <section className="card">
        <h1>Top Stock Movers</h1>
        <p className="subtitle">
          Daily stock analytics dashboard powered by AWS Lambda, DynamoDB, and API Gateway.
        </p>

        {loading && <p>Loading movers...</p>}
        {error && <p className="error">{error}</p>}

        {!loading && !error && (
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
        )}
      </section>
    </main>
  );
}

export default App;
