# PureSnap — TikTok / YouTube / Instagram / Twitter Video Downloader (No Watermark)

**All-in-one no-watermark video downloader for AI agents. Save videos, images, and audio from TikTok, YouTube, Instagram, Twitter/X, Bilibili, Facebook, Reddit, Xiaohongshu, and 999+ platforms.**

No API key needed. No configuration. Install and start downloading.

## Supported Platforms

| Platform | What you can download |
|----------|----------------------|
| **TikTok** | Videos without watermark, slideshows, audio |
| **YouTube** | Videos up to 8K, shorts, playlists, subtitles (SRT/VTT) |
| **Instagram** | Reels, Stories, Posts, IGTV, profile media |
| **Twitter/X** | Videos, GIFs, images from tweets |
| **Bilibili** | Videos, bangumi, audio |
| **Facebook** | Videos, Reels, Stories |
| **Reddit** | Videos with audio, GIFs |
| **Xiaohongshu** | Images, videos, notes |
| **Pinterest** | Videos, images, pins |
| **Snapchat** | Stories, Spotlight videos |
| **Threads** | Videos, images |
| **LinkedIn** | Videos from posts |
| **Twitch** | Clips, VODs |
| **SoundCloud** | Audio tracks |
| **Spotify** | Preview tracks |
| **Suno** | AI-generated music |
| **OpenAI Sora2** | Watermark-free original videos |
| **999+ more** | Vimeo, Dailymotion, Tumblr, etc. |

## What it does

Paste any social media link in chat, and the agent downloads watermark-free media for you:

- **TikTok video downloader** — save TikTok without watermark
- **YouTube video downloader** — download YouTube videos in multiple resolutions
- **Instagram downloader** — save Reels, Stories, Posts
- **Twitter video downloader** — download Twitter/X videos and GIFs
- **Bilibili downloader** — download Bilibili videos
- **Sora2 watermark remover** — get original Sora2 videos without watermark
- **Subtitle downloader** — extract YouTube subtitles in SRT, VTT, TTML
- **Batch downloader** — download entire playlists, channels, profiles

## Usage

After installing, simply tell the agent what you want:

```
Download this TikTok video: https://www.tiktok.com/@user/video/xxx
```

```
Save this YouTube video: https://www.youtube.com/watch?v=xxx
```

```
Download Instagram Reel: https://www.instagram.com/reel/xxx
```

```
Save this tweet video: https://twitter.com/user/status/xxx
```

```
Download all videos from this channel: https://www.youtube.com/@Nike/videos
```

```
Remove Sora watermark: https://sora.chatgpt.com/p/s_xxxxx
```

## Install

```bash
# skills.sh
npx skills add wells1137/meowload-downloader

# Sundial Hub
npx sundial-hub add wells1137/puresnap

# ClawHub
clawdhub install puresnap

# localskills.sh
localskills install kew9C6g570

# Playbooks
npx playbooks add skill wells1137/meowload-downloader
```

## Features

| Feature | Description |
|---------|-------------|
| No-Watermark Download | Save TikTok, Douyin videos without watermark |
| Multi-Resolution | YouTube up to 8K, choose quality (144p–8K) |
| Sora2 Watermark Removal | Original quality, zero loss |
| Subtitle Extraction | YouTube subtitles in SRT, VTT, TTML, JSON3 |
| Batch Download | Entire playlists, channels, profiles |
| 999+ Platforms | TikTok, YouTube, Instagram, Twitter, Bilibili, Facebook, Reddit, and more |

## How it works

PureSnap wraps the [MeowLoad (哼哼猫)](https://www.henghengmao.com) developer API. An API key is built-in so you can use it immediately. To use your own key, set the `MEOWLOAD_API_KEY` environment variable.

## Keywords

tiktok video downloader, youtube video downloader, instagram reels downloader, twitter video downloader, bilibili video downloader, facebook video downloader, reddit video downloader, xiaohongshu downloader, no watermark, remove watermark, save video, download video, sora2 watermark remover, media downloader, video saver, social media downloader

## License

MIT
