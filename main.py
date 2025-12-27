import asyncio
import logging
import os
import random
from aiohttp import web
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
)
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest

from config import BOT_TOKEN, LANGUAGES, COLOR_KEY_TO_ID
from texts import MESSAGES
from utils import download_avatar, render_sticker, delete_message_safe, startup_browser, shutdown_browser

class QuoteState(StatesGroup):
    waiting_for_initial_text = State()
    menu_processing = State()
    editing_text = State()
    editing_name = State()
    editing_avatar = State()
    editing_color = State()
    
    last_bot_msg_id = State() 
    lang = State()
    pref_theme = State() 
    pref_default_color = State()
    is_custom_avatar = State() 
    content_image = State() 
    quote_text = State()
    quote_name = State()
    quote_color_key = State()
    avatar_base64 = State()
    original_uid = State()

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
router = Router()
dp.include_router(router)

async def health_check(request): return web.Response(text="OK")
async def start_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

def get_text(lang_code, key):
    lang_code = lang_code if lang_code in MESSAGES else 'ua'
    return MESSAGES.get(lang_code, MESSAGES['ua']).get(key, "Text Error")

def get_color_name(lang_code, color_key, short=False):
    if isinstance(color_key, int):
        return get_text(lang_code, 'btn_auto_color') 
    names = get_text(lang_code, 'color_names')
    full_name = names.get(str(color_key), str(color_key))
    if short: return full_name.split(' ')[0]
    return full_name

def get_main_keyboard(lang_code):
    t = lambda k: get_text(lang_code, k)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t('btn_create'), callback_data="make_quote")],
        [InlineKeyboardButton(text=t('btn_edit_name'), callback_data="edit_name"),
         InlineKeyboardButton(text=t('btn_edit_text'), callback_data="edit_text")],
        [InlineKeyboardButton(text=t('btn_edit_avatar'), callback_data="edit_avatar"),
         InlineKeyboardButton(text=t('btn_edit_color'), callback_data="edit_color")],
        [InlineKeyboardButton(text=t('btn_cancel_all'), callback_data="cancel_inline")]
    ])

def get_settings_keyboard(lang_code):
    t = lambda k: get_text(lang_code, k)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=t('btn_settings_lang'), callback_data="open_lang_menu")],
        [InlineKeyboardButton(text=t('btn_settings_theme'), callback_data="open_theme_menu")],
        [InlineKeyboardButton(text=t('btn_settings_help'), callback_data="open_help_from_settings"),
         InlineKeyboardButton(text=t('btn_settings_info'), callback_data="open_info_from_settings")],
        [InlineKeyboardButton(text=t('btn_close'), callback_data="delete_msg")]
    ])

def get_theme_keyboard(lang_code, is_quick_menu=False):
    t = lambda k: get_text(lang_code, k)
    buttons = [[InlineKeyboardButton(text=t('theme_dark'), callback_data="set_theme_dark"),
                InlineKeyboardButton(text=t('theme_light'), callback_data="set_theme_light")]]
    if is_quick_menu:
        buttons.append([InlineKeyboardButton(text=t('btn_close'), callback_data="delete_msg")])
    else:
        buttons.append([InlineKeyboardButton(text=t('btn_back'), callback_data="back_to_settings")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_lang_keyboard(current_lang, from_settings=False):
    buttons = []
    for code, label in LANGUAGES.items():
        buttons.append([InlineKeyboardButton(text=label, callback_data=f"set_lang_{code}_{str(from_settings).lower()}")])
    if from_settings:
        buttons.append([InlineKeyboardButton(text=get_text(current_lang, 'btn_back'), callback_data="back_to_settings")])
    else:
        buttons.append([InlineKeyboardButton(text=get_text(current_lang, 'btn_close'), callback_data="delete_msg")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_start_lang_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇦 Українська", callback_data="start_lang_ua")],
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="start_lang_en")]
    ])

def get_inline_cancel_keyboard(lang_code):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=get_text(lang_code, 'btn_cancel_action'), callback_data="cancel_edit")]])

def get_color_inline_keyboard(lang_code):
    names = get_text(lang_code, 'color_names')
    buttons = []
    buttons.append([InlineKeyboardButton(text=get_text(lang_code, 'btn_auto_color'), callback_data="set_color_auto")])
    row = []
    for key in COLOR_KEY_TO_ID.keys():
        if key == 'gold': continue
        label = names.get(key, key)
        row.append(InlineKeyboardButton(text=label, callback_data=f"set_color_{key}"))
        if len(row) == 2:
            buttons.append(row); row = []
    if row: buttons.append(row)
    buttons.append([InlineKeyboardButton(text="⬅️", callback_data="back_to_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_close_keyboard(lang_code):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=get_text(lang_code, 'btn_close'), callback_data="delete_msg")]])

def get_back_keyboard(lang_code):
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=get_text(lang_code, 'btn_back'), callback_data="back_to_settings")]])

