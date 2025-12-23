# Videos Directory

## Video Naming Convention

Videos should be named according to the card's `name_short`:

- `ar00.mp4` - El Loco
- `ar01.mp4` - El Mago
- `ar02.mp4` - La Sacerdotisa
- ... (ar00 through ar21 for all 22 Major Arcana)

## Format Requirements

- **Container**: MP4 (H.264)
- **Fallback**: WebM (VP9) optional
- **Resolution**: Max 1080p
- **Optimization**: Compressed for web delivery

## First Frame Extraction

For each video, we also need the first frame as a static image.
Command: `ffmpeg -i ar00.mp4 -vframes 1 -f image2 ar00.jpg`
