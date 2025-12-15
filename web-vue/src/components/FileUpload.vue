<template>
  <div
    class="upload-area"
    :class="{ dragover: isDragging }"
    @click="$emit('click')"
    @dragover.prevent="$emit('dragover')"
    @dragleave.prevent="$emit('dragleave')"
    @drop.prevent="$emit('drop', $event)"
  >
    <div class="upload-icon">
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4" />
        <polyline points="17,8 12,3 7,8" />
        <line x1="12" y1="3" x2="12" y2="15" />
      </svg>
    </div>
    <p class="upload-text">拖拽文件到此处上传</p>
    <p class="upload-subtext">或点击选择文件</p>
    <span class="upload-formats"
      >支持格式: WAV, MP3, M4A, FLAC, MP4, AVI, MKV, MOV</span
    >
  </div>
</template>

<script setup>
defineProps({
  isDragging: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["click", "dragover", "dragleave", "drop"]);
</script>

<style scoped>
.upload-area {
  border: 2px dashed var(--border-light);
  border-radius: 16px;
  padding: 48px 32px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  background: var(--bg-card);
  margin-bottom: 24px;
}

.upload-area:hover {
  border-color: var(--accent-blue);
  background: rgba(59, 130, 246, 0.05);
}

.upload-area.dragover {
  border-color: var(--accent-blue);
  background: rgba(59, 130, 246, 0.1);
}

.upload-icon {
  width: 56px;
  height: 56px;
  margin: 0 auto 16px;
  color: var(--accent-blue);
}

.upload-icon svg {
  width: 100%;
  height: 100%;
}

.upload-text {
  font-size: 16px;
  color: var(--text-white);
  margin-bottom: 4px;
  font-weight: 500;
}

.upload-subtext {
  font-size: 14px;
  color: var(--text-muted);
  margin-bottom: 16px;
}

.upload-formats {
  font-size: 12px;
  color: var(--text-muted);
  background: var(--bg-input);
  display: inline-block;
  padding: 8px 16px;
  border-radius: 20px;
}
</style>
