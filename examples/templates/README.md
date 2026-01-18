# Templates for Golden Source Testing

This directory contains template files used to create golden source .note files on the Supernote device.

## Files

### blank_template.png
- **Dimensions:** 1404 x 1872 pixels (A5X native resolution)
- **Format:** PNG, RGB, white background
- **Purpose:** Used as a custom template for creating test notes

### sample_document.pdf
- **Pages:** 2
- **Purpose:** Used as a PDF template for multi-page note testing
- **Content:** Simple test document with text on each page

## How to Use

1. **Copy to Supernote:**
   - Connect Supernote via USB or use Supernote Partner app
   - Copy `blank_template.png` to `MyStyle/` folder on device
   - Copy `sample_document.pdf` to `Document/` folder on device

2. **Create Notes:**
   - For PNG template: Create new note → Template → Select from MyStyle
   - For PDF template: Create note → Settings → Change Template → Select PDF

## Template Requirements

### PNG Templates
- Must be exactly **1404 x 1872 pixels** for A5X
- Format: PNG (RGB or RGBA)
- Recommended: Use white or light background for readability

### PDF Templates
- Any standard PDF file
- Each page becomes a separate template page
- Pages are rendered at device DPI (226 for A5X)
