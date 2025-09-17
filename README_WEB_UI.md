# Tamil Character Recognition - Web Interface

This web interface provides an easy-to-use way to upload images and extract individual characters using the existing Tamil Character Recognition functionality.

## Features

- **Web-based Upload**: Simple drag-and-drop or click-to-upload interface
- **Character Extraction**: Uses the existing ImageWithText class to split images into individual characters
- **Visual Results**: Displays extracted characters in a clean grid layout
- **Multiple Formats**: Supports PNG, JPG, JPEG, GIF, and BMP image formats
- **Responsive Design**: Works on desktop and mobile devices

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the web application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

## Usage

1. **Upload an Image**: Click "Choose File" or drag and drop an image containing text/characters
2. **Process**: Click "Extract Characters" to process the image
3. **View Results**: Browse the extracted characters in the results page
4. **Download**: Click on individual characters to view them in detail, or download all characters

## Technical Details

### Dependencies Updated

The original code used deprecated `scipy.misc.imread` functions. The web interface includes compatibility layers that support:
- **imageio** (preferred): Modern image I/O library
- **Pillow (PIL)**: Alternative image processing library
- **scipy.misc** (fallback): For backward compatibility

### File Structure

```
tcr/
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html        # Upload interface
│   └── results.html      # Results display
├── sources/              # Original character recognition code
│   ├── TextWithImage.py  # Updated with new image loading methods
│   └── identify_text.py  # Updated with modern image libraries
├── uploads/              # Temporary upload storage
├── results/              # Extracted character storage
└── requirements.txt      # Python dependencies
```

### API Endpoints

- `GET /`: Main upload interface
- `POST /upload`: Handle file upload and processing
- `GET /results/<session_id>`: Display extraction results
- `GET /character/<session_id>/<filename>`: Serve individual character images

## Original Functionality

The web interface preserves all original character recognition functionality:
- Black and white image conversion
- Row and column character detection
- Individual character extraction
- GIF output format

## Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

## Limitations

- Maximum file size: 16MB
- Supported formats: PNG, JPG, JPEG, GIF, BMP
- Character images are saved as GIF files (original format)
- Temporary files are cleaned up after processing
