# PureSnap

**Grab pure, watermark-free videos, images, and audio from 999+ platforms — right inside your AI agent.**

No API key needed. No configuration. Install and start downloading.

## What it does

Paste any social media link in chat, and the agent extracts watermark-free media for you:

- Direct download URLs for videos, images, and audio
- Multi-resolution support (up to 8K for YouTube)
- Sora2 watermark removal (original quality, zero loss)
- Subtitle extraction (YouTube, multiple languages and formats)
- Batch extraction from playlists, channels, and profiles

## Supported Platforms (999+)

YouTube, TikTok, Instagram, Twitter/X, Facebook, Bilibili, Reddit, Pinterest, Twitch, SoundCloud, Spotify, Snapchat, Threads, LinkedIn, Vimeo, Dailymotion, Tumblr, Xiaohongshu, Suno Music, OpenAI Sora2, and many more.

## Usage

After installing, simply tell the agent what you want:

```
Download this video: https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

```
Extract all videos from this channel: https://www.youtube.com/@Nike/videos
```

```
Remove the Sora watermark: https://sora.chatgpt.com/p/s_xxxxx
```

```
Get subtitles for this video: https://www.youtube.com/watch?v=xxxxx
```

The agent calls the API, parses the results, and gives you direct download links or saves files locally.

## Install

```bash
# Cursor Marketplace
# Install from cursor.com/marketplace (search "PureSnap")

# skills.sh
npx skills add wells1137/meowload-downloader

# Sundial Hub
npx sundial-hub add wells1137/puresnap

# ClawHub
clawdhub install puresnap

# localskills.sh
localskills install meowload-downloader

# Playbooks
npx playbooks add skill wells1137/meowload-downloader
```

## Features

| Feature | Description |
|---------|-------------|
| Single Post Download | Extract media from any single post URL |
| Batch Extraction | Download entire playlists, channels, or profiles |
| Multi-Resolution | Choose from multiple quality options (144p to 8K) |
| Sora2 Watermark Removal | Get original watermark-free Sora2 videos |
| Subtitle Download | Extract YouTube subtitles in SRT, VTT, TTML, etc. |
| Credits Check | Monitor remaining API usage |

## How it works

PureSnap wraps the [MeowLoad (哼哼猫)](https://www.henghengmao.com) developer API. An API key is built-in so you can use it immediately. To use your own key, set the `MEOWLOAD_API_KEY` environment variable.

## License

MIT
