#!/usr/bin/env python3
"""
Health Symptom Tracker CLI
A fast, accessible command-line symptom tracker
"""
import argparse
import sys
from datetime import datetime
from symptom_tracker import SymptomDatabase, SymptomEntry, COMMON_SYMPTOMS


def cmd_add(args, db):
    """Add a new symptom entry"""
    # Validate severity
    try:
        severity = int(args.severity)
        if severity < 1 or severity > 10:
            print("ERROR: Severity must be between 1 and 10")
            return 1
    except ValueError:
        print("ERROR: Severity must be a number between 1 and 10")
        return 1

    # Create entry
    entry = SymptomEntry(
        timestamp=datetime.now().isoformat(),
        symptom_type=args.symptom,
        severity=severity,
        description=args.description,
        location=args.location or "",
        duration=args.duration or "",
        triggers=args.triggers or "",
        medications=args.medications or "",
        notes=args.notes or ""
    )

    db.add_entry(entry)
    print("Symptom entry saved")
    print(f"  Symptom(s): {entry.symptom_type}")
    print(f"  Severity: {entry.severity}/10")
    print(f"  Time: {entry.timestamp}")
    return 0


def cmd_quick(args, db):
    """Quick entry - minimal fields"""
    # Get inputs interactively if not provided
    symptom = args.symptom
    if not symptom:
        print("\nCommon symptoms: " + ", ".join(COMMON_SYMPTOMS[:7]))
        symptom = input("Symptom(s) [separate multiple with commas]: ").strip()
        if not symptom:
            print("ERROR: Symptom type is required")
            return 1

    severity = args.severity
    if not severity:
        severity = input("Severity (1-10): ").strip()

    try:
        severity = int(severity)
        if severity < 1 or severity > 10:
            print("ERROR: Severity must be between 1 and 10")
            return 1
    except ValueError:
        print("ERROR: Severity must be a number")
        return 1

    description = args.description
    if not description:
        description = input("Description: ").strip()
        if not description:
            print("ERROR: Description is required")
            return 1

    # Create entry
    entry = SymptomEntry(
        timestamp=datetime.now().isoformat(),
        symptom_type=symptom,
        severity=severity,
        description=description,
        location="",
        duration="",
        triggers="",
        medications="",
        notes=""
    )

    db.add_entry(entry)
    print("\nSymptom entry saved")
    return 0


def cmd_list(args, db):
    """List recent symptom entries"""
    entries = db.get_entries(
        start_date=args.start_date,
        end_date=args.end_date,
        symptom_type=args.symptom
    )

    if not entries:
        print("No entries found")
        return 0

    limit = args.limit or 20
    print(f"\nShowing {min(len(entries), limit)} of {len(entries)} entries:\n")
    print("=" * 80)

    for i, entry in enumerate(entries[:limit]):
        date_time = entry.timestamp.replace('T', ' ')[:19]
        print(f"\n[{i+1}] {date_time}")
        print(f"Symptom: {entry.symptom_type}")
        print(f"Severity: {entry.severity}/10")
        print(f"Description: {entry.description}")

        if entry.location:
            print(f"Location: {entry.location}")
        if entry.duration:
            print(f"Duration: {entry.duration}")
        if entry.triggers:
            print(f"Triggers: {entry.triggers}")
        if entry.medications:
            print(f"Medications: {entry.medications}")
        if entry.notes:
            print(f"Notes: {entry.notes}")

    print("\n" + "=" * 80)
    return 0


def cmd_stats(args, db):
    """Show statistics"""
    stats = db.get_stats()

    print("\nHEALTH SYMPTOM TRACKER - STATISTICS")
    print("=" * 80)
    print(f"\nTotal Entries: {stats['total_entries']}")
    print(f"Average Severity: {stats['avg_severity']:.1f}/10")

    if stats['date_range']:
        print(f"\nDate Range:")
        print(f"  First entry: {stats['date_range']['first']}")
        print(f"  Last entry: {stats['date_range']['last']}")

    if stats['symptom_types']:
        print(f"\nSymptom Breakdown:")
        for symptom, count in sorted(stats['symptom_types'].items(),
                                     key=lambda x: x[1], reverse=True):
            pct = (count / stats['total_entries']) * 100
            print(f"  {symptom}: {count} ({pct:.1f}%)")

    print("\n" + "=" * 80)
    return 0


