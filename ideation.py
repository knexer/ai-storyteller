import os
import sys
import re
import openai

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

class Ideation:
    def __init__(self, conditioning_info):
        self.conditioning_info = conditioning_info

    def outline_prompt(self):
        return f"""You are an AI storybook writer. You write engaging, creative, and highly diverse content for illustrated books for children.
The first step in your process is ideation - workshop a bunch of ideas and find the ones with that special spark.

Your client has provided some constraints for you to satisfy, but within those constraints you have total artistic control, so get creative with it!
Client constraints:
{self.conditioning_info}

Come up with a numbered list of ten ideas. Focus on variety. Each idea should have a title and a one sentence summary.
"""

    def make_ideas(self, n):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": self.outline_prompt()},
            ],
            n=n,
            temperature=1,
        )

        return parse_ideas([choice.message.content for choice in response.choices])
