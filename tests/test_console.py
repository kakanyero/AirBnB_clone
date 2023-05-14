#!/usr/bin/python3
"""Module for testing the HBNBCommand Class"""
import unittest
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO
from models.engine.file_storage import FileStorage
import datetime
from unittest.mock import patch
import sys
import re
import os


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
        with patch("sys.stdout", new=StringIO()) as f:
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

    # Test cases for do_create
    def test_do_create(self):
        """Test create command"""
        for classname in self.classes():
            self.help_test_do_create(classname)

    def help_test_do_create(self, classname):
        """Helper method to test the create command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        key = "{}.{}".format(classname, uid)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all {}".format(classname))
        self.assertTrue(uid in f.getvalue())

    def test_do_create_error(self):
        """Tests the create command with errors"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    # Test cases for do_show
    def test_do_show(self):
        """Tests show command"""
        for classname in self.classes():
            self.help_test_do_show(classname)
            self.help_test_do_show_advanced(classname)

    def help_test_do_show(self, classname):
        """Helper method to test the show command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show {} {}".format(classname, uid))
        s = f.getvalue()[:-1]
        self.assertTrue(uid in s)

    def test_do_show_error(self):
        """Tests the show command with errors"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 6524359")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def help_test_show_advanced(self, classname):
        """Helps to test the .show() command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertTrue(uid in s)

    def test_do_show_error_advanced(self):
        """Tests show() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".show()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.show()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.show("6524359")')
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    # Test cases for do_destroy
    def test_do_destroy(self):
        """Tests destroy command"""
        for classname in self.classes():
            self.help_test_do_destroy(classname)
            self.help_test_do_destroy_advanced(classname)

    def help_test_do_destroy(self, classname):
        """Helps test the destrot command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy {} {}".format(classname, uid))
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) == 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".all()")
        self.assertFalse(uid in f.getvalue())

    def test_do_destroy_error(self):
        """Tests the destroy command with errors"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel 6524359")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def help_test_show_advanced(self, classname):
        """Helps to test the destroy command"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.destroy("{}")'.format(classname, uid))
        s = f.getvalue()
        self.assertTrue(len(s) == 0)

    def test_do_destroy_error_advanced(self):
        """Tests destroy() command with errors."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".destroy()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.destroy()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.destroy("6524359")')
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")


if __name__ == "__main__":
    unittest.main()
