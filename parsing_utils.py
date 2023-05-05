import re


def parse_numbered_list(response):
    # Response is a string with a numbered list of items

    # Match the start of each list element
    # Regex explanation:
    # ^(\d+) - Match a number at the start of a line
    # [^\w\n] - Match a non-word character (e.g. a period, colon, or close parenthesis)
    matches = re.finditer(r"^(\d+)[^\w\n]", response, re.MULTILINE)

    # Extract indices and sort them
    indices = [match.start() for match in matches]
    indices.append(len(response))
    indices.sort()

    # Extract items using indices
    items = [
        response[indices[i] : indices[i + 1]].strip() for i in range(len(indices) - 1)
    ]

    # Remove the number, punctuation, and leading whitespace from each item
    items = [re.sub(r"^\d+[^\w\n]\s*", "", item, flags=re.MULTILINE) for item in items]

    if len(items) != 3:
        return []

    return items