@router.message(Command("theme", "t"))
async def cmd_theme_quick(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    await message.answer(get_text(lang, 'theme_select_header'), reply_markup=get_theme_keyboard(lang, is_quick_menu=True))

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    data = await state.get_data()
    theme = data.get('pref_theme', 'dark')
    def_color = data.get('pref_default_color', None)
    await state.clear()
    await state.update_data(pref_theme=theme, pref_default_color=def_color)
    await delete_message_safe(bot, message.chat.id, message.message_id)
    await message.answer("👋 <b>Welcome! / Привіт!</b>\n\n🇺🇦 Будь ласка, обери мову:", reply_markup=get_start_lang_keyboard())

@router.message(Command("cancel", "c"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Команда скасування створення цитати з будь-якого стану"""
    current_state = await state.get_state()
    
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    
    # Якщо користувач не в процесі створення цитати
    if current_state is None:
        msg = await message.answer(get_text(lang, 'error_nothing_to_cancel'))
        await asyncio.sleep(2)
        await delete_message_safe(bot, message.chat.id, msg.message_id)
        return
    
    theme = data.get('pref_theme', 'dark')
    def_color = data.get('pref_default_color', None)
    
    # Видаляємо останнє повідомлення бота (інлайн меню)
    last_msg_id = data.get('last_bot_msg_id')
    if last_msg_id:
        await delete_message_safe(bot, message.chat.id, last_msg_id)
    
    # Очищаємо стан, зберігаючи налаштування
    await state.clear()
    await state.update_data(lang=lang, pref_theme=theme, pref_default_color=def_color)
    
    # Показуємо повідомлення про скасування
    msg = await message.answer(get_text(lang, 'msg_quote_canceled'))
    await asyncio.sleep(2)
    await delete_message_safe(bot, message.chat.id, msg.message_id)

@router.callback_query(F.data.startswith("start_lang_"))
async def cb_start_lang(callback: CallbackQuery, state: FSMContext):
    lang_code = callback.data.split("_")[-1]
    await state.update_data(lang=lang_code)
    await callback.answer(get_text(lang_code, 'toast_lang_changed'), show_alert=False)
    await callback.message.answer(get_text(lang_code, 'welcome'))
    await callback.message.delete()

@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    await message.answer(get_text(lang, 'help'), reply_markup=get_close_keyboard(lang))

@router.message(Command("info", "i"))
async def cmd_info(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    text = get_text(lang, 'info')
    photo_url = get_text(lang, 'info_photo_url')
    if photo_url:
        try: await message.answer_photo(photo_url, caption=text, reply_markup=get_close_keyboard(lang))
        except: await message.answer(text, reply_markup=get_close_keyboard(lang))
    else: await message.answer(text, reply_markup=get_close_keyboard(lang))

@router.message(Command("settings", "s"))
async def cmd_settings(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    msg = await message.answer(get_text(lang, 'settings_header'), reply_markup=get_settings_keyboard(lang))
    await state.update_data(last_bot_msg_id=msg.message_id)

@router.message(Command("lang", "l"))
async def cmd_lang_direct(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    text = get_text(lang, 'lang_select_header').format(lang=LANGUAGES.get(lang, lang))
    msg = await message.answer(text, reply_markup=get_lang_keyboard(lang, from_settings=False))
    await state.update_data(last_bot_msg_id=msg.message_id)

@router.callback_query(F.data == "back_to_settings")
async def cb_back_settings(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    try: await callback.message.edit_text(get_text(lang, 'settings_header'), reply_markup=get_settings_keyboard(lang))
    except:
        await callback.message.delete()
        msg = await callback.message.answer(get_text(lang, 'settings_header'), reply_markup=get_settings_keyboard(lang))
        await state.update_data(last_bot_msg_id=msg.message_id)

@router.callback_query(F.data == "open_lang_menu")
async def cb_open_lang(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    text = get_text(lang, 'lang_select_header').format(lang=LANGUAGES.get(lang, lang))
    await callback.message.edit_text(text, reply_markup=get_lang_keyboard(lang, from_settings=True))

@router.callback_query(F.data == "open_help_from_settings")
async def cb_open_help(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    await callback.message.edit_text(get_text(lang, 'help'), reply_markup=get_back_keyboard(lang))

@router.callback_query(F.data == "open_info_from_settings")
async def cb_open_info(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    text = get_text(lang, 'info')
    photo_url = get_text(lang, 'info_photo_url')
    await callback.message.delete()
    kb = get_back_keyboard(lang)
    if photo_url:
        try: msg = await callback.message.answer_photo(photo_url, caption=text, reply_markup=kb)
        except: msg = await callback.message.answer(text, reply_markup=kb)
    else: msg = await callback.message.answer(text, reply_markup=kb)
    await state.update_data(last_bot_msg_id=msg.message_id)

@router.callback_query(F.data.startswith("set_lang_"))
async def cb_set_lang(callback: CallbackQuery, state: FSMContext):
    parts = callback.data.split("_")
    new_lang = parts[2]
    from_settings = parts[3] == "true"
    await state.update_data(lang=new_lang)
    await callback.answer(get_text(new_lang, 'toast_lang_changed'), show_alert=False)
    if from_settings: await cb_back_settings(callback, state)
    else:
        text = get_text(new_lang, 'lang_select_header').format(lang=LANGUAGES.get(new_lang, new_lang))
        await callback.message.edit_text(text, reply_markup=get_lang_keyboard(new_lang, from_settings=False))

@router.callback_query(F.data == "open_theme_menu")
async def cb_open_theme(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    await callback.message.edit_text(get_text(lang, 'theme_select_header'), reply_markup=get_theme_keyboard(lang))

@router.callback_query(F.data.startswith("set_theme_"))
async def cb_set_theme(callback: CallbackQuery, state: FSMContext):
    theme = callback.data.split("_")[-1]
    await state.update_data(pref_theme=theme)
    lang = (await state.get_data()).get('lang', 'ua')
    await callback.answer(get_text(lang, 'toast_theme_changed'), show_alert=False)
    is_quick = True
    if callback.message.reply_markup:
        for row in callback.message.reply_markup.inline_keyboard:
            for btn in row:
                if btn.callback_data == "back_to_settings": is_quick = False; break
    if is_quick:
        await callback.message.delete()
    else: await cb_back_settings(callback, state)

@router.callback_query(F.data == "delete_msg")
async def cb_delete_msg(callback: CallbackQuery): await callback.message.delete()

@router.message(Command("q", "create"))
async def cmd_create_demo(message: Message, state: FSMContext):
    await bot.send_chat_action(message.chat.id, action="typing")
    
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    theme = data.get('pref_theme', 'dark')
    demo_color = random.choice(list(COLOR_KEY_TO_ID.keys()))
    demo_text = get_text(lang, 'demo_text')
    demo_name = message.from_user.full_name
    avatar_base64 = await download_avatar(bot, user_id=message.from_user.id)
    await state.update_data(
        quote_text=demo_text, quote_name=demo_name, quote_color_key=demo_color, 
        avatar_base64=avatar_base64, is_custom_avatar=False, content_image=None, 
        pref_theme=theme, last_bot_msg_id=None,
        original_uid=message.from_user.id 
    )
    await show_menu(message, state, is_new=True)

@router.message(F.forward_date | F.text | F.photo | F.caption, StateFilter(None))
async def handle_content(message: Message, state: FSMContext):
    if message.text and message.text.startswith("/"): return
    
    await bot.send_chat_action(message.chat.id, action="typing")
    
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    theme = data.get('pref_theme', 'dark')
    def_color = data.get('pref_default_color', None)
    text = message.text or message.caption or ""
    content_img = None
    if message.photo:
        file_id = message.photo[-1].file_id
        content_img = await download_avatar(bot, file_id=file_id) 
    if not text and not content_img:
        msg = await message.answer(get_text(lang, 'error_no_text'))
        await asyncio.sleep(2)
        await delete_message_safe(bot, message.chat.id, msg.message_id)
        return
    name = "Unknown"; uid_color = 0; uid_ava = 0
    if message.forward_from:
        name = message.forward_from.full_name; uid_color = message.forward_from.id; uid_ava = message.forward_from.id
    elif message.forward_sender_name:
        name = message.forward_sender_name; uid_color = sum(ord(c) for c in name)
    elif message.forward_from_chat:
        name = message.forward_from_chat.title; uid_color = message.forward_from_chat.id; uid_ava = message.forward_from_chat.id
    else:
        name = message.from_user.full_name; uid_color = message.from_user.id; uid_ava = message.from_user.id
    
    final_color_key = def_color if def_color else uid_color
    await state.update_data(
        quote_text=text, quote_name=name, quote_color_key=final_color_key, 
        avatar_base64=await download_avatar(bot, user_id=uid_ava), content_image=content_img, 
        is_custom_avatar=False, lang=lang, pref_theme=theme, pref_default_color=def_color,
        original_uid=uid_color 
    )
    await show_menu(message, state, is_new=True)

async def show_menu(message: Message, state: FSMContext, is_new=False):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    theme = data.get('pref_theme', 'dark')
    text_preview = data.get('quote_text', '')[:50] + "..." if len(data.get('quote_text', '')) > 50 else data.get('quote_text', '')
    
    if isinstance(data['quote_color_key'], int):
        color_display = get_text(lang, 'btn_auto_color')
    else:
        color_display = get_text(lang, 'color_names').get(data['quote_color_key'], data['quote_color_key'])
        
    lang_flag = LANGUAGES.get(lang, lang).split()[0]
    ava_line = ""
    if data.get('is_custom_avatar'): ava_line = f"🖼 <b>{get_text(lang, 'lbl_avatar')}</b>: {get_text(lang, 'ava_custom')}\n"
    if data.get('content_image'): text_preview = f"{get_text(lang, 'tag_photo')} {text_preview}"
    theme_label = get_text(lang, f'theme_{theme}_short')
    info_text = get_text(lang, 'menu_header').format(curr_lang=lang_flag, theme=theme_label, text=text_preview, name=data['quote_name'], color=color_display, avatar_line=ava_line)
    kb = get_main_keyboard(lang)
    
    if is_new:
        msg = await message.answer(info_text, reply_markup=kb)
        await state.update_data(last_bot_msg_id=msg.message_id)
    else:
        last_msg_id = data.get('last_bot_msg_id')
        if last_msg_id:
            try: await bot.edit_message_text(text=info_text, chat_id=message.chat.id, message_id=last_msg_id, reply_markup=kb)
            except TelegramBadRequest: pass
        else:
            msg = await message.answer(info_text, reply_markup=kb)
            await state.update_data(last_bot_msg_id=msg.message_id)
    await state.set_state(QuoteState.menu_processing)

@router.callback_query(F.data == "make_quote", QuoteState.menu_processing)
async def cb_make(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    theme = data.get('pref_theme', 'dark')
    await callback.answer(get_text(lang, 'toast_generating'), show_alert=False)
    
    await bot.send_chat_action(callback.message.chat.id, action="choose_sticker")
    
    await callback.message.delete()
    await render_sticker(
        bot, callback.message.chat.id,
        data.get('quote_text', ''), data['quote_name'], 
        data['quote_color_key'], data.get('avatar_base64'),
        data.get('content_image'),
        theme
    )
    saved_def_color = data.get('pref_default_color')
    await state.clear()
    await state.update_data(lang=lang, pref_theme=theme, pref_default_color=saved_def_color)

@router.callback_query(F.data == "cancel_inline")
async def cb_cancel_all(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    saved_def_color = data.get('pref_default_color')
    theme = data.get('pref_theme', 'dark')
    await state.clear()
    await state.update_data(lang=lang, pref_theme=theme, pref_default_color=saved_def_color)
    await callback.message.delete()
    await callback.answer(get_text(lang, 'toast_canceled'), show_alert=False)

@router.callback_query(F.data == "back_to_menu")
async def cb_back_to_menu(callback: CallbackQuery, state: FSMContext): await show_menu(callback.message, state, is_new=False)

async def start_editing(callback: CallbackQuery, state: FSMContext, next_state, prompt_key):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    kb = get_color_inline_keyboard(lang) if next_state == QuoteState.editing_color else get_inline_cancel_keyboard(lang)
    try: await callback.message.edit_text(get_text(lang, prompt_key), reply_markup=kb)
    except TelegramBadRequest:
        await callback.message.delete()
        msg = await callback.message.answer(get_text(lang, prompt_key), reply_markup=kb)
        await state.update_data(last_bot_msg_id=msg.message_id)
    await state.set_state(next_state)

@router.callback_query(F.data == "edit_name")
async def cb_edit_name(cb: CallbackQuery, state: FSMContext): await start_editing(cb, state, QuoteState.editing_name, 'ask_name')
@router.callback_query(F.data == "edit_text")
async def cb_edit_text(cb: CallbackQuery, state: FSMContext): await start_editing(cb, state, QuoteState.editing_text, 'ask_text')
@router.callback_query(F.data == "edit_avatar")
async def cb_edit_avatar(cb: CallbackQuery, state: FSMContext): await start_editing(cb, state, QuoteState.editing_avatar, 'ask_avatar')
@router.callback_query(F.data == "edit_color")
async def cb_edit_color(cb: CallbackQuery, state: FSMContext): await start_editing(cb, state, QuoteState.editing_color, 'ask_color')

@router.callback_query(F.data == "cancel_edit")
async def cb_cancel_edit(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state == QuoteState.waiting_for_initial_text:
        await callback.message.delete()
        return
    lang = (await state.get_data()).get('lang', 'ua')
    await callback.answer(get_text(lang, 'toast_canceled'), show_alert=False)
    await show_menu(callback.message, state, is_new=False)

@router.callback_query(F.data.startswith("set_color_"))
async def cb_pick_color(callback: CallbackQuery, state: FSMContext):
    val = callback.data.split("set_color_")[1]
    
    if val == "auto":
        data = await state.get_data()
        original_uid = data.get('original_uid')
        new_color_key = original_uid if original_uid else random.randint(1, 100000)
    else:
        new_color_key = val
        
    await state.update_data(quote_color_key=new_color_key)
    lang = (await state.get_data()).get('lang', 'ua')
    
    if val == "auto":
        await callback.answer(get_text(lang, 'toast_auto_color'), show_alert=False)
    else:
        await callback.answer(get_text(lang, 'toast_color_changed'), show_alert=False)
        
    await show_menu(callback.message, state, is_new=False)

@router.message(QuoteState.editing_text, F.text | F.caption | F.photo)
async def process_text_or_photo_edit(message: Message, state: FSMContext):
    data = await state.get_data()
    await delete_message_safe(bot, message.chat.id, data.get('last_bot_msg_id'))
    if message.photo:
        file_id = message.photo[-1].file_id
        content_img = await download_avatar(bot, file_id=file_id)
        await state.update_data(content_image=content_img)
        if message.caption: await state.update_data(quote_text=message.caption)
    elif message.text: await state.update_data(quote_text=message.text)
    await show_menu(message, state, is_new=True)

@router.message(QuoteState.editing_name, F.text)
async def process_name(message: Message, state: FSMContext):
    data = await state.get_data()
    await delete_message_safe(bot, message.chat.id, data.get('last_bot_msg_id'))
    await state.update_data(quote_name=message.text)
    await show_menu(message, state, is_new=True)

@router.message(QuoteState.editing_name, F.photo | F.document)
async def process_wrong_input_name(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    msg = await message.answer(get_text(lang, 'error_name_wrong_type'))
    await asyncio.sleep(4)  # ⬅️ ТУТ МОЖНА ЗМІНИТИ ЧАС (в секундах)
    await delete_message_safe(bot, message.chat.id, msg.message_id)

@router.message(QuoteState.editing_avatar, F.photo)
async def process_avatar(message: Message, state: FSMContext):
    file_id = message.photo[-1].file_id
    await delete_message_safe(bot, message.chat.id, message.message_id) 
    data = await state.get_data()
    await delete_message_safe(bot, message.chat.id, data.get('last_bot_msg_id'))
    new_ava = await download_avatar(bot, file_id=file_id)
    await state.update_data(avatar_base64=new_ava, is_custom_avatar=True)
    await show_menu(message, state, is_new=True)

@router.message(QuoteState.editing_avatar, F.text | F.document)
async def process_wrong_input_avatar(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    msg = await message.answer(get_text(lang, 'error_avatar_wrong_type'))
    await asyncio.sleep(4)  # ⬅️ ТУТ МОЖНА ЗМІНИТИ ЧАС (в секундах)
    await delete_message_safe(bot, message.chat.id, msg.message_id)

@router.message(QuoteState.menu_processing, F.text | F.photo | F.document)
async def process_wrong_input_main_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    msg = await message.answer(get_text(lang, 'error_menu_deleted'))
    await asyncio.sleep(4)  # ⬅️ ТУТ МОЖНА ЗМІНИТИ ЧАС (в секундах)
    await delete_message_safe(bot, message.chat.id, msg.message_id)

@router.message(QuoteState.editing_color, F.text | F.photo | F.document)
async def process_wrong_input_color_menu(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang', 'ua')
    msg = await message.answer(get_text(lang, 'error_color_menu_deleted'))
    await asyncio.sleep(4)  # ⬅️ ТУТ МОЖНА ЗМІНИТИ ЧАС (в секундах)
    await delete_message_safe(bot, message.chat.id, msg.message_id)

async def main():
    logging.basicConfig(level=logging.INFO)
    await startup_browser()
    asyncio.create_task(start_web_server())
    try: await dp.start_polling(bot)
    finally: await shutdown_browser()

if __name__ == "__main__":
    try: asyncio.run(main())
    except KeyboardInterrupt: print("Bot Stopped")