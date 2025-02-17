import argparse
import os
import sys
import re
import subprocess
from bs4 import BeautifulSoup
from jinja2 import Environment, DictLoader
# For handling file paths
from pathlib import Path
from datetime import datetime


# === FUNCTIONS ===

# Extract data from the HTML content
def extract_data_from_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Initialize list to hold data for each story
    stories = []
    
    # Iterate over each .article-story element
    for story_div in soup.find_all('div', class_='article-story'):
        # Extract the heading and remove the back-link
        header_div = story_div.find('div', class_='header')
        if header_div:
            back_link = header_div.find('a', class_='back-link')
            if back_link:
                back_link.decompose()  # Remove the back-link
            header = header_div.get_text(strip=True)
            heading = re.sub(r'^\d+\.\s+', '', header)
        else:
            heading = None
        
        # Extract the source
        source = None
        for li in story_div.find_all('li'):
            if 'Zdroj:' in li.get_text():
                source = li.find('strong').get_text(strip=True)
                # Remove everything after the first slash
                if '/' in source:
                    source = source.split('/')[0]
                break

        # Extract the publication date
        pub_date = None
        for li in story_div.find_all('li'):
            if 'Publikováno:' in li.get_text():
                pub_date_text = li.get_text(strip=True)
                pub_date = re.search(r'\d+\.\s*\d+\.\s*\d+', pub_date_text).group(0).replace(' ', '')
                break

        # Extract the article URL (odkaz)
        article_url = None
        article_transcript = story_div.find('div', class_='article-transcript')
        if article_transcript:
            p_tags = article_transcript.find_all('p')
            for p_tag in p_tags:
                if 'Odkaz:' in p_tag.get_text():
                    a_tag = p_tag.find('a')
                    if a_tag:
                        article_url = a_tag['href']
                        break

        # Add story data to list
        stories.append({
            'heading': heading,
            'source': source,
            'pub_date': pub_date,
            'article_url': article_url
        })

    return stories

# Generate an HTML report from the data
def generate_html_from_template(stories, out_folder, out_file_name):
    # Define the Jinja2 template as a string
    template_str = """{% for story in stories %}        
        <tr>
          <td>{{ story.pub_date }}</td>
          <td>{{ story.source }}</td>
          <td><a target="_blank" href="{{ story.article_url }}">{{ story.heading }}</a></td>
        </tr>{% endfor %}"""
    
    
    # Prepend/append template_str with lines of HTML comments with current date
    today_8601 = datetime.now().strftime("%Y-%m-%d")
    template_str = f"<!-- Přidáno {today_8601} -->\n{template_str}\n        \n<!-- Přidáno {today_8601} (end) -->"


    # Create a Jinja2 environment with the template string
    env = Environment(loader=DictLoader({'template.html': template_str}))
    template = env.get_template('template.html')
    
    # Render the template with the data
    html_content = template.render(stories=stories)

    out_file_path = out_folder / out_file_name
    
    try:
        # Write the rendered HTML to the specified file with UTF-8 encoding
        with open(out_file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        # print(f"HTML report generated successfully at '{out_file_path}'.")

    except PermissionError:
        print(f"Permission denied: Cannot write to '{out_file_path}'.")

    except Exception as e:
        print(f"An error occurred while writing the file: {e}")

# Open file in VSCode
def open_in_vscode(file_path):
    try:
        subprocess.run(["code", file_path], check=True, shell=True) # shell=True is needed for Windows, else it throws "[WinError 2] The system cannot find the file specified"
    except Exception as e:
        print(f"Failed to open in VSCode: {e}")
        print(f"file_path: {file_path}")

# === END OF FUNCTIONS ===


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Process an HTML file and generate a report.')
    parser.add_argument('input_file', nargs='?', help='The path to the input HTML file.')
    
    # Parse arguments
    args = parser.parse_args()

    while True:
        if args.input_file:
            input_file = args.input_file
        else:
            input_file = input("""
┌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┐
┊                                             ┊
┊      Přetáhni HTML export z Mediaboard      ┊
┊                                             ┊
┊                     nebo                    ┊
┊                                             ┊
┊            vlož cestu k souboru             ┊
┊                                             ┊
└╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌┘
""").strip()

        # Remove surrounding quotes if they exist
        if input_file.startswith('"') and input_file.endswith('"'):
            input_file = input_file[1:-1]

        # Check if the file has an .html extension
        if not input_file.lower().endswith('.html'):
            print(f"Error: The file '{input_file}' is not an HTML file. Please provide a valid HTML file.")
            continue

        # Check if the file exists
        if not os.path.isfile(input_file):
            print(f"Error: The file '{input_file}' does not exist. Please provide a valid HTML file.")
            continue

        break

    try:
        # Read the HTML file with UTF-8 encoding
        with open(input_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        # Extract data from the HTML
        stories = extract_data_from_html(html_content)

        # Get path to desktop with pathlib, using environment variable %USERPROFILE%
        # out_folder = Path(os.environ['USERPROFILE']) / 'Desktop'                   # Outputs to current user's desktop
        out_folder = Path(input_file).parent                         # Outputs to the same folder as the input file
        out_file_name_base = "Mediaboard - Napsali o nás.html"
        out_file_name = out_file_name_base
        out_file_path = out_folder / out_file_name

        # Check if the output file already exists and increment the suffix number
        counter = 1
        while out_file_path.exists():
            out_file_name = f"{out_file_name_base} ({counter}).html"
            out_file_path = out_folder / out_file_name
            counter += 1

        # Generate the HTML report
        generate_html_from_template(stories, out_folder, out_file_name)
        
        # Print the file_path
        print(f"Úspěšně vytvořen soubor: {out_file_name} ve složce: {out_folder}")

        # Open the generated HTML file in VSCode
        open_in_vscode(out_folder / out_file_name)
    
    except Exception as e:
        print(f"An error occurred: {e}")

    # Keep the command prompt open
    # input("Press Enter to exit...")

if __name__ == '__main__':
    main()