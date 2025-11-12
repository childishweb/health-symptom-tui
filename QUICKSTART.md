# Quick Start Guide

Get tracking your symptoms in under 1 minute!

## Installation (10 seconds)

```bash
cd health-symptom-tui
chmod +x tracker.py
```

That's it! No dependencies required (python-dateutil is optional).

## Your First Entry (10 seconds)

**Option 1: Interactive (Easiest)**
```bash
python tracker.py quick
```
Answer 3 questions and you're done!

**Option 2: One Command (Fastest)**
```bash
python tracker.py add -s "Headache" -S 7 -d "Throbbing pain in temples"
```

## Essential Commands

```bash
# Add a symptom
python tracker.py add -s "Headache" -S 7 -d "Pain after work"

# Track multiple symptoms
python tracker.py add -s "Headache, Nausea" -S 8 -d "Migraine symptoms"

# View recent entries
python tracker.py list

# Get statistics
python tracker.py stats

# Search
python tracker.py search "headache"

# Export for doctor
python tracker.py export --format txt
```

## Real World Examples

### Quick daily log
```bash
python tracker.py add -s "Fatigue" -S 6 -d "Tired, didn't sleep well"
```

### Track pain with medication
```bash
python tracker.py add -s "Back pain" -S 8 \
  -d "Lower back pain" -l "lumbar" -m "ibuprofen 400mg"
```

### Multiple symptoms
```bash
python tracker.py add -s "Headache, Nausea, Dizziness" -S 9 \
  -d "Bad migraine attack" -t "stress, lack of sleep"
```

### Review for appointment
```bash
python tracker.py list -n 30
python tracker.py stats
python tracker.py export --format txt -o doctor_visit.txt
```

## Tips for Speed

### Create an alias
Add to `~/.bashrc` or `~/.zshrc`:
```bash
alias sym='python3 /full/path/to/tracker.py'
```

Then just:
```bash
sym quick
sym add -s "Headache" -S 7 -d "Pain"
sym list
```

### Use short flags
```bash
sym add -s "Pain" -S 6 -d "Back hurts" -l "lower back" -m "tylenol"
```

### Interactive mode for casual logging
```bash
sym quick
# Just answer 3 questions, skip optional fields
```

## Get Help

```bash
# Main help
python tracker.py --help

# Command-specific help
python tracker.py add --help
python tracker.py list --help
```

## Next Steps

- Read the full [README.md](README.md) for all features
- Set up a shell alias for faster access
- Create automated backups with cron

---

**Remember**: This is for personal tracking. Always consult healthcare professionals for medical advice!
