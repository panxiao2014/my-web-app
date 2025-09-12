import { useState, useCallback } from "react";
import { getPing } from "../services/api";

export function usePing() {
  const [message, setMessage] = useState("");
  const [error, setError] = useState(null);

  const fetchPing = useCallback(async () => {
    setError(null);
    try {
      const data = await getPing();
      setMessage(data.message ?? "");
    } catch (e) {
      setError(e);
      setMessage("");
    }
  }, []);

  return { message, error, fetchPing };
}


