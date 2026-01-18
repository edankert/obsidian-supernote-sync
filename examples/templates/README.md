# Templates for Golden Source Testing

This directory contains template files used to create golden source .note files on the Supernote device.

## Files

### blank_template_a5x2.png (Manta)
- **Dimensions:** 1920 x 2560 pixels (A5X2/Manta native resolution)
- **Format:** PNG, RGB, white background
- **Purpose:** Used as a custom template for creating test notes on Manta

### blank_template_a5x.png (A5X)
- **Dimensions:** 1404 x 1872 pixels (A5X native resolution)
- **Format:** PNG, RGB, white background
- **Purpose:** Used as a custom template for creating test notes on A5X

### sample_document.pdf
- **Pages:** 2
- **Purpose:** Used as a PDF template for multi-page note testing
- **Content:** Simple test document with text on each page

## How to Use

1. **Copy to Supernote:**
   - Connect Supernote via USB or use Supernote Partner app
   - Copy the appropriate `blank_template_*.png` to `MyStyle/` folder on device
   - Copy `sample_document.pdf` to `Document/` folder on device

2. **Create Notes:**
   - For PNG template: Create new note → Template → Select from MyStyle
   - For PDF template: Create note → Settings → Change Template → Select PDF

## Device Resolutions

| Device | Model Name | Resolution | DPI |
|--------|------------|------------|-----|
| A5X2 | Manta | 1920 x 2560 | 300 |
| A5X | - | 1404 x 1872 | 226 |
| A6X2 | Nomad | 1404 x 1872 | 300 |
| A6X | - | 1404 x 1872 | 300 |

## Template Requirements

### PNG Templates
- Must match device native resolution exactly
- **A5X2 (Manta):** 1920 x 2560 pixels
- **A5X/A6X:** 1404 x 1872 pixels
- Format: PNG (RGB or RGBA)
- Recommended: Use white or light background for readability

### PDF Templates
- Any standard PDF file
- Each page becomes a separate template page
- Pages are rendered at device native DPI and resized to device resolution
