import os
import re
import random
import pdfkit
import base64
import requests
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Educational values and lessons for fairytales
FAIRYTALE_LESSONS = [
    "Kindness and compassion towards others, even strangers",
    "The importance of honesty and telling the truth",
    "Hard work and perseverance lead to success",
    "Being brave doesn't mean you're not scared, it means doing what's right despite fear",
    "True friendship means helping each other through difficult times",
    "Don't judge others by their appearance - look for inner beauty",
    "Sharing what you have makes everyone happier",
    "Being humble is more important than being proud",
    "Listening to wise advice can save you from trouble",
    "Forgiveness is more powerful than revenge",
    "Being grateful for what you have brings contentment",
    "Everyone has special talents - believe in yourself",
    "Helping others without expecting anything in return",
    "Patience and waiting for the right moment",
    "The value of family and taking care of each other",
    "Being responsible for your actions and choices",
    "Curiosity and learning new things make life exciting",
    "Standing up for what is right, even when it's difficult",
    "The magic of believing in yourself and your dreams",
    "Treating all living things with respect and care"
]

# Master storytellers and their distinctive styles
STORYTELLER_STYLES = [
    {
        "name": "Astrid Lindgren",
        "style": """Write in Astrid Lindgren's warm, empathetic style:
        - Deep understanding of children's emotions and inner worlds
        - Mix of everyday life with magical adventures
        - Strong, independent child protagonists who solve their own problems
        - Gentle humor and whimsy
        - Nature as a character - forests, meadows, seasons
        - Cozy, safe feeling even during adventures
        - Simple, clear language that respects children's intelligence
        - Emphasis on freedom, imagination, and the joy of childhood""",
        "classic_elements": ["talking animals", "secret forest places", "midnight adventures", "wise old trees",
                             "magical summer days", "helpful creatures", "ancient wisdom"]
    },
    {
        "name": "Oscar Wilde",
        "style": """Write in Oscar Wilde's elegant, poetic fairytale style:
        - Rich, beautiful language with lyrical descriptions
        - Deep moral messages woven elegantly into the narrative
        - Bittersweet elements - beauty mixed with melancholy
        - Vivid, jewel-like imagery and metaphors
        - Characters who learn through sacrifice and love
        - Philosophical depth presented simply
        - Emphasis on beauty, art, and the human heart
        - Touching endings that stay with the reader""",
        "classic_elements": ["enchanted statues", "talking nightingales", "magical gardens", "precious gems that weep",
                             "stars that speak", "roses with secrets", "golden hearts"]
    },
    {
        "name": "Roald Dahl",
        "style": """Write in Roald Dahl's delightfully mischievous style:
        - Clever, witty narrative voice that speaks directly to children
        - Delicious vocabulary and invented words
        - Good characters are very good, bad characters are horrid
        - Surprising plot twists and comeuppances
        - Dark humor that children love but doesn't frighten
        - Adults who don't understand children vs those who do
        - Magic that feels both impossible and completely logical
        - Fast-paced, exciting adventures with satisfying endings""",
        "classic_elements": ["chocolate waterfalls", "dream bottles", "friendly giants", "magical candies",
                             "peculiar inventions", "terrible aunts", "fantastic medicines"]
    },
    {
        "name": "Hans Christian Andersen",
        "style": """Write in Hans Christian Andersen's classic fairytale style:
        - Transformative journeys and metamorphoses
        - Ordinary objects coming to life with personalities
        - Deep empathy for outsiders and underdogs
        - Nature imagery - flowers, seasons, weather as metaphors
        - Gentle melancholy mixed with hope
        - Simple beginnings leading to profound adventures
        - Characters finding where they truly belong
        - Timeless, universal themes in specific stories""",
        "classic_elements": ["tin soldiers", "paper dancers", "snow queens", "little mermaids", "ugly ducklings",
                             "magical mirrors", "enchanted swans"]
    },
    {
        "name": "Beatrix Potter",
        "style": """Write in Beatrix Potter's charming, detailed style:
        - Precise, delightful descriptions of small worlds
        - Animal characters with very human problems
        - Gentle adventures in gardens, forests, and countryside
        - Cozy domestic details - tea times, warm beds, tidy homes
        - Natural consequences teaching lessons
        - British countryside sensibility
        - Perfect balance of danger and safety
        - Miniature worlds described with loving detail""",
        "classic_elements": ["rabbit burrows", "hedgehog laundries", "mouse tidying", "squirrel provisions",
                             "frog fishing", "garden gates", "cozy kitchens"]
    }
]


