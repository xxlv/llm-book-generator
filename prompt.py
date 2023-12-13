from tool import load_file
from config import BuildConfig
class LLMBasePrompt:
    def __init__(self, title_prompt="", summary_prompt="", toc_prompt="", content_detail_prompt="") -> None:
        # Constructor to initialize the prompts
        # Gen title
        self.title_prompt = title_prompt
        # Gen Book summary
        self.summary_prompt = summary_prompt
        # Gen chapter summary
        self.toc_prompt = toc_prompt
        # Gen chapter content 
        self.content_detail_prompt = content_detail_prompt

    def load(self, lang="en",conf=None):
        self.title_prompt = load_file(f"./prompts/{lang}/title_{lang}.prompt")
        self.summary_prompt = load_file(f"./prompts/{lang}/summary_{lang}.prompt")
        self.toc_prompt = load_file(f"./prompts/{lang}/chapter_summary_toc_prompt_{lang}.prompt")
        self.content_detail_prompt = load_file(f"./prompts/{lang}/chapter_content_detail_prompt_{lang}.prompt")

        if conf is not None:
            self._update_attach_limit(conf)

        return self
    

    def _update_attach_limit(self,conf:BuildConfig):
        """ Gen limit """

        chapterp=load_file("./internal_prompt/limit_chapter.prompt")
        if conf.min_chapter and conf.max_chapter:
            chapterp=chapterp.format(min_chapter=conf.min_chapter,max_chapter=conf.max_chapter)
     
        if self.toc_prompt is not None:
            self.toc_prompt=chapterp+"\n"+self.toc_prompt
            
