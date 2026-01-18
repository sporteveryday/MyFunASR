<template>
  <div class="progress-wrapper" v-if="show">
    <div class="progress-info">
      <span class="progress-status">{{ statusText }}</span>
      <span class="progress-percent">{{ progress }}%</span>
    </div>
    <div class="progress-bar-bg">
      <div
        class="progress-bar-fill"
        :style="{ width: progress + '%' }"
        :class="{ processing: isProcessing }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  progress: {
    type: Number,
    default: 0,
  },
  status: {
    type: String,
    default: "uploading", // 'uploading' | 'processing' | 'analyzing'
  },
});

const isProcessing = computed(
  () => props.status === "processing" || props.status === "analyzing",
);

const statusText = computed(() => {
  if (props.status === "analyzing") return "识别完成，正在进行 AI 深度洞察...";
  if (props.status === "processing") return "正在识别多媒体内容...";
  if (props.progress === 100) return "上传完成，准备转写";
  return "正在上传媒体文件...";
});
</script>

<style scoped>
.progress-wrapper {
  margin-top: 20px;
  width: 100%;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.progress-status {
  font-size: 13px;
  color: var(--text-muted);
}

.progress-percent {
  font-size: 13px;
  font-weight: 600;
  color: var(--accent-blue);
}

.progress-bar-bg {
  height: 8px;
  background: var(--bg-input);
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent-blue), #60a5fa);
  border-radius: 4px;
  transition: width 0.3s ease;
  position: relative;
}

.progress-bar-fill.processing {
  background: linear-gradient(90deg, #60a5fa, #34d399);
}

.progress-bar-fill::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0) 0%,
    rgba(255, 255, 255, 0.2) 50%,
    rgba(255, 255, 255, 0) 100%
  );
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}
</style>
