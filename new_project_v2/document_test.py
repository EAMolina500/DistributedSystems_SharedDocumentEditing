import unittest
from unittest.mock import patch, MagicMock  # For mocking file operations

from operation import Operation
import file


class DocumentTest(unittest.TestCase):

  def setUp(self):
    self.server_id = 1

  @patch('file.File')  # Mock File class for controlled behavior
  def test_init_empty_file(self, mock_file):
    """Tests that the constructor creates a Document object and reads
    content from an empty file."""
    mock_file_instance = MagicMock()
    mock_file_instance.is_empty.return_value = True
    mock_file.return_value = mock_file_instance

    document = Document(self.server_id)

    self.assertEqual(document._server_id, self.server_id)
    self.assertEqual(document._file_name, f"server_{self.server_id}_file")
    self.assertEqual(document._operations, [])
    mock_file.assert_called_once_with(f"server_{self.server_id}_file")

  @patch('file.File')  # Mock File class
  def test_init_existing_file(self, mock_file):
    """Tests that the constructor creates a Document object, reads
    content from a non-empty file, and populates operations."""
    mock_file_instance = MagicMock()
    mock_file_instance.is_empty.return_value = False
    mock_file_instance.get_content.return_value = [
      "insert/1/x/[1, 0, 2]/replica1\n", "delete/2/None/[2, 1, 0]/replica2\n"]
    mock_file.return_value = mock_file_instance

    document = Document(self.server_id)

    self.assertEqual(document._server_id, self.server_id)
    self.assertEqual(document._file_name, f"server_{self.server_id}_file")
    self.assertEqual(len(document._operations), 2)
    # Assuming Operation object parsing works correctly (not tested here)
    self.assertIsInstance(document._operations[0], Operation)
    mock_file.assert_called_once_with(f"server_{self.server_id}_file")

  @patch('file.File')  # Mock File class
  def test_get_operations(self, mock_file):
    """Tests that get_operations returns the current list of operations."""
    document = Document(self.server_id)
    document._operations = ["operation1", "operation2"]

    self.assertEqual(document.get_operations(), document._operations)

  @patch('file.File')  # Mock File class
  def test_set_operations(self, mock_file):
    """Tests that set_operations updates the internal operations list."""
    document = Document(self.server_id)
    new_operations = ["updated_op1", "updated_op2"]

    document.set_operations(new_operations)

    self.assertEqual(document._operations, new_operations)

  @patch('file.File')  # Mock File class
  def test_insert_valid(self, mock_file):
    """Tests that insert adds a new operation to the internal list
    and calls the file's insert_operation method."""
    mock_file_instance = MagicMock()
    mock_file.return_value = mock_file_instance

    document = Document(self.server_id)
    index = 3
    char = "y"
    vector_clock = [0, 3, 1]
    replica_id = "replica3"

    document.insert(index, char, vector_clock, replica_id)

    expected_operation = Operation("insert", index, char, vector_clock, replica_id)
    self.assertEqual(document._operations[-1], expected_operation)
    mock_file_instance.insert_operation.assert_called_once_with(expected_operation)

  @patch('file.File')  # Mock File class
  def test_delete_valid(self, mock_file):
    """Tests that delete adds a new delete operation to the internal list
    and calls the file's insert_operation method."""
    mock_file_instance = MagicMock()
