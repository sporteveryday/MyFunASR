<template>
  <div class="info-card">
    <div class="card-header">
      <span class="card-title">{{ title }}</span>
      <button v-if="showRemove" class="remove-btn" @click="$emit('remove')">
        {{ removeText }}
      </button>
    </div>
    <div class="card-content">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  showRemove: {
    type: Boolean,
    default: false,
  },
  removeText: {
    type: String,
    default: "移除",
  },
});

defineEmits(["remove"]);
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

.remove-btn {
  padding: 6px 12px;
  border: 1px solid var(--border-color);
  background: transparent;
  color: var(--text-muted);
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.15s ease;
}

.remove-btn:hover {
  background: rgba(239, 68, 68, 0.15);
  color: var(--error);
  border-color: var(--error);
}
</style>
