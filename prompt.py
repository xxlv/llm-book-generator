from tool import load_file

class LLMBasePrompt:
    def __init__(self, title_prompt=None, summary_prompt=None, toc_prompt=None, content_detail_prompt=None) -> None:
        # Constructor to initialize the prompts
        # Gen title
        self.title_prompt = title_prompt
        # Gen Book summary
        self.summary_prompt = summary_prompt
        # Gen chapter summary
        self.toc_prompt = toc_prompt
        # Gen chapter content 
        self.content_detail_prompt = content_detail_prompt

    def load(self, lang="en"):
        self.title_prompt = load_file(f"./prompts/{lang}/title_{lang}.prompt")
        self.summary_prompt = load_file(f"./prompts/{lang}/summary_{lang}.prompt")
        self.toc_prompt = load_file(f"./prompts/{lang}/chapter_summary_toc_prompt_{lang}.prompt")
        self.content_detail_prompt = load_file(f"./prompts/{lang}/chapter_content_detail_prompt_{lang}.prompt")
        return self
    

class LLMBookMetaPrompt(LLMBasePrompt):
    # Utilizes LLM for prompt generation, replacing built-in prompt templates.
    # TODO
    pass
