#!/usr/bin/env python3
"""
Enhanced Logger for File Organizer v2.0
Advanced logging with multiple formats, rotation, and analysis
"""

import json
import csv
import sqlite3
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import threading

class LogLevel(Enum):
    """Log levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"

class ActionType(Enum):
    """Types of file actions"""
    MOVED = "MOVED"
    COPIED = "COPIED"
    DELETED = "DELETED"
    RENAMED = "RENAMED"
    SKIPPED = "SKIPPED"
    ERROR = "ERROR"

@dataclass
class LogEntry:
    """A single log entry"""
    timestamp: str
    session_id: str
    action: ActionType
    source_path: str
    destination_path: Optional[str] = None
    file_size: Optional[int] = None
    file_type: Optional[str] = None
    category: Optional[str] = None
    error_message: Optional[str] = None
    level: LogLevel = LogLevel.INFO
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'timestamp': self.timestamp,
            'session_id': self.session_id,
            'action': self.action.value,
            'source_path': self.source_path,
            'destination_path': self.destination_path,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'category': self.category,
            'error_message': self.error_message,
            'level': self.level.value
        }

@dataclass
class SessionSummary:
    """Summary of an organization session"""
    session_id: str
    start_time: str
    end_time: str
    profile_name: str
    target_directory: str
    total_files: int
    files_moved: int
    files_copied: int
    files_skipped: int
    errors: int
    categories: Dict[str, int]
    total_size_processed: int
    duration_seconds: float

class Logger:
    """Enhanced logger with multiple output formats and analysis"""
    
    def __init__(self, log_dir: str = "logs", enable_database: bool = True):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        self.current_session_id = self._generate_session_id()
        self.session_start_time = datetime.now()
        self.entries: List[LogEntry] = []
        
        # Thread safety
        self._lock = threading.Lock()
        
        # File handles
        self.text_log_file = None
        self.json_log_file = None
        self.csv_log_file = None
        self.csv_writer = None
        
        # Database connection
        self.db_connection = None
        if enable_database:
            self._init_database()
        
        # Setup file logging
        self._setup_file_logging()
        
        # Current session stats
        self.session_stats = {
            'total_files': 0,
            'files_moved': 0,
            'files_copied': 0,
            'files_skipped': 0,
            'errors': 0,
            'categories': {},
            'total_size': 0
        }
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def _init_database(self):
        """Initialize SQLite database for structured logging"""
        try:
            db_path = self.log_dir / "file_organizer.db"
            self.db_connection = sqlite3.connect(str(db_path), check_same_thread=False)
            
            # Create tables
            self.db_connection.execute("""
                CREATE TABLE IF NOT EXISTS log_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    source_path TEXT NOT NULL,
                    destination_path TEXT,
                    file_size INTEGER,
                    file_type TEXT,
                    category TEXT,
                    error_message TEXT,
                    level TEXT DEFAULT 'INFO'
                )
            """)
            
            self.db_connection.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    profile_name TEXT,
                    target_directory TEXT,
                    total_files INTEGER DEFAULT 0,
                    files_moved INTEGER DEFAULT 0,
                    files_copied INTEGER DEFAULT 0,
                    files_skipped INTEGER DEFAULT 0,
                    errors INTEGER DEFAULT 0,
                    total_size_processed INTEGER DEFAULT 0,
                    duration_seconds REAL DEFAULT 0.0
                )
            """)
            
            self.db_connection.commit()
            
        except Exception as e:
            print(f"Warning: Could not initialize database: {e}")
            self.db_connection = None
    
    def _setup_file_logging(self):
        """Setup file-based logging"""
        try:
            # Text log file
            text_log_path = self.log_dir / f"{self.current_session_id}.log"
            self.text_log_file = open(text_log_path, 'w', encoding='utf-8')
            
            # JSON log file
            json_log_path = self.log_dir / f"{self.current_session_id}.json"
            self.json_log_file = open(json_log_path, 'w', encoding='utf-8')
            self.json_log_file.write('[\n')  # Start JSON array
            
            # CSV log file
            csv_log_path = self.log_dir / f"{self.current_session_id}.csv"
            self.csv_log_file = open(csv_log_path, 'w', newline='', encoding='utf-8')
            self.csv_writer = csv.writer(self.csv_log_file)
            
            # Write CSV header
            self.csv_writer.writerow([
                'timestamp', 'session_id', 'action', 'source_path', 'destination_path',
                'file_size', 'file_type', 'category', 'error_message', 'level'
            ])
            
        except Exception as e:
            print(f"Warning: Could not setup file logging: {e}")
    
    def log(self, action: ActionType, source_path: str, destination_path: str = None,
            file_size: int = None, file_type: str = None, category: str = None,
            error_message: str = None, level: LogLevel = LogLevel.INFO):
        """Log a file operation"""
        
        with self._lock:
            entry = LogEntry(
                timestamp=datetime.now().isoformat(),
                session_id=self.current_session_id,
                action=action,
                source_path=source_path,
                destination_path=destination_path,
                file_size=file_size,
                file_type=file_type,
                category=category,
                error_message=error_message,
                level=level
            )
            
            self.entries.append(entry)
            self._update_session_stats(action, category, file_size)
            
            # Write to files
            self._write_to_files(entry)
            
            # Write to database
            if self.db_connection:
                self._write_to_database(entry)
    
    def _update_session_stats(self, action: ActionType, category: str, file_size: int):
        """Update current session statistics"""
        self.session_stats['total_files'] += 1
        
        if action == ActionType.MOVED:
            self.session_stats['files_moved'] += 1
        elif action == ActionType.COPIED:
            self.session_stats['files_copied'] += 1
        elif action == ActionType.SKIPPED:
            self.session_stats['files_skipped'] += 1
        elif action == ActionType.ERROR:
            self.session_stats['errors'] += 1
        
        if category:
            self.session_stats['categories'][category] = self.session_stats['categories'].get(category, 0) + 1
        
        if file_size:
            self.session_stats['total_size'] += file_size
    
    def _write_to_files(self, entry: LogEntry):
        """Write log entry to file outputs"""
        try:
            # Text log
            if self.text_log_file:
                if entry.destination_path:
                    text_line = f"{entry.timestamp} | {entry.action.value}: {entry.source_path} → {entry.destination_path}"
                else:
                    text_line = f"{entry.timestamp} | {entry.action.value}: {entry.source_path}"
                
                if entry.error_message:
                    text_line += f" | ERROR: {entry.error_message}"
                
                self.text_log_file.write(text_line + '\n')
                self.text_log_file.flush()
            
            # JSON log
            if self.json_log_file:
                if len(self.entries) > 1:
                    self.json_log_file.write(',\n')
                json.dump(entry.to_dict(), self.json_log_file, indent=2)
                self.json_log_file.flush()
            
            # CSV log
            if self.csv_writer:
                self.csv_writer.writerow([
                    entry.timestamp, entry.session_id, entry.action.value,
                    entry.source_path, entry.destination_path or '',
                    entry.file_size or '', entry.file_type or '',
                    entry.category or '', entry.error_message or '',
                    entry.level.value
                ])
                self.csv_log_file.flush()
                
        except Exception as e:
            print(f"Warning: Error writing to log files: {e}")
    
    def _write_to_database(self, entry: LogEntry):
        """Write log entry to database"""
        try:
            self.db_connection.execute("""
                INSERT INTO log_entries (
                    timestamp, session_id, action, source_path, destination_path,
                    file_size, file_type, category, error_message, level
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.timestamp, entry.session_id, entry.action.value,
                entry.source_path, entry.destination_path, entry.file_size,
                entry.file_type, entry.category, entry.error_message, entry.level.value
            ))
            self.db_connection.commit()
            
        except Exception as e:
            print(f"Warning: Error writing to database: {e}")
    
    def start_session(self, profile_name: str, target_directory: str):
        """Start a new logging session"""
        if self.db_connection:
            try:
                self.db_connection.execute("""
                    INSERT INTO sessions (session_id, start_time, profile_name, target_directory)
                    VALUES (?, ?, ?, ?)
                """, (self.current_session_id, self.session_start_time.isoformat(), profile_name, target_directory))
                self.db_connection.commit()
            except Exception as e:
                print(f"Warning: Error starting session in database: {e}")
    
    def end_session(self) -> SessionSummary:
        """End the current logging session and return summary"""
        end_time = datetime.now()
        duration = (end_time - self.session_start_time).total_seconds()
        
        summary = SessionSummary(
            session_id=self.current_session_id,
            start_time=self.session_start_time.isoformat(),
            end_time=end_time.isoformat(),
            profile_name="",  # Will be set by caller
            target_directory="",  # Will be set by caller
            total_files=self.session_stats['total_files'],
            files_moved=self.session_stats['files_moved'],
            files_copied=self.session_stats['files_copied'],
            files_skipped=self.session_stats['files_skipped'],
            errors=self.session_stats['errors'],
            categories=self.session_stats['categories'].copy(),
            total_size_processed=self.session_stats['total_size'],
            duration_seconds=duration
        )
        
        # Update database
        if self.db_connection:
            try:
                self.db_connection.execute("""
                    UPDATE sessions SET 
                        end_time = ?, total_files = ?, files_moved = ?, files_copied = ?,
                        files_skipped = ?, errors = ?, total_size_processed = ?, duration_seconds = ?
                    WHERE session_id = ?
                """, (
                    end_time.isoformat(), summary.total_files, summary.files_moved,
                    summary.files_copied, summary.files_skipped, summary.errors,
                    summary.total_size_processed, summary.duration_seconds, self.current_session_id
                ))
                self.db_connection.commit()
            except Exception as e:
                print(f"Warning: Error updating session in database: {e}")
        
        # Close file handles
        self._close_files()
        
        return summary
    
    def _close_files(self):
        """Close log file handles"""
        try:
            if self.text_log_file:
                self.text_log_file.close()
                self.text_log_file = None
            
            if self.json_log_file:
                self.json_log_file.write('\n]')  # Close JSON array
                self.json_log_file.close()
                self.json_log_file = None
            
            if self.csv_log_file:
                self.csv_log_file.close()
                self.csv_log_file = None
                self.csv_writer = None
                
        except Exception as e:
            print(f"Warning: Error closing log files: {e}")
    
    def get_recent_sessions(self, limit: int = 10) -> List[SessionSummary]:
        """Get recent organization sessions"""
        if not self.db_connection:
            return []
        
        try:
            cursor = self.db_connection.execute("""
                SELECT * FROM sessions 
                ORDER BY start_time DESC 
                LIMIT ?
            """, (limit,))
            
            sessions = []
            for row in cursor.fetchall():
                session = SessionSummary(
                    session_id=row[0],
                    start_time=row[1],
                    end_time=row[2] or "",
                    profile_name=row[3] or "",
                    target_directory=row[4] or "",
                    total_files=row[5],
                    files_moved=row[6],
                    files_copied=row[7],
                    files_skipped=row[8],
                    errors=row[9],
                    categories={},  # Would need separate table for this
                    total_size_processed=row[10],
                    duration_seconds=row[11]
                )
                sessions.append(session)
            
            return sessions
            
        except Exception as e:
            print(f"Error getting recent sessions: {e}")
            return []
    
    def get_session_entries(self, session_id: str) -> List[LogEntry]:
        """Get all entries for a specific session"""
        if not self.db_connection:
            return []
        
        try:
            cursor = self.db_connection.execute("""
                SELECT * FROM log_entries 
                WHERE session_id = ? 
                ORDER BY timestamp
            """, (session_id,))
            
            entries = []
            for row in cursor.fetchall():
                entry = LogEntry(
                    timestamp=row[1],
                    session_id=row[2],
                    action=ActionType(row[3]),
                    source_path=row[4],
                    destination_path=row[5],
                    file_size=row[6],
                    file_type=row[7],
                    category=row[8],
                    error_message=row[9],
                    level=LogLevel(row[10])
                )
                entries.append(entry)
            
            return entries
            
        except Exception as e:
            print(f"Error getting session entries: {e}")
            return []
    
    def search_logs(self, query: str, days_back: int = 30) -> List[LogEntry]:
        """Search log entries"""
        if not self.db_connection:
            return []
        
        try:
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            cursor = self.db_connection.execute("""
                SELECT * FROM log_entries 
                WHERE (source_path LIKE ? OR destination_path LIKE ? OR category LIKE ?)
                AND timestamp > ?
                ORDER BY timestamp DESC
            """, (f"%{query}%", f"%{query}%", f"%{query}%", cutoff_date.isoformat()))
            
            entries = []
            for row in cursor.fetchall():
                entry = LogEntry(
                    timestamp=row[1],
                    session_id=row[2],
                    action=ActionType(row[3]),
                    source_path=row[4],
                    destination_path=row[5],
                    file_size=row[6],
                    file_type=row[7],
                    category=row[8],
                    error_message=row[9],
                    level=LogLevel(row[10])
                )
                entries.append(entry)
            
            return entries
            
        except Exception as e:
            print(f"Error searching logs: {e}")
            return []
    
    def get_statistics(self, days_back: int = 30) -> Dict[str, Any]:
        """Get comprehensive statistics"""
        if not self.db_connection:
            return {}
        
        try:
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            # Get basic stats
            cursor = self.db_connection.execute("""
                SELECT 
                    COUNT(*) as total_operations,
                    COUNT(CASE WHEN action = 'MOVED' THEN 1 END) as moved,
                    COUNT(CASE WHEN action = 'COPIED' THEN 1 END) as copied,
                    COUNT(CASE WHEN action = 'ERROR' THEN 1 END) as errors,
                    SUM(CASE WHEN file_size IS NOT NULL THEN file_size ELSE 0 END) as total_size
                FROM log_entries
                WHERE timestamp > ?
            """, (cutoff_date.isoformat(),))
            
            basic_stats = cursor.fetchone()
            
            # Get category stats
            cursor = self.db_connection.execute("""
                SELECT category, COUNT(*) as count
                FROM log_entries
                WHERE timestamp > ? AND category IS NOT NULL
                GROUP BY category
                ORDER BY count DESC
            """, (cutoff_date.isoformat(),))
            
            category_stats = dict(cursor.fetchall())
            
            # Get session stats
            cursor = self.db_connection.execute("""
                SELECT COUNT(*), AVG(duration_seconds), AVG(total_files)
                FROM sessions
                WHERE start_time > ?
            """, (cutoff_date.isoformat(),))
            
            session_stats = cursor.fetchone()
            
            return {
                'period_days': days_back,
                'total_operations': basic_stats[0],
                'files_moved': basic_stats[1],
                'files_copied': basic_stats[2],
                'errors': basic_stats[3],
                'total_size_processed': basic_stats[4],
                'categories': category_stats,
                'total_sessions': session_stats[0],
                'avg_session_duration': session_stats[1] or 0,
                'avg_files_per_session': session_stats[2] or 0
            }
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def export_to_csv(self, output_path: str, session_id: str = None) -> bool:
        """Export logs to CSV file"""
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow([
                    'timestamp', 'session_id', 'action', 'source_path', 'destination_path',
                    'file_size', 'file_type', 'category', 'error_message', 'level'
                ])
                
                # Get entries
                if session_id:
                    entries = self.get_session_entries(session_id)
                else:
                    entries = self.entries
                
                # Write data
                for entry in entries:
                    writer.writerow([
                        entry.timestamp, entry.session_id, entry.action.value,
                        entry.source_path, entry.destination_path or '',
                        entry.file_size or '', entry.file_type or '',
                        entry.category or '', entry.error_message or '',
                        entry.level.value
                    ])
            
            return True
            
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def cleanup_old_logs(self, days_to_keep: int = 90):
        """Clean up old log files and database entries"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # Clean up database
        if self.db_connection:
            try:
                self.db_connection.execute("""
                    DELETE FROM log_entries WHERE timestamp < ?
                """, (cutoff_date.isoformat(),))
                
                self.db_connection.execute("""
                    DELETE FROM sessions WHERE start_time < ?
                """, (cutoff_date.isoformat(),))
                
                self.db_connection.commit()
            except Exception as e:
                print(f"Error cleaning up database: {e}")
        
        # Clean up log files
        try:
            cutoff_timestamp = cutoff_date.strftime('%Y%m%d_%H%M%S')
            
            for log_file in self.log_dir.glob("session_*.log"):
                if log_file.stem.split('_', 1)[1] < cutoff_timestamp:
                    log_file.unlink()
            
            for log_file in self.log_dir.glob("session_*.json"):
                if log_file.stem.split('_', 1)[1] < cutoff_timestamp:
                    log_file.unlink()
            
            for log_file in self.log_dir.glob("session_*.csv"):
                if log_file.stem.split('_', 1)[1] < cutoff_timestamp:
                    log_file.unlink()
                    
        except Exception as e:
            print(f"Error cleaning up log files: {e}")
    
    def __del__(self):
        """Cleanup when logger is destroyed"""
        self._close_files()
        if self.db_connection:
            self.db_connection.close()