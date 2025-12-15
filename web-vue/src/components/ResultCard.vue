<template>
  <div class="info-card">
    <div class="card-header result-header">
      <span class="card-title">识别结果</span>
      <div class="action-buttons" v-if="result">
        <button class="action-btn" @click="$emit('copy')" title="复制">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <rect x="9" y="9" width="13" height="13" rx="2" />
            <path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />
          </svg>
        </button>
      </div>
    </div>
    <div class="card-content">
      <div v-if="result">
        <div class="stats-bar">
          <div class="stat-item">
            <div class="stat-value">{{ result.duration }}s</div>
            <div class="stat-label">音频时长</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">
              {{ result.text ? result.text.length : 0 }}
            </div>
            <div class="stat-label">生成字数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ result.processing_time }}s</div>
            <div class="stat-label">处理耗时</div>
          </div>
        </div>
        <p class="result-text">{{ result.text }}</p>
      </div>
      <div class="empty-result" v-else>
        {{ emptyText }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  result: {
    type: Object,
    default: null,
  },
  emptyText: {
    type: String,
    default: '点击"开始识别"按钮进行语音转文字',
  },
});

defineEmits(["copy"]);
</script>

<style scoped>
.info-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  overflow: hidden;
}

.card-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-input);
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-white);
}

.card-content {
  padding: 20px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.action-btn {
  width: 32px;
  height: 32px;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  color: var(--text-gray);
  border-radius: 6px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.action-btn:hover {
  background: var(--bg-hover);
  color: var(--text-white);
  border-color: var(--accent-blue);
}

.action-btn svg {
  width: 16px;
  height: 16px;
}

.stats-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
}

.stat-item {
  flex: 1;
  padding: 12px 16px;
  background: var(--bg-input);
  border-radius: 10px;
  text-align: center;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--accent-blue);
  margin-bottom: 4px;
}

.stat-label {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.result-text {
  font-size: 15px;
  line-height: 1.8;
  color: var(--text-white);
  white-space: pre-wrap;
  max-height: 400px;
  overflow-y: auto;
}

.result-text::-webkit-scrollbar {
  width: 6px;
}

.result-text::-webkit-scrollbar-track {
  background: var(--bg-input);
}

.result-text::-webkit-scrollbar-thumb {
  background: var(--border-light);
  border-radius: 3px;
}

.empty-result {
  color: var(--text-muted);
  font-style: italic;
  text-align: center;
  padding: 40px 0;
}
</style>
