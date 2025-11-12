# 🚀 Quick Start Guide

Get up and running in under 2 minutes!

## Installation (30 seconds)

```bash
# Option 1: Quick install
pip install -r requirements.txt
python main.py

# Option 2: Use the install script
chmod +x install.sh
./install.sh
```

## First Entry (30 seconds)

1. **Launch**: `python main.py`
2. **Press** `1` for Quick Entry
3. **Select** symptom type (use arrow keys)
4. **Enter** severity (1-10)
5. **Type** a brief description
6. **Press** `Ctrl+S` to save
7. **Done!** ✓

## Essential Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `1` | Quick Entry (from main menu) |
| `2` | View History |
| `3` | Search Symptoms |
| `4` | Export Data |
| `Q` | Quit |
| `Ctrl+S` | Save Entry |
| `Esc` | Go Back |
| `Tab` | Next Field |

## Quick Tips for Speed

### Fastest Entry Method
1. Press `1` (Quick Entry)
2. Arrow down to your symptom or press Enter if it's pre-selected
3. Tab to severity, type number
4. Tab to description, type brief note
5. `Ctrl+S` to save

**Total time: ~10-15 seconds** ⚡

### Skip Optional Fields
Only 3 fields are required:
- Symptom type
- Severity (1-10)
- Description

Everything else is optional. Skip what you don't need!

### Common Workflows

**Morning check-in:**
```
1 → Select symptom → Tab → Severity → Tab → "Woke up with this" → Ctrl+S
```

**Quick pain log:**
```
1 → Pain → Tab → 7 → Tab → "Sharp pain in lower back" → Ctrl+S
```

**Medication tracking:**
```
1 → Symptom → Severity → Description → Tab through to Medications →
"Ibuprofen 400mg at 10am" → Ctrl+S
```

## Export Your Data

### To share with your doctor:
1. Press `4` (Export)
2. Choose "Export to .txt"
3. File saved to `symptom_data/symptom_export_TIMESTAMP.txt`
4. Open and print or email to doctor

### For long-term tracking:
1. Press `4` (Export)
2. Choose "Export to .org"
3. Open in Emacs or any text editor
4. Organized by date with full details

## File Locations

```
health-symptom-tui/
├── main.py              # Run this
├── symptom_tracker.py   # Data handling
├── symptom_data/        # Your data
│   ├── symptoms.json    # Database
│   ├── *.txt            # Text exports
│   └── *.org            # Org exports
```

## Backup Your Data

**Important:** Backup regularly!

```bash
# Quick backup
cp -r symptom_data symptom_data_backup

# Or just the database
cp symptom_data/symptoms.json symptoms_backup.json
```

## Accessibility Features

✅ **100% keyboard driven** - No mouse needed
✅ **Tab navigation** - Move through fields easily
✅ **Single-key commands** - Main menu uses 1, 2, 3, 4, Q
✅ **Clear visual hierarchy** - Easy to scan
✅ **Quick defaults** - Minimal typing required
✅ **Escape anywhere** - Always easy to exit

## Example Session

```
# Start the app
$ python main.py

# You see the main menu
# Press 1 for Quick Entry

# Use arrows to select "Headache"
# Press Enter or Tab

# Type: 7 (severity)
# Press Tab

# Type: "Throbbing pain behind eyes after screen time"
# Press Ctrl+S

# ✓ Saved! Back to main menu

# Press 2 to view history
# See your entry in the table

# Press E to export
# Choose .txt format
# ✓ Exported!

# Press Esc twice to get back to main menu
# Press Q to quit
```

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out all keyboard shortcuts
- Learn about search and filtering
- Explore both export formats

---

**Remember**: This is for personal tracking. Always consult healthcare professionals for medical advice!

Need help? Check [README.md](README.md) for troubleshooting.
