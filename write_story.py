import os
import sys
import openai
from dotenv import load_dotenv

from ideation import Ideation
from filter_ideas import filter_ideas

load_dotenv()
openai.api_key = os.environ["OPENAI_API_KEY"]

if len(sys.argv) != 2:
    print(f"wrong number of args, expected 1, got {len(sys.argv)}")
    exit()

# Collect (optional) user-specified conditioning information, e.g. target audience, characters, setting, visual style, plot elements, etc.
conditioning_info = sys.argv[1]

print(f"Generating a story conditioned on:\n{conditioning_info}")

# Come up with a bunch of ideas
ideas = Ideation(conditioning_info).make_ideas(4)

print("\nGenerated ideas:\n")
for i, idea in enumerate(ideas, start=1):
    print(f'{i}. {idea}')

# Find the best ideas
most_creative = filter_ideas(ideas, "most creative, surprising, and unexpected ideas that excite the imagination")

print("\nMost creative ideas:\n")
for i, idea in enumerate(most_creative, start=1):
    print(f'{i}. {idea}')

best_fit = filter_ideas(ideas, "ideas that best fit the client's constraints:\n{conditioning_info}")

print("\nMost targeted ideas:\n")
for i, idea in enumerate(best_fit, start=1):
    print(f'{i}. {idea}')

cutest = filter_ideas(ideas, "cutest and most adorable stories")

print("\nCutest ideas:\n")
for i, idea in enumerate(cutest, start=1):
    print(f'{i}. {idea}')

# Write a more detailed story description
# Split the story up into pages, each with a couple lines of story and a brief image description.
# Produce an illustration for each page. Special care will need to be taken to get (semi) consistent characters and settings.
# Format the series of pages into a book.
