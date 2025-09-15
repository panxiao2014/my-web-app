import { useState, useCallback } from "react";
import { addUserApi, getRandomUserApi } from "../services/api";

export function useAddUser() {
  const [userForm, setUserForm] = useState({ name: "", gender: "Male", age: "" });
  const [error, setError] = useState(null);

  const updateField = useCallback((field, value) => {
    setUserForm((prev) => ({ ...prev, [field]: value }));
  }, []);

  const addUser = useCallback(async () => {
    setError(null);
    try {
      await addUserApi({
        name: userForm.name,
        gender: userForm.gender,
        age: userForm.age,
      });
    } catch (e) {
      setError(e);
    }
  }, [userForm]);

  return { userForm, error, updateField, addUser };
}

export function useRandomUser() {
  const [randomUser, setRandomUser] = useState(null);
  const [error, setError] = useState(null);

  const fetchRandomUser = useCallback(async () => {
    setError(null);
    try {
      const user = await getRandomUserApi();
      setRandomUser(user);
    } catch (e) {
      setError(e);
      setRandomUser(null);
    }
  }, []);

  return { randomUser, error, fetchRandomUser };
}


