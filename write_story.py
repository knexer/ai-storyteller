import os
import sys
import openai
from dotenv import load_dotenv

from ideation import Ideation

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

if len(sys.argv) != 2:
    print(f"wrong number of args, expected 1, got {len(sys.argv)}")
    exit()

# Collect (optional) user-specified conditioning information, e.g. target audience, characters, setting, visual style, plot elements, etc.
conditioning_info = sys.argv[1]

print(f"Generating a story conditioned on:\n{conditioning_info}")

ideas = Ideation(conditioning_info).make_ideas(3)

print("\nGenerated ideas:\n")
for i, idea in enumerate(ideas, start=1):
    print(f'{i}. {idea}')

# Split the story up into pages, each with a couple lines of story and a brief image description.
# Produce an illustration for each page. Special care will need to be taken to get (semi) consistent characters and settings.
# Format the series of pages into a book.
