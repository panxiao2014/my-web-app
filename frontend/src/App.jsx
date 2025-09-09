import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");

  const handleClick = async () => {
    try {
      const res = await fetch("/api/ping"); // proxy to backend
      const data = await res.json();
      setMessage(data.message);
    } catch (err) {
      console.error("Error:", err);
      setMessage("Error connecting to backend");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <button
        onClick={handleClick}
        className="px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600"
      >
        Click me
      </button>
      {message && (
        <p className="mt-4 text-xl font-bold text-gray-800">{message}</p>
      )}
    </div>
  );
}

export default App;
