<template>
  <div id="app">
    <AppHeader
      :is-connected="isConnected"
      @open-settings="showSettings = true"
    />

    <div class="main-container">
      <h1 class="page-title">语音识别</h1>
      <p class="page-subtitle">上传文件或输入视频链接，自动转换为文字</p>

      <!-- Mode Tabs -->
      <ModeTabs v-model="mode" />

      <!-- File Upload Mode -->
      <div v-if="mode === 'file' && !selectedFile">
        <FileUpload
          :is-dragging="isDragging"
          @click="triggerFileInput"
          @dragover="handleDragOver"
          @dragleave="handleDragLeave"
          @drop="handleDrop"
        />
        <input
          type="file"
          ref="fileInput"
          style="display: none"
          accept=".wav,.mp3,.m4a,.flac,.aac,.ogg,.wma,.mp4,.avi,.mkv,.mov,.wmv,.flv,.webm"
          @change="handleFileSelect"
        />
      </div>

      <!-- Processing State for File Mode -->
      <div
        v-if="mode === 'file' && selectedFile && !result"
        class="processing-view"
      >
        <InfoCard :title="selectedFile.name">
          <div class="processing-placeholder">
            <div class="pulse-icon">📂</div>
            <p>文件已选定，准备开启 AI 识别与分析之旅</p>
          </div>
          <ProgressBar
            :show="isLoading"
            :progress="processingProgress"
            :status="processingStatus"
          />
          <div class="actions" v-if="!isLoading">
            <button class="primary-btn" @click="handleFileTranscribe">
              开始识别分析
            </button>
            <button class="remove-btn" @click="clearFile">更换文件</button>
          </div>
        </InfoCard>
      </div>

      <!-- URL Input Mode -->
      <div v-if="mode === 'url' && !urlInfo">
        <URLInput
          v-model="videoUrl"
          :is-loading="isLoading"
          @submit="handleUrlTranscribe"
        />
        <ProgressBar
          :show="isLoading"
          :progress="processingProgress"
          :status="processingStatus"
          style="margin-top: 24px"
        />
      </div>

      <!-- Result Content Grid (Common for both modes when ready) -->
      <div
        class="content-grid"
        v-if="(mode === 'file' && result) || (mode === 'url' && urlInfo)"
      >
        <InfoCard
          :title="mode === 'file' ? '媒体预览' : '视频预览'"
          :show-remove="true"
          :remove-text="mode === 'file' ? '移除文件' : '重新输入'"
          @remove="mode === 'file' ? clearFile() : clearUrl()"
        >
          <MediaPreview
            v-if="mode === 'file'"
            :is-video="isVideo"
            :is-audio="isAudio"
            :preview-url="previewUrl"
            @loaded="onMediaLoaded"
          />
          <MediaPreview
            v-else
            :embed-url="embedUrl"
            :placeholder-text="urlInfo.title"
          />

          <FileDetails
            v-if="mode === 'file'"
            :file-name="selectedFile.name"
            :file-size="formatFileSize(selectedFile.size)"
            :duration="mediaDuration"
            :is-loading="false"
            style="margin-top: 16px"
          />
          <div v-else class="file-details" style="margin-top: 16px">
            <div class="detail-item">
              <span class="detail-label">视频标题</span>
              <span class="detail-value">{{ urlInfo.title }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">时长</span>
              <span class="detail-value">{{
                formatDuration(urlInfo.duration)
              }}</span>
            </div>
          </div>
        </InfoCard>

        <ResultCard
          :result="mode === 'file' ? result : urlInfo"
          @copy="copyResult"
        />
      </div>
    </div>

    <!-- Settings Modal -->
    <SettingsModal
      v-model="tempApiUrl"
      :show="showSettings"
      :is-connected="isConnected"
      @close="showSettings = false"
      @test="testConnection"
      @save="saveSettings"
    />

    <!-- Toast Notification -->
    <Toast :toast="toast" />

    <!-- AI Report Inline Section -->
    <AIReport
      v-if="(mode === 'file' && result) || (mode === 'url' && urlInfo)"
      :result="mode === 'file' ? result : urlInfo"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import AppHeader from "./components/AppHeader.vue";
import ModeTabs from "./components/ModeTabs.vue";
import FileUpload from "./components/FileUpload.vue";
import URLInput from "./components/URLInput.vue";
import MediaPreview from "./components/MediaPreview.vue";
import InfoCard from "./components/InfoCard.vue";
import FileDetails from "./components/FileDetails.vue";
import ResultCard from "./components/ResultCard.vue";
import ProgressBar from "./components/ProgressBar.vue";
import AIReport from "./components/AIReport.vue";
import SettingsModal from "./components/SettingsModal.vue";
import Toast from "./components/Toast.vue";

import { useApi } from "./composables/useApi";
import { useToast } from "./composables/useToast";
import { useFileUpload } from "./composables/useFileUpload";
import { useUrlTranscribe } from "./composables/useUrlTranscribe";
import { formatFileSize, formatDuration } from "./utils/formatters";

// State
const mode = ref("file");
const result = ref(null);
const isLoading = ref(false);
const processingProgress = ref(0);
const processingStatus = ref("uploading"); // "uploading" | "processing"
const fileInput = ref(null);
const showSettings = ref(false);
const tempApiUrl = ref("");

// Composables
const {
  apiUrl,
  isConnected,
  transcribeFile,
  transcribeUrl,
  analyzeText,
  saveApiUrl,
  testConnection: testApiConnection,
} = useApi();
const { toast, showToast } = useToast();
const {
  selectedFile,
  previewUrl,
  mediaDuration,
  isDragging,
  isVideo,
  isAudio,
  handleFileSelect,
  handleDrop,
  handleDragOver,
  handleDragLeave,
  onMediaLoaded,
  clearFile: clearFileUpload,
} = useFileUpload();
const { videoUrl, urlInfo, embedUrl, clearUrl } = useUrlTranscribe();

// Initialize tempApiUrl
onMounted(() => {
  tempApiUrl.value = apiUrl.value;
});

// Methods
const triggerFileInput = () => {
  fileInput.value?.click();
};

const clearFile = () => {
  clearFileUpload();
  result.value = null;
};

const handleFileTranscribe = async () => {
  if (!selectedFile.value) return;

  isLoading.value = true;
  processingProgress.value = 0;
  processingStatus.value = "uploading";
  result.value = null; // 重置识别结果，确保同步展示

  try {
    // 1. 转写
    const transcribeRes = await transcribeFile(
      selectedFile.value,
      (percent) => {
        processingProgress.value = percent;
        if (percent === 100) {
          processingStatus.value = "processing";
          startProcessingSimulation();
        }
      },
    );

    // 2. 自动分析
    stopProcessingSimulation();
    processingStatus.value = "analyzing";
    processingProgress.value = 99;

    try {
      const analysisData = await analyzeText(transcribeRes.text);
      if (analysisData.success) {
        transcribeRes.aiAnalysis = analysisData;
      }
    } catch (analysisError) {
      console.error("AI Analysis failed:", analysisError);
      // 分析失败不影响转写结果显示，但标记一下
      transcribeRes.aiAnalysisError = analysisError.message;
    }

    result.value = transcribeRes;
    processingProgress.value = 100;
    showToast("识别与分析完成！", "success");
  } catch (error) {
    console.error("Error:", error);
    showToast(error.message || "处理失败", "error");
  } finally {
    isLoading.value = false;
    stopProcessingSimulation();
  }
};

let processingInterval = null;
const startProcessingSimulation = () => {
  let simulatedProgress = 0;
  processingInterval = setInterval(() => {
    if (simulatedProgress < 95) {
      simulatedProgress += Math.random() * 5;
      processingProgress.value = Math.min(Math.floor(simulatedProgress), 99);
    }
  }, 1000);
};

const stopProcessingSimulation = () => {
  if (processingInterval) {
    clearInterval(processingInterval);
    processingInterval = null;
  }
};

const handleUrlTranscribe = async () => {
  if (!videoUrl.value) return;

  isLoading.value = true;
  processingProgress.value = 0;
  processingStatus.value = "processing";
  urlInfo.value = null;

  startProcessingSimulation();

  try {
    // 1. 转写
    const transcribeRes = await transcribeUrl(videoUrl.value);

    // 2. 自动分析
    stopProcessingSimulation();
    processingStatus.value = "analyzing";
    processingProgress.value = 99;

    try {
      const analysisData = await analyzeText(transcribeRes.text);
      if (analysisData.success) {
        transcribeRes.aiAnalysis = analysisData;
      }
    } catch (analysisError) {
      console.error("AI Analysis failed:", analysisError);
      transcribeRes.aiAnalysisError = analysisError.message;
    }

    urlInfo.value = transcribeRes;
    processingProgress.value = 100;
    showToast("识别与分析完成！", "success");
  } catch (error) {
    console.error("Error:", error);
    showToast(error.message || "处理失败", "error");
  } finally {
    isLoading.value = false;
    stopProcessingSimulation();
  }
};

const copyResult = async () => {
  const text = mode.value === "file" ? result.value?.text : urlInfo.value?.text;
  if (text) {
    try {
      await navigator.clipboard.writeText(text);
      showToast("已复制到剪贴板！", "success");
    } catch (error) {
      showToast("复制失败", "error");
    }
  }
};

const testConnection = async () => {
  const isOk = await testApiConnection(tempApiUrl.value);
  if (isOk) {
    showToast("连接成功！", "success");
  } else {
    showToast("连接失败：无法访问服务器", "error");
  }
};

const saveSettings = () => {
  saveApiUrl(tempApiUrl.value);
  showSettings.value = false;
  showToast("设置已保存！", "success");
};
</script>

<style scoped>
.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px;
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  text-align: center;
  margin-bottom: 8px;
}