def get_personalization_details():
    """Gather personalization details from the user"""
    print("\n🌟 Let's personalize your fairytales! 🌟")
    print("=" * 60)

    # Main character details
    hero_name = input("What's the name of the main character (you or your loved one)? ")
    hero_age = input(f"How old is {hero_name}? ")
    hero_gender = input(f"What pronouns should we use for {hero_name}? (he/she/they): ").lower()

    # Physical appearance for more personalized stories and images
    print(f"\n📝 Let's add some details about {hero_name} to make the stories more personal:")
    hair_color = input(f"What color is {hero_name}'s hair? ")
    eye_color = input(f"What color are {hero_name}'s eyes? ")
    favorite_color = input(f"What's {hero_name}'s favorite color? ")

    # Interests and personality
    favorite_animal = input(f"What's {hero_name}'s favorite animal? ")
    favorite_activity = input(f"What does {hero_name} love to do? (e.g., singing, drawing, playing soccer): ")
    personality_trait = input(f"Describe {hero_name} in one word (e.g., curious, brave, kind): ")

    # Special details
    best_friend = input(f"Does {hero_name} have a best friend or pet to include? (name or press Enter to skip): ")
    special_item = input(
        f"Does {hero_name} have a special toy or item? (e.g., teddy bear, lucky bracelet, or press Enter): ")

    # Dreams and fears (for story depth)
    big_dream = input(f"What's something {hero_name} dreams about? (e.g., flying, being a doctor, meeting a unicorn): ")
    small_fear = input(
        f"What's something small that {hero_name} is working on overcoming? (e.g., darkness, loud noises): ")

    return {
        'name': hero_name,
        'age': hero_age,
        'gender': hero_gender,
        'pronouns': {
            'he': {'subject': 'he', 'object': 'him', 'possessive': 'his', 'reflexive': 'himself'},
            'she': {'subject': 'she', 'object': 'her', 'possessive': 'her', 'reflexive': 'herself'},
            'they': {'subject': 'they', 'object': 'them', 'possessive': 'their', 'reflexive': 'themselves'}
        }.get(hero_gender, {'subject': 'they', 'object': 'them', 'possessive': 'their', 'reflexive': 'themselves'}),
        'appearance': {
            'hair_color': hair_color,
            'eye_color': eye_color,
            'favorite_color': favorite_color
        },
        'interests': {
            'favorite_animal': favorite_animal,
            'favorite_activity': favorite_activity,
            'personality': personality_trait
        },
        'relationships': {
            'best_friend': best_friend if best_friend else None,
            'special_item': special_item if special_item else None
        },
        'inner_world': {
            'dream': big_dream,
            'fear': small_fear
        }
    }


