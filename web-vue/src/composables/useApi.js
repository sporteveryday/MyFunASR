import { ref, onMounted, onUnmounted } from "vue";

const DEFAULT_API_URL = "http://localhost:8000";

export function useApi() {
  const apiUrl = ref(localStorage.getItem("funasr_api_url") || DEFAULT_API_URL);
  const isConnected = ref(false);
  let connectionCheckInterval = null;

  // Check API health
  const checkConnection = async () => {
    try {
      const response = await fetch(`${apiUrl.value}/health`, { method: "GET" });
      isConnected.value = response.ok;
    } catch {
      isConnected.value = false;
    }
  };

  // Transcribe file
  const transcribeFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${apiUrl.value}/transcribe`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "识别失败");
    }

    return await response.json();
  };

  // Transcribe URL
  const transcribeUrl = async (url) => {
    const response = await fetch(`${apiUrl.value}/transcribe_url`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "识别失败");
    }

    return await response.json();
  };

  // Save API URL
  const saveApiUrl = (newUrl) => {
    apiUrl.value = newUrl;
    localStorage.setItem("funasr_api_url", newUrl);
    checkConnection();
  };

  // Test connection
  const testConnection = async (testUrl) => {
    try {
      const response = await fetch(`${testUrl}/health`, { method: "GET" });
      return response.ok;
    } catch {
      return false;
    }
  };

  // Start periodic connection check
  const startConnectionCheck = () => {
    checkConnection();
    connectionCheckInterval = setInterval(checkConnection, 30000); // Every 30 seconds
  };

  // Stop connection check
  const stopConnectionCheck = () => {
    if (connectionCheckInterval) {
      clearInterval(connectionCheckInterval);
      connectionCheckInterval = null;
    }
  };

  onMounted(() => {
    startConnectionCheck();
  });

  onUnmounted(() => {
    stopConnectionCheck();
  });

  return {
    apiUrl,
    isConnected,
    checkConnection,
    transcribeFile,
    transcribeUrl,
    saveApiUrl,
    testConnection,
  };
}
