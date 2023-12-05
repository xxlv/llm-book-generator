from book import Book,Chapter
import subprocess
import os
import toml 
from tool import write_file,load_file
from log import setup_logger
logger=setup_logger()

class MdBook:
    def __init__(self, book: Book, location: str = ".") -> None:
        """
        Initializes MdBook object.

        Parameters:
        - book (Book): The Book object containing information about the book.
        - location (str): The location where the mdbook project will be created. Default is the current directory.
        """
        self.book = book
        self.location = location

    def check_mdbook_installation(self):
        """
        Checks if mdbook is installed.

        Returns:
        - bool: True if mdbook is installed, False otherwise.
        """
        try:
            subprocess.run(["mdbook", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except Exception:
            return False

    def init_project(self):
        """
        Initializes the mdbook project.

        Returns:
        - bool: True if the project initialization is successful, False otherwise.
        """
        if not self.check_mdbook_installation():
            logger.info("Please install the mdbook tool first.")
            return False
        try:
            logger.info("Preparing to create the project {}".format(self.book.title))
            subprocess.run(["mdbook", "init", "--title", self.book.title], check=True, cwd=self.location)
            return True
        except subprocess.CalledProcessError as e:
            logger.info("An error occurred during project initialization.\n{}".format(e))
            return False


    def create(self):
        """
        Initializes the SUMMARY.md file for the mdbook project.

        Creates the SUMMARY.md file based on the chapters in the book.

        Returns:
        - None
        """
        # Summary
        summary_content = "# Summary\n"
        for c in self.book.chapters:
            chapter_filename = os.path.join("chapters", "{}.md".format(c.nu))
            summary_content += "- [{}]({}) \n".format(c.title, chapter_filename)
            c.update_location(os.path.join(self.location, "src", chapter_filename))
            write_file(c.location, c.content)

        summary_file = os.path.join(self.location, "src", "SUMMARY.md")
        write_file(summary_file, summary_content)

        # Update book metadata 
        conf_file = os.path.join(self.location, "book.toml")
        with open(conf_file, 'r') as file:
            data = toml.load(file)
        data['book']['authors'] = self.book.authors


    def build(self):
        """
        Builds the mdbook project.

        Initializes the project, creates the SUMMARY.md file, and builds the mdbook project.

        Returns:
        - None
        """
        if not os.path.exists(self.location):
            os.makedirs(self.location)
        self.init_project()
        self.create()

        logger.info("Building mdbook {}".format(self.book))


if __name__=="__main__":

    MdBook(book=Book(title="test"),location="./temp").build()

