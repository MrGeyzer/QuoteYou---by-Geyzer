import base64
import io
import aiohttp
from playwright.async_api import async_playwright
from PIL import Image

from config import HTML_TEMPLATE, TELEGRAM_COLORS, COLOR_KEY_TO_ID

# Глобальний браузер
browser = None

async def startup_browser():
    global browser
    if browser is None:
        p = await async_playwright().start()
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])

async def shutdown_browser():
    global browser
    if browser:
        await browser.close()
        browser = None

async def download_avatar(bot, user_id=None, file_id=None):
    """Завантажує фото і конвертує в base64"""
    try:
        if file_id:
            file = await bot.get_file(file_id)
            file_path = file.file_path
            url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"
        elif user_id:
            photos = await bot.get_user_profile_photos(user_id, limit=1)
            if not photos.photos:
                return None
            file = await bot.get_file(photos.photos[0][-1].file_id)
            url = f"https://api.telegram.org/file/bot{bot.token}/{file.file_path}"
        else:
            return None

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    return base64.b64encode(data).decode('utf-8')
    except Exception as e:
        print(f"Error downloading avatar: {e}")
    return None

def get_soft_color(color_key_or_id):
    """Отримує м'який колір за ID або ключем"""
    if isinstance(color_key_or_id, str):
        idx = COLOR_KEY_TO_ID.get(color_key_or_id, 0)
    else:
        idx = abs(int(color_key_or_id)) % 7
    
    return TELEGRAM_COLORS.get(idx, TELEGRAM_COLORS[0])

def calculate_font_sizes(text_length, name_length=0):
    """Розраховує розмір шрифту залежно від довжини тексту та імені"""
    # Якщо і ім'я, і текст короткі - використовуємо великий шрифт
    if text_length < 10 and name_length < 10:
        return 42, 46  # Зменшено розмір імені з 48 до 32
    elif text_length < 20 and name_length < 20:
        return 36, 36  # Зменшено з 42 до 28 для імені
    elif text_length < 40:
        return 34, 34  # Зменшено з 38 до 26 для імені
    elif text_length < 80:
        return 32, 32  # Зменшено з 34 до 24 для імені
    elif text_length < 120:
        return 31, 31  # Зменшено з 30 до 22 для імені
    elif text_length < 180:
        return 29, 29  # Зменшено з 28 до 20 для імені
    else:
        return 27, 27  # Зменшено з 25 до 18 для імені

def calculate_bubble_width(text_length, name_length):
    """Розраховує оптимальну ширину бульбашки"""
    max_len = max(text_length, name_length)
    
    # Для дуже коротких - компактна бульбашка
    if max_len < 10:
        return 250
    elif max_len < 15:
        return 250
    elif max_len < 25:
        return 280
    elif max_len < 40:
        return 340
    elif max_len < 70:
        return 390
    elif max_len < 120:
        return 440
    else:
        return 480  # Максимум для дуже довгих текстів 

async def render_sticker(bot, chat_id, text, name, color_key, avatar_base64=None, content_image_base64=None, theme='dark'):
    global browser
    if not browser:
        await startup_browser()

    # --- ТЕМА ---
    if theme == 'light':
        bubble_bg = "#ffffff"
        text_color = "#000000"
    else:
        bubble_bg = "#212121"
        text_color = "#ffffff"

    # --- КОЛІР ---
    main_color = get_soft_color(color_key)
    
    # --- АВАТАРКА ---
    if avatar_base64:
        avatar_bg = f"url('data:image/jpeg;base64,{avatar_base64}')"
        avatar_text = ""
    else:
        avatar_bg = main_color
        avatar_text = name[0].upper() if name else "?"

    # Картинка всередині повідомлення
    content_image_block = ""
    if content_image_base64:
        content_image_block = f'<img src="data:image/jpeg;base64,{content_image_base64}" class="content-image" />'

    # Розрахунок розмірів з урахуванням імені
    name_size, text_size = calculate_font_sizes(len(text), len(name))
    bubble_max_width = calculate_bubble_width(len(text), len(name))

    # Підстановка в HTML
    html_content = HTML_TEMPLATE.format(
        avatar_bg=avatar_bg,
        fallback_color=main_color, 
        avatar_text=avatar_text,
        bubble_bg=bubble_bg,
        text_color=text_color,
        name_color=main_color,
        name_size=name_size,
        text_size=text_size,
        name=name,
        text=text,
        content_image_block=content_image_block,
        bubble_max_width=bubble_max_width
    )

    # device_scale_factor=3.0 для чіткості + збільшений viewport
    page = await browser.new_page(
        viewport={'width': 512, 'height': 2000}, 
        device_scale_factor=3.0
    )
    
    try:
        await page.set_content(html_content)
        # Чекаємо прогрузки шрифтів
        await page.evaluate("document.fonts.ready")
        
        # Невелика затримка для повного рендерингу
        await page.wait_for_timeout(100)
        
        element = await page.query_selector('.message-container')
        
        if element:
            # Робимо скріншот у пам'ять
            png_data = await element.screenshot(omit_background=True)
            
            # --- ОБРОБКА PIL (Pillow) для якості ---
            image = Image.open(io.BytesIO(png_data))
            
            # Зменшуємо до 512px по ширині з використанням якісного алгоритму LANCZOS
            w_percent = (512 / float(image.size[0]))
            h_size = int((float(image.size[1]) * float(w_percent)))
            image = image.resize((512, h_size), Image.Resampling.LANCZOS)
            
            # Зберігаємо у буфер як WebP (стандарт для стікерів)
            output = io.BytesIO()
            image.save(output, format="WEBP")
            output.seek(0)
            
            from aiogram.types import BufferedInputFile
            input_file = BufferedInputFile(output.read(), filename="sticker.webp")
            await bot.send_sticker(chat_id, sticker=input_file)
        else:
            await bot.send_message(chat_id, "Error rendering sticker (element not found)")
            
    except Exception as e:
        print(f"Render error: {e}")
        await bot.send_message(chat_id, "Render error occurred.")
    finally:
        await page.close()

def delete_message_safe(bot, chat_id, msg_id):
    import asyncio
    async def _delete():
        if not msg_id: return
        try:
            await bot.delete_message(chat_id, msg_id)
        except:
            pass
    return asyncio.create_task(_delete())