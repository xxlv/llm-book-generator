# LLM Book Generator

This script generates a book using OpenAI's GPT-3.5-turbo language model and Markdown.

## Prerequisites

Before running the script, make sure you have the required dependencies installed:

```bash
pip install python-dotenv openai
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/xxlv/llm-book-generator.git
cd llm-book-generator
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables:

Create a `.env` file and add your OpenAI API key:

`OPENAI_API_KEY=your-api-key`

4. Run the script:

```bash
python buildbook.py --input "Your book content goes here." --location "/path/to/save/generated/book"
```

Replace `"Your book content goes here."` with the text you want to use for the book, and specify the location where you want to save the generated book.

## Configuration

You can customize the prompts used for generating the book by modifying the prompt files in the `prompts` directory.

- `title.prompt`: Prompt for generating the book title.
- `summary.prompt`: Prompt for generating the book summary.
- `chapter_summary_toc_prompt.prompt`: Prompt for generating chapter summaries and table of contents.
- `chapter_content_detail_prompt.prompt`: Prompt for generating detailed chapter content.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://openai.com) for providing the GPT-3.5-turbo model.
- [dotenv](https://pypi.org/project/python-dotenv/) for managing environment variables.

Feel free to contribute, report issues, or provide feedback!

