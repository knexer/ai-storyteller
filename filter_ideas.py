import openai
import json
import concurrent

num_voters = 4

def filter_ideas(ideas, criteria):
    all_ideas = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Use a list comprehension to create a list of two Future objects
        future_list = [executor.submit(pick_five, ideas, criteria) for _ in range(num_voters)]

        # As the futures complete, extend `all_ideas` with their results
        for future in concurrent.futures.as_completed(future_list):
            all_ideas.extend(future.result())

    counts = [(idea, all_ideas.count(idea)) for idea in set(all_ideas)]
    sorted_by_votes = sorted(counts, key=lambda x:x[1], reverse=True)

    return sorted_by_votes

def format_ideas(ideas):
    return "\n".join([f'{i}. {idea}' for i, idea in enumerate(ideas, start=1)])

def pick_five(ideas, criteria):
    prompt = f"""You are an AI writing assistant helping an author filter through their story concepts. The following is a list of ideas for an illustrated children's book:

{format_ideas(ideas)}

Pick the five {criteria}."""

    unformatted_five_ideas = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ],
        n=1,
        temperature=1,
    )

    five_titles_list = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": prompt},
        unformatted_five_ideas.choices[0].message,
        {"role": "user", "content": "Write the titles of your chosen five ideas in a json list. Output json only, with no other text - your output will be parsed as json."}
        ],
        n=1,
        temperature=0,
    )

    try:
        return json.loads(five_titles_list.choices[0].message.content)
    except:
        print(f"Could not parse as JSON: {five_titles_list.choices[0].message.content}")
        return []