def cmd_export(args, db):
    """Export data"""
    if args.format == 'txt':
        filename = db.export_to_txt(args.output)
        print(f"Exported to: {filename}")
    elif args.format == 'org':
        filename = db.export_to_org(args.output)
        print(f"Exported to: {filename}")
    else:
        print(f"ERROR: Unknown format '{args.format}'")
        return 1

    return 0


def cmd_search(args, db):
    """Search symptoms"""
    results = db.get_entries(
        start_date=args.start_date,
        end_date=args.end_date,
        symptom_type=args.query
    )

    if not results:
        print(f"No results found for '{args.query}'")
        return 0

    print(f"\nFound {len(results)} entries matching '{args.query}':\n")
    print("=" * 80)

    for i, entry in enumerate(results[:20]):
        date_time = entry.timestamp.replace('T', ' ')[:19]
        print(f"\n[{i+1}] {date_time} - {entry.symptom_type} (Severity: {entry.severity}/10)")
        print(f"    {entry.description}")

    if len(results) > 20:
        print(f"\n... and {len(results) - 20} more results")

    print("\n" + "=" * 80)
    return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Health Symptom Tracker - Fast, accessible command-line symptom tracking',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Quick entry (interactive)
  tracker.py quick

  # Add symptom with all details
  tracker.py add -s "Headache" -S 7 -d "Throbbing pain" -l "temples" -m "ibuprofen 400mg"

  # Add multiple symptoms
  tracker.py add -s "Headache, Nausea" -S 8 -d "Migraine with nausea"

  # List recent entries
  tracker.py list

  # Show statistics
  tracker.py stats

  # Search for specific symptom
  tracker.py search "headache"

  # Export to text file
  tracker.py export --format txt

  # Export to org-mode file
  tracker.py export --format org
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Quick entry command
    parser_quick = subparsers.add_parser('quick', help='Quick symptom entry (interactive)')
    parser_quick.add_argument('-s', '--symptom', help='Symptom type(s)')
    parser_quick.add_argument('-S', '--severity', help='Severity (1-10)')
    parser_quick.add_argument('-d', '--description', help='Description')

    # Add command
    parser_add = subparsers.add_parser('add', help='Add a new symptom entry')
    parser_add.add_argument('-s', '--symptom', required=True,
                           help='Symptom type(s) - separate multiple with commas')
    parser_add.add_argument('-S', '--severity', required=True,
                           help='Severity (1-10)')
    parser_add.add_argument('-d', '--description', required=True,
                           help='Description of the symptom')
    parser_add.add_argument('-l', '--location',
                           help='Location (e.g., "left temple")')
    parser_add.add_argument('-D', '--duration',
                           help='Duration (e.g., "2 hours")')
    parser_add.add_argument('-t', '--triggers',
                           help='Triggers (e.g., "bright lights")')
    parser_add.add_argument('-m', '--medications',
                           help='Medications taken (e.g., "ibuprofen 400mg")')
    parser_add.add_argument('-n', '--notes',
                           help='Additional notes')

    # List command
    parser_list = subparsers.add_parser('list', help='List recent symptom entries')
    parser_list.add_argument('-n', '--limit', type=int,
                            help='Number of entries to show (default: 20)')
    parser_list.add_argument('--start-date',
                            help='Start date filter (YYYY-MM-DD)')
    parser_list.add_argument('--end-date',
                            help='End date filter (YYYY-MM-DD)')
    parser_list.add_argument('-s', '--symptom',
                            help='Filter by symptom type')

    # Stats command
    subparsers.add_parser('stats', help='Show statistics')

    # Search command
    parser_search = subparsers.add_parser('search', help='Search symptoms')
    parser_search.add_argument('query', help='Search query (symptom name)')
    parser_search.add_argument('--start-date',
                              help='Start date filter (YYYY-MM-DD)')
    parser_search.add_argument('--end-date',
                              help='End date filter (YYYY-MM-DD)')

    # Export command
    parser_export = subparsers.add_parser('export', help='Export data')
    parser_export.add_argument('-f', '--format', choices=['txt', 'org'],
                              default='txt',
                              help='Export format (default: txt)')
    parser_export.add_argument('-o', '--output',
                              help='Output filename (optional)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Initialize database
    db = SymptomDatabase()

    # Execute command
    commands = {
        'add': cmd_add,
        'quick': cmd_quick,
        'list': cmd_list,
        'stats': cmd_stats,
        'export': cmd_export,
        'search': cmd_search
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        return cmd_func(args, db)
    else:
        print(f"ERROR: Unknown command '{args.command}'")
        return 1


if __name__ == "__main__":
    sys.exit(main())
