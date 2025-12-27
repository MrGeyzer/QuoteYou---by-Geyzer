import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    BOT_TOKEN = "" 

# --- Кольори імен ---
# https://imagecolorpicker.com/uk
TELEGRAM_COLORS = {
    0: "#f17055", # Red 
    1: "#fcae53", # Orange
    2: "#a88bf4", # Purple 
    3: "#83cb5b", # Green
    4: "#4cb8dd", # Blue 
    5: "#55a6f0", # Blue (Standard)
    6: "#f3799a"  # Pink
}

# Мапінг для меню
COLOR_KEY_TO_ID = {
    "red": 0, "orange": 1, "purple": 2, "green": 3, 
    "cyan": 4, "blue": 5, "pink": 6, "gold": 1
}

LANGUAGES = {
    'ua': "🇺🇦 Українська",
    'en': "🇺🇸 English"
}

# --- HTML ШАБЛОН ---
# Виправлено padding-bottom для правильного розташування часу
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Noto+Color+Emoji&display=swap" rel="stylesheet">

<style>
    body {{
        width: 512px;
        background-color: transparent;
        margin: 0; padding: 0;
        display: flex;
        flex-direction: column;
        font-family: 'Roboto', 'Noto Color Emoji', sans-serif;
    }}
    .message-container {{
        display: flex;
        flex-direction: row;
        align-items: flex-end;
        padding: 10px 10px 60px 15px;
        box-sizing: border-box;
        width: 100%;
        min-height: 150px;
    }}
    .avatar {{
        width: 100px; 
        height: 100px;
        border-radius: 50%;
        margin-right: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 48px; 
        font-weight: 700;
        font-family: 'Roboto', sans-serif;
        text-transform: uppercase;
        
        background: {avatar_bg}; 
        background-color: {fallback_color};
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        
        flex-shrink: 0;
        margin-bottom: 5px; 
        box-shadow: 0 4px 8px rgba(0,0,0,0.25);
    }}
    .bubble {{
        background-color: {bubble_bg};
        color: {text_color};
        padding: 22px 28px 28px 28px;
        border-radius: 35px 35px 35px 10px;
        position: relative;
        max-width: {bubble_max_width}px; 
        min-width: 140px;
        width: auto;
        box-shadow: 0 1px 2px rgba(0,0,0,0.15), 0 4px 12px rgba(0,0,0,0.1); 
        border: 1px solid rgba(128, 128, 128, 0.15);
        display: table;
    }}
    .name {{
        color: {name_color};
        font-weight: 700;
        font-size: {name_size}px; 
        line-height: 1.2;
        margin-bottom: 8px;
        display: block;
        width: 100%;
        font-family: 'Roboto', 'Noto Color Emoji', sans-serif;
    }}
    .content-image {{
        display: block;
        max-width: 100%;
        border-radius: 15px;
        margin-bottom: 12px;
        margin-top: 5px;
    }}
    .text {{
        color: {text_color} !important; 
        font-weight: 400;
        font-size: {text_size}px; 
        line-height: 1.4;
        word-wrap: break-word;
        word-break: break-word;
        white-space: pre-wrap;
        margin: 0;
        font-family: 'Roboto', 'Noto Color Emoji', sans-serif;
        hyphens: auto;
        display: block;
        width: 100%;
    }}
</style>
</head>
<body>
    <div class="message-container">
        <div class="avatar">{avatar_text}</div>
        <div class="bubble">
            <span class="name">{name}</span>
            {content_image_block}
            <div class="text">{text}</div>
        </div>
    </div>
</body>
</html>
"""