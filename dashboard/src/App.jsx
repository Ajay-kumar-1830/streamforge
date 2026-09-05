import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:5000";

function App() {
  const [alerts, setAlerts] = useState([]);
  const [metrics, setMetrics] = useState({
    total: 0,
    critical: 0,
    high: 0,
    medium: 0,
    low: 0,
  });
  const [status, setStatus] = useState("Checking...");
  const [processing, setProcessing] = useState(false);

  const loadData = async () => {
    try {
      const health = await fetch(`${API_URL}/health`);
      const healthData = await health.json();

      setStatus(healthData.status);

      const response = await fetch(`${API_URL}/alerts`);
      const data = await response.json();

      setAlerts(data.alerts || []);
      setMetrics(data.metrics || {});
    } catch (error) {
      console.error(error);
      setStatus("API Offline");
    }
  };

  const runPipeline = async () => {
    try {
      setProcessing(true);

      const response = await fetch(`${API_URL}/process`, {
        method: "POST",
      });

      const data = await response.json();

      setAlerts(data.data.alerts || []);
      setMetrics(data.data.metrics || {});
      setStatus("healthy");
    } catch (error) {
      console.error(error);
      setStatus("Pipeline Error");
    } finally {
      setProcessing(false);
    }
  };

  useEffect(() => {
    loadData();

    const interval = setInterval(loadData, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="app">
      <header>
        <div>
          <h1>StreamForge</h1>
          <p>Real-Time Alert Processing Dashboard</p>
        </div>

        <div className="status">
          <span className="dot"></span>
          {status}
        </div>
      </header>

      <main>
        <section className="metrics">
          <div className="card">
            <h3>Total Alerts</h3>
            <strong>{metrics.total}</strong>
          </div>

          <div className="card critical">
            <h3>Critical</h3>
            <strong>{metrics.critical}</strong>
          </div>

          <div className="card high">
            <h3>High</h3>
            <strong>{metrics.high}</strong>
          </div>

          <div className="card medium">
            <h3>Medium</h3>
            <strong>{metrics.medium}</strong>
          </div>

          <div className="card low">
            <h3>Low</h3>
            <strong>{metrics.low}</strong>
          </div>
        </section>

        <section className="alerts-section">
          <div className="section-header">
            <h2>Recent Alerts</h2>

            <div>
              <button onClick={loadData}>Refresh</button>

              <button
                onClick={runPipeline}
                disabled={processing}
                style={{ marginLeft: "10px" }}
              >
                {processing ? "Processing..." : "Run Pipeline"}
              </button>
            </div>
          </div>

          {alerts.length === 0 ? (
            <p className="empty">No alerts available.</p>
          ) : (
            <div className="alert-list">
              {alerts.map((alert) => (
                <div className="alert" key={alert.id}>
                  <div>
                    <h3>{alert.type}</h3>
                    <p>{alert.message}</p>
                    <small>{alert.timestamp}</small>
                  </div>

                  <div className="alert-right">
                    <span className={`badge ${alert.severity}`}>
                      {alert.severity.toUpperCase()}
                    </span>
                    <p>{alert.action}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;