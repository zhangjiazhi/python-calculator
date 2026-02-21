#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
History management for calculator operations.
Stores and manages calculation history with timestamps.
"""

from datetime import datetime
from typing import List, Optional


class HistoryEntry:
    """Represents a single calculation history entry."""

    def __init__(self, expression: str, result: float, timestamp: Optional[datetime] = None):
        """
        Initialize a history entry.

        Args:
            expression: The mathematical expression
            result: The calculated result
            timestamp: When the calculation was performed (defaults to now)
        """
        self.expression = expression
        self.result = result
        self.timestamp = timestamp or datetime.now()

    def __str__(self):
        """String representation of the history entry."""
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{time_str}] {self.expression} = {self.result}"

    def __repr__(self):
        return f"HistoryEntry('{self.expression}', {self.result}, {self.timestamp})"


class HistoryManager:
    """Manages calculation history with size limits."""

    def __init__(self, max_entries: int = 100):
        """
        Initialize the history manager.

        Args:
            max_entries: Maximum number of entries to keep (default 100)
        """
        self.max_entries = max_entries
        self._history: List[HistoryEntry] = []

    def add(self, expression: str, result: float) -> None:
        """
        Add a new calculation to history.

        Args:
            expression: The mathematical expression
            result: The calculated result
        """
        entry = HistoryEntry(expression, result)
        self._history.append(entry)

        # Maintain size limit
        if len(self._history) > self.max_entries:
            self._history.pop(0)  # Remove oldest entry

    def get_all(self) -> List[HistoryEntry]:
        """
        Get all history entries.

        Returns:
            List of HistoryEntry objects, oldest first
        """
        return self._history.copy()

    def clear(self) -> None:
        """Clear all history entries."""
        self._history.clear()

    def __len__(self):
        """Return the number of history entries."""
        return len(self._history)

    def is_empty(self) -> bool:
        """Check if history is empty."""
        return len(self._history) == 0
