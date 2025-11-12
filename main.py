#!/usr/bin/env python3
"""
Health Symptom Tracker TUI
A fast, accessible terminal-based symptom tracker for disabled users
"""
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Button, Static, Input, TextArea,
    Select, Label, DataTable, Markdown
)
from textual.screen import Screen
from textual.binding import Binding
from datetime import datetime
from symptom_tracker import SymptomDatabase, SymptomEntry, COMMON_SYMPTOMS


class QuickEntryScreen(Screen):
    """Fast symptom entry screen - optimized for speed"""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("ctrl+s", "save_entry", "Save (Ctrl+S)"),
    ]

    def __init__(self, db: SymptomDatabase):
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header()

        with ScrollableContainer():
            yield Static("⚡ QUICK SYMPTOM ENTRY", classes="title")
            yield Static("\nPress numbers 1-9 or use arrow keys to select symptom type:\n")

            # Symptom type selection
            yield Label("Symptom Type:")
            options = [(symptom, symptom) for symptom in COMMON_SYMPTOMS]
            yield Select(options, prompt="Select symptom type", id="symptom_type")

            # Quick severity input
            yield Label("\nSeverity (1-10):")
            yield Input(placeholder="Enter 1-10", id="severity", type="integer")

            # Description
            yield Label("\nDescription (required):")
            yield TextArea(id="description")

            # Optional fields
            yield Label("\nLocation (optional):")
            yield Input(placeholder="e.g., left temple, lower back", id="location")

            yield Label("\nDuration (optional):")
            yield Input(placeholder="e.g., 2 hours, all day", id="duration")

            yield Label("\nTriggers (optional):")
            yield Input(placeholder="e.g., bright lights, stress", id="triggers")

            yield Label("\nMedications taken (optional):")
            yield Input(placeholder="e.g., ibuprofen 400mg", id="medications")

            yield Label("\nAdditional notes (optional):")
            yield TextArea(id="notes")

            with Horizontal(classes="buttons"):
                yield Button("💾 Save (Ctrl+S)", variant="primary", id="save")
                yield Button("❌ Cancel (Esc)", variant="default", id="cancel")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "save":
            self.action_save_entry()
        elif event.button.id == "cancel":
            self.app.pop_screen()

    def action_save_entry(self) -> None:
        """Save the symptom entry"""
        symptom_select = self.query_one("#symptom_type", Select)
        severity_input = self.query_one("#severity", Input)
        description_input = self.query_one("#description", TextArea)
        location_input = self.query_one("#location", Input)
        duration_input = self.query_one("#duration", Input)
        triggers_input = self.query_one("#triggers", Input)
        medications_input = self.query_one("#medications", Input)
        notes_input = self.query_one("#notes", TextArea)

        # Validation
        if symptom_select.value == Select.BLANK:
            self.notify("Please select a symptom type", severity="error")
            return

        if not severity_input.value or not severity_input.value.strip():
            self.notify("Please enter severity (1-10)", severity="error")
            return

        try:
            severity = int(severity_input.value)
            if severity < 1 or severity > 10:
                self.notify("Severity must be between 1 and 10", severity="error")
                return
        except ValueError:
            self.notify("Severity must be a number between 1 and 10", severity="error")
            return

        if not description_input.text.strip():
            self.notify("Please enter a description", severity="error")
            return

        # Create entry
        entry = SymptomEntry(
            timestamp=datetime.now().isoformat(),
            symptom_type=str(symptom_select.value),
            severity=severity,
            description=description_input.text.strip(),
            location=location_input.value.strip(),
            duration=duration_input.value.strip(),
            triggers=triggers_input.value.strip(),
            medications=medications_input.value.strip(),
            notes=notes_input.text.strip()
        )

        self.db.add_entry(entry)
        self.notify("✓ Symptom entry saved!", severity="information")
        self.app.pop_screen()


