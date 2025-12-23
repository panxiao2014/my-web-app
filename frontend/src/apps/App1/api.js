export async function sendPing() {
  try {
    const response = await fetch(`/api/app1/ping`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error('Error sending ping:', error);
    throw error;
  }
}