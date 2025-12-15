<template>
  <div class="url-input-area">
    <div class="url-input-wrapper">
      <input
        type="text"
        class="url-input"
        :value="modelValue"
        @input="$emit('update:modelValue', $event.target.value)"
        placeholder="输入视频链接，例如 https://www.bilibili.com/video/..."
        @keyup.enter="$emit('submit')"
      />
      <button
        class="url-submit-btn"
        :disabled="!modelValue || isLoading"
        @click="$emit('submit')"
      >
        <span class="btn-spinner" v-if="isLoading"></span>
        <span>{{ isLoading ? "处理中..." : "开始识别" }}</span>
      </button>
    </div>
    <p class="url-hint">
      支持平台: <span>YouTube</span>, <span>Bilibili</span>, <span>抖音</span>,
      <span>西瓜视频</span> 等
    </p>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    default: "",
  },
  isLoading: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["update:modelValue", "submit"]);
</script>

<style scoped>
.url-input-area {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 24px;
}

.url-input-wrapper {
  display: flex;
  gap: 12px;
}

.url-input {
  flex: 1;
  padding: 14px 18px;
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-white);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.url-input:focus {
  border-color: var(--accent-blue);
}

.url-input::placeholder {
  color: var(--text-muted);
}

.url-submit-btn {
  padding: 14px 28px;
  background: var(--accent-gradient);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.url-submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
}

.url-submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.url-hint {
  margin-top: 16px;
  font-size: 12px;
  color: var(--text-muted);
  text-align: center;
}

.url-hint span {
  color: var(--accent-blue);
}

@media (max-width: 768px) {
  .url-input-wrapper {
    flex-direction: column;
  }
}
</style>
