# Health Symptom Tracker CLI

A fast, accessible command-line health symptom tracker designed with disabled users in mind. Track your symptoms quickly and export to `.txt` or `.org` files for your medical records.

## Features

- **Lightning Fast**: Add symptoms with a single command
- **Multiple Symptoms**: Track multiple symptoms in one entry (e.g., "Headache, Nausea")
- **Comprehensive Tracking**: Record symptom type, severity, location, duration, triggers, medications, and notes
- **Search & Filter**: Find past symptoms by type or date range
- **Multiple Export Formats**:
  - `.txt` - Plain text format, universally readable
  - `.org` - Org-mode format for Emacs users
- **Statistics**: View symptom frequency and severity trends
- **Persistent Storage**: All data saved locally in JSON format
- **100% Offline**: No internet required, complete privacy

## Quick Start

### Installation

```bash
# Clone or download this repository
cd health-symptom-tui

# Install dependencies (optional, only needs python-dateutil)
pip install -r requirements.txt

# Make executable
chmod +x tracker.py
```

### First Use

Add your first symptom:

```bash
# Quick interactive mode
python tracker.py quick

# Or add directly with one command
python tracker.py add -s "Headache" -S 7 -d "Throbbing pain in temples"
```

## Usage Guide

### Quick Entry (Interactive)

The fastest way to log symptoms:

```bash
python tracker.py quick
```

This will prompt you for:
- Symptom type(s)
- Severity (1-10)
- Description

### Add Symptom (Command Line)

Add a symptom with all details in one command:

```bash
python tracker.py add -s "Headache" -S 7 -d "Throbbing pain" \
  -l "temples" -D "2 hours" -t "screen time" -m "ibuprofen 400mg"
```

**Required flags:**
- `-s`, `--symptom`: Symptom type(s) - separate multiple with commas
- `-S`, `--severity`: Severity rating (1-10)
- `-d`, `--description`: Description of the symptom

**Optional flags:**
- `-l`, `--location`: Where you feel it
- `-D`, `--duration`: How long it lasted
- `-t`, `--triggers`: What might have caused it
- `-m`, `--medications`: What medications you took
- `-n`, `--notes`: Additional notes

### Track Multiple Symptoms

```bash
python tracker.py add -s "Headache, Nausea, Fatigue" -S 8 \
  -d "Migraine with multiple symptoms"
```

### List Recent Entries

```bash
# List last 20 entries (default)
python tracker.py list

# List last 5 entries
python tracker.py list -n 5

# Filter by symptom type
python tracker.py list -s "headache"

# Filter by date range
python tracker.py list --start-date 2024-01-01 --end-date 2024-12-31
```

### View Statistics

```bash
python tracker.py stats
```

Shows:
- Total entries
- Average severity
- Date range
- Symptom breakdown by frequency

### Search Symptoms

```bash
python tracker.py search "headache"

# With date filters
python tracker.py search "headache" --start-date 2024-01-01
```

### Export Data

```bash
# Export to plain text
python tracker.py export --format txt

# Export to org-mode
python tracker.py export --format org

# Export to specific file
python tracker.py export --format txt -o my_symptoms.txt
```

## Examples

### Daily Migraine Tracking

```bash
# Morning entry
python tracker.py add -s "Migraine" -S 9 \
  -d "Severe throbbing pain, light sensitivity" \
  -l "right side of head" -t "poor sleep" \
  -m "Sumatriptan 50mg at 7am"

# Follow-up after medication
python tracker.py add -s "Headache" -S 4 \
  -d "Much improved after medication" \
  -l "right temple" -n "Sumatriptan effective"
```

### Chronic Pain Monitoring

```bash
# Morning check-in
python tracker.py add -s "Pain" -S 6 \
  -d "Lower back pain upon waking" \
  -l "lower lumbar" -t "slept wrong"

# After physical therapy
python tracker.py add -s "Pain" -S 3 \
  -d "Much better after PT" \
  -l "lower back" -n "PT exercises helpful"
```

### Allergy Tracking

