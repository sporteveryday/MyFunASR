<template>
  <div class="toast" :class="toast.type" v-if="toast.show">
    {{ toast.message }}
  </div>
</template>

<script setup>
defineProps({
  toast: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.toast {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 14px 20px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  color: var(--text-white);
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  z-index: 1000;
  animation: slideUp 0.3s ease;
}

.toast.success {
  border-left: 3px solid var(--success);
}

.toast.error {
  border-left: 3px solid var(--error);
}
</style>
