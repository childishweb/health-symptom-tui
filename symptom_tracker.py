"""
Health Symptom Tracker - Data Models and Storage
Handles symptom entries, persistence, and data management
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Any
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class SymptomEntry:
    """Represents a single symptom entry"""
    timestamp: str
    symptom_type: str
    severity: int  # 1-10 scale
    description: str
    location: str = ""
    duration: str = ""
    triggers: str = ""
    medications: str = ""
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SymptomEntry':
        """Create from dictionary"""
        return cls(**data)


class SymptomDatabase:
    """Manages symptom data storage and retrieval"""

    def __init__(self, data_dir: str = "symptom_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.data_file = self.data_dir / "symptoms.json"
        self.entries: List[SymptomEntry] = []
        self.load()

    def load(self):
        """Load symptoms from JSON file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.entries = [SymptomEntry.from_dict(entry) for entry in data]
            except (json.JSONDecodeError, KeyError):
                self.entries = []

    def save(self):
        """Save symptoms to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump([entry.to_dict() for entry in self.entries], f, indent=2)

    def add_entry(self, entry: SymptomEntry):
        """Add a new symptom entry"""
        self.entries.append(entry)
        self.save()

    def get_entries(self,
                    start_date: Optional[str] = None,
                    end_date: Optional[str] = None,
                    symptom_type: Optional[str] = None) -> List[SymptomEntry]:
        """Get filtered symptom entries"""
        filtered = self.entries

        if symptom_type:
            filtered = [e for e in filtered if symptom_type.lower() in e.symptom_type.lower()]

        if start_date:
            filtered = [e for e in filtered if e.timestamp >= start_date]

        if end_date:
            filtered = [e for e in filtered if e.timestamp <= end_date]

        return sorted(filtered, key=lambda x: x.timestamp, reverse=True)

    def export_to_txt(self, filename: Optional[str] = None) -> str:
        """Export symptoms to formatted text file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.data_dir / f"symptom_export_{timestamp}.txt"

        with open(filename, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("HEALTH SYMPTOM TRACKER - EXPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Entries: {len(self.entries)}\n\n")

            for entry in sorted(self.entries, key=lambda x: x.timestamp, reverse=True):
                f.write("-" * 80 + "\n")
                f.write(f"Date/Time: {entry.timestamp}\n")
                f.write(f"Symptom: {entry.symptom_type}\n")
                f.write(f"Severity: {entry.severity}/10\n")

                if entry.location:
                    f.write(f"Location: {entry.location}\n")
                if entry.duration:
                    f.write(f"Duration: {entry.duration}\n")
                if entry.triggers:
                    f.write(f"Triggers: {entry.triggers}\n")
                if entry.medications:
                    f.write(f"Medications: {entry.medications}\n")

                f.write(f"\nDescription: {entry.description}\n")

                if entry.notes:
                    f.write(f"\nAdditional Notes:\n{entry.notes}\n")

                f.write("\n")

        return str(filename)

    def export_to_org(self, filename: Optional[str] = None) -> str:
        """Export symptoms to Org-mode format"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = self.data_dir / f"symptom_export_{timestamp}.org"

        with open(filename, 'w') as f:
            f.write("#+TITLE: Health Symptom Tracker Export\n")
            f.write(f"#+DATE: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("#+AUTHOR: Health Symptom Tracker\n\n")

            f.write("* Overview\n\n")
            f.write(f"Total entries: {len(self.entries)}\n\n")

            # Group by date
            entries_by_date = {}
            for entry in self.entries:
                date = entry.timestamp.split('T')[0]
                if date not in entries_by_date:
                    entries_by_date[date] = []
                entries_by_date[date].append(entry)

            f.write("* Symptom Log\n\n")

            for date in sorted(entries_by_date.keys(), reverse=True):
                f.write(f"** {date}\n\n")

                for entry in sorted(entries_by_date[date],
                                   key=lambda x: x.timestamp, reverse=True):
                    time = entry.timestamp.split('T')[1] if 'T' in entry.timestamp else ""
                    f.write(f"*** {entry.symptom_type} - {time}\n")
                    f.write(":PROPERTIES:\n")
                    f.write(f":SEVERITY: {entry.severity}/10\n")
                    if entry.location:
                        f.write(f":LOCATION: {entry.location}\n")
                    if entry.duration:
                        f.write(f":DURATION: {entry.duration}\n")
                    f.write(":END:\n\n")

                    f.write(f"{entry.description}\n\n")

                    if entry.triggers:
                        f.write(f"*Triggers:* {entry.triggers}\n\n")
                    if entry.medications:
                        f.write(f"*Medications:* {entry.medications}\n\n")
                    if entry.notes:
                        f.write(f"*Notes:*\n{entry.notes}\n\n")

        return str(filename)

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about tracked symptoms"""
        if not self.entries:
            return {
                "total_entries": 0,
                "symptom_types": {},
                "avg_severity": 0,
                "date_range": None
            }

        symptom_types = {}
        total_severity = 0

        for entry in self.entries:
            symptom_types[entry.symptom_type] = symptom_types.get(entry.symptom_type, 0) + 1
            total_severity += entry.severity

        dates = [e.timestamp for e in self.entries]

        return {
            "total_entries": len(self.entries),
            "symptom_types": symptom_types,
            "avg_severity": total_severity / len(self.entries),
            "date_range": {
                "first": min(dates),
                "last": max(dates)
            }
        }


# Common symptom types for quick access
COMMON_SYMPTOMS = [
    "Headache",
    "Nausea",
    "Fatigue",
    "Pain",
    "Dizziness",
    "Fever",
    "Cough",
    "Shortness of breath",
    "Anxiety",
    "Depression",
    "Insomnia",
    "Muscle ache",
    "Joint pain",
    "Stomach pain",
    "Other"
]
