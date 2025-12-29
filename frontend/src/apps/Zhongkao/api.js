
export async function generateScores() {
  try {
    const response = await fetch(`/api/zhongkao/genScore`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data.scores;
  } catch (error) {
    console.error('Error generating scores:', error);
    throw error;
  }
}