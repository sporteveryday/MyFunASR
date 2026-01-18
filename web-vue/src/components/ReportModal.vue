<template>
  <div class="modal-backdrop" v-if="show" @click.self="$emit('close')">
    <div class="modal-container">
      <div class="modal-header">
        <h2 class="modal-title">识别报告分析</h2>
        <button class="close-btn" @click="$emit('close')">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>
        </button>
      </div>

      <div class="modal-body" v-if="analysis">
        <!-- Summary Section -->
        <section class="analysis-section">
          <h3><span class="icon">📝</span> 核心重点提炼</h3>
          <div class="summary-content">
            <div
              v-for="(item, i) in analysis.summary"
              :key="i"
              class="summary-item"
            >
              <h4 class="summary-item-title">{{ item.title }}</h4>
              <ul class="points-list">
                <li v-for="(point, j) in item.points" :key="j">{{ point }}</li>
              </ul>
            </div>
          </div>
        </section>

        <!-- Emotion/Event Section -->
        <section class="analysis-section" v-if="analysis.emotions.length > 0">
          <h3><span class="icon">🎭</span> 情感与事件检测</h3>
          <div class="emotion-tags">
            <span
              v-for="tag in analysis.emotions"
              :key="tag.label"
              class="emotion-tag"
              :class="tag.type"
            >
              {{ tag.emoji }} {{ tag.label }}
            </span>
          </div>
        </section>

        <div class="grid-layout">
          <!-- Keywords Section -->
          <section class="analysis-section">
            <h3><span class="icon">🔑</span> 核心关键词</h3>
            <div class="keyword-cloud">
              <span
                v-for="word in analysis.keywords"
                :key="word"
                class="keyword"
                >{{ word }}</span
              >
            </div>
          </section>

          <!-- Stats Section -->
          <section class="analysis-section">
            <h3><span class="icon">📊</span> 数值统计</h3>
            <div class="stats-grid">
              <div class="stat-box">
                <span class="label">语速 (字/分)</span>
                <span class="value">{{ analysis.speed }}</span>
              </div>
              <div class="stat-box">
                <span class="label">处理效率</span>
                <span class="value">{{ analysis.efficiency }}x</span>
              </div>
            </div>
          </section>
        </div>
      </div>

      <div class="modal-footer">
        <button class="primary-btn" @click="$emit('close')">关闭报告</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  show: Boolean,
  result: Object,
});

defineEmits(["close"]);

