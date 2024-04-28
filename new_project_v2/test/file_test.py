import unittest
from unittest.mock import patch, MagicMock  # For mocking file operations

import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from file import File


class FileTest(unittest.TestCase):

  def setUp(self):
    self.file_name = "test_file"

  @patch('file.open')  # Mock open function for controlled behavior
  def test_init_new_file(self, mock_open):
    """Tests that the constructor creates a new file and sets content to empty list."""
    mock_open.return_value = MagicMock()  # Simulate successful file creation

    file = File(self.file_name)

    self.assertEqual(file._name, self.file_name + ".txt")
    self.assertIsNone(file._file)  # File handle should be closed
    self.assertEqual(file._content, [])
    mock_open.assert_called_once_with(self.file_name + ".txt", 'x')  # Verify mode

  @patch('file.open')  # Mock open function
  def test_init_existing_file(self, mock_open):
    """Tests that the constructor handles existing files and calls get_content_from_file."""
    mock_open.side_effect = FileExistsError  # Raise FileExistsError on first call

    file = File(self.file_name)

    self.assertEqual(file._name, self.file_name + ".txt")
    self.assertIsNone(file._file)  # File handle should be closed
    self.assertEqual(file._content, [])
    mock_open.assert_has_calls([patch.call(self.file_name + ".txt", 'x'), patch.call(self.file_name, 'r')])

  @patch('file.open')  # Mock open function
  def test_get_content_from_file(self, mock_open):
    """Tests that get_content_from_file successfully reads file content."""
    mock_file = MagicMock()
    mock_file.__iter__.return_value = iter(["line1\n", "line2\n"])  # Mock file content
    mock_open.return_value = mock_file

    file = File(self.file_name)

    self.assertEqual(file._content, ["line1", "line2"])
    mock_open.assert_called_once_with(self.file_name, 'r')

  @patch('file.open')  # Mock open function
  def test_get_content_from_file_empty(self, mock_open):
    """Tests that get_content_from_file handles empty files."""
    mock_file = MagicMock()
    mock_file.__iter__.return_value = iter([])  # Mock empty file
    mock_open.return_
