# texts.py

MESSAGES = {
    'ua': {
        'welcome': (
            "👋 <b>Привіт!</b>\n"
            "🔹 Напиши або перешли з групи текст/фото, з якого ти хочеш зробити цитату.\n"
            "🔹 Введи <b>/q</b> для демонстрації роботи бота\n"
            "🔹 <b>/help</b> - довідка.\n"
            "🔹 <b>/settings</b> - налаштування.\n"
        ),
        'help': (
            "📚 <b>Довідка:</b>\n\n"
            "1. Для створення цитати просто напиши її в бота або перешли з групи текст/фото.\n"
            "2. <b>Команди:</b>\n"
            "   /q - Демонстрація роботи\n"
            "   /theme (/t) - Змінити тему\n"
            "   /lang (/l) - Змінити мову\n"
            "   /cancel (/c) - Скасувати створення цитати\n"
            "   /info (/i) - Інформація про бота\n"
            "   /settings (/s) - Налаштування\n"
        ),
	    'info': (
            "🌊 <b>QuoteYouBot - створюю круті цитати! 💬</b>\n\n"
            "🔹Цей бот зроблений для створення красивих цитат, які містять текст і/або фото. Можна змінювати саму цитату, редагувати фон цитати, аватарку, ім'я, колір імені цитати.\n\n"
            "‍👨‍💻 Власник: @mrgeyzer\n"
            "🔸 Instagram: instagram.com/vitya_zhadan\n\n"
            "📲 Знайшли баг, пишіть: @mrgeyzer\n"
            "🥷 GitHub: github.com/MrGeyzer\n"
        ),
        'info_photo_url': "",
        
        'menu_header': (
            "🌍 Мова: {curr_lang} | 🌗 Тема: {theme}\n"
            "➖➖➖➖➖➖➖\n"
            "📝 <b>Цитата:</b> {text}\n"
            "👤 <b>Ім'я автора:</b> {name}\n"
            "🎨 <b>Колір імені:</b> {color}\n"
            "{avatar_line}\n"
            "👇 <b>Редактор:</b>"
        ),
        
        'settings_header': "⚙ <b>Налаштування:</b>\n\nТут ти можеш змінити параметри за замовчуванням.",
        'btn_settings_lang': "🌍 Мова / Language",
        'btn_settings_theme': "🌗 Тема (Фон цитати)",
        'btn_settings_def_color': "🎨 Колір імені",
        'btn_settings_help': "📚 Довідка",
        'btn_settings_info': "ℹ Інфо",
        'btn_back': "⬅️ Назад",
        
        'theme_select_header': "🌗 Обери тему(фон) для стікера:",
        'theme_dark': "🌚 Темна",
        'theme_light': "☀️ Світла",
        'theme_dark_short': "🌑",
        'theme_light_short': "☀",
        
        'def_color_header': "🎨 Обери колір імені, який буде ставитись автоматично:",
        'def_color_auto': "🎲 Автоматично (Рандом)",
        
        'lang_select_header': "🌍 <b>Поточна мова:</b> {lang}\nОбери нову:",
        
        'toast_lang_changed': "✅ Мову змінено!",
        'toast_theme_changed': "✅ Тему змінено!",
        'toast_color_changed': "✅ Дефолтний колір змінено!",
        'toast_canceled': "✅ Редагування скасовано",
        'toast_generating': "🎨 Створюю стікер...",
        'toast_auto_color': "🎲 Встановлено авто-колір!",
        
        'msg_quote_canceled': "✅ Створення цитати cкасовано",
        'error_nothing_to_cancel': "ℹ️ Немає активної цитати для скасування.",
        
        'btn_create': "✅ Створити стікер",
        'btn_edit_name': "✏ Ім'я",
        'btn_edit_text': "📝 Цитата",
        'btn_edit_avatar': "🖼 Ава",
        'btn_edit_color': "🎨 Колір",
        'btn_cancel_all': "❌ Закрити",
        'btn_cancel_action': "❌ Скасувати",
        'btn_close': "❌ Закрити",
        'btn_auto_color': "🎲 Авто",
        
        'ask_text_init': "✍ <b>Створення цитати</b>\n\nНадішли <b>текст</b> цитати:",
        'ask_text': "📝 Надішли новий <b>текст</b>:",
        'ask_name': "👤 Введи нове <b>ім'я</b>:",
        'ask_avatar': "📸 Надішли <b>фото</b> або файл:",
        'ask_color': "🎨 Обери колір:",
        
        'error_no_text': "⚠️ Це не текст.",
        'error_no_photo': "⚠️ Це не фото.",
        'error_name_wrong_type': (
            "⚠️ <b>Помилка:</b> Для зміни імені потрібно надіслати текст, а не фото чи файл.\n\n"
            "💡 Якщо хочеш скасувати створення цитати, введи команду <b>/cancel</b> (або <b>/c</b>)"
        ),
        'error_avatar_wrong_type': (
            "⚠️ <b>Помилка:</b> Для зміни аватарки потрібно надіслати фото, а не текст чи інший файл.\n\n"
            "💡 Якщо хочеш скасувати створення цитати, введи команду <b>/cancel</b> (або <b>/c</b>)"
        ),
        'error_menu_deleted': (
            "⚠️ <b>Помилка:</b> Схоже, ти видалив інлайн меню редактора.\n\n"
            "💡 Якщо хочеш скасувати створення поточної цитати, введи команду <b>/cancel</b> (або <b>/c</b>)"
        ),
        'error_color_menu_deleted': (
            "⚠️ <b>Помилка:</b> Схоже, ти видалив меню вибору кольору.\n\n"
            "💡 Якщо хочеш скасувати створення поточної цитати, введи команду <b>/cancel</b> (або <b>/c</b>)"
        ),
        
        'lbl_avatar': "Аватарка",
        'ava_custom': "Власна",
        'ava_default': "З профілю",
        'tag_photo': "[Фото]",
        
        'demo_text': "Це демонстраційна цитата! Надішли мені будь-який текст/фото, щоб створити власну 😎",

        'color_names': {
            'blue': "💙 Блакитний",
            'red': "❤️ Червоний",
            'green': "💚 Зелений",
            'gold': "💛 Золотий",
            'purple': "💜 Фіолетовий",
            'orange': "🧡 Помаранчевий",
            'cyan': "🩵 Бірюзовий",
            'pink': "🩷 Рожевий"
        }
    },
    'en': {
        'welcome': (
            "👋 <b>Hello!</b>\n"
            "🔹 Write here or forward text/photo to turn it into a sticker.\n"
            "🔹 Type <b>/q</b> to demo the bot\n"
            "🔹 <b>/help</b> - help.\n"
            "🔹 <b>/settings</b> - settings.\n"
        ),
        'help': (
            "📚 <b>Help:</b>\n\n"
            "1. To create a quote, just write it to the bot or forward text/photo.\n"
            "2. <b>Commands:</b>\n"
            "   /q - Demo Quote\n"
            "   /theme (/t) - Change theme\n"
            "   /lang (/l) - Change language\n"
            "   /cancel (/c) - Cancel quote creation\n"
            "   /info (/i) - Bot Info\n"
            "   /settings (/s) - Settings\n"
        ),
        'info': (
            "🌊 <b>QuoteYouBot - I create cool quotes! 💬</b>\n\n"
            "🔹This bot is made to create beautiful quotes that contain text and/or photos. You can change the quote itself, edit the quote background, avatar, name, quote name color.\n\n"
            "‍👨‍💻 Owner: @mrgeyzer\n"
            "🔸 Instagram: instagram.com/vitya_zhadan\n\n"
            "📲 Found a bug, write: @mrgeyzer\n"
            "🥷 GitHub: github.com/MrGeyzer\n"
        ),
        'info_photo_url': "",

        'menu_header': (
            "🌍 Lang: {curr_lang} | 🌗 Theme: {theme}\n"
            "➖➖➖➖➖➖➖\n"
            "📝 <b>Quote:</b> {text}\n"
            "👤 <b>Author Name:</b> {name}\n"
            "🎨 <b>Name Color:</b> {color}\n"
            "{avatar_line}\n"
            "👇 <b>Editor:</b>"
        ),
        
        'settings_header': "⚙ <b>Settings:</b>\n\nCustomize your defaults here.",
        'btn_settings_lang': "🌍 Language / Мова",
        'btn_settings_theme': "🌗 Theme (Quote Background)",
        'btn_settings_def_color': "🎨 Name Color",
        'btn_settings_help': "📚 Bot Help",
        'btn_settings_info': "ℹ Info",
        'btn_back': "⬅️ Back",
        
        'theme_select_header': "🌗 Choose sticker theme (background):",
        'theme_dark': "🌑 Dark",
        'theme_light': "☀️ Light",
        'theme_dark_short': "🌑",
        'theme_light_short': "☀️",
        
        'def_color_header': "🎨 Choose automatic name color:",
        'def_color_auto': "🎲 Automatic (Random)",
        
        'lang_select_header': "🌍 <b>Current Language:</b> {lang}\nSelect new:",
        
        'toast_lang_changed': "✅ Language changed!",
        'toast_theme_changed': "✅ Theme changed!",
        'toast_color_changed': "✅ Default color changed!",
        'toast_canceled': "✅ Edit canceled",
        'toast_generating': "🎨 Creating sticker...",
        'toast_auto_color': "🎲 Auto color set!",
        
        'msg_quote_canceled': "✅ Quote creation canceled",
        'error_nothing_to_cancel': "ℹ️ No active quote to cancel.",
        
        'btn_create': "✅ Create Sticker",
        'btn_edit_name': "✏ Name",
        'btn_edit_text': "📝 Quote",
        'btn_edit_avatar': "🖼 Avatar",
        'btn_edit_color': "🎨 Color",
        'btn_cancel_all': "❌ Close",
        'btn_cancel_action': "❌ Cancel",
        'btn_close': "❌ Close",
        'btn_auto_color': "🎲 Auto",
        
        'ask_text_init': "✍ <b>Create Quote</b>\n\nSend the <b>text</b> first:",
        'ask_text': "📝 Send new <b>text</b>:",
        'ask_name': "👤 Enter new <b>name</b>:",
        'ask_avatar': "📸 Send <b>photo</b> or file:",
        'ask_color': "🎨 Pick a color:",
        
        'error_no_text': "⚠️ Not a text.",
        'error_no_photo': "⚠️ Not a photo.",
        'error_name_wrong_type': (
            "⚠️ <b>Error:</b> To change the name, you need to send text, not a photo or file.\n\n"
            "💡 If you want to cancel quote creation, type <b>/cancel</b> (or <b>/c</b>)"
        ),
        'error_avatar_wrong_type': (
            "⚠️ <b>Error:</b> To change the avatar, you need to send a photo, not text or another file.\n\n"
            "💡 If you want to cancel quote creation, type <b>/cancel</b> (or <b>/c</b>)"
        ),
        'error_menu_deleted': (
            "⚠️ <b>Error:</b> It seems you deleted the inline editor menu.\n\n"
            "💡 If you want to cancel current quote creation, type <b>/cancel</b> (or <b>/c</b>)"
        ),
        'error_color_menu_deleted': (
            "⚠️ <b>Error:</b> It seems you deleted the color selection menu.\n\n"
            "💡 If you want to cancel current quote creation, type <b>/cancel</b> (or <b>/c</b>)"
        ),
        
        'lbl_avatar': "Avatar",
        'ava_custom': "Custom",
        'ava_default': "Profile",
        'tag_photo': "[Photo]",
        
        'demo_text': "This is a demo quote! Send me any text/photo to create your own. 😎",

        'color_names': {
            'blue': "💙 Blue",
            'red': "❤️ Red",
            'green': "💚 Green",
            'gold': "💛 Gold",
            'purple': "💜 Purple",
            'orange': "🧡 Orange",
            'cyan': "🩵 Cyan",
            'pink': "🩷 Pink"
        }
    }
}