.page-subtitle {
  font-size: 14px;
  color: var(--text-muted);
  text-align: center;
  margin-bottom: 24px;
}

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.file-details {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--bg-input);
  border-radius: 10px;
}

.detail-label {
  font-size: 13px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 8px;
}

.detail-label svg {
  width: 16px;
  height: 16px;
}

.detail-value {
  font-size: 14px;
  color: var(--text-white);
  font-weight: 500;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .content-grid {
    grid-template-columns: 1fr;
  }

  .main-container {
    padding: 20px;
  }
}

/* Processing View Styles */
.processing-view {
  max-width: 600px;
  margin: 0 auto;
}

.processing-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  text-align: center;
  color: var(--text-muted);
}

.pulse-icon {
  font-size: 48px;
  margin-bottom: 20px;
  animation: pulse 2s infinite ease-in-out;
}

.processing-placeholder p {
  font-size: 15px;
  color: var(--text-gray);
  margin: 0;
}

.actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 24px;
}

.remove-btn {
  background: var(--bg-input);
  color: var(--text-white);
  border: 1px solid var(--border-color);
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.remove-btn:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--text-muted);
}

@keyframes pulse {
  0% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.1);
    opacity: 1;
  }
  100% {
    transform: scale(1);
    opacity: 0.8;
  }
}
</style>
