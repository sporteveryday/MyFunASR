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

      <!-- URL Input Mode -->
      <div v-if="mode === 'url' && !urlInfo">
        <URLInput
          v-model="videoUrl"
          :is-loading="isLoading"
          @submit="handleUrlTranscribe"
        />
      </div>

      <!-- File Mode Content Grid-->
      <div class="content-grid" v-if="mode === 'file' && selectedFile">
        <InfoCard
          title="媒体预览"
          :show-remove="true"
          remove-text="移除文件"
          @remove="clearFile"
        >
          <MediaPreview
            :is-video="isVideo"
            :is-audio="isAudio"
            :preview-url="previewUrl"
            @loaded="onMediaLoaded"
          />
          <FileDetails
            :file-name="selectedFile.name"
            :file-size="formatFileSize(selectedFile.size)"
            :duration="mediaDuration"
            :is-loading="isLoading"
            @transcribe="handleFileTranscribe"
            style="margin-top: 16px"
          />
        </InfoCard>

        <ResultCard :result="result" @copy="copyResult" />
      </div>

      <!-- URL Mode Content Grid -->
      <div class="content-grid" v-if="mode === 'url' && urlInfo">
        <InfoCard
          title="视频预览"
          :show-remove="true"
          remove-text="重新输入"
          @remove="clearUrl"
        >
          <MediaPreview
            :embed-url="embedUrl"
            :placeholder-text="urlInfo.title"
          />
          <div class="file-details" style="margin-top: 16px">
            <div class="detail-item">
              <span class="detail-label">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <polygon points="23,7 16,12 23,17" />
                  <rect x="1" y="5" width="15" height="14" rx="2" />
                </svg>
                视频标题
              </span>
              <span class="detail-value" :title="urlInfo.title">{{
                urlInfo.title
              }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <circle cx="12" cy="12" r="10" />
                  <polyline points="12,6 12,12 16,14" />
                </svg>
                时长
              </span>
              <span class="detail-value">{{
                formatDuration(urlInfo.duration)
              }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">
                <svg
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
                </svg>
                处理耗时
              </span>
              <span class="detail-value">{{ urlInfo.processing_time }}s</span>
            </div>
          </div>
        </InfoCard>

        <ResultCard :result="urlInfo" @copy="copyResult" />
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
const fileInput = ref(null);
const showSettings = ref(false);
const tempApiUrl = ref("");

// Composables
const {
  apiUrl,
  isConnected,
  transcribeFile,
  transcribeUrl,
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
  try {
    result.value = await transcribeFile(selectedFile.value);
    showToast("识别完成！", "success");
  } catch (error) {
    console.error("Error:", error);
    showToast(error.message || "识别失败", "error");
  } finally {
    isLoading.value = false;
  }
};

const handleUrlTranscribe = async () => {
  if (!videoUrl.value) return;

  isLoading.value = true;
  try {
    urlInfo.value = await transcribeUrl(videoUrl.value);
    showToast("识别完成！", "success");
  } catch (error) {
    console.error("Error:", error);
    showToast(error.message || "识别失败", "error");
  } finally {
    isLoading.value = false;
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
</style>
