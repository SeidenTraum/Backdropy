# Writing unit tests for backdropy.py
import backdropy
import unittest

class TestBackdrop(unittest.TestCase):
    #* Testing the config_set_default function
    # The function's written output should match default_config.test
    def test_config_set_default(self):
        backdropy.config_set_default()
        output:str = ""
        exp_output:str = ""
        with open(backdropy.config_path, "r") as file:
            output = file.read()
        with open("Testfiles/default_config.test", "r") as file:
            exp_output = file.read()
        self.assertEqual(output, exp_output)

if __name__ == '__main__':
    unittest.main()