def generate_personalized_image(title, hero_details, story_context, main_theme, storyteller_name, is_first_image=False):
    """Generate a personalized image featuring the hero with consistent character appearance"""

    # Create a consistent character description that will be used for ALL images
    base_character = f"""
    EXACT CHARACTER APPEARANCE (must be identical in every image):
    - Child named {hero_details['name']}, exactly {hero_details['age']} years old
    - {hero_details['appearance']['hair_color']} hair (exact same style and length in all images)
    - {hero_details['appearance']['eye_color']} eyes
    - Wearing {hero_details['appearance']['favorite_color']} colored clothing
    - {hero_details['interests']['personality']} expression
    - Same facial features, body proportions, and overall appearance in every single image
    """

    # Map storyteller to background/scene style only
    scene_styles = {
        "Astrid Lindgren": "Scandinavian countryside, forests, meadows, cozy homes",
        "Oscar Wilde": "ornate palace gardens, magical fountains, jeweled settings",
        "Roald Dahl": "whimsical candy factories, peculiar buildings, fantastic landscapes",
        "Hans Christian Andersen": "enchanted forests, misty lakes, fairy tale castles",
        "Beatrix Potter": "English gardens, countryside cottages, woodland paths"
    }

    scene = scene_styles.get(storyteller_name, "magical fairytale setting")

    # Create a personalized prompt with emphasis on character consistency
    image_prompt = f"""
    Children's book illustration featuring the EXACT SAME child character in every image:
    {base_character}

    CRITICAL: The child must look EXACTLY THE SAME as in all other images - same face, same hair, same clothes, same proportions.

    Scene: {story_context}
    Background setting: {scene} in {main_theme}

    Style: Consistent Disney/Pixar 3D animation style for character consistency.
    The character {hero_details['name']} should be doing something related to: {story_context}

    No text in the image. Focus on making the character appearance identical across all images.
    """

    try:
        print(f"   🎨 Creating consistent character illustration...")
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url

        # Download the image and convert to base64
        image_response = requests.get(image_url)
        image_base64 = base64.b64encode(image_response.content).decode('utf-8')

        return f"data:image/png;base64,{image_base64}"
    except Exception as e:
        print(f"   ⚠️  Could not generate image: {str(e)}")
        return None


def determine_story_length():
    """Randomly determine story length in pages and return word count"""
    pages = random.randint(2, 5)
    # Approximate words per page for children's books (less dense than adult books)
    words_per_page = random.randint(250, 400)
    total_words = pages * words_per_page
    return pages, total_words


