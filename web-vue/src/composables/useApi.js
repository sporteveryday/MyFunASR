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

  // Transcribe file with progress
  const transcribeFile = (file, onProgress) => {
    return new Promise((resolve, reject) => {
      const formData = new FormData();
      formData.append("file", file);

      const xhr = new XMLHttpRequest();
      xhr.open("POST", `${apiUrl.value}/transcribe`);

      // Monitor upload progress
      if (xhr.upload && onProgress) {
        xhr.upload.addEventListener("progress", (event) => {
          if (event.lengthComputable) {
            const percentComplete = Math.round(
              (event.loaded / event.total) * 100,
            );
            onProgress(percentComplete);
          }
        });
      }

      xhr.onload = () => {
        if (xhr.status >= 200 && xhr.status < 300) {
          try {
            resolve(JSON.parse(xhr.responseText));
          } catch (e) {
            reject(new Error("解析响应失败"));
          }
        } else {
          try {
            const error = JSON.parse(xhr.responseText);
            reject(new Error(error.detail || "识别失败"));
          } catch (e) {
            reject(new Error("识别失败"));
          }
        }
      };

      xhr.onerror = () => reject(new Error("网络错误"));
      xhr.send(formData);
    });
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
