from book import Book,Chapter
import subprocess
import os
from tool import write_file,load_file
from log import setup_logger

logger=setup_logger()

class MdBook:
    def __init__(self,book:Book,location:str=".") -> None:
        self.book=book  
        self.location=location

    def check_mdbook_installation(self):
        try:
            subprocess.run(["mdbook", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except Exception:
            return False

    def init_project(self):
        if not self.check_mdbook_installation():
            logger.info("请先安装 mdbook 工具。")
            return False
        try:
            logger.info("准备创建项目 {}".format(self.book.title))
            subprocess.run(["mdbook", "init", "--title", self.book.title], check=True, cwd=self.location)
            return True
        except subprocess.CalledProcessError as e:
            logger.info("初始化项目时发生错误。\n{}".format(e))
            return False
        
    def init_summary(self):
        # Summary
        summary_content="# Summary\n"
        for c in self.book.chapters:
            chapter_filename=os.path.join("chapters","{}.md".format(c.nu))
            summary_content+="- [{}]({}) \n".format(c.title,chapter_filename)
            c.update_location(os.path.join(self.location,"src",chapter_filename))
            write_file(c.location,c.content)

        summary_file=os.path.join(self.location,"src","SUMMARY.md")
        logger.info(summary_file)
        write_file(summary_file,summary_content)


    def build(self):
        if not os.path.exists(self.location):
            os.makedirs(self.location)
        self.init_project()
        self.init_summary()
        logger.info("构建mdbook {}".format(self.book))


if __name__=="__main__":

    MdBook(book=Book(title="test"),location="./temp").build()