const analysis = computed(() => {
  if (!props.result || !props.result.text) return null;

  const text = props.result.text;
  const duration = props.result.duration || 1;
  const processingTime = props.result.processing_time || 1;

  // 1. Extract emotions/events
  const emotionMap = {
    HAPPY: { label: "开心", emoji: "😊", type: "positive" },
    SAD: { label: "悲伤", emoji: "😢", type: "negative" },
    ANGRY: { label: "愤怒", emoji: "😠", type: "negative" },
    NEUTRAL: { label: "中性", emoji: "😐", type: "neutral" },
    LAUGHTER: { label: "笑声", emoji: "😂", type: "event" },
    APPLAUSE: { label: "掌声", emoji: "👏", type: "event" },
    MUSIC: { label: "音乐", emoji: "🎵", type: "event" },
    COUGH: { label: "咳嗽", emoji: "😷", type: "event" },
  };

  const emotions = [];
  const tagRegex = /<\|([^|]+)\|>/g;
  let match;
  const foundTags = new Set();
  while ((match = tagRegex.exec(text)) !== null) {
    const tag = match[1];
    if (emotionMap[tag] && !foundTags.has(tag)) {
      emotions.push(emotionMap[tag]);
      foundTags.add(tag);
    }
  }

  const cleanText = text.replace(/<\|[^|]+\|>/g, "").trim();

  // 2. Content Categorization into Key Points (Wait for Keywords)
  const sentences = cleanText
    .split(/[。！？]/)
    .filter((s) => s.trim().length > 5);

  // 3. Refined Keyword Extraction (Frequency based) - Move up for scoring
  const commonStopWords = new Set([
    "的",
    "了",
    "和",
    "是",
    "就",
    "都",
    "而",
    "及",
    "与",
    "这",
    "那",
    "有",
    "在",
    "我",
    "你",
    "他",
    "她",
    "它",
    "们",
    "个",
    "上",
    "下",
    "里",
    "外",
    "到",
    "去",
    "又",
    "也",
    "还",
    "个",
    "一个",
    "没有",
    "什么",
    "可以",
    "我们",
    "这个",
    "那个",
    "这样",
    "那样",
  ]);

  const frequencyMap = {};
  for (let i = 0; i < cleanText.length - 1; i++) {
    const bigram = cleanText.substring(i, i + 2);
    if (
      /[\u4e00-\u9fa5]{2}/.test(bigram) &&
      !commonStopWords.has(bigram[0]) &&
      !commonStopWords.has(bigram[1])
    ) {
      frequencyMap[bigram] = (frequencyMap[bigram] || 0) + 1;
    }
  }

  const sortedKeyEntries = Object.entries(frequencyMap)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  const keywords = sortedKeyEntries.slice(0, 6).map((entry) => entry[0]);
  if (keywords.length === 0) keywords.push("核心主题", "关键讨论");

  // Scoring Logic per Sentence
  const scoreSentence = (s, kws, index, total) => {
    let score = 0;
    // 关键词加分
    kws.forEach((kw) => {
      if (s.includes(kw)) score += 5;
    });
    // 转折词/引导词加分
    const markers = [
      "建议",
      "决定",
      "核心",
      "结论",
      "首先",
      "重要",
      "必须",
      "建议",
      "重点",
      "总之",
      "实际上",
      "主要",
    ];
    markers.forEach((mark) => {
      if (s.includes(mark)) score += 10;
    });
    // 长度优化 (15-50字最佳)
    const len = s.length;
    if (len >= 15 && len <= 50) score += 5;
    // 位置权重
    if (index === 0 || index === total - 1) score += 5;
    return score;
  };

  const categories = [];

  if (sentences.length > 0) {
    const partSize = Math.ceil(sentences.length / 3);

    const getBestPoints = (sArr) => {
      return sArr
        .map((s, idx) => ({
          text: s.trim() + "。",
          score: scoreSentence(s, keywords, idx, sArr.length),
        }))
        .sort((a, b) => b.score - a.score)
        .slice(0, 2)
        .map((item) => item.text);
    };

    if (sentences.length <= 3) {
      categories.push({
        title: "核心内容",
        points: sentences.map((s) => s.trim() + "。"),
      });
    } else {
      categories.push({
        title: "内容开篇",
        points: getBestPoints(sentences.slice(0, partSize)),
      });
      if (sentences.length > partSize) {
        categories.push({
          title: "核心论述",
          points: getBestPoints(sentences.slice(partSize, partSize * 2)),
        });
      }
      if (sentences.length > partSize * 2) {
        categories.push({
          title: "总结要点",
          points: getBestPoints(sentences.slice(partSize * 2)),
        });
      }
    }
  }

  // 4. Final aggregation of stats
  const charCount = cleanText.length;
  const speed = Math.round((charCount / duration) * 60) || 0;
  const efficiency = (duration / processingTime).toFixed(1);

  return {
    summary: categories,
    emotions,
    keywords,
    speed,
    efficiency,
  };
});
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-container {
  background: var(--bg-card);
  width: 100%;
  max-width: 700px;
  border-radius: 20px;
  border: 1px solid var(--border-color);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column;
  max-height: 90vh;
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-white);
}

.close-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px;
}

.close-btn svg {
  width: 24px;
  height: 24px;
}

.modal-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.analysis-section {
  margin-bottom: 24px;
}

.analysis-section h3 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 12px;
  color: var(--text-white);
  display: flex;
  align-items: center;
  gap: 8px;
}

.summary-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.summary-item {
  background: var(--bg-input);
  padding: 16px;
  border-radius: 12px;
}

.summary-item-title {
  font-size: 13px;
  font-weight: 700;
  color: var(--accent-blue);
  margin-bottom: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.summary-item-title::before {
  content: "";
  width: 3px;
  height: 12px;
  background: var(--accent-blue);
  border-radius: 2px;
}

.points-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.points-list li {
  position: relative;
  padding-left: 18px;
  color: var(--text-gray);
  font-size: 14px;
  line-height: 1.5;
}

.points-list li::before {
  content: "→";
  position: absolute;
  left: 0;
  color: var(--accent-blue);
  font-weight: 700;
  font-size: 12px;
}

.emotion-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.emotion-tag {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.emotion-tag.positive {
  background: rgba(52, 211, 153, 0.15);
  color: #34d399;
}
.emotion-tag.negative {
  background: rgba(248, 113, 113, 0.15);
  color: #f87171;
}
.emotion-tag.neutral {
  background: rgba(156, 163, 175, 0.15);
  color: #9ca3af;
}
.emotion-tag.event {
  background: rgba(96, 165, 250, 0.15);
  color: #60a5fa;
}

.grid-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.keyword-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.keyword {
  padding: 4px 10px;
  background: var(--bg-input);
  border: 1px solid var(--border-light);
  border-radius: 6px;
  font-size: 12px;
  color: var(--text-muted);
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stat-box {
  background: var(--bg-input);
  padding: 12px;
  border-radius: 10px;
  text-align: center;
}

.stat-box .label {
  display: block;
  font-size: 11px;
  color: var(--text-muted);
  margin-bottom: 4px;
}

.stat-box .value {
  font-size: 18px;
  font-weight: 700;
  color: var(--accent-blue);
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
}

.primary-btn {
  background: var(--accent-blue);
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.primary-btn:hover {
  opacity: 0.9;
}

@media (max-width: 600px) {
  .grid-layout {
    grid-template-columns: 1fr;
  }
}
</style>
