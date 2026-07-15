import html
import random
import streamlit as st

st.set_page_config(page_title="Apartment Morning Adventure", page_icon="🏡", layout="wide")

st.markdown(
    """
    <style>
    :root {
        --bg: #fffafc;
        --card: #ffffff;
        --accent: #f7b6c8;
        --accent-strong: #e88fb1;
        --text: #4d3a45;
        --muted: #7a6470;
    }

    .stApp {
        background: linear-gradient(135deg, #fffafc 0%, #fff2f7 100%);
        color: var(--text);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(90deg, #ffffff 0%, #ffe8f0 100%);
        border: 1px solid #f7dce6;
        border-radius: 20px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 10px 30px rgba(232, 143, 177, 0.16);
        margin-bottom: 1.2rem;
    }

    .card {
        background: var(--card);
        border: 1px solid #f4dce6;
        border-radius: 18px;
        padding: 1rem 1.2rem;
        box-shadow: 0 8px 20px rgba(248, 205, 221, 0.2);
        margin-bottom: 1rem;
    }

    .story-output-card {
        margin-bottom: 0.75rem;
    }

    .story-output-pane {
        height: 360px;
        max-height: 360px;
        min-height: 360px;
        overflow-y: auto;
        padding: 0.9rem 1rem;
        border: 1px solid #f4dce6;
        border-radius: 14px;
        background: #fffdfd;
        scrollbar-gutter: stable;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
        gap: 0.35rem;
    }

    .story-output-line {
        margin: 0;
        line-height: 1.45;
        white-space: pre-line;
        color: var(--text);
    }

    .pill {
        display: inline-block;
        background: #ffe8f0;
        color: #9b4f6b;
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        font-size: 0.9rem;
        margin: 0.2rem 0.25rem 0.2rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


ACTION_BREAK_MARKER = "__ACTION_BREAK__"
OUTFIT_REDO_ENTRY = "Great! Now that your outfit is chosen, you walk over to your desk and notice your backpack is a tiny disaster. You still have a little time before the day gets truly unhinged."


def init_game():
    st.session_state.health = 50
    st.session_state.temperature = random.randint(20, 81)
    st.session_state.story = [
        "The morning sun spills across your apartment, and your day is about to begin.",
        "A little sparkle of chaos is already waiting in the air.",
        ACTION_BREAK_MARKER,
    ]
    st.session_state.backpack = []
    st.session_state.stage = "intro"
    st.session_state.outfit_redo_shown = False
    st.session_state.temp_health = None
    st.session_state.recipe = None
    st.session_state.ingredients = []
    st.session_state.ingredient_source = None
    st.session_state.outfit_started = False
    st.session_state.repacked = False


if "health" not in st.session_state:
    init_game()


def add_story(text):
    st.session_state.story.append(text)


def add_action_break():
    if st.session_state.story and st.session_state.story[-1] != ACTION_BREAK_MARKER:
        st.session_state.story.append(ACTION_BREAK_MARKER)


def move_story_line_to_last(line):
    if line in st.session_state.story:
        st.session_state.story = [item for item in st.session_state.story if item != line]
        st.session_state.story.append(line)


def get_room_from_stage(stage):
    bedroom_stages = {
        "intro",
        "bed_choice",
        "bed_make",
        "closet_bottoms",
        "closet_tops",
        "closet_coat",
        "outfit_redo",
        "desk_choice",
        "hair_choice_2",
        "backpack_pack",
    }
    kitchen_stages = {"destination", "kitchen_intro", "kitchen_recipe", "kitchen_gather", "kitchen_pick"}
    if stage in bedroom_stages:
        return "bedroom"
    if stage in kitchen_stages:
        return "kitchen"
    if stage in {"living_room", "ending"}:
        return "living_room"
    return "other"


def transition_stage(next_stage, intro_text=None):
    current_room = get_room_from_stage(st.session_state.stage)
    next_room = get_room_from_stage(next_stage)

    if next_room != current_room:
        st.session_state.story = []
        if intro_text:
            st.session_state.story.append(intro_text)
    elif intro_text and not st.session_state.story:
        st.session_state.story.append(intro_text)

    st.session_state.stage = next_stage


def change_health(delta, text):
    st.session_state.health += delta
    add_story(text)
    if st.session_state.health <= 0:
        st.session_state.health = 0
        add_story("Your happiness hit zero. The apartment wins, darling. The morning implodes in a glittery little disaster.")
        st.session_state.stage = "game_over"


st.markdown(
    """
<div class="hero">
    <h1 style="margin-bottom:0.2rem; color:#b05077;">Apartment Morning Adventure</h1>
    <p style="margin-top:0.2rem; color:#7a6470;">A dreamy, slightly chaotic morning routine with sparkle, drama, and just enough nonsense to make it feel magical.</p>
</div>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([2, 1])

with left:
    story_lines = [line for line in st.session_state.story if line]
    story_segments = []
    for line in story_lines:
        if line == ACTION_BREAK_MARKER:
            story_segments.append("<div class='story-output-line' style='height:0.6rem'></div>")
        else:
            story_segments.append(f"<p class='story-output-line'>{html.escape(line).replace(chr(10), '<br>')}</p>")

    story_content = "".join(story_segments) or "<p class='story-output-line'>A little sparkle is waiting for you in the next room.</p>"

    st.markdown(
        f"""
        <div class='card story-output-card'>
            <h4 style='margin-top:0; color:#b05077;'>Output</h4>
            <div id='story-output-pane' class='story-output-pane'>
                {story_content}
            </div>
        </div>
        <script>
        const scrollOutputArea = () => {{
            const pane = document.getElementById('story-output-pane');
            if (pane) {{
                requestAnimationFrame(() => {{
                    pane.scrollTop = pane.scrollHeight;
                }});
                setTimeout(() => {{ pane.scrollTop = pane.scrollHeight; }}, 50);
            }}
        }};
        scrollOutputArea();
        window.addEventListener('load', scrollOutputArea);
        setTimeout(scrollOutputArea, 0);
        setTimeout(scrollOutputArea, 100);
        setTimeout(scrollOutputArea, 250);
        </script>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    if st.session_state.health <= 0 and st.session_state.stage != "game_over":
        st.session_state.stage = "game_over"

    if st.session_state.stage == "game_over":
        st.markdown("<div class='card'><h3 style='margin-top:0; color:#b05077;'>Game Over</h3><p>Oh, honey. Your happiness hit zero, and the morning went completely off the rails.</p><p>You should have treated yourself a little better. A little sparkle, a little self-care, and maybe one less dramatic choice next time.</p></div>", unsafe_allow_html=True)
        st.markdown("<div class='card'><p>Only one thing remains now: restart and try again with a little more grace and a lot more sparkle.</p></div>", unsafe_allow_html=True)
    elif st.session_state.stage == "intro":
        st.markdown(
            "<div class='card'><p>Complete each objective, keep your happiness sparkling, and leave your apartment before the chaos consumes your whole morning. The apartment is waiting, and it is very dramatic.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Start my chaotic morning", use_container_width=True):
            add_story("You wake up in your big, comfy bed, perfectly content with staying there all day.")
            add_story("Unfortunately, it is a school day and you have lots to do.")
            add_story("You really should get out of bed, but what do you want to do?")
            st.session_state.stage = "bed_choice"
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "bed_choice":
        st.markdown("<div class='card'><p>Options are <strong>Get up</strong> or <strong>Stay in bed</strong>.</p></div>", unsafe_allow_html=True)
        if st.button("Get up", use_container_width=True):
            add_story("Yay! Good morning! Time to start your day.")
            st.session_state.stage = "bed_make"
            add_action_break()
            st.rerun()
        if st.button("Stay in bed", use_container_width=True):
            change_health(-10, "How lazy of you. Your happiness decreases by 10.")
            st.session_state.stage = "bed_choice"
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "bed_make":
        st.markdown("<div class='card'><p>You turn around and look at your messy bed. Would you like to make it?</p></div>", unsafe_allow_html=True)
        if st.button("Yes, make the bed", use_container_width=True):
            change_health(10, "Now your bed looks so nice and pretty. Seeing this increases your happiness by 10.")
            st.session_state.temp_health = st.session_state.health
            st.session_state.outfit_started = True
            st.session_state.stage = "closet_bottoms"
            add_action_break()
            st.rerun()
        if st.button("No, leave it messy", use_container_width=True):
            change_health(-10, "How lazy of you. Your happiness decreases by 10 points.")
            st.session_state.temp_health = st.session_state.health
            st.session_state.outfit_started = True
            st.session_state.stage = "closet_bottoms"
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "closet_bottoms":
        st.markdown(
            f"<div class='card'><p>Today it will be {st.session_state.temperature} degrees outside, and your closet is somehow both stylish and chaotic. Choose your bottoms.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Sweatpants", use_container_width=True):
            if st.session_state.temperature < 60:
                change_health(5, "Good choice! You will be nice and warm. Happiness increases by 5.")
            else:
                change_health(-15, "Bad choice, you will be too warm. Happiness decreases by 15.")
            st.session_state.stage = "closet_tops"
            add_action_break()
            st.rerun()
        if st.button("Leggings", use_container_width=True):
            if st.session_state.temperature < 60:
                change_health(5, "Good choice! You will be nice and warm. Happiness increases by 5.")
            else:
                change_health(-15, "Bad choice, you will be too warm. Happiness decreases by 15.")
            st.session_state.stage = "closet_tops"
            add_action_break()
            st.rerun()
        if st.button("Shorts", use_container_width=True):
            if st.session_state.temperature < 60:
                change_health(-15, "Bad choice, you will freeze. Happiness decreases by 15.")
            else:
                change_health(5, "Good choice! You will be nice and comfortable. Happiness increases by 5.")
            st.session_state.stage = "closet_tops"
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "closet_tops":
        st.markdown("<div class='card'><p>Now pick your top. The outfit gods are watching.</p></div>", unsafe_allow_html=True)
        if st.button("Sweatshirt", use_container_width=True):
            if st.session_state.temperature < 60:
                change_health(5, "Good choice! You will be nice and warm. Happiness increases by 5.")
            else:
                change_health(-15, "Bad choice, you will be too warm. Happiness decreases by 15.")
            st.session_state.stage = "closet_coat"
            add_action_break()
            st.rerun()
        if st.button("Long sleeve", use_container_width=True):
            if st.session_state.temperature < 60:
                change_health(5, "Good choice! You will be nice and warm. Happiness increases by 5.")
            else:
                change_health(-15, "Bad choice, you will be too warm. Happiness decreases by 15.")
            st.session_state.stage = "closet_coat"
            add_action_break()
            st.rerun()
        if st.button("T-shirt", use_container_width=True):
            if st.session_state.temperature < 60:
                change_health(-15, "Bad choice, you will freeze. Happiness decreases by 15.")
            else:
                change_health(5, "Good choice! You will be nice and comfortable. Happiness increases by 5.")
            st.session_state.stage = "closet_coat"
            add_action_break()
            st.rerun()
        if st.button("Tank top", use_container_width=True):
            if st.session_state.temperature < 60:
                change_health(-15, "Bad choice, you will freeze. Happiness decreases by 15.")
            else:
                change_health(5, "Good choice! You will be nice and comfortable. Happiness increases by 5.")
            st.session_state.stage = "closet_coat"
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "closet_coat":
        st.markdown("<div class='card'><p>Since the temperature is dramatic, would you like to wear a coat?</p></div>", unsafe_allow_html=True)
        if st.button("Yes, wear a coat", use_container_width=True):
            if st.session_state.temperature < 35:
                change_health(5, "Good choice, you would have been cold without it. Happiness increases by 5.")
            else:
                change_health(-15, "Bad choice, you will be way too warm. Happiness decreases by 15.")
            st.session_state.stage = "outfit_redo"
            add_action_break()
            st.rerun()
        if st.button("No, skip the coat", use_container_width=True):
            if st.session_state.temperature < 35:
                change_health(-15, "Bad choice, you will freeze. Happiness decreases by 15.")
            else:
                change_health(5, "Good choice, you didn't need one anyway. Happiness increases by 5.")
            st.session_state.stage = "outfit_redo"
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "outfit_redo":
        if not st.session_state.outfit_redo_shown:
            add_story("Great! Now that your outfit is chosen, you walk over to your desk and notice your backpack is a tiny disaster. You still have a little time before the day gets truly unhinged.")
            st.session_state.outfit_redo_shown = True
        st.markdown(
            f"<div class='card'><p>Keeping in mind that your happiness could drop to zero, would you like to redo your outfit? If you do, your happiness will reset to {st.session_state.temp_health - 15} for the sake of extra laundry and extra chaos.</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Yes, redo my outfit", use_container_width=True):
            st.session_state.health = st.session_state.temp_health - 15
            add_story("You decide to redo your outfit, which feels very dramatic and mildly chaotic.")
            st.session_state.stage = "closet_bottoms"
            add_action_break()
            st.rerun()
        if st.button("No, this outfit is fabulous", use_container_width=True):
            add_story("You decide to leave your outfit exactly as it is. The sparkle is enough.")
            if OUTFIT_REDO_ENTRY in st.session_state.story:
                st.session_state.story = [item for item in st.session_state.story if item != OUTFIT_REDO_ENTRY]
            st.session_state.story.append(OUTFIT_REDO_ENTRY)
            st.session_state.stage = "desk_choice"
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "desk_choice":
        st.markdown(
            "<div class='card'><p>Your computer sits on the desk, your water bottle is nearby, and your backpack is slumped against the chair like it has given up. What would you like to do?</p></div>",
            unsafe_allow_html=True,
        )
        if st.button("Makeup", use_container_width=True):
            change_health(10, "You put on a little mascara and lip gloss. You feel pretty and your happiness increases by 10.")
            st.session_state.stage = "backpack_pack"
            add_action_break()
            st.rerun()
        if st.button("Hair", use_container_width=True):
            st.session_state.stage = "hair_choice_2"
            add_action_break()
            st.rerun()
        if st.button("Both", use_container_width=True):
            change_health(10, "You give yourself a little makeup moment and a little hair moment. The sparkle level is now dangerously high.")
            st.session_state.stage = "backpack_pack"
            add_action_break()
            st.rerun()
        if st.button("Neither", use_container_width=True):
            add_story("You decide to leave the desk as is and move on. The morning is already doing enough.")
            st.session_state.stage = "backpack_pack"
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "hair_choice_2":
        st.markdown("<div class='card'><p>How would you like to style your hair?</p></div>", unsafe_allow_html=True)
        if st.button("Leave down", use_container_width=True):
            change_health(10, "Your hair looks so pretty down. Happiness increases by 10.")
            st.session_state.stage = "backpack_pack"
            add_action_break()
            st.rerun()
        if st.button("Claw clip", use_container_width=True):
            change_health(10, "Somehow it looks good on the first try. Happiness increases by 10.")
            st.session_state.stage = "backpack_pack"
            add_action_break()
            st.rerun()
        if st.button("Ponytail", use_container_width=True):
            change_health(10, "Somehow your ponytail looks good on the first try. Happiness increases by 10.")
            st.session_state.stage = "backpack_pack"
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "backpack_pack":
        st.markdown(
            "<div class='card'><p>You realize you have to repack your backpack. Some of the items on your desk include Computer, Lipgloss, Computer charger, Phone charger, Perfume, Airpods, Waterbottle, and Clawclip. What would you like to pack?</p></div>",
            unsafe_allow_html=True,
        )
        options = [
            ("Computer", 10),
            ("Computer charger", 10),
            ("Waterbottle", 10),
            ("Phone charger", 5),
            ("Airpods", 5),
            ("Lipgloss", 0),
            ("Perfume", 0),
            ("Clawclip", 0),
        ]
        for item, gain in options:
            if st.button(item, use_container_width=True):
                if item not in st.session_state.backpack:
                    st.session_state.backpack.append(item)
                    if gain > 0:
                        change_health(gain, f"Good job, you packed {item}. Happiness increases by {gain}.")
                    else:
                        add_story(f"You packed {item}. The backpack is now slightly more chaotic and slightly more fabulous.")
                else:
                    add_story(f"You already packed {item}. The chaos is becoming repetitive.")
                add_action_break()
                st.rerun()
        if st.button("Done packing", use_container_width=True):
            add_story("You step back and admire your very overpacked backpack. It is a masterpiece of organization and panic.")
            st.session_state.stage = "destination"
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "destination":
        st.markdown("<div class='card'><p>You exit your bedroom and walk into the hall. You can choose to head into the kitchen or the living room before you leave the apartment.</p></div>", unsafe_allow_html=True)
        if st.button("Kitchen", use_container_width=True):
            transition_stage("kitchen_intro", "You step into the kitchen and the smell of breakfast drifts through the air.")
            add_action_break()
            st.rerun()
        if st.button("Living Room", use_container_width=True):
            transition_stage("living_room", "You step into the living room and the day feels a little more real.")
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "kitchen_intro":
        st.markdown("<div class='card'><p>You walk into your kitchen and realize how hungry you are. Would you like to make breakfast?</p></div>", unsafe_allow_html=True)
        if st.button("Yes, make breakfast", use_container_width=True):
            transition_stage("kitchen_recipe")
            add_action_break()
            st.rerun()
        if st.button("No, skip breakfast", use_container_width=True):
            change_health(-20, "Breakfast is really good for you. You should not skip it. Happiness decreases by 20.")
            transition_stage("living_room", "You leave the kitchen behind and drift into the living room.")
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "kitchen_recipe":
        st.markdown("<div class='card'><p>Choose a breakfast recipe. The kitchen is glowing with suspiciously hopeful energy.</p></div>", unsafe_allow_html=True)
        if st.button("Scrambled eggs", use_container_width=True):
            st.session_state.recipe = "Scrambled eggs"
            st.session_state.ingredients = []
            st.session_state.stage = "kitchen_gather"
            add_action_break()
            st.rerun()
        if st.button("Pancakes", use_container_width=True):
            st.session_state.recipe = "Pancakes"
            st.session_state.ingredients = []
            st.session_state.stage = "kitchen_gather"
            add_action_break()
            st.rerun()
        if st.button("Oatmeal", use_container_width=True):
            st.session_state.recipe = "Oatmeal"
            st.session_state.ingredients = []
            st.session_state.stage = "kitchen_gather"
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "kitchen_gather":
        st.markdown(f"<div class='card'><p>Your recipe is <strong>{st.session_state.recipe}</strong>. Gather the ingredients from the fridge or pantry.</p></div>", unsafe_allow_html=True)
        if st.button("Go to the fridge", use_container_width=True):
            st.session_state.ingredient_source = "fridge"
            st.session_state.stage = "kitchen_pick"
            add_action_break()
            st.rerun()
        if st.button("Go to the pantry", use_container_width=True):
            st.session_state.ingredient_source = "pantry"
            st.session_state.stage = "kitchen_pick"
            add_action_break()
            st.rerun()
        if st.button("Done gathering ingredients", use_container_width=True):
            if len(st.session_state.ingredients) >= 2:
                add_story("You have everything you need and the breakfast comes together beautifully.")
                change_health(20, "Yay! You eat your delicious breakfast. Happiness increases by 20.")
                st.session_state.stage = "living_room"
                add_action_break()
                st.rerun()
            else:
                add_story("You still need a few more ingredients before you can cook.")
                add_action_break()
                st.rerun()

    elif st.session_state.stage == "kitchen_pick":
        if st.session_state.recipe == "Scrambled eggs":
            options = ["Eggs", "Butter", "Milk", "Water"]
        elif st.session_state.recipe == "Pancakes":
            options = ["Water", "Butter", "Pancake mix"]
        else:
            options = ["Milk", "Water", "Oatmeal pack"]

        st.markdown(f"<div class='card'><p>Pick ingredients from the {st.session_state.ingredient_source}.</p></div>", unsafe_allow_html=True)
        for item in options:
            if st.button(item, use_container_width=True):
                if item not in st.session_state.ingredients:
                    st.session_state.ingredients.append(item)
                    add_story(f"You gathered {item} for your breakfast.")
                else:
                    add_story(f"You already grabbed {item}. The kitchen has a little too much drama today.")
                add_action_break()
                st.rerun()
        if st.button("Back to kitchen menu", use_container_width=True):
            st.session_state.stage = "kitchen_gather"
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "living_room":
        st.markdown("<div class='card'><p>You walk into the living room and notice that you forgot to take your iPad and book back to your room last night. Oops. Would you like to put them in your backpack?</p></div>", unsafe_allow_html=True)
        if st.button("Yes, put them in my backpack", use_container_width=True):
            if "Ipad" not in st.session_state.backpack:
                st.session_state.backpack.append("Ipad")
            if "Book" not in st.session_state.backpack:
                st.session_state.backpack.append("Book")
            add_story("Perfect! Your backpack now feels a little more prepared for the day.")
            transition_stage("ending", "You gather your things and head out, feeling a little more ready for the day.")
            add_action_break()
            st.rerun()
        if st.button("No, leave them behind", use_container_width=True):
            add_story("Okay. You leave the items behind and head out, slightly more chaotic than before.")
            transition_stage("ending", "You leave the items behind and head out, slightly more chaotic than before.")
            add_action_break()
            st.rerun()

    elif st.session_state.stage == "ending":
        st.session_state.previous_stage = st.session_state.stage
        st.markdown(
            "<div class='card'><p>Now that you are completely ready to take on the day, you run out the door, almost forgetting your car keys on the way out. The morning was chaotic, sparkly, and somehow still charming.</p></div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<div class='card'><p>Thanks for playing! Your happiness ended at <strong>{st.session_state.health}</strong>.</p></div>",
            unsafe_allow_html=True,
        )
        if st.session_state.health > 100:
            st.markdown("<div class='card'><p>You did amazing! Have the best day.</p></div>", unsafe_allow_html=True)
        elif st.session_state.health >= 50:
            st.markdown("<div class='card'><p>You did good! Have a great day.</p></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='card'><p>You did okay. Maybe do more things that make you happy tomorrow.</p></div>", unsafe_allow_html=True)


with right:
    st.markdown("<div class='card'><h4 style='margin-top:0; color:#b05077;'>Status</h4><p><strong>Happiness:</strong> {}</p><div style='background:#f7dce6;border-radius:999px;overflow:hidden;height:12px;'><div style='width:{}%;background:linear-gradient(90deg,#f7b6c8,#e88fb1);height:100%;'></div></div></div>".format(st.session_state.health, min(max(st.session_state.health, 0), 100)), unsafe_allow_html=True)
    st.markdown(f"<div class='card'><h4 style='margin-top:0; color:#b05077;'>Outside Temp</h4><p>{st.session_state.temperature}°</p></div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='card'><h4 style='margin-top:0; color:#b05077;'>Backpack</h4><div style='margin-top:0.4rem;'>"
        + ("".join(f"<span class='pill'>{item}</span>" for item in st.session_state.backpack) if st.session_state.backpack else "<p>Your backpack is still empty.</p>")
        + "</div></div>",
        unsafe_allow_html=True,
    )

    if st.button("Start over", use_container_width=True):
        init_game()
        add_action_break()
        st.rerun()