def create_personalized_titles(hero_details, main_theme, num_fairytales, storytellers):
    """Generate personalized fairytale titles that feel like classic stories"""

    # Classic title patterns that feel authentic
    title_patterns = [
        f"{hero_details['name']} and the [magical object/creature]",
        f"The [adjective] [noun] of {main_theme}",
        f"When {hero_details['name']} Met the [creature]",
        f"The Secret of [mysterious place]",
        f"The [time of day] the [magical thing] Appeared",
        f"{hero_details['name']}'s [adjective] Discovery",
        f"The [creature] Who [did something unexpected]",
        f"Beyond the [color] [barrier]",
        f"The Last [magical item] in {main_theme}",
        f"A Most Unusual [day of week]"
    ]

    prompt = f"""
    Create {num_fairytales} fairytale titles that sound like classic stories from great authors.
    Mix these approaches:
    - Some titles should include {hero_details['name']}
    - Some should be mysterious without mentioning names
    - Some should reference {main_theme}
    - All should sound magical and intriguing

    Examples of good titles:
    - "{hero_details['name']} and the Clockwork Dragon"
    - "The Whispering Woods of {main_theme}"
    - "When the Stars Fell Down"
    - "{hero_details['name']}'s Midnight Garden"
    - "The {hero_details['appearance']['favorite_color'].title()} Phoenix"
    - {hero_details['name']} and the [magical object/creature]
    - The [adjective] [noun] of {main_theme}
    - When {hero_details['name']} Met the [creature]
    - The Secret of [mysterious place]
    - The [time of day] the [magical thing] Appeared
    - {hero_details['name']}'s [adjective] Discovery
    - The [creature] Who [did something unexpected]
    - Beyond the [color] [barrier]
    - The Last [magical item] in {main_theme}
    - A Most Unusual [day of week]

    Make them varied - not all starting with the character's name!

    Format as:
    1. [title]
    2. [title]
    etc.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": "You create magical fairytale titles in the style of classic children's literature."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9
    )

    titles = re.findall(r"\d+\.\s(.+)", response.choices[0].message.content)
    return titles


def save_pdf_with_cover(book_title: str, html_body: str, author_name: str = "AI Storyteller", hero_name: str = "",
                        output_file="fairytale_collection.pdf"):
    html_template = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600&family=Dancing+Script:wght@700&family=Merriweather:wght@400;700&display=swap');

            body {{
                font-family: 'Merriweather', serif;
                margin: 0;
                line-height: 1.8;
                color: #2d3748;
            }}

            /* Stunning Cover Page */
            .cover-page {{
                height: 100vh;
                background: radial-gradient(ellipse at top, #1a1a2e 0%, #0f0f1e 50%, #16213e 100%);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                color: white;
                page-break-after: always;
                position: relative;
                overflow: hidden;
            }}

            /* Magical sparkles animation */
            .cover-page::before {{
                content: '';
                position: absolute;
                width: 200%;
                height: 200%;
                background-image: 
                    radial-gradient(circle at 20% 35%, rgba(255, 255, 255, 0.3) 0%, transparent 1%),
                    radial-gradient(circle at 75% 44%, rgba(255, 255, 255, 0.2) 0%, transparent 1%),
                    radial-gradient(circle at 68% 85%, rgba(255, 215, 0, 0.4) 0%, transparent 1%);
                background-size: 30% 30%, 40% 40%, 50% 50%;
                animation: sparkle 20s linear infinite;
            }}

            @keyframes sparkle {{
                0% {{ transform: translate(0, 0) rotate(0deg); }}
                100% {{ transform: translate(-50%, -50%) rotate(360deg); }}
            }}

            .cover-title {{
                font-family: 'Cinzel', serif;
                font-size: 60pt;
                font-weight: 600;
                margin-bottom: 30px;
                text-shadow: 
                    0 0 30px rgba(255, 215, 0, 0.7),
                    0 0 60px rgba(255, 215, 0, 0.5),
                    0 0 90px rgba(255, 215, 0, 0.3);
                background: linear-gradient(45deg, #FFD700, #FFA500, #FFD700);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                position: relative;
                z-index: 1;
            }}

            .cover-dedication {{
                font-family: 'Dancing Script', cursive;
                font-size: 32pt;
                margin: 40px 0;
                padding: 30px 60px;
                border: 3px solid rgba(255, 215, 0, 0.6);
                border-radius: 20px;
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(10px);
                text-shadow: 0 0 20px rgba(255, 215, 0, 0.8);
                position: relative;
                z-index: 1;
            }}

            .cover-subtitle {{
                font-size: 20pt;
                margin-bottom: 20px;
                opacity: 0.9;
                letter-spacing: 3px;
                text-transform: uppercase;
                font-weight: 300;
                position: relative;
                z-index: 1;
            }}

            .cover-decoration {{
                position: absolute;
                font-size: 150pt;
                opacity: 0.1;
                animation: float 6s ease-in-out infinite;
            }}

            .cover-decoration:nth-child(1) {{ top: 10%; left: 10%; animation-delay: 0s; }}
            .cover-decoration:nth-child(2) {{ top: 20%; right: 15%; animation-delay: 2s; }}
            .cover-decoration:nth-child(3) {{ bottom: 20%; left: 20%; animation-delay: 4s; }}

            @keyframes float {{
                0%, 100% {{ transform: translateY(0px) rotate(0deg); }}
                50% {{ transform: translateY(-20px) rotate(10deg); }}
            }}

            .cover-author {{
                font-size: 16pt;
                position: absolute;
                bottom: 60px;
                letter-spacing: 2px;
                opacity: 0.8;
                position: relative;
                z-index: 1;
            }}

            /* Content Styles with Better Margins */
            .content {{
                margin: 2.5cm 3cm 3cm 3cm;
                max-width: 18cm;
            }}

            h1 {{
                text-align: center;
                font-size: 32pt;
                margin-bottom: 1.5em;
                color: #2d3748;
                font-family: 'Cinzel', serif;
                font-weight: 600;
                letter-spacing: 2px;
                position: relative;
                padding-bottom: 20px;
            }}

            h1::after {{
                content: '';
                position: absolute;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 100px;
                height: 3px;
                background: linear-gradient(to right, transparent, #667eea, transparent);
            }}

            p {{
                text-align: justify;
                font-size: 12pt;
                margin-bottom: 1.2em;
                color: #2d3748;
            }}

            /* Beautiful Fairytale Titles */
            .fairytale-title {{
                font-family: 'Cinzel', serif;
                font-size: 28pt;
                color: #4a5568;
                text-align: center;
                margin: 3em 0 1.5em 0;
                padding: 30px;
                position: relative;
                letter-spacing: 1px;
            }}

            .fairytale-title::before,
            .fairytale-title::after {{
                content: '';
                position: absolute;
                width: 50px;
                height: 50px;
                border: 2px solid #667eea;
            }}

            .fairytale-title::before {{
                top: 0;
                left: 0;
                border-right: none;
                border-bottom: none;
            }}

            .fairytale-title::after {{
                bottom: 0;
                right: 0;
                border-left: none;
                border-top: none;
            }}

            .storyteller-note {{
                text-align: center;
                font-style: italic;
                color: #718096;
                margin-bottom: 30px;
                font-size: 11pt;
                letter-spacing: 1px;
            }}

            .pagebreak {{
                page-break-after: always;
            }}

            /* Table of Contents Styling */
            .toc-entry {{
                margin: 20px 0;
                font-size: 14pt;
                padding-bottom: 10px;
                position: relative;
            }}

            .toc-entry::after {{
                content: '';
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 1px;
                background: linear-gradient(to right, #e2e8f0, transparent);
            }}

            .toc-storyteller {{
                font-style: italic;
                color: #718096;
                font-size: 10pt;
                margin-left: 20px;
                margin-top: 5px;
            }}

            .foreword {{
                font-style: italic;
                background: linear-gradient(135deg, #f8f9fa 0%, #f0f4f8 100%);
                padding: 30px;
                border-radius: 15px;
                margin: 30px 0;
                border-left: 4px solid #667eea;
                font-size: 11pt;
                line-height: 1.8;
            }}

            /* Image Styles */
            .fairytale-image {{
                text-align: center;
                margin: 40px 0;
                page-break-inside: avoid;
            }}

            .fairytale-image img {{
                max-width: 75%;
                height: auto;
                border-radius: 15px;
                box-shadow: 
                    0 10px 30px rgba(0, 0, 0, 0.15),
                    0 5px 15px rgba(0, 0, 0, 0.08);
            }}

            .image-caption {{
                font-style: italic;
                color: #718096;
                margin-top: 15px;
                font-size: 10pt;
            }}

            .dedication-page {{
                text-align: center;
                padding: 120px 60px;
                font-style: italic;
                font-size: 16pt;
                color: #4a5568;
                line-height: 2;
            }}

            .dedication-page h2 {{
                font-family: 'Dancing Script', cursive;
                font-size: 36pt;
                color: #667eea;
                margin-bottom: 40px;
            }}

            .story-info {{
                display: flex;
                justify-content: space-between;
                font-size: 9pt;
                color: #a0aec0;
                margin-bottom: 25px;
                padding-bottom: 10px;
                border-bottom: 1px solid #e2e8f0;
            }}
        </style>
    </head>
    <body>
        {html_body}
    </body>
    </html>
    """

    options = {
        'page-size': 'A4',
        'margin-top': '0mm',
        'margin-right': '0mm',
        'margin-bottom': '0mm',
        'margin-left': '0mm',
        'encoding': "UTF-8",
        'no-outline': None,
        'enable-local-file-access': None
    }

    pdfkit.from_string(html_template, output_file, options=options)


