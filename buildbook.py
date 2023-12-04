import argparse
from dotenv import load_dotenv
from book import Book,Chapter
from mdbook import MdBook
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.chains import SequentialChain
from langchain.prompts import PromptTemplate

from tool import load_file
import log 

load_dotenv()

# Define LLM chain
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo",timeout=120)

logger = log.setup_logger()


class LLMBookPrompt:

    def __init__(self,title_prompt=None,summary_propmt=None,chapter_summary_toc_prompt=None,chapter_content_detail_prompt=None) -> None:
        # Constructor to initialize the prompts
        
        # Gen title
        self.title_prompt=title_prompt
        # Gen Book summary
        self.summary_propmt=summary_propmt
        # Gen chapter summary
        self.chapter_summary_toc_prompt=chapter_summary_toc_prompt
        # Gen chapter content 
        self.chapter_content_detail_prompt=chapter_content_detail_prompt

    def load_default(self):
        self.title_prompt=load_file("./prompts/title.prompt")
        self.summary_propmt=load_file("./prompts/summary.prompt")
        self.chapter_summary_toc_prompt=load_file("./prompts/chapter_summary_toc_prompt.prompt")
        self.chapter_content_detail_prompt=load_file("./prompts/chapter_content_detail_prompt.prompt")

        return self 


class LLMBookGen:

    def __init__(self,prompt:LLMBookPrompt,llm) -> None:
        """LLMBookGen 根据Prompt生成Book"""
        self.book_prompt=prompt
        self.llm=llm 
    
    
    def gen_book(self,input:str,verbose=True):
        
        title_prompt_tpl=self.book_prompt.title_prompt
        title_prompt=PromptTemplate(template=title_prompt_tpl,input_variables=["input"])
        title_chain=LLMChain(llm=llm,prompt=title_prompt,output_key="title",verbose=verbose)

        summary_prompt_tpl=self.book_prompt.summary_propmt
        summary_prompt=PromptTemplate(template=summary_prompt_tpl,input_variables=["title"])
        summary_chain=LLMChain(llm=llm,prompt=summary_prompt,output_key="summary",verbose=verbose)

        chapter_prompt_tpl=self.book_prompt.chapter_summary_toc_prompt
        chapter_prompt=PromptTemplate(template=chapter_prompt_tpl,input_variables=["summary"])
        chapter_chain=LLMChain(llm=llm,prompt=chapter_prompt,output_key="chapters",verbose=verbose)

        # core chain 
        core_chain=SequentialChain(chains=[title_chain,summary_chain,chapter_chain],input_variables=["input"], output_variables=["title","summary","chapters"])
        result=core_chain({"input":input})

        return self.as_book(result) 
    

    def as_book(self,result,author="GPT") ->Book:
        
        chapters=result['chapters']
        chapterslines=chapters.split("\n")
        title=result['title']
        summary=result['summary']

        book=Book(title=title,summary=summary,author=author)
        
        for c in chapterslines:
            seqc=c.split("::::")
            if len(seqc)>=3:
                nu=int(seqc[0])
                title=seqc[1]
                summary=seqc[2]
                # content 需要下一次gpt
                the_chapter=Chapter(nu=nu,title=title,summary=summary)
                book.add_chapter(self.gen_chapter(the_chapter,book.title,book.summary))

        return book

    def gen_chapter(self,chapter:Chapter,book_title:str,book_summary:str):
        promot_tpl=self.book_prompt.chapter_content_detail_prompt
        prompt=PromptTemplate(template=promot_tpl,input_variables=["title","summary","subtitle","subsummary"])

        title_chain=LLMChain(llm=llm,prompt=prompt,output_key="content",verbose=True)
        result=title_chain({"title":book_title,"summary":book_summary,"subtitle":chapter.title,"subsummary":chapter.summary})
        if "content" in result:
            chapter.content=self._parse_content(result["content"])
        else:
            chapter.content="**** FAIL GEN {} **** ".format(chapter)

        return chapter

    def _parse_content(self,content:str):

        prefix="Result:"
        if content.startswith(prefix):
            return content[len(prefix):]
        return content 

def main():
    parser = argparse.ArgumentParser(description="Generate and build a book using LLM and Markdown.")
    parser.add_argument("--input", type=str, help="The input text for the book.")
    parser.add_argument("--location", type=str, help="The location to save the generated book.")

    args = parser.parse_args()

    if not args.input or not args.location:
        print("Both --input and --location are required.")
        return
    
    llm_book_gen = LLMBookGen(llm=llm, prompt=LLMBookPrompt().load_default())
    book = llm_book_gen.gen_book(args.input)
    MdBook(book, args.location).build()

if __name__=="__main__":
    main()