```bash
python tracker.py add -s "Allergies" -S 7 \
  -d "Sneezing, runny nose, itchy eyes" \
  -l "eyes, nose, throat" -D "all day" \
  -t "high pollen count, oak pollen" \
  -m "Claritin 10mg, Flonase" \
  -n "Pollen count: 9.2"
```

### Review Before Doctor Appointment

```bash
# View recent symptoms
python tracker.py list -n 30

# Get statistics
python tracker.py stats

# Export for doctor
python tracker.py export --format txt -o doctor_visit_2024-03-15.txt
```

## File Locations

All data is stored locally:

```
health-symptom-tui/
├── tracker.py           # Main CLI tool
├── symptom_tracker.py   # Data models
├── symptom_data/        # Your data (created on first use)
│   ├── symptoms.json    # Symptom database
│   ├── *.txt            # Text exports
│   └── *.org            # Org-mode exports
```

## Backup Your Data

**Important:** Backup your symptom data regularly!

```bash
# Backup the entire data directory
cp -r symptom_data symptom_data_backup_$(date +%Y%m%d)

# Or just backup the JSON file
cp symptom_data/symptoms.json symptoms_backup_$(date +%Y%m%d).json
```

## Accessibility Features

- **Fast**: Add a symptom in seconds with one command
- **Simple**: Only 3 required fields (symptom, severity, description)
- **Keyboard-only**: Standard command-line interface
- **No dependencies**: Minimal requirements (just Python)
- **Offline**: Works anywhere, no internet needed
- **Private**: All data stays on your computer

## Command Reference

```bash
# Help
python tracker.py --help
python tracker.py add --help

# Quick entry
python tracker.py quick

# Add symptom
python tracker.py add -s SYMPTOM -S SEVERITY -d DESCRIPTION [options]

# List entries
python tracker.py list [-n LIMIT] [--start-date DATE] [--end-date DATE] [-s SYMPTOM]

# Statistics
python tracker.py stats

# Search
python tracker.py search QUERY [--start-date DATE] [--end-date DATE]

# Export
python tracker.py export [-f FORMAT] [-o OUTPUT]
```

## Privacy & Security

- **100% Local**: All data stays on your computer
- **No Internet Required**: Works completely offline
- **No Telemetry**: No tracking or analytics
- **Your Data, Your Control**: You own and control all your health data
- **Open Source**: Fully transparent code

## Troubleshooting

### Installation Issues

```bash
# Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Permission Issues

```bash
# Make tracker executable
chmod +x tracker.py

# Ensure data directory is writable
mkdir -p symptom_data
chmod 755 symptom_data
```

### Python Version

Requires Python 3.7 or higher. Check your version:

```bash
python3 --version
```

## Advanced Usage

### Create Shell Alias

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias symptoms='python3 /path/to/health-symptom-tui/tracker.py'
```

Then use:

```bash
symptoms quick
symptoms add -s "Headache" -S 7 -d "Pain after work"
symptoms list
symptoms stats
```

### Automated Backups

Create a cron job to backup daily:

```bash
# Add to crontab (crontab -e)
0 2 * * * cp /path/to/symptom_data/symptoms.json /path/to/backups/symptoms_$(date +\%Y\%m\%d).json
```

## Data Format

Symptoms are stored as JSON:

```json
{
  "timestamp": "2024-11-12T10:30:00",
  "symptom_type": "Headache, Nausea",
  "severity": 8,
  "description": "Migraine with nausea",
  "location": "temples, stomach",
  "duration": "3 hours",
  "triggers": "bright lights",
  "medications": "ibuprofen 400mg",
  "notes": "Worse than usual"
}
```

## Contributing

This is an open-source project. Contributions, bug reports, and feature requests are welcome!

## License

MIT License with Medical Disclaimer - see LICENSE file

---

**Medical Disclaimer**: This tool is for personal tracking only and is not a substitute for professional medical advice. Always consult with healthcare providers about your symptoms and health concerns.

**Remember**: Back up your data regularly!