class HistoryScreen(Screen):
    """View symptom history"""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("e", "export", "Export"),
    ]

    def __init__(self, db: SymptomDatabase):
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header()

        with Container():
            yield Static("📋 SYMPTOM HISTORY", classes="title")

            # Stats summary
            stats = self.db.get_stats()
            stats_text = f"""
**Total Entries:** {stats['total_entries']}
**Average Severity:** {stats['avg_severity']:.1f}/10

**Symptom Breakdown:**
"""
            for symptom, count in sorted(stats['symptom_types'].items(),
                                        key=lambda x: x[1], reverse=True):
                stats_text += f"  • {symptom}: {count}\n"

            yield Markdown(stats_text)

            # Recent entries table
            yield Static("\n**Recent Entries:**")
            table = DataTable(id="history_table")
            table.add_columns("Date/Time", "Symptom", "Severity", "Description")

            for entry in self.db.get_entries()[:50]:  # Show last 50
                date_time = entry.timestamp.replace('T', ' ')[:19]
                desc = entry.description[:50] + "..." if len(entry.description) > 50 else entry.description
                table.add_row(date_time, entry.symptom_type, f"{entry.severity}/10", desc)

            yield table

            with Horizontal(classes="buttons"):
                yield Button("📤 Export (E)", variant="primary", id="export")
                yield Button("🔙 Back (Esc)", variant="default", id="back")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "export":
            self.action_export()
        elif event.button.id == "back":
            self.app.pop_screen()

    def action_export(self) -> None:
        """Show export options"""
        self.app.push_screen(ExportScreen(self.db))


class ExportScreen(Screen):
    """Export data screen"""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
    ]

    def __init__(self, db: SymptomDatabase):
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header()

        with Container():
            yield Static("📤 EXPORT DATA", classes="title")
            yield Static("\nChoose export format:")

            with Vertical(classes="export-options"):
                yield Button("📄 Export to .txt (Plain Text)", variant="primary", id="export_txt")
                yield Button("📝 Export to .org (Org-mode)", variant="primary", id="export_org")
                yield Button("🔙 Back", variant="default", id="back")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "export_txt":
            filename = self.db.export_to_txt()
            self.notify(f"✓ Exported to {filename}", severity="information")
            self.app.pop_screen()
        elif event.button.id == "export_org":
            filename = self.db.export_to_org()
            self.notify(f"✓ Exported to {filename}", severity="information")
            self.app.pop_screen()
        elif event.button.id == "back":
            self.app.pop_screen()


class SearchScreen(Screen):
    """Search and filter symptoms"""

    BINDINGS = [
        Binding("escape", "app.pop_screen", "Back"),
        Binding("ctrl+f", "do_search", "Search"),
    ]

    def __init__(self, db: SymptomDatabase):
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header()

        with ScrollableContainer():
            yield Static("🔍 SEARCH SYMPTOMS", classes="title")

            yield Label("\nSearch by symptom type:")
            yield Input(placeholder="Enter symptom name", id="search_term")

            yield Label("\nStart date (YYYY-MM-DD, optional):")
            yield Input(placeholder="e.g., 2024-01-01", id="start_date")

            yield Label("\nEnd date (YYYY-MM-DD, optional):")
            yield Input(placeholder="e.g., 2024-12-31", id="end_date")

            with Horizontal(classes="buttons"):
                yield Button("🔍 Search (Ctrl+F)", variant="primary", id="search")
                yield Button("🔙 Back (Esc)", variant="default", id="back")

            yield Static("\n**Results:**", id="results_header")
            yield DataTable(id="results_table")

        yield Footer()

    def on_mount(self) -> None:
        """Set up the results table"""
        table = self.query_one("#results_table", DataTable)
        table.add_columns("Date/Time", "Symptom", "Severity", "Description")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "search":
            self.action_do_search()
        elif event.button.id == "back":
            self.app.pop_screen()

    def action_do_search(self) -> None:
        """Perform the search"""
        search_input = self.query_one("#search_term", Input)
        start_date_input = self.query_one("#start_date", Input)
        end_date_input = self.query_one("#end_date", Input)
        table = self.query_one("#results_table", DataTable)

        # Clear previous results
        table.clear()

        # Get search parameters
        symptom_type = search_input.value.strip() if search_input.value else None
        start_date = start_date_input.value.strip() if start_date_input.value else None
        end_date = end_date_input.value.strip() if end_date_input.value else None

        # Perform search
        results = self.db.get_entries(
            start_date=start_date,
            end_date=end_date,
            symptom_type=symptom_type
        )

        # Display results
        for entry in results:
            date_time = entry.timestamp.replace('T', ' ')[:19]
            desc = entry.description[:50] + "..." if len(entry.description) > 50 else entry.description
            table.add_row(date_time, entry.symptom_type, f"{entry.severity}/10", desc)

        self.notify(f"Found {len(results)} entries", severity="information")


