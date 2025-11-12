# 🏥 Health Symptom Tracker TUI

A fast, accessible terminal-based health symptom tracker designed with disabled users in mind. Track your symptoms quickly and export to `.txt` or `.org` files for your medical records.

## ✨ Features

- **⚡ Lightning Fast Entry**: Optimized for quick symptom logging with minimal keystrokes
- **♿ Accessibility First**: Fully keyboard-driven interface, no mouse required
- **📊 Comprehensive Tracking**: Record symptom type, severity, location, duration, triggers, medications, and notes
- **🔍 Search & Filter**: Find past symptoms by type, date range, or keyword
- **📤 Multiple Export Formats**:
  - `.txt` - Plain text format, universally readable
  - `.org` - Org-mode format for Emacs users and structured note-taking
- **📈 Statistics**: View symptom frequency, severity trends, and patterns
- **💾 Persistent Storage**: All data saved locally in JSON format
- **🎨 Clean Interface**: Modern TUI with intuitive navigation

## 🚀 Quick Start

### Installation

```bash
# Clone or download this repository
cd health-symptom-tui

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### First Use

1. Launch the app: `python main.py`
2. Press `1` or click "Quick Entry" to log your first symptom
3. Fill in the required fields (symptom type, severity, description)
4. Press `Ctrl+S` to save
5. Done! Your symptom is now tracked.

## 📖 Usage Guide

### Main Menu

When you start the application, you'll see the main menu with these options:

- **⚡ Quick Entry (1)**: Log a new symptom
- **📋 View History (2)**: See all your tracked symptoms
- **🔍 Search (3)**: Find specific symptoms
- **📤 Export Data (4)**: Export to .txt or .org files
- **❌ Quit (Q)**: Exit the application

### Quick Entry

The quick entry screen lets you log symptoms fast:

**Required Fields:**
- **Symptom Type**: Choose from common symptoms or select "Other"
- **Severity**: Rate 1-10 (1 = mild, 10 = severe)
- **Description**: Describe what you're experiencing

**Optional Fields:**
- **Location**: Where do you feel it? (e.g., "left temple", "lower back")
- **Duration**: How long has it lasted? (e.g., "2 hours", "all day")
- **Triggers**: What might have caused it? (e.g., "bright lights", "stress")
- **Medications**: What did you take? (e.g., "ibuprofen 400mg")
- **Notes**: Any additional information

**Keyboard Shortcuts:**
- `Ctrl+S`: Save entry
- `Esc`: Cancel and return to main menu
- `Tab`: Move to next field
- `Shift+Tab`: Move to previous field

### View History

See all your logged symptoms with:
- Total entries count
- Average severity
- Breakdown by symptom type
- Table of recent entries (last 50)

Press `E` to export from this screen.

### Search

Filter your symptoms by:
- **Symptom type**: Search by name (e.g., "headache")
- **Date range**: Filter by start/end dates (YYYY-MM-DD format)

Press `Ctrl+F` to perform the search.

### Export

Export your data in two formats:

1. **Plain Text (.txt)**
   - Human-readable format
   - Easy to share with doctors
   - Can be opened in any text editor
   - Great for printing

2. **Org-mode (.org)**
   - Structured format for Emacs
   - Hierarchical organization by date
   - Includes property drawers for metadata
   - Perfect for long-term record keeping

Exported files are saved in `symptom_data/` directory with timestamps.

## 🎯 Accessibility Features

### Designed for Speed
- Single-key navigation (1, 2, 3, 4, Q)
- Minimal required fields
- Smart defaults
- No unnecessary confirmations

### Keyboard-Friendly
- No mouse required
- Clear visual focus indicators
- Consistent keyboard shortcuts across all screens
- Tab navigation through all fields

### Visual Clarity
- High-contrast interface
- Clear section headers
- Emoji icons for quick visual recognition
- Large, readable buttons

### Common Symptoms Quick-Select
Pre-populated list includes:
- Headache
- Nausea
- Fatigue
- Pain
- Dizziness
- Fever
- Cough
- Shortness of breath
- Anxiety
- Depression
- Insomnia
- Muscle ache
- Joint pain
- Stomach pain
- Other (for custom entries)

## 📁 Data Storage

All data is stored locally on your computer:

- **symptom_data/symptoms.json**: Your symptom database
- **symptom_data/symptom_export_*.txt**: Text exports
- **symptom_data/symptom_export_*.org**: Org-mode exports

### Data Format

Symptoms are stored as JSON with the following structure:

```json
{
  "timestamp": "2024-11-12T10:30:00",
  "symptom_type": "Headache",
  "severity": 7,
  "description": "Throbbing pain in temples",
  "location": "Both temples",
  "duration": "2 hours",
  "triggers": "Bright screen",
  "medications": "Ibuprofen 400mg",
  "notes": "Started after work meeting"
}
```

### Backup Your Data

It's important to backup your symptom data regularly:

```bash
# Backup the entire data directory
cp -r symptom_data symptom_data_backup_$(date +%Y%m%d)

