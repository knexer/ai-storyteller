import os
import sys
from collections import defaultdict
from fuzzywuzzy import fuzz
import openai
from dotenv import load_dotenv

from ideation import Ideation
from filter_ideas import filter_ideas
from outline_story import Outliner

def print_numbered_list(label, list):
    print(f"\n{label}:\n")
    for i, item in enumerate(list, start=1):
        print(f'{i}. {item}')

def get_full_idea(ideas, title):
    return max([(idea, fuzz.partial_ratio(idea, title)) for idea in ideas], key=lambda x:x[1])[0]

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
print_numbered_list("Generated ideas", ideas)

# Find the best ideas
most_creative = filter_ideas(ideas, "most creative, surprising, and unexpected ideas that excite the imagination")
print_numbered_list("Most creative ideas", most_creative)

best_fit = filter_ideas(ideas, "ideas that best fit the client's constraints:\n{conditioning_info}")
print_numbered_list("Most targeted ideas", best_fit)

cutest = filter_ideas(ideas, "cutest and most adorable stories")
print_numbered_list("Cutest ideas", cutest)

# Combine the weighted vote counts from each filter
combined_vote_counts = defaultdict(float)
for weight, votes in zip([0.5, 0.3, 0.2], [most_creative, best_fit, cutest]):
    for idea, count in votes:
        combined_vote_counts[idea] += count * weight

# Sort the combined vote counts in descending order
sorted_by_combined_votes = sorted(combined_vote_counts.items(), key=lambda x: x[1], reverse=True)

print_numbered_list("Overall best ideas", sorted_by_combined_votes)

selected_title = sorted_by_combined_votes[0][0]
selected_idea = get_full_idea(ideas, selected_title)
print(f"\nSelected idea:\n")
print(selected_idea)

outlines = Outliner(conditioning_info, selected_title, selected_idea).outline()
print(f"\nPotential outlines:\n")
print("\n\n========\n\n".join(outline for outline in outlines))

# Write a more detailed story description
# Split the story up into pages, each with a couple lines of story and a brief image description.
# Produce an illustration for each page. Special care will need to be taken to get (semi) consistent characters and settings.
# Format the series of pages into a book.