# === Step 1: Get user input ===
print("🧚‍♀️ Welcome to the Personalized Fairytale Collection Generator! ✨")
print("Create magical stories starring YOU or your loved ones!")
print("Written in the style of the world's greatest storytellers!")
print("=" * 60)

# Get hero details first
hero_details = get_personalization_details()

print(f"\n📚 Now let's create magical stories for {hero_details['name']}!")
print("=" * 60)

main_theme = input(
    "What magical world should the stories take place in? (e.g., enchanted forest, underwater kingdom, cloud castle): ")
num_fairytales = int(input("How many personalized fairytales would you like? (recommended 3-5): "))
collection_title = input(
    f"What should we call {hero_details['name']}'s story collection? (or press Enter for auto-generated): ")

if not collection_title:
    collection_title = f"{hero_details['name']}'s Magical Adventures in {main_theme.title()}"

# === Step 2: Generate personalized titles ===
print(f"\n✨ Creating magical story titles inspired by classic fairytales...")
fairytale_titles = create_personalized_titles(hero_details, main_theme, num_fairytales, STORYTELLER_STYLES)

# Assign a storyteller to each tale
storytellers_for_tales = []
for i in range(num_fairytales):
    storyteller = random.choice(STORYTELLER_STYLES)
    storytellers_for_tales.append(storyteller)

