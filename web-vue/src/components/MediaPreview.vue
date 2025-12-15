<template>
  <div class="video-preview">
    <!-- Video Player -->
    <video
      v-if="isVideo && previewUrl"
      :src="previewUrl"
      controls
      @loadedmetadata="$emit('loaded', $event)"
    />

    <!-- Audio Player -->
    <audio
      v-else-if="isAudio && previewUrl"
      :src="previewUrl"
      controls
      @loadedmetadata="$emit('loaded', $event)"
    />

    <!-- Embed Video (YouTube, Bilibili) -->
    <iframe
      v-else-if="embedUrl"
      :src="embedUrl"
      frameborder="0"
      allowfullscreen
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    />

    <!-- Placeholder -->
    <div class="preview-placeholder" v-else>
      <svg
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <rect x="2" y="4" width="20" height="16" rx="2" />
        <polygon points="10,8 16,12 10,16" fill="currentColor" />
      </svg>
      <p>{{ placeholderText || "暂无预览" }}</p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  isVideo: {
    type: Boolean,
    default: false,
  },
  isAudio: {
    type: Boolean,
    default: false,
  },
  previewUrl: {
    type: String,
    default: null,
  },
  embedUrl: {
    type: String,
    default: null,
  },
  placeholderText: {
    type: String,
    default: "",
  },
});

defineEmits(["loaded"]);
</script>

<style scoped>
.video-preview {
  width: 100%;
  aspect-ratio: 16/9;
  background: var(--bg-dark);
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.video-preview video,
.video-preview iframe {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.video-preview audio {
  width: 100%;
}

.preview-placeholder {
  color: var(--text-muted);
  font-size: 14px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.preview-placeholder svg {
  width: 48px;
  height: 48px;
  opacity: 0.5;
}
</style>
