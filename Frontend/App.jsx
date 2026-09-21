import { useState } from "react";
import "./App.css";
import { MapContainer, TileLayer, Marker, Popup, Polyline }
 from "react-leaflet";
 import "leaflet/dist/leaflet.css";
 import Dashboard from "./Dashboard";

function App() {
  console.log("Current Path:", window.location.pathname);

  const [startPoint, setStartPoint] = useState("");
  const [destination, setDestination] = useState("");
  const [destinations, setDestinations] = useState([]);
  const [showDashboard, setShowDashboard] = useState(false);
  const [route, setRoute] = useState([]);
  const [vehicles, setVehicles] = useState([]);

  const [distance, setDistance] = useState(18.5);
  const [estimatedTime, setEstimatedTime] = useState(42);
  const [stops, setStops] = useState(3);

  
   const handleRoute = async () => {
  if (!startPoint || (!destination && destinations.length === 0)) {
    alert("Please enter starting point and destination");
    return;
  }

  console.log("Starting Point:", startPoint);
  console.log("Destinations:", destinations);

  setStops(destinations.length +
    (destination.trim()? 1: 0)
  );
  setDistance(18.5 + destinations.length * 7.2);
setEstimatedTime(42 + destinations.length * 15);

  setVehicles([
    {
      id: "Vehicle 1",
      color: "#00008B",
      routePath: [
        [12.9766, 77.5713],
        [12.9730, 77.6500],
        [12.9698, 77.7500]
      ]
    },
    {
      id: "Vehicle 2",
      color: "#F97316",
      routePath: [
        [12.9766, 77.5713],
        [12.9900, 77.6600],
        [12.9698, 77.7500]
      ]
    },
    {
      id: "Vehicle 3",
      color: "#006400",
      routePath: [
        [12.9766, 77.5713],
        [12.9400, 77.6600],
        [12.9698, 77.7500]
      ]
    }
  ]);
};
if (showDashboard) {
  return <Dashboard/> ;
}
  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>OptiRoute</h1>
          <p>Smart Route Planning & Optimization</p>
        </div>

        <div className="city">
          📍 Bengaluru
        </div>
        <button
  className="dashboard-btn"
  onClick={() => setShowDashboard(true)}
>
  📊 Dashboard
</button>

      </header>

      <main className="dashboard">
        <section className="control-panel">
          <h2>Plan Your Route</h2>

          <label>Starting Point</label>
          <input
            type="text"
            placeholder="Enter starting location"
            value={startPoint}
            onChange={(e) =>
              setStartPoint(e.target.value)
            }
          />

          <label>Destination</label>
          <input
            type="text"
            placeholder="Enter destination"
            value={destination}
            onChange={(e) => setDestination(e.target.value)}
          />
          {destinations.length > 0 && (
  <div className="destination-list">
    {destinations.map((item, index) => (
      <div className="destination-item" key={index}>
        📍 {item}
      </div>
    ))}
  </div>
)}

          <button
  className="add-btn"
  onClick={() => {
    if (!destination.trim()) {
      alert("Please enter a destination first");
      return;
    }

    setDestinations([...destinations, destination]);
    setDestination("");
  }}
>
  + Add Destination
</button>

          <button className="optimize-btn"
            onClick={handleRoute}>
            ⚡ Optimize Route
          </button>

          <div className="route-info">
            <h3>Route Summary</h3>
            <div className="info-row">
              <span>Distance</span>
              <strong>{distance} km</strong>
            </div>
            <div className="info-row">
              <span>Estimated Time</span>
              <strong>{estimatedTime} min</strong>
            </div>
            <div className="info-row">
              <span>Stops</span>
              <strong>{stops}</strong>
            </div>
          </div>
        </section>

        <section className="map-section">
          <MapContainer
  center={[12.9716, 77.5946]}
  zoom={12}
  className="map"
  style={{height: "100%", width:"100%"}}
>
  <TileLayer
    attribution='&copy; OpenStreetMap contributors'
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
  />
  <Marker position={[12.9716, 77.5946]}>
  <Popup>
    Starting Point - Bengaluru
  </Popup>
</Marker>
<Marker position={[12.9352, 77.6245]}>
  <Popup>
    Destination
  </Popup>
</Marker>
{vehicles.map((vehicle) => (
  <Polyline
    key={vehicle.id}
    positions={vehicle.routePath}
    color={vehicle.color}
    weight={7}
  />
))}
  
</MapContainer>
        </section>
      </main>
    </div>
  );
}

export default App;