# === Generate personalized foreword ===
foreword_prompt = f"""
Write a warm, personal foreword for a fairytale collection starring {hero_details['name']}.
Mention:
- This collection was created especially for {hero_details['name']}
- {hero_details['name']} is {hero_details['age']} years old and loves {hero_details['interests']['favorite_activity']}
- Each story features {hero_details['name']} as the brave hero
- The stories are told by master storytellers like Astrid Lindgren, Oscar Wilde, and others
- Each tale varies in length (2-5 pages) and teaches important life lessons

Keep it warm, encouraging, and personal (100-150 words).
"""

foreword_resp = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": foreword_prompt}
    ],
    temperature=0.7,
    max_tokens=400
)
foreword = foreword_resp.choices[0].message.content

# === Generate personalized fairytales ===
fairytales_html = ""
toc_entries = ""
all_fairytales_text = ""

print(f"\n📚 Writing {len(fairytale_titles)} personalized fairytales starring {hero_details['name']}...")
print("🎨 Each story will have a unique illustration and be written by a master storyteller!")
print("=" * 60)

for i, (title, storyteller) in enumerate(zip(fairytale_titles, storytellers_for_tales), 1):
    # Select a lesson that connects to the hero's journey
    lesson = random.choice(FAIRYTALE_LESSONS)

    # Determine story length
    pages, target_words = determine_story_length()

    # Select random classic elements from the storyteller
    classic_elements = random.sample(storyteller['classic_elements'], 2)

    # Generate a variety of story openings
    story_openings = [
        f"In the heart of {main_theme}, where {classic_elements[0]} whispered secrets to the wind",
        f"It was on a perfectly ordinary Tuesday that {hero_details['name']} discovered",
        f"The {classic_elements[1]} had been waiting for exactly the right child",
        f"Nobody believed the old legend about {main_theme}, until",
        f"There are some secrets that only {hero_details['interests']['favorite_animal']}s know",
        f"The invitation arrived by {classic_elements[0]}, which was unusual",
        f"Most children would have run away, but {hero_details['name']}",
        f"The {hero_details['appearance']['favorite_color']} door had always been there",
        f"'Impossible!' everyone said, but {hero_details['name']} knew better",
        f"The map was drawn in starlight and could only be read"
    ]

    # Create highly personalized story prompt with storyteller style
    fairytale_prompt = f"""
    Write a fairytale titled "{title}" in the authentic style of {storyteller['name']}.

    STORYTELLER INSTRUCTIONS:
    {storyteller['style']}

    STORY SETUP:
    - Setting: {main_theme}
    - Opening line suggestion: {random.choice(story_openings)}
    - Include these classic {storyteller['name']} elements: {', '.join(classic_elements)}
    - Length: {target_words} words ({pages} pages)

    MAIN CHARACTER: {hero_details['name']} 
    - {hero_details['age']} years old, {hero_details['interests']['personality']}
    - Has {hero_details['appearance']['hair_color']} hair and loves {hero_details['interests']['favorite_activity']}
    - Accompanied by or encounters: {hero_details['interests']['favorite_animal']}

    IMPORTANT WRITING RULES:
    1. Start with action, mystery, or wonder - NOT with describing {hero_details['name']}
    2. Introduce {hero_details['name']} naturally as the story unfolds
    3. Include other memorable characters (magical beings, talking animals, wise elders, etc.)
    4. Write like {storyteller['name']}'s actual fairytales - with their rhythm, vocabulary, and story structure
    5. Weave in the life lesson naturally through events (never state it): {lesson}
    6. Include a scene involving {hero_details['inner_world']['fear']} and {hero_details['inner_world']['dream']}
    7. Make the {hero_details['appearance']['favorite_color']} color appear magically in the story
    8. Create a rich cast of characters - {hero_details['name']} shouldn't be alone
    9. Use varied dialogue and character interactions
    10. End with {storyteller['name']}'s typical ending style

    Remember: This should read like an authentic {storyteller['name']} story that happens to star {hero_details['name']}, 
    NOT a story about {hero_details['name']} with their characteristics listed.
    """

    print(f"✨ Story {i}: {title}")
    print(f"   📖 In the style of: {storyteller['name']}")
    print(f"   📄 Length: {pages} pages (~{target_words} words)")
    print(f"   💫 Teaching: {lesson}")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system",
             "content": f"You are {storyteller['name']}, the master storyteller. Write an authentic fairytale in your classic style, featuring a child named {hero_details['name']} naturally woven into the narrative."},
            {"role": "user", "content": fairytale_prompt}
        ],
        temperature=0.85,
        max_tokens=4000
    )

    fairytale_text = response.choices[0].message.content.strip()
    all_fairytales_text += f"\n\n{title}\nTold in the style of {storyteller['name']}\n\n{fairytale_text}"

    # Generate personalized image for EVERY fairytale
    image_html = ""
    # Extract a key scene from the story for the image
    story_context = f"{hero_details['name']} in a key scene from {title}"
    image_data = generate_personalized_image(title, hero_details, story_context, main_theme, storyteller['name'])
    if image_data:
        image_html = f"""
        <div class="fairytale-image">
            <img src="{image_data}" alt="{hero_details['name']} in {title}">
            <div class="image-caption">Illustration from "{title}"</div>
        </div>
        """

    # Add to table of contents with storyteller info
    toc_entries += f"""
    <div class="toc-entry">
        {i}. {title}
        <div class="toc-storyteller">In the style of {storyteller['name']} • {pages} pages</div>
    </div>
    """

    # Add formatted fairytale to HTML
    formatted_text = fairytale_text.replace('\n\n', '</p><p>').replace('\n', '</p><p>')
    fairytales_html += f"""
    <div class='pagebreak'></div>
    <div class='fairytale-title'>{title}</div>
    <div class='storyteller-note'>A tale told in the style of {storyteller['name']}</div>
    <div class="content">
        <div class="story-info">
            <span>Pages: {pages}</span>
            <span>Words: ~{target_words}</span>
            <span>Reading time: ~{target_words // 200} minutes</span>
        </div>
        {image_html}
        <p>{formatted_text}</p>
    </div>
    """

