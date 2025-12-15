<template>
  <div class="modal-overlay" v-if="show" @click.self="$emit('close')">
    <div class="modal">
      <div class="modal-header">
        <span class="modal-title">API 设置</span>
        <button class="modal-close" @click="$emit('close')">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>
      <div class="modal-body">
        <div class="connection-status">
          <span
            class="status-dot"
            :class="{ connected: isConnected, disconnected: !isConnected }"
          ></span>
          <span class="status-text">{{
            isConnected ? "服务已连接" : "服务未连接"
          }}</span>
        </div>
        <div class="form-group">
          <label class="form-label">API 服务器地址</label>
          <input
            type="text"
            class="form-input"
            :value="modelValue"
            @input="$emit('update:modelValue', $event.target.value)"
            placeholder="http://localhost:8000"
          />
          <p class="form-hint">部署后端服务后，填入您的服务器地址</p>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-secondary" @click="$emit('test')">测试连接</button>
        <button class="btn-primary" @click="$emit('save')">保存设置</button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  modelValue: {
    type: String,
    default: "",
  },
  isConnected: {
    type: Boolean,
    default: false,
  },
});

defineEmits(["close", "update:modelValue", "test", "save"]);
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  animation: fadeIn 0.2s ease;
}

.modal {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 16px;
  width: 90%;
  max-width: 480px;
  animation: scaleIn 0.2s ease;
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  font-size: 18px;
  font-weight: 600;
}

.modal-close {
  width: 32px;
  height: 32px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  cursor: pointer;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.modal-close:hover {
  background: var(--bg-hover);
  color: var(--text-white);
}

.modal-close svg {
  width: 20px;
  height: 20px;
}

.modal-body {
  padding: 24px;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  background: var(--bg-input);
  border-radius: 8px;
  margin-bottom: 20px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.connected {
  background: var(--success);
}

.status-dot.disconnected {
  background: var(--error);
}

.status-text {
  font-size: 13px;
  color: var(--text-gray);
}

.form-group {
  margin-bottom: 0;
}

.form-label {
  display: block;
  font-size: 13px;
  color: var(--text-gray);
  margin-bottom: 8px;
}

.form-input {
  width: 100%;
  padding: 12px 16px;
  background: var(--bg-input);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  color: var(--text-white);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

.form-input:focus {
  border-color: var(--accent-blue);
}

.form-hint {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 6px;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--border-color);
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-secondary {
  padding: 10px 20px;
  border: 1px solid var(--border-color);
  background: transparent;
  color: var(--text-gray);
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.15s;
}

.btn-secondary:hover {
  background: var(--bg-hover);
  color: var(--text-white);
}

.btn-primary {
  padding: 10px 20px;
  border: none;
  background: var(--accent-gradient);
  color: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.15s;
}

.btn-primary:hover {
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.3);
}
</style>
