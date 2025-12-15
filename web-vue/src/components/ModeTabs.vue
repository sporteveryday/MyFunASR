<template>
  <div class="tabs">
    <button
      class="tab-btn"
      :class="{ active: modelValue === 'file' }"
      @click="$emit('update:modelValue', 'file')"
    >
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
      文件上传
    </button>
    <button
      class="tab-btn"
      :class="{ active: modelValue === 'url' }"
      @click="$emit('update:modelValue', 'url')"
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71" />
        <path
          d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"
        />
      </svg>
      视频链接
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue: {
    type: String,
    required: true,
  },
});

defineEmits(["update:modelValue"]);
</script>

<style scoped>
.tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 24px;
  justify-content: center;
}

.tab-btn {
  padding: 10px 24px;
  border: 1px solid var(--border-color);
  background: var(--bg-card);
  color: var(--text-gray);
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tab-btn:hover {
  background: var(--bg-hover);
  color: var(--text-white);
}

.tab-btn.active {
  background: var(--accent-gradient);
  color: white;
  border-color: transparent;
}

.tab-btn svg {
  width: 18px;
  height: 18px;
}
</style>
