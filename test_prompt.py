import unittest
from config import BuildConfig
from prompt import LLMBasePrompt

class LLMBasePromptTests(unittest.TestCase):

    def test_update_attach_limit_with_min_and_max_chapter(self):
        conf = BuildConfig(min_chapter=5, max_chapter=10)
        theprompt = LLMBasePrompt()
        theprompt._update_attach_limit(conf)

        # Assert that the prompt is updated correctly with both min_chapter and max_chapter values
        expected_prompt = "Generate an article with a minimum of 5 chapters and a maximum of 10 chapters."
        self.assertEqual(theprompt.toc_prompt.strip(), expected_prompt)

    def test_update_attach_limit_with_no_chapter_values(self):
        conf = BuildConfig()
        theprompt = LLMBasePrompt()
        theprompt._update_attach_limit(conf)

        # Assert that the prompt remains unchanged when no chapter values are provided
        expected_prompt = "Generate an article with a minimum of {min_chapter} chapters and a maximum of {max_chapter} chapters."
        self.assertEqual(theprompt.toc_prompt.strip(), expected_prompt)

if __name__ == '__main__':
    unittest.main()
