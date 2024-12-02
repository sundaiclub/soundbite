from __future__ import print_function
import os.path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import base64
import email
from email.header import decode_header
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import socket
from bs4 import BeautifulSoup
import html2text
from datetime import datetime
import re
import time
from googleapiclient.errors import HttpError

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def find_free_port():
    """Find a free port to use for the local server."""
    ports_to_try = [8080, 8090, 8000, 8888, 3000]
    for port in ports_to_try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return port
            except OSError:
                continue
    return 0  # If no specific ports are free, let the OS choose one

def extract_urls_with_text(html_content):
    """Extract URLs and their corresponding text from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    
    # Find all <a> tags
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if 'substack.com/redirect' in href:
            # Get the visible text of the link
            text = a.get_text(strip=True)
            if not text:  # If no text, use the URL as text
                text = href
            # Clean the URL by removing tracking parameters
            clean_url = href.split('?')[0]
            links.append((text, clean_url))
    
    return links

def clean_content(content):
    """Remove boilerplate content from the article."""
    # First, find the main content after "READ IN APP"
    content_parts = content.split("READ IN APP")
    if len(content_parts) > 1:
        content = content_parts[1].strip()
    
    # Remove Restack sections
    content = re.sub(r'\[\[\[Restack.*?\]\]\]', '', content, flags=re.DOTALL)
    
    # Common boilerplate phrases to remove along with surrounding content
    boilerplate_patterns = [
        r"(?i)Like this post\?.*?(\n|$)",
        r"(?i)Subscribe to.*?(\n|$)",
        r"(?i)Thank you for reading.*?(\n|$)",
        r"(?i)Thanks for reading.*?(\n|$)",
        r"(?i)Share this post.*?(\n|$)",
        r"(?i)Did someone forward this to you\?.*?(\n|$)",
        r"(?i)You're receiving this email because.*?(\n|$)",
        r"(?i)Unsubscribe.*?(\n|$)",
        r"(?i) \d{4}.*?All rights reserved.*?(\n|$)",
        r"(?i)Sent to.*?(\n|$)",
        r"(?i)View in browser.*?(\n|$)",
        r"(?i)Get the app.*?(\n|$)",
        r"(?i)Share.*?(\n|$)",
        r"(?i)Comment.*?(\n|$)",
        r"(?i)Like.*?(\n|$)",
        r"(?i)Forwarded this email\?.*?(\n|$)",
        r"(?i)This post is free to read.*?(\n|$)",
        r"(?i)You're currently a free subscriber.*?(\n|$)",
        r"(?i)Upgrade to paid.*?(\n|$)",
        r"͏ ­͏.*?(\n|$)",  # Remove those invisible characters
        r"^\s*\*\*\*\s*$"  # Remove separator lines
    ]
    
    cleaned = content
    for pattern in boilerplate_patterns:
        # Don't remove lines that contain URLs
        if not re.search(r'https?://[^\s<>"]+|www\.[^\s<>"]+', pattern):
            cleaned = re.sub(pattern, '', cleaned, flags=re.MULTILINE | re.DOTALL)
    
    # Remove multiple consecutive newlines
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    # Remove trailing whitespace
    cleaned = cleaned.strip()
    
    return cleaned

def get_email_body(payload):
    """Extract and process the email body content."""
    if payload.get('parts'):
        for part in payload['parts']:
            if part['mimeType'] == 'text/html':
                try:
                    data = part['body']['data']
                    decoded_bytes = base64.urlsafe_b64decode(data)
                    decoded_str = decoded_bytes.decode('utf-8')
                    
                    # Parse HTML with BeautifulSoup
                    soup = BeautifulSoup(decoded_str, 'html.parser')
                    
                    # Remove script, style, and footer elements
                    for element in soup(['script', 'style', 'footer']):
                        element.decompose()
                    
                    # Remove elements with specific classes or IDs
                    selectors_to_remove = [
                        '.footer',
                        '.post-footer',
                        '.subscription-widget-wrap',
                        '.button-wrapper',
                        '.social-links',
                        '.footer-links',
                        '#footer',
                        '.email-footer',
                        '.post-footer',
                        '.subscription-footer'
                    ]
                    
                    for selector in selectors_to_remove:
                        for element in soup.select(selector):
                            element.decompose()
                    
                    # Convert to plain text while preserving links
                    h = html2text.HTML2Text()
                    h.ignore_images = True
                    h.ignore_tables = True
                    h.body_width = 0  # Don't wrap text
                    h.ignore_links = False  # Keep links
                    h.inline_links = True  # Show links inline
                    
                    text = h.handle(str(soup))
                    
                    # Clean the content
                    cleaned_text = clean_content(text)
                    
                    return cleaned_text
                    
                except Exception as e:
                    print(f"Error processing email body: {str(e)}")
                    continue
    
    return ""

def save_articles_to_file(messages, output_file):
    """Save the processed articles to a file in the specified format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, msg in enumerate(messages, 1):
            # Write article header
            f.write(f"Article {i}\n")
            f.write("=" * 59 + "\n")
            
            # Write metadata
            f.write(f"Date: {msg.get('date', '')}\n")
            f.write(f"From: {msg.get('from', '')}\n")
            f.write(f"Subject: {msg.get('subject', '')}\n")
            
            # Write content separator
            f.write("-" * 40 + "\n")
            f.write("ARTICLE CONTENT:\n")
            f.write("-" * 40 + "\n")
            
            # Write content and add spacing between articles
            f.write(f"{msg.get('content', '')}\n\n")

def main():
    """Main function to process Gmail messages."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            port = find_free_port()
            if port == 0:
                raise RuntimeError("Could not find an available port")
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'Client Secret Soundbites.json', SCOPES, port=port)
            creds = flow.run_local_server(port=port)
        
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        
        # Modified query to exclude no-reply emails
        query = "from:*@substack.com -from:no-reply@substack.com"
        results = service.users().messages().list(userId='me', q=query, maxResults=10).execute()
        messages = results.get('messages', [])

        if not messages:
            print('No Substack messages found.')
            return
        
        processed_messages = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
            
            headers = msg['payload']['headers']
            email_data = {
                'date': '',
                'from': '',
                'subject': '',
                'content': ''
            }
            
            for header in headers:
                name = header['name'].lower()
                if name in ['date', 'from', 'subject']:
                    email_data[name] = header['value']
            
            # Skip if it's from no-reply (additional check)
            if 'no-reply@substack.com' in email_data.get('from', '').lower():
                continue
                
            # Get and clean email content
            content = get_email_body(msg['payload'])
            if content and len(content.strip()) > 0:
                email_data['content'] = content
                processed_messages.append(email_data)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'substack_articles_{timestamp}.txt'
        
        save_articles_to_file(processed_messages, output_file)
        print(f'Processed {len(processed_messages)} articles and saved to {output_file}')

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    main()


