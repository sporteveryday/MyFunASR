<template>
  <div class="file-details">
    <div class="detail-item">
      <span class="detail-label">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" />
          <polyline points="14,2 14,8 20,8" />
        </svg>
        文件名
      </span>
      <span class="detail-value">{{ fileName }}</span>
    </div>
    <div class="detail-item">
      <span class="detail-label">
        <svg
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"
          />
        </svg>
        文件大小
      </span>
      <span class="detail-value">{{ fileSize }}</span>
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
        媒体时长
      </span>
      <span class="detail-value">{{ duration || "--" }}</span>
    </div>
  </div>
</template>

<script setup>
defineProps({
  fileName: {
    type: String,
    required: true,
  },
  fileSize: {
    type: String,
    required: true,
  },
  duration: {
    type: String,
    default: null,
  },
});
</script>

<style scoped>
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
</style>
