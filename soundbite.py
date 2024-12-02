import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Agent:
    def __init__(self, system_prompt):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not found")
        print(f"API Key found: {api_key[:8]}...")
        
        self.model = 'gpt-4-turbo-preview'  # Using GPT-4 Turbo with 128k token limit
        self.messages = [{"role": "system", "content": system_prompt}]
        try:
            self.client = OpenAI(
                api_key=api_key
            )
            print("OpenAI client initialized successfully")
        except Exception as e:
            print(f"Error initializing OpenAI client: {str(e)}")
            raise

    def get_response(self, temperature=0.3, top_p=0.5):  # Adjusted temperature for more creative responses
        try:
            print(f"Sending request to model {self.model} with {len(self.messages)} messages")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=temperature,
                top_p=top_p
            )
            print("Response received successfully")
            return response.choices[0].message.content
        except Exception as e:
            print(f"Detailed error in get_response: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response status: {e.response.status_code}")
                print(f"Response body: {e.response.text}")
            return None

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

def process_article_file(file_path):
    """Read and process the article file, extracting content between the markers."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        articles = []
        sections = content.split('=' * 80)
        
        for section in sections:
            if not section.strip():
                continue
            
            # Extract article details
            lines = section.strip().split('\n')
            article = {
                'date': '',
                'from': '',
                'subject': '',
                'content': ''
            }
            
            for line in lines:
                if line.startswith('Date:'):
                    article['date'] = line[5:].strip()
                elif line.startswith('From:'):
                    article['from'] = line[5:].strip()
                elif line.startswith('Subject:'):
                    article['subject'] = line[8:].strip()
                elif line.startswith('ARTICLE CONTENT:'):
                    # Get content after "ARTICLE CONTENT:" marker
                    content_start = lines.index(line) + 1
                    article_content = '\n'.join(lines[content_start:]).strip()
                    article['content'] = article_content
            
            if article['content']:  # Only add articles with content
                articles.append(article)
        
        return articles
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        return []

def main():
    system_prompt = (
        "You are an expert podcast scriptwriter specializing in summarizing email content. "
        "Your task is to create a comprehensive and engaging podcast script for a single narrator, following these guidelines:\n\n"
        "1. **Introduction:**\n"
        "   - Begin with an overview that contextualizes the listener to the variety of articles in the emails.\n"
        "   - Mention any common themes, trends, or notable topics present across the articles.\n\n"
        "2. **Contextual Summaries for Each Article:**\n"
        "   - Provide a concise yet comprehensive summary of each article.\n"
        "   - Highlight the main points, key arguments, and significant details.\n"
        "   - Offer context to help the listener understand the relevance and importance of each article.\n\n"
        "3. **Logical Organization:**\n"
        "   - Arrange the summaries in a logical order, grouping similar topics together if appropriate.\n"
        "   - Use clear and smooth transitions between articles to maintain a coherent flow.\n\n"
        "4. **Engaging Tone and Style:**\n"
        "   - Write in a conversational and relatable tone suitable for a podcast audience.\n"
        "   - Incorporate storytelling elements, rhetorical questions, or anecdotes where appropriate to enhance engagement.\n\n"
        "5. **Comprehensive Coverage:**\n"
        "   - Ensure all articles from the emails are included in the script.\n"
        "   - Avoid omitting any significant content or details.\n\n"
        "6. **Clarity and Conciseness:**\n"
        "   - Keep language clear and concise while being thorough.\n"
        "   - Eliminate unnecessary jargon or overly complex sentences.\n\n"
        "7. **Content Fidelity:**\n"
        "   - Do not introduce new information or personal opinions.\n"
        "   - Base the script solely on the content provided in the emails.\n\n"
        "8. **Formatting:**\n"
        "   - Provide the script in plain text without any special formatting, bullet points, or headings."
    )

    # Initialize agent
    script_agent = Agent(system_prompt)
    
    # Get the article file path
    if len(sys.argv) > 1:
        article_file = sys.argv[1]
    else:
        print("Please provide the path to the article file as a command line argument.")
        return

    # Process articles
    articles = process_article_file(article_file)
    
    if not articles:
        print("No articles found in the file.")
        return

    # Create a comprehensive prompt with all articles
    full_content = "Here are the articles to summarize:\n\n"
    for i, article in enumerate(articles, 1):
        full_content += f"ARTICLE {i}:\n"
        full_content += f"Title: {article['subject']}\n"
        full_content += f"Author: {article['from']}\n"
        full_content += f"Content:\n{article['content']}\n\n"

    # Get script from agent
    script_agent.add_message("user", full_content)
    script = script_agent.get_response()
    
    if script:
        # Save script to file
        timestamp = articles[0]['date'].replace(':', '').replace(' ', '_').replace(',', '')
        output_file = f"podcast_script_{timestamp}.txt"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("PODCAST SCRIPT\n")
                f.write("=" * 40 + "\n\n")
                f.write(script)
            print(f"Script saved to: {output_file}")
        except Exception as e:
            print(f"Error saving script: {str(e)}")
    else:
        print("Error: Could not generate script")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {str(e)}")