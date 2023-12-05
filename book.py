class Chapter:
    """
    chapter 
    """
    def __init__(self,nu:int,title:str,summary:str,content:str='') -> None:
        self.title=title
        self.summary=summary
        self.content=content 
        self.nu=nu 
        self.location=None 

    def __str__(self) -> str:
        return "Chapter#{}({})({})".format(self.nu,self.title,self.summary)
    
    def update_location(self,location):
        self.location=location

class Book:
    """
    Book core model
    """
    def __init__(self,title,summary="",author="GPT") -> None:
        self.curr_no=0
        self.summary=summary
        self.title=title
        self.authors=[author]
        self.chapters=[]
    
    def add_chapter(self,chapter:Chapter):
        self.curr_no=(self.curr_no)
        self.curr_no+=1

        chapter.nu=self.curr_no
        if not self.chapters:
            self.chapters=[]
        self.chapters.append(chapter)


    def __str__(self) -> str:
        book_str = f"Title: {self.title}\nAuthor: {self.author}\nSummary: {self.summary}\n"
        
        if self.chapters:
            chapters_str = "\n".join([str(chapter) for chapter in self.chapters])
            book_str += f"Chapters:\n{chapters_str}"

        return book_str
