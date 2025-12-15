/**
 * Generate embed URL for video platforms
 * @param {string} url - Video URL
 * @returns {string|null} Embed URL or null
 */
export function getEmbedUrl(url) {
  if (!url) return null;

  // YouTube
  const youtubeMatch = url.match(
    /(?:youtube\.com\/(?:watch\?v=|embed\/)|youtu\.be\/)([a-zA-Z0-9_-]{11})/
  );
  if (youtubeMatch) {
    return `https://www.youtube.com/embed/${youtubeMatch[1]}`;
  }

  // Bilibili
  const bvMatch = url.match(/bilibili\.com\/video\/(BV[a-zA-Z0-9]+)/);
  if (bvMatch) {
    return `https://player.bilibili.com/player.html?bvid=${bvMatch[1]}&autoplay=0`;
  }

  return null;
}
