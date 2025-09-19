import { useState, useCallback } from "react";
import { addUserApi, getRandomUserApi } from "../services/api";
import { isNameValid, isAgeValid } from "../utils/utils";


export function useAddUser() {
  const [userForm, setUserForm] = useState({ name: "", gender: "Male", age: "" });
  const [addUserError, setError] = useState(null);

  const updateField = useCallback((field, value) => {
    setUserForm((prev) => ({ ...prev, [field]: value }));
  }, []);

  const addUser = useCallback(async () => {
    setError(null);
    if (!isNameValid(userForm.name)) {
      setError(new Error("Name must not be empty and must start with a letter (a-z or A-Z)."));
      return;
    }
    if (!isAgeValid(userForm.age)) {
      setError(new Error("Age must be between 0 and 100."));
      return;
    }
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

  // Provide a hook-friendly isNameValid for consumers, bound to current name
  const isNameValidForForm = useCallback(() => isNameValid(userForm.name), [userForm.name]);

  return { userForm, addUserError, updateField, addUser, isNameValid: isNameValidForForm };
}

export function useRandomUser() {
  const [randomUser, setRandomUser] = useState(null);
  const [randomUserError, setError] = useState(null);

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

  return { randomUser, randomUserError, fetchRandomUser };
}


