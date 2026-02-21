#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unit tests for history management.
"""

import pytest
from datetime import datetime
from calculator.history import HistoryEntry, HistoryManager


class TestHistoryEntry:
    """Test suite for HistoryEntry class."""

    def test_create_entry(self):
        """Test creating a history entry."""
        entry = HistoryEntry("2 + 3", 5)
        assert entry.expression == "2 + 3"
        assert entry.result == 5
        assert isinstance(entry.timestamp, datetime)

    def test_create_entry_with_timestamp(self):
        """Test creating entry with custom timestamp."""
        ts = datetime(2026, 2, 22, 10, 30, 0)
        entry = HistoryEntry("10 * 5", 50, ts)
        assert entry.timestamp == ts

    def test_entry_string_representation(self):
        """Test string representation of entry."""
        ts = datetime(2026, 2, 22, 10, 30, 0)
        entry = HistoryEntry("2 + 3", 5, ts)
        str_repr = str(entry)
        assert "2026-02-22 10:30:00" in str_repr
        assert "2 + 3 = 5" in str_repr

    def test_entry_repr(self):
        """Test repr of entry."""
        entry = HistoryEntry("2 + 3", 5)
        repr_str = repr(entry)
        assert "HistoryEntry" in repr_str
        assert "2 + 3" in repr_str


class TestHistoryManager:
    """Test suite for HistoryManager class."""

    def test_create_manager(self):
        """Test creating a history manager."""
        manager = HistoryManager()
        assert manager.max_entries == 100
        assert len(manager) == 0
        assert manager.is_empty()

    def test_create_manager_with_custom_max(self):
        """Test creating manager with custom max entries."""
        manager = HistoryManager(max_entries=50)
        assert manager.max_entries == 50

    def test_add_entry(self):
        """Test adding an entry to history."""
        manager = HistoryManager()
        manager.add("2 + 3", 5)
        assert len(manager) == 1
        assert not manager.is_empty()

    def test_add_multiple_entries(self):
        """Test adding multiple entries."""
        manager = HistoryManager()
        manager.add("2 + 3", 5)
        manager.add("10 * 5", 50)
        manager.add("100 / 4", 25)
        assert len(manager) == 3

    def test_get_all_entries(self):
        """Test retrieving all entries."""
        manager = HistoryManager()
        manager.add("2 + 3", 5)
        manager.add("10 * 5", 50)

        entries = manager.get_all()
        assert len(entries) == 2
        assert entries[0].expression == "2 + 3"
        assert entries[0].result == 5
        assert entries[1].expression == "10 * 5"
        assert entries[1].result == 50

    def test_get_all_returns_copy(self):
        """Test that get_all returns a copy, not the original list."""
        manager = HistoryManager()
        manager.add("2 + 3", 5)

        entries1 = manager.get_all()
        entries2 = manager.get_all()

        assert entries1 is not entries2
        assert entries1 == entries2

    def test_clear_history(self):
        """Test clearing history."""
        manager = HistoryManager()
        manager.add("2 + 3", 5)
        manager.add("10 * 5", 50)
        assert len(manager) == 2

        manager.clear()
        assert len(manager) == 0
        assert manager.is_empty()

    def test_max_entries_limit(self):
        """Test that history respects max entries limit."""
        manager = HistoryManager(max_entries=3)

        manager.add("1 + 1", 2)
        manager.add("2 + 2", 4)
        manager.add("3 + 3", 6)
        assert len(manager) == 3

        # Adding 4th entry should remove the oldest
        manager.add("4 + 4", 8)
        assert len(manager) == 3

        entries = manager.get_all()
        # First entry should be removed
        assert entries[0].expression == "2 + 2"
        assert entries[1].expression == "3 + 3"
        assert entries[2].expression == "4 + 4"

    def test_max_entries_removes_oldest(self):
        """Test that exceeding max removes oldest entries."""
        manager = HistoryManager(max_entries=2)

        manager.add("1 + 1", 2)
        manager.add("2 + 2", 4)
        manager.add("3 + 3", 6)
        manager.add("4 + 4", 8)

        entries = manager.get_all()
        assert len(entries) == 2
        assert entries[0].expression == "3 + 3"
        assert entries[1].expression == "4 + 4"

    def test_empty_check(self):
        """Test is_empty method."""
        manager = HistoryManager()
        assert manager.is_empty()

        manager.add("2 + 3", 5)
        assert not manager.is_empty()

        manager.clear()
        assert manager.is_empty()

    def test_len_method(self):
        """Test __len__ method."""
        manager = HistoryManager()
        assert len(manager) == 0

        for i in range(5):
            manager.add(f"{i} + {i}", i * 2)
            assert len(manager) == i + 1