# === Assemble final HTML with stunning cover ===
html_body = f"""
<!-- Stunning Cover Page with magical effects -->
<div class='cover-page'>
    <div class='cover-decoration'>✨</div>
    <div class='cover-decoration'>🌟</div>
    <div class='cover-decoration'>⭐</div>
    <div class='cover-title'>{collection_title}</div>
    <div class='cover-dedication'>Starring {hero_details['name']}</div>
    <div class='cover-subtitle'>Magical Adventures Created Just for You</div>
    <div class='cover-subtitle' style='font-size: 14pt; margin-top: 20px; letter-spacing: 1px;'>By the World's Greatest Storytellers</div>
    <div class='cover-author'>Collected by Your AI Storyteller</div>
</div>

<!-- Dedication Page -->
<div class="dedication-page">
    <h2>For {hero_details['name']}</h2>
    <p>
        These stories were written just for you.<br/>
        Each one crafted by a master storyteller,<br/>
        Each one starring you as the hero.<br/>
        <br/>
        From Astrid Lindgren's warm embrace<br/>
        To Oscar Wilde's poetic grace,<br/>
        From Roald Dahl's delightful wit<br/>
        To Hans Andersen's timeless spirit.<br/>
        <br/>
        May these tales remind you always:<br/>
        You are brave, you are kind, you are special.<br/>
        <br/>
        With love and magic,<br/>
        Your AI Storyteller
    </p>
</div>

<div class='pagebreak'></div>

<!-- Foreword -->
<div class="content">
    <h1>A Special Message for {hero_details['name']}</h1>
    <div class="foreword">
        {foreword.replace('\n', '</p><p>')}
    </div>
</div>

<div class='pagebreak'></div>

<!-- Table of Contents -->
<div class="content">
    <h1>Your Adventures</h1>
    {toc_entries}
</div>

{fairytales_html}

<div class='pagebreak'></div>
<div class="content">
    <h1>Remember, {hero_details['name']}...</h1>
    <p>These stories were created especially for you, each one told by a legendary storyteller who wanted to share their magic with you.</p>
    <p>Just like in these fairytales, you have the power to be brave, kind, and make a difference in the world. Your love of {hero_details['interests']['favorite_activity']} and your {hero_details['interests']['personality']} spirit will take you on many real adventures.</p>
    <p>The storytellers in this book—Astrid Lindgren, Oscar Wilde, Roald Dahl, Hans Christian Andersen, and Beatrix Potter—have inspired millions of children around the world. Now their voices tell YOUR story.</p>
    <p>Whenever you read these tales, remember that you are the hero of your own life story too!</p>
    <div style="text-align: center; margin-top: 40px; font-size: 18pt; color: #667eea;">
        🌟 The Beginning of Your Adventures 🌟
    </div>
</div>
"""