class MainScreen(Screen):
    """Main menu screen"""

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("1", "quick_entry", "Quick Entry"),
        Binding("2", "view_history", "History"),
        Binding("3", "search", "Search"),
        Binding("4", "export", "Export"),
    ]

    def __init__(self, db: SymptomDatabase):
        super().__init__()
        self.db = db

    def compose(self) -> ComposeResult:
        """Create child widgets"""
        yield Header()

        with Container():
            yield Static("""
╔═══════════════════════════════════════════════════════╗
║                                                       ║
║       🏥 HEALTH SYMPTOM TRACKER                       ║
║                                                       ║
║       Fast, Accessible Terminal Symptom Tracking     ║
║                                                       ║
╚═══════════════════════════════════════════════════════╝
            """, classes="logo")

            stats = self.db.get_stats()
            yield Markdown(f"""
**Quick Stats:**
- Total entries tracked: {stats['total_entries']}
- Average severity: {stats['avg_severity']:.1f}/10
            """)

            yield Static("\n**Quick Actions:**\n")

            with Vertical(classes="menu"):
                yield Button("⚡ Quick Entry (1)", variant="primary", id="quick_entry")
                yield Button("📋 View History (2)", variant="default", id="history")
                yield Button("🔍 Search (3)", variant="default", id="search")
                yield Button("📤 Export Data (4)", variant="default", id="export")
                yield Button("❌ Quit (Q)", variant="error", id="quit")

        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "quick_entry":
            self.action_quick_entry()
        elif event.button.id == "history":
            self.action_view_history()
        elif event.button.id == "search":
            self.action_search()
        elif event.button.id == "export":
            self.action_export()
        elif event.button.id == "quit":
            self.app.exit()

    def action_quick_entry(self) -> None:
        """Open quick entry screen"""
        self.app.push_screen(QuickEntryScreen(self.db))

    def action_view_history(self) -> None:
        """Open history screen"""
        self.app.push_screen(HistoryScreen(self.db))

    def action_search(self) -> None:
        """Open search screen"""
        self.app.push_screen(SearchScreen(self.db))

    def action_export(self) -> None:
        """Open export screen"""
        self.app.push_screen(ExportScreen(self.db))


class SymptomTrackerApp(App):
    """Main application"""

    CSS = """
    Screen {
        background: $surface;
    }

    .title {
        text-align: center;
        text-style: bold;
        color: $accent;
        padding: 1;
    }

    .logo {
        text-align: center;
        color: $accent;
        padding: 1;
    }

    .menu {
        padding: 1 2;
        width: 100%;
    }

    .menu Button {
        width: 100%;
        margin: 1 0;
    }

    .buttons {
        padding: 1;
        height: auto;
    }

    .buttons Button {
        margin: 0 1;
    }

    .export-options {
        padding: 2;
    }

    .export-options Button {
        width: 100%;
        margin: 1 0;
    }

    Label {
        padding: 1 0 0 0;
        text-style: bold;
    }

    Input, TextArea, Select {
        margin: 0 0 1 0;
    }

    DataTable {
        height: auto;
        margin: 1 0;
    }

    Markdown {
        padding: 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def __init__(self):
        super().__init__()
        self.db = SymptomDatabase()

    def on_mount(self) -> None:
        """App startup"""
        self.title = "Health Symptom Tracker"
        self.sub_title = "Fast & Accessible Symptom Tracking"
        self.push_screen(MainScreen(self.db))


def main():
    """Run the application"""
    app = SymptomTrackerApp()
    app.run()


if __name__ == "__main__":
    main()
