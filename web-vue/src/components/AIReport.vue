<template>
  <div class="ai-report-container" v-if="result && result.aiAnalysis">
    <div class="report-header">
      <div class="header-main">
        <span class="report-icon">✨</span>
        <h2 class="report-title">AI 深度分析报告</h2>
      </div>
      <div class="report-badge">Mistral Large 2 Powered</div>
    </div>

    <!-- AI Deep Insight Section -->
    <section class="report-section ai-insight">
      <div class="section-header">
        <span class="icon">🤖</span>
        <h3>AI 核心摘要与洞察</h3>
      </div>
      <div class="ai-content">
        <div class="ai-summary">
          <span class="quote">“</span>{{ result.aiAnalysis.summary
          }}<span class="quote">”</span>
        </div>
        <div class="ai-grid">
          <div class="ai-box highlights">
            <h4><span class="icon">🎯</span> 核心重点</h4>
            <ul>
              <li v-for="(h, i) in result.aiAnalysis.highlights" :key="i">
                {{ h }}
              </li>
            </ul>
          </div>
          <div class="ai-box suggestions">
            <h4><span class="icon">💡</span> 行动建议</h4>
            <ul>
              <li v-for="(s, i) in result.aiAnalysis.suggestions" :key="i">
                {{ s }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
defineProps({
  result: {
    type: Object,
    required: true,
  },
});
</script>

<style scoped>
.ai-report-container {
  margin-top: 32px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 32px;
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--border-color);
}

.header-main {
  display: flex;
  align-items: center;
  gap: 12px;
}

.report-icon {
  font-size: 24px;
}

.report-title {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-white);
  letter-spacing: -0.5px;
}

.report-badge {
  background: rgba(139, 92, 246, 0.15);
  color: var(--accent-purple);
  padding: 6px 12px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  border: 1px solid rgba(139, 92, 246, 0.2);
}

.report-section {
  margin-bottom: 24px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.section-header h3 {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-white);
}

/* AI Insight Box */
.ai-insight {
  background: linear-gradient(
    135deg,
    rgba(59, 130, 246, 0.08) 0%,
    rgba(139, 92, 246, 0.08) 100%
  );
  border: 1px solid rgba(59, 130, 246, 0.15);
  border-radius: 16px;
  padding: 24px;
}

.ai-summary {
  font-size: 17px;
  font-weight: 600;
  color: var(--text-white);
  line-height: 1.6;
  text-align: center;
  margin-bottom: 24px;
  padding: 0 40px;
}

.ai-summary .quote {
  color: var(--accent-blue);
  font-size: 28px;
  font-family: serif;
  opacity: 0.6;
}

.ai-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.ai-box {
  background: rgba(0, 0, 0, 0.2);
  padding: 20px;
  border-radius: 12px;
}

.ai-box h4 {
  font-size: 13px;
  color: var(--text-muted);
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.ai-box ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ai-box li {
  font-size: 14px;
  color: var(--text-gray);
  line-height: 1.5;
  position: relative;
  padding-left: 18px;
}

.ai-box li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: var(--accent-blue);
  font-weight: bold;
}

@media (max-width: 900px) {
  .ai-grid {
    grid-template-columns: 1fr;
  }
}
</style>
