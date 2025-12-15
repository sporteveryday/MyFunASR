import { ref, computed, onUnmounted } from "vue";
import { formatDuration } from "../utils/formatters";

export function useFileUpload() {
  const selectedFile = ref(null);
  const previewUrl = ref(null);
  const mediaDuration = ref(null);
  const isDragging = ref(false);

  const isVideo = computed(() => {
    if (!selectedFile.value) return false;
    const ext = selectedFile.value.name.split(".").pop().toLowerCase();
    return ["mp4", "avi", "mkv", "mov", "wmv", "flv", "webm"].includes(ext);
  });

  const isAudio = computed(() => {
    if (!selectedFile.value) return false;
    const ext = selectedFile.value.name.split(".").pop().toLowerCase();
    return ["wav", "mp3", "m4a", "flac", "aac", "ogg", "wma"].includes(ext);
  });

  const setFile = (file) => {
    selectedFile.value = file;
    mediaDuration.value = null;

    // Revoke old preview URL
    if (previewUrl.value) {
      URL.revokeObjectURL(previewUrl.value);
    }

    // Create new preview URL
    previewUrl.value = URL.createObjectURL(file);
  };

  const clearFile = () => {
    if (previewUrl.value) {
      URL.revokeObjectURL(previewUrl.value);
    }
    selectedFile.value = null;
    previewUrl.value = null;
    mediaDuration.value = null;
  };

  const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file) {
      setFile(file);
    }
  };

  const handleDrop = (event) => {
    isDragging.value = false;
    const file = event.dataTransfer.files[0];
    if (file) {
      setFile(file);
    }
  };

  const handleDragOver = () => {
    isDragging.value = true;
  };

  const handleDragLeave = () => {
    isDragging.value = false;
  };

  const onMediaLoaded = (event) => {
    const duration = event.target.duration;
    mediaDuration.value = formatDuration(duration);
  };

  // Cleanup on unmount
  onUnmounted(() => {
    if (previewUrl.value) {
      URL.revokeObjectURL(previewUrl.value);
    }
  });

  return {
    selectedFile,
    previewUrl,
    mediaDuration,
    isDragging,
    isVideo,
    isAudio,
    setFile,
    clearFile,
    handleFileSelect,
    handleDrop,
    handleDragOver,
    handleDragLeave,
    onMediaLoaded,
  };
}
