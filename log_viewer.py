#!/usr/bin/env python3
"""
FileNest Log Viewer
Friendly log viewing with filtering and search capabilities
"""

import os
import re
import argparse
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timezone
from collections import defaultdict

class LogViewer:
    """Friendly log viewer for FileNest operation logs"""
    
    def __init__(self, log_path: str = "file_organizer.log"):
        self.log_path = log_path
        self.log_entries = []
        self.load_logs()
    
    def load_logs(self):
        """Load and parse log entries"""
        if not os.path.exists(self.log_path):
            print(f"Log file not found: {self.log_path}")
            return
        
        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self.log_entries = []
            for line_num, line in enumerate(lines, 1):
                entry = self.parse_log_entry(line.strip(), line_num)
                if entry:
                    self.log_entries.append(entry)
                    
        except Exception as e:
            print(f"Error loading logs: {e}")
    
    def parse_log_entry(self, line: str, line_num: int) -> Optional[Dict]:
        """Parse a single log entry"""
        # Expected format: "2025-01-26T10:45:03Z | Moved | filename | source | dest"
        parts = [part.strip() for part in line.split('|')]
        
        if len(parts) < 3:
            return None
        
        try:
            timestamp_str = parts[0].strip()
            action = parts[1].strip()
            
            # Try to parse timestamp
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except:
                # Fallback for other timestamp formats
                timestamp = None
            
            entry = {
                'line_num': line_num,
                'timestamp': timestamp,
                'timestamp_str': timestamp_str,
                'action': action,
                'raw_line': line
            }
            
            # Parse additional fields based on action
            if action in ['Moved', 'Copied'] and len(parts) >= 5:
                entry.update({
                    'filename': parts[2].strip(),
                    'source': parts[3].strip(),
                    'destination': parts[4].strip()
                })
            elif action in ['Skipped', 'Error'] and len(parts) >= 4:
                entry.update({
                    'filename': parts[2].strip(),
                    'reason': parts[3].strip() if len(parts) > 3 else ''
                })
            elif action == 'Created' and len(parts) >= 3:
                entry.update({
                    'folder': parts[2].strip()
                })
            
            return entry
            
        except Exception:
            return None
    
    def show_recent_logs(self, count: int = 20):
        """Show recent log entries"""
        print(f"=== Recent {count} Log Entries ===")
        
        if not self.log_entries:
            print("No log entries found.")
            return
        
        recent_entries = self.log_entries[-count:] if len(self.log_entries) > count else self.log_entries
        
        for entry in recent_entries:
            self.print_entry(entry)
    
    def show_today_logs(self):
        """Show today's log entries"""
        print("=== Today's Log Entries ===")
        
        today = datetime.now().date()
        today_entries = []
        
        for entry in self.log_entries:
            if entry['timestamp'] and entry['timestamp'].date() == today:
                today_entries.append(entry)
        
        if not today_entries:
            print("No log entries for today.")
            return
        
        for entry in today_entries:
            self.print_entry(entry)
    
    def search_logs(self, query: str, case_sensitive: bool = False):
        """Search logs for specific text"""
        print(f"=== Search Results for '{query}' ===")
        
        if not case_sensitive:
            query = query.lower()
        
        matches = []
        
        for entry in self.log_entries:
            search_text = entry['raw_line']
            if not case_sensitive:
                search_text = search_text.lower()
            
            if query in search_text:
                matches.append(entry)
        
        if not matches:
            print("No matches found.")
            return
        
        print(f"Found {len(matches)} matches:")
        for entry in matches:
            self.print_entry(entry, highlight=query if case_sensitive else None)
    
    def filter_by_action(self, action: str):
        """Filter logs by action type"""
        print(f"=== Entries with Action: {action} ===")
        
        filtered_entries = [entry for entry in self.log_entries if entry['action'].lower() == action.lower()]
        
        if not filtered_entries:
            print(f"No entries found with action '{action}'.")
            return
        
        for entry in filtered_entries:
            self.print_entry(entry)
    
    def show_statistics(self):
        """Show log statistics"""
        print("=== Log Statistics ===")
        
        if not self.log_entries:
            print("No log entries to analyze.")
            return
        
        # Action counts
        action_counts = defaultdict(int)
        for entry in self.log_entries:
            action_counts[entry['action']] += 1
        
        print("\nAction Summary:")
        for action, count in sorted(action_counts.items()):
            print(f"  {action}: {count}")
        
        # Date range
        timestamps = [entry['timestamp'] for entry in self.log_entries if entry['timestamp']]
        if timestamps:
            earliest = min(timestamps)
            latest = max(timestamps)
            print(f"\nDate Range:")
            print(f"  Earliest: {earliest.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Latest: {latest.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # File type analysis (for Moved/Copied actions)
        extensions = defaultdict(int)
        for entry in self.log_entries:
            if entry['action'] in ['Moved', 'Copied'] and 'filename' in entry:
                filename = entry['filename']
                ext = Path(filename).suffix.lower()
                if ext:
                    extensions[ext] += 1
        
        if extensions:
            print(f"\nTop File Types (by count):")
            sorted_extensions = sorted(extensions.items(), key=lambda x: x[1], reverse=True)
            for ext, count in sorted_extensions[:10]:  # Top 10
                print(f"  {ext}: {count}")
        
        print(f"\nTotal Entries: {len(self.log_entries)}")
    
    def show_errors(self):
        """Show error entries"""
        print("=== Error Entries ===")
        
        error_entries = [entry for entry in self.log_entries if entry['action'] == 'Error']
        
        if not error_entries:
            print("No error entries found.")
            return
        
        for entry in error_entries:
            self.print_entry(entry, highlight_errors=True)
    
    def export_filtered_logs(self, output_file: str, action: Optional[str] = None, 
                           date_from: Optional[str] = None, date_to: Optional[str] = None):
        """Export filtered logs to file"""
        try:
            filtered_entries = self.log_entries.copy()
            
            # Filter by action
            if action:
                filtered_entries = [entry for entry in filtered_entries if entry['action'].lower() == action.lower()]
            
            # Filter by date range
            if date_from or date_to:
                date_filtered = []
                for entry in filtered_entries:
                    if not entry['timestamp']:
                        continue
                    
                    entry_date = entry['timestamp'].date()
                    
                    if date_from:
                        from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
                        if entry_date < from_date:
                            continue
                    
                    if date_to:
                        to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
                        if entry_date > to_date:
                            continue
                    
                    date_filtered.append(entry)
                
                filtered_entries = date_filtered
            
            # Write to file
            with open(output_file, 'w', encoding='utf-8') as f:
                for entry in filtered_entries:
                    f.write(entry['raw_line'] + '\n')
            
            print(f"✓ Exported {len(filtered_entries)} entries to: {output_file}")
            
        except Exception as e:
            print(f"Error exporting logs: {e}")
    
    def print_entry(self, entry: Dict, highlight: Optional[str] = None, highlight_errors: bool = False):
        """Print a formatted log entry"""
        timestamp = entry['timestamp_str']
        action = entry['action']
        
        # Color coding based on action
        if highlight_errors and action == 'Error':
            action_display = f"❌ {action}"
        elif action == 'Moved':
            action_display = f"📁 {action}"
        elif action == 'Created':
            action_display = f"🆕 {action}"
        elif action == 'Skipped':
            action_display = f"⏭️ {action}"
        elif action == 'Error':
            action_display = f"❌ {action}"
        else:
            action_display = action
        
        print(f"[{timestamp}] {action_display}", end="")
        
        # Add specific details based on action
        if action in ['Moved', 'Copied'] and 'filename' in entry:
            filename = entry['filename']
            source = entry.get('source', '')
            dest = entry.get('destination', '')
            print(f" | {filename}")
            print(f"    From: {source}")
            print(f"    To:   {dest}")
        elif action in ['Skipped', 'Error'] and 'filename' in entry:
            filename = entry['filename']
            reason = entry.get('reason', '')
            print(f" | {filename}")
            if reason:
                print(f"    Reason: {reason}")
        elif action == 'Created' and 'folder' in entry:
            folder = entry['folder']
            print(f" | {folder}")
        else:
            print()
    
    def interactive_viewer(self):
        """Interactive log viewer"""
        print("=== FileNest Interactive Log Viewer ===")
        print(f"Log file: {self.log_path}")
        print(f"Total entries: {len(self.log_entries)}")
        print()
        
        while True:
            print("\nOptions:")
            print("  1. Show recent entries")
            print("  2. Show today's entries") 
            print("  3. Search logs")
            print("  4. Filter by action")
            print("  5. Show statistics")
            print("  6. Show errors only")
            print("  7. Export filtered logs")
            print("  8. Reload logs")
            print("  q. Quit")
            
            choice = input("\nEnter choice: ").strip().lower()
            
            if choice == 'q':
                break
            elif choice == '1':
                count = input("Number of recent entries (default 20): ").strip()
                try:
                    count = int(count) if count else 20
                    self.show_recent_logs(count)
                except ValueError:
                    print("Invalid number, using default (20)")
                    self.show_recent_logs(20)
            elif choice == '2':
                self.show_today_logs()
            elif choice == '3':
                query = input("Enter search query: ").strip()
                if query:
                    case_sensitive = input("Case sensitive? (y/N): ").strip().lower() == 'y'
                    self.search_logs(query, case_sensitive)
            elif choice == '4':
                print("Available actions:", sorted(set(entry['action'] for entry in self.log_entries)))
                action = input("Enter action to filter by: ").strip()
                if action:
                    self.filter_by_action(action)
            elif choice == '5':
                self.show_statistics()
            elif choice == '6':
                self.show_errors()
            elif choice == '7':
                output_file = input("Output file name: ").strip()
                if output_file:
                    action = input("Filter by action (optional): ").strip() or None
                    date_from = input("From date (YYYY-MM-DD, optional): ").strip() or None
                    date_to = input("To date (YYYY-MM-DD, optional): ").strip() or None
                    self.export_filtered_logs(output_file, action, date_from, date_to)
            elif choice == '8':
                self.load_logs()
                print(f"✓ Reloaded logs. Total entries: {len(self.log_entries)}")
            else:
                print("Invalid choice. Please try again.")

def main():
    """Main CLI entry point for log viewer"""
    parser = argparse.ArgumentParser(
        prog='log_viewer',
        description='FileNest Log Viewer',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('--log', type=str, default='file_organizer.log',
                       help='Log file path (default: file_organizer.log)')
    parser.add_argument('--recent', type=int, metavar='N',
                       help='Show N recent log entries')
    parser.add_argument('--today', action='store_true',
                       help="Show today's log entries")
    parser.add_argument('--search', type=str, metavar='QUERY',
                       help='Search logs for specific text')
    parser.add_argument('--action', type=str, metavar='ACTION',
                       help='Filter logs by action (Moved, Created, Error, etc.)')
    parser.add_argument('--stats', action='store_true',
                       help='Show log statistics')
    parser.add_argument('--errors', action='store_true',
                       help='Show error entries only')
    parser.add_argument('--export', type=str, metavar='FILE',
                       help='Export filtered logs to file')
    parser.add_argument('--interactive', action='store_true',
                       help='Start interactive log viewer')
    
    args = parser.parse_args()
    
    # Create log viewer instance
    viewer = LogViewer(args.log)
    
    if args.interactive:
        viewer.interactive_viewer()
    elif args.recent is not None:
        viewer.show_recent_logs(args.recent)
    elif args.today:
        viewer.show_today_logs()
    elif args.search:
        viewer.search_logs(args.search)
    elif args.action:
        viewer.filter_by_action(args.action)
    elif args.stats:
        viewer.show_statistics()
    elif args.errors:
        viewer.show_errors()
    elif args.export:
        viewer.export_filtered_logs(args.export, args.action)
    else:
        # Default: show recent entries
        viewer.show_recent_logs()

if __name__ == "__main__":
    main()