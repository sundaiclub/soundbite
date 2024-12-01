import requests
import json
import os

def shorten_text(text, api_key, api_url="https://api.sambanova.ai/v1/chat/completions", attempt=1):
    """
    Intelligently shorten input text using SambaNova API with multiple retry strategies.
    
    Args:
        text (str): Input text to be shortened
        api_key (str): SambaNova API authorization key
        api_url (str, optional): API endpoint URL
        attempt (int, optional): Current attempt number
    
    Returns:
        dict: Contains shortened text and its length
    """
    # Prepare system prompts for different attempts
    system_prompts = [
        "You are an expert text summarizer. Condense the following text while preserving its core meaning, key arguments, and most important details. Maintain the original tone and style. Ensure the summary is coherent and readable.",
        "You are an expert text condenser. Significantly reduce the text length while keeping only the most crucial information. Focus on the absolute core message.",
        "You are an extreme text minimalist. Compress the text to its absolute bare minimum, preserving only the most essential ideas and key phrases."
    ]
    
    # Prepare request payload
    payload = {
        "stream": False,
	    "model": "Meta-Llama-3.1-405B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": system_prompts[attempt - 1]
            },
            {
                "role": "user", 
                "content": f"Please shorten the following text, keeping it as concise as possible:\n\n{text}"
            }
        ]
    }
    
    # Set up headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        # Send API request
        response = requests.post(api_url, 
                                 headers=headers, 
                                 data=json.dumps(payload),
                                 timeout=30)
        
        # Check for successful response
        response.raise_for_status()
        
        # Extract shortened text
        result = response.json()
        shortened_text = result['choices'][0]['message']['content'].strip()
        
        # Return result with additional metadata
        return {
            'text': shortened_text,
            'length': len(shortened_text),
            'attempt': attempt
        }
    
    except requests.RequestException as e:
        print(f"API Request Error: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Response Parsing Error: {e}")
        return None

def process_text(input_text, api_key):
    """
    Process text with intelligent shortening and length management.
    
    Args:
        input_text (str): Text to be processed
        api_key (str): SambaNova API key
    
    Returns:
        str: Optimally shortened text
    """
    # Initial tracking of attempts and results
    attempts = []
    
    # Attempt to shorten text up to 3 times
    for attempt in range(1, 4):
        # Shorten the text
        result = shorten_text(input_text, api_key, attempt=attempt)
        
        if result is None:
            print(f"Attempt {attempt} failed completely.")
            continue
        
        # Store the result
        attempts.append(result)
        
        # Check length constraints
        if 650 <= result['length'] <= 850:
            print(f"Successful shortening on attempt {attempt}")
            return result['text']
        
        # Prepare for next iteration
        input_text = result['text']
    
    # If all attempts fail, find the closest to target length
    if attempts:
        closest = min(attempts, key=lambda x: abs(x['length'] - 4500))
        print(f"Using result from attempt {closest['attempt']} (length: {closest['length']})")
        return closest['text']
    
    # Fallback if everything fails
    print("Could not shorten text successfully.")
    return input_text

def main():
    # Read input from file in the same directory
    input_file = 'coehlo_text.txt'
    api_key = "743469fc-de31-407d-bea3-a45c35f05ea2"  # Replace with actual API key
    
    # Check if file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found in the current directory.")
        return
    
    # Read the input text from file
    with open(input_file, 'r', encoding='utf-8') as file:
        input_text = file.read()
    
    # Extract the source from the input text (assuming it starts with 'Source:')
    source_line = input_text.split('\n')[0]
    source = source_line.replace('Source:', '').strip() if 'Source:' in source_line else 'an unknown source'
    
    # Process and shorten the text
    shortened_text = process_text(input_text, api_key)
    
    # Append the custom message
    custom_message = f"\n\nThis is the news from {source} reported for you by Sound Bite, made by Sundai Club in Boston."
    final_output = shortened_text + custom_message
    
    # Print lengths and final text
    print("Original Length:", len(input_text))
    print("Final Length:", len(final_output))
    
    # Save final output to a new file
    output_file = 'shortened_coehlo_text.txt'
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(final_output)
    print(f"\nFinal text saved to {output_file}")

if __name__ == "__main__":
    main()
