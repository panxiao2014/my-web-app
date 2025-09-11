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
      setMessage("Error connecting to the backend");
    }
  };

  return (
    <div className="min-h-screen p-4">
      <div className="flex items-center gap-4">
        <button
          onClick={handleClick}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition-colors duration-200"
        >
          Click me
        </button>
        <span className="text-xl font-bold text-gray-800 dark:text-gray-200 bg-gray-100 dark:bg-gray-800 px-4 py-2 rounded-lg border border-gray-200 dark:border-gray-700">
          {message}
        </span>
      </div>
    </div>
  );
}

export default App;