# Or just backup the JSON file
cp symptom_data/symptoms.json symptoms_backup_$(date +%Y%m%d).json
```

## 🔒 Privacy

- **100% Local**: All data stays on your computer
- **No Internet Required**: Works completely offline
- **No Telemetry**: No tracking or analytics
- **Your Data, Your Control**: You own and control all your health data

## ⌨️ Keyboard Shortcuts Reference

### Global Shortcuts
- `Ctrl+Q`: Quit application (from anywhere)
- `Esc`: Go back / Cancel
- `Tab`: Next field
- `Shift+Tab`: Previous field

### Main Menu
- `1`: Quick Entry
- `2`: View History
- `3`: Search
- `4`: Export
- `Q`: Quit

### Quick Entry Screen
- `Ctrl+S`: Save entry

### History Screen
- `E`: Export

### Search Screen
- `Ctrl+F`: Perform search

## 🛠️ Advanced Usage

### Custom Symptom Types

While the app provides common symptoms, you can always select "Other" and enter your own custom symptom type in the description field.

### Batch Export

You can export your data anytime:
1. From the main menu, press `4`
2. Choose your format (txt or org)
3. Files are saved with timestamps

### Viewing Export Files

```bash
# View text exports
cat symptom_data/symptom_export_*.txt

# View in your preferred text editor
nano symptom_data/symptom_export_*.txt

# For Org-mode users
emacs symptom_data/symptom_export_*.org
```

## 🐛 Troubleshooting

### Installation Issues

If you have trouble installing dependencies:

```bash
# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### Display Issues

If the interface doesn't display correctly:

1. Make sure your terminal supports Unicode
2. Increase your terminal size (at least 80x24)
3. Try a different terminal emulator (e.g., Windows Terminal, iTerm2, Alacritty)

### Permission Issues

If you can't save data:

```bash
# Make sure the data directory is writable
mkdir -p symptom_data
chmod 755 symptom_data
```

## 🤝 Contributing

This is an open-source project. Contributions, bug reports, and feature requests are welcome!

### Potential Enhancements
- Medication tracking integration
- Chart/graph generation
- Calendar view
- Reminder notifications
- Multi-user support
- Cloud backup option
- CSV export
- PDF report generation

## 📄 License

This project is open source and available under the MIT License.

## 💬 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the keyboard shortcuts reference
3. Ensure you're running the latest version
4. Check that all dependencies are installed

## 🙏 Acknowledgments

Built with:
- [Textual](https://textual.textualize.io/) - Modern TUI framework
- [Rich](https://rich.readthedocs.io/) - Beautiful terminal formatting
- Python 3.x

---

**Remember**: This tool is for personal tracking only and is not a substitute for professional medical advice. Always consult with healthcare providers about your symptoms and health concerns.

**Your health data is important. Back it up regularly!**
