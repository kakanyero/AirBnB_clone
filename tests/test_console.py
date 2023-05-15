#!/usr/bin/python3
"""Module for testing the HBNBCommand Class"""
import unittest
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO
from models.engine.file_storage import FileStorage
from unittest.mock import patch
import sys


class Test_Console(unittest.TestCase):
    def setUp(self):
        """Set up the mock stdin and stdout"""
        self.mock_stdin = StringIO()
        self.mock_stdout = StringIO()
        sys.stdout = self.mock_stdout

    def tearDown(self):
        """Restore the ooriginal stdin and stdout"""
        sys.stdout = sys.__stdout__

    """Test the HBNBCommand Console"""

#     def test_help(self):
#         """Tests the help commmand"""
#         with patch('sys.stdout', new=StringIO()) as f:
#             HBNBCommand().onecmd("help")
#         string = """
# Documented commands (type help <topic>):
# ========================================
# EOF  all  count  create  destroy  help  quit  show  update
# """
#         msg = f.getvalue()
#         self.assertEqual(string, msg)

    def test_help(self):
        """Tests the help command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        s = """
Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

"""
        self.assertEqual(s, f.getvalue())

    # Test cases for quit

    def test_do_quit(self):
        """Tests the quit commmand"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
        # modelling what happens when someone types `quit`
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit garbage")
        # modelling when user types `quit anything`
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)

    # Test cases for EOF
    def test_do_EOF(self):
        """Tests the EOF commmand"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
        # modelling what happens when user types `quit`
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF garbage")
        # modelling when user types `EOF anything`
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)

    # Test cases for emptyline
    def test_do_emptyline(self):
        """Tests the emptyline command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
        # modelling what happens when user doesn't type anything
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("                     \n")
        # modelling when user types lots of whitespaces & enter
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)

    # Test cases for do_all
    def test_do_all(self):
        """Tests the do_all command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")


if __name__ == "__main__":
    unittest.main()
