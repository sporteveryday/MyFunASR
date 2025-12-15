import { ref, computed } from "vue";
import { getEmbedUrl } from "../utils/videoEmbed";

export function useUrlTranscribe() {
  const videoUrl = ref("");
  const urlInfo = ref(null);

  const embedUrl = computed(() => getEmbedUrl(videoUrl.value));

  const clearUrl = () => {
    videoUrl.value = "";
    urlInfo.value = null;
  };

  return {
    videoUrl,
    urlInfo,
    embedUrl,
    clearUrl,
  };
}
