import { usePing } from "./hooks/usePing";
import { useAddUser, useRandomUser } from "./hooks/userHook";

function App() {
  const { message, error, fetchPing } = usePing();
  const { userForm, updateField, addUser, addUserError } = useAddUser();
  const { randomUser, fetchRandomUser, randomUserError } = useRandomUser();

  function handleAddUser(e) {
    e.preventDefault();
    addUser();
  }

  return (
    <div className="min-h-screen p-4">
      <div className="flex items-center gap-4">
        <button
          onClick={fetchPing}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg shadow-md hover:bg-blue-600 transition-colors duration-200"
        >
          Click me
        </button>
        {message !== "" && (
          <span className="text-xl font-bold text-gray-800 dark:text-gray-200">
            {message}
          </span>
        )}
        {error && (
          <span className="text-red-600">Error connecting to the backend</span>
        )}
      </div>

      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-8">
        <div id="add-user-section" className="p-4 border rounded-lg shadow-sm bg-white/60 dark:bg-gray-800/40" data-testid="add-user-form">
          <h2 className="text-lg font-semibold mb-4">Add a user</h2>
          <form onSubmit={handleAddUser} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="name">Name</label>
              <input
                id="name"
                type="text"
                value={userForm.name}
                onChange={(e) => updateField("name", e.target.value)}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="gender">Gender</label>
              <select
                id="gender"
                value={userForm.gender}
                onChange={(e) => updateField("gender", e.target.value)}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="Male">Male</option>
                <option value="Female">Female</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-1" htmlFor="age">Age</label>
              <input
                id="age"
                type="number"
                min="0"
                max="100"
                value={userForm.age}
                onChange={(e) => updateField("age", e.target.value)}
                className="w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="0 - 100"
              />
            </div>
            <div>
              <button
                type="submit"
                className="px-4 py-2 bg-green-600 text-white rounded-lg shadow-md hover:bg-green-700 transition-colors duration-200"
              >
                Add User
              </button>
              {addUserError && (
                <div className="mt-2 text-red-600 text-sm">
                  Error: {addUserError.message}
                </div>
              )}
            </div>
          </form>
        </div>

        <div id="display-user-section" className="p-4 border rounded-lg shadow-sm bg-white/60 dark:bg-gray-800/40" data-testid="display-user-area">
          <h2 className="text-lg font-semibold mb-4">Random User</h2>
          <div className="flex items-center gap-4 mb-4">
            <button
              onClick={fetchRandomUser}
              className="px-4 py-2 bg-purple-600 text-white rounded-lg shadow-md hover:bg-purple-700 transition-colors duration-200"
            >
              Show me a user
            </button>
          </div>
          <div id="user-display-content" className="rounded-md border p-3 text-sm text-gray-800 dark:text-gray-100 min-h-[64px]" data-testid="user-display-content">
            {randomUserError ? (
              <div className="text-red-600">
                Error: {randomUserError.message}
              </div>
            ) : randomUser ? (
              <div>
                <div><span className="font-medium">Name:</span> {randomUser.name}</div>
                <div><span className="font-medium">Gender:</span> {randomUser.gender}</div>
                <div><span className="font-medium">Age:</span> {randomUser.age}</div>
              </div>
            ) : (
              <span>No user selected yet.</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