# === Save files ===
print(f"\n📖 Saving {hero_details['name']}'s personalized fairytale collection...")

# Create personalized filename
safe_name = hero_details['name'].replace(' ', '_').lower()
txt_filename = f"{safe_name}_fairytales.txt"
pdf_filename = f"{safe_name}_fairytales.pdf"

# Save raw text version
with open(txt_filename, "w", encoding="utf-8") as f:
    f.write(f"{collection_title}\n")
    f.write("=" * len(collection_title) + "\n\n")
    f.write(f"Created especially for: {hero_details['name']}\n\n")
    f.write("FOREWORD:\n")
    f.write(foreword + "\n\n")
    f.write("FAIRYTALES:\n")
    f.write(all_fairytales_text)

# Save PDF with cover
save_pdf_with_cover(collection_title, html_body, "AI Storyteller", hero_details['name'], pdf_filename)

# Create a requirements.txt file
with open("requirements.txt", "w") as f:
    f.write("openai\n")
    f.write("requests\n")
    f.write("pdfkit\n")

print(f"✅ {hero_details['name']}'s magical fairytale collection is ready!")
print(f"📄 Text version saved as: {txt_filename}")
print(f"📚 Beautiful personalized PDF saved as: {pdf_filename}")
print(f"\n🎉 Created {len(fairytale_titles)} personalized fairytales starring {hero_details['name']}!")
print("\n📖 Story Details:")
for i, (title, storyteller) in enumerate(zip(fairytale_titles, storytellers_for_tales), 1):
    print(f"   {i}. {title} - In the style of {storyteller['name']}")
print(f"\n🎨 Added personalized illustrations for all {num_fairytales} stories!")
print(f"\nThese stories celebrate {hero_details['name']}'s unique personality and interests,")
print("each told by a legendary storyteller in their distinctive voice.")
print("\n📋 requirements.txt file created for easy setup")
print("\nHappy reading! 📖✨")