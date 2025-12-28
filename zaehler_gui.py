#!/usr/bin/env python3
"""
GTK4‑GUI zum Erfassen von Strom‑Zählerständen und Export als CSV.
Author: Lumo (Proton AI)
"""

import csv
import datetime
import sys
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk, GLib, Gio

# ------------------------------------------------------------
# Hilfsfunktionen
# ------------------------------------------------------------
def today_str() -> str:
    """Rückgabe des heutigen Datums im ISO‑Format (YYYY‑MM‑DD)."""
    return datetime.date.today().isoformat()


def parse_date(text: str) -> datetime.date | None:
    """Versucht, einen String in ein Datum zu parsen (ISO oder DD.MM.YYYY)."""
    for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.datetime.strptime(text.strip(), fmt).date()
        except ValueError:
            continue
    return None


# ------------------------------------------------------------
# Hauptfenster
# ------------------------------------------------------------
class ZaehlerWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Zählerstand‑Erfassung")
        self.set_default_size(500, 400)

        # ----- Layout -------------------------------------------------
        grid = Gtk.Grid(row_spacing=10, column_spacing=10, margin=20)
        self.set_child(grid)

        # Eingabefelder
        lbl_date = Gtk.Label(label="Datum (YYYY‑MM‑DD):")
        self.entry_date = Gtk.Entry()
        self.entry_date.set_text(today_str())
        grid.attach(lbl_date, 0, 0, 1, 1)
        grid.attach(self.entry_date, 1, 0, 1, 1)

        lbl_value = Gtk.Label(label="Zählerstand (kWh):")
        self.entry_value = Gtk.Entry()
        self.entry_value.set_placeholder_text("z. B. 12345.6")
        grid.attach(lbl_value, 0, 1, 1, 1)
        grid.attach(self.entry_value, 1, 1, 1, 1)

        btn_add = Gtk.Button(label="Eintrag hinzufügen")
        btn_add.connect("clicked", self.on_add_clicked)
        grid.attach(btn_add, 0, 2, 2, 1)

        # ListStore + TreeView für die Übersicht
        self.store = Gtk.ListStore(str, str)  # Datum, Wert
        treeview = Gtk.TreeView(model=self.store)

        for i, col_title in enumerate(("Datum", "Wert (kWh)")):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)
            column.set_resizable(True)
            treeview.append_column(column)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.set_child(treeview)
        grid.attach(scrolled, 0, 3, 2, 1)

        # Export‑Buttons
        btn_export = Gtk.Button(label="Als CSV exportieren …")
        btn_export.connect("clicked", self.on_export_clicked)
        grid.attach(btn_export, 0, 4, 2, 1)

        # Status‑Label
        self.lbl_status = Gtk.Label(label="")
        grid.attach(self.lbl_status, 0, 5, 2, 1)

    # ------------------------------------------------------------------
    # Event‑Handler
    # ------------------------------------------------------------------
    def on_add_clicked(self, button):
        """Prüft Eingaben, fügt sie dem ListStore hinzu und leert die Felder."""
        date_txt = self.entry_date.get_text()
        value_txt = self.entry_value.get_text().strip()

        # Datum prüfen
        datum = parse_date(date_txt)
        if not datum:
            self._set_status("Ungültiges Datum – bitte im Format YYYY‑MM‑DD oder DD.MM.YYYY.", error=True)
            return

        # Wert prüfen
        try:
            wert = float(value_txt.replace(",", "."))  # Komma‑zu‑Punkt‑Umwandlung
        except ValueError:
            self._set_status("Zählerstand muss eine Zahl sein.", error=True)
            return

        # Eintrag speichern
        self.store.append([datum.isoformat(), f"{wert:.3f}"])
        self.entry_value.set_text("")
        self._set_status(f"Eintrag für {datum.isoformat()} hinzugefügt.", error=False)

    def on_export_clicked(self, button):
        """Öffnet einen Dateiauswahldialog und schreibt die CSV‑Datei."""
        dialog = Gtk.FileChooserDialog(
            title="CSV‑Datei speichern",
            parent=self,
            action=Gtk.FileChooserAction.SAVE,
        )
        dialog.add_button("_Abbrechen", Gtk.ResponseType.CANCEL)
        dialog.add_button("_Speichern", Gtk.ResponseType.ACCEPT)
        dialog.set_current_name("zaehlerstaende.csv")
        dialog.set_do_overwrite_confirmation(True)

        # Filter für CSV‑Dateien
        filter_csv = Gtk.FileFilter()
        filter_csv.set_name("CSV‑Dateien")
        filter_csv.add_pattern("*.csv")
        dialog.add_filter(filter_csv)

        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            path = Path(dialog.get_file().get_path())
            try:
                self._write_csv(path)
                self._set_status(f"Datei erfolgreich gespeichert: {path}", error=False)
            except Exception as exc:
                self._set_status(f"Fehler beim Schreiben: {exc}", error=True)
        dialog.destroy()

    # ------------------------------------------------------------------
    # Hilfsmethoden
    # ------------------------------------------------------------------
    def _write_csv(self, path: Path):
        """Schreibt den Inhalt des ListStore in eine CSV‑Datei."""
        with path.open("w", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow(["Datum", "Zählerstand_kWh"])
            for row in self.store:
                writer.writerow(row)

    def _set_status(self, message: str, *, error: bool = False):
        """Setzt das Status‑Label (rot bei Fehler)."""
        self.lbl_status.set_label(message)
        if error:
            self.lbl_status.add_css_class("error")
        else:
            self.lbl_status.remove_css_class("error")


# ------------------------------------------------------------
# Application‑Klasse
# ------------------------------------------------------------
class ZaehlerApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.proton.zaehlergui",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = ZaehlerWindow(self)
        win.show()


# ------------------------------------------------------------
# Einstiegspunkt
# ------------------------------------------------------------
if __name__ == "__main__":
    app = ZaehlerApp()
    exit_code = app.run(sys.argv)
    sys.exit(exit_code)