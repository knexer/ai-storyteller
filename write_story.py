import os
import sys
import re
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

if len(sys.argv) != 2:
    print(f"wrong number of args, expected 1, got {len(sys.argv)}")
    exit()

# Collect (optional) user-specified conditioning information, e.g. target audience, characters, setting, visual style, plot elements, etc.
conditioning_info = sys.argv[1]

print(f"Generating a story conditioned on:\n{conditioning_info}")

def outline_prompt(conditioning_info):
    return f"""You are an AI storybook writer. You write engaging, creative, and highly diverse content for illustrated books for children.
The first step in your process is ideation - workshop a bunch of ideas and find the ones with that special spark.

Your client has provided some constraints for you to satisfy, but within those constraints you have total artistic control, so get creative with it!
Client constraints:
{conditioning_info}

Come up with a numbered list of ten ideas. Focus on variety. Each idea should have a title and a one sentence summary.
"""

# Generate a cohesive story outline.
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": outline_prompt(conditioning_info)},
    ],
    n=3,
    temperature=1,
)

def parse_ideas(texts):
    # The regular expression pattern:
    # It looks for a number followed by a '.', ':', or ')' (with optional spaces)
    # and then captures any text until it finds a newline character or the end of the string
    pattern = re.compile(r'\d[\.\:\)]\s*(.*?)(?=\n\d|$)', re.MULTILINE)

    # Find all matches using the 'findall' method
    matches = []
    for text in texts:
        matches = matches + pattern.findall(text)

    # Return the matches
    return matches

ideas = parse_ideas([choice.message.content for choice in response.choices])

print("\nGenerated ideas:\n")
for i, idea in enumerate(ideas, start=1):
    print(f'{i}. {idea}')

# Split the story up into pages, each with a couple lines of story and a brief image description.
# Produce an illustration for each page. Special care will need to be taken to get (semi) consistent characters and settings.
# Format the series of pages into a book.
