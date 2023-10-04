# (c) AlenPaulVarghese
# -*- coding: utf-8 -*-

import os

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import Config
from helper.printer import CacheData, RenderType, ScrollMode
from webshotbot import WebshotBot


@WebshotBot.on_message(
    filters.regex(pattern="http[s]*://.+") & filters.private & ~filters.create(lambda _, __, m: bool(m.edit_date))
)
async def checker(client: WebshotBot, message: Message):
    msg = await message.reply_text("Çalışıyor\nWorking", True)
    markup = []
    _settings = client.get_settings_cache(message.chat.id)
    if _settings is None:
        _settings = CacheData(
            render_type=RenderType.PDF,
            fullpage=True,
            scroll_control=ScrollMode.OFF,
            resolution="Letter",
            split=False,
        )
    markup.extend(
        [
            [
                InlineKeyboardButton(
                    text=f"Format - {_settings['render_type'].name.upper()}",
                    callback_data="format",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"Page - {'Full' if _settings['fullpage'] else 'Partial'}",
                    callback_data="page",
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"Scroll Site - {_settings['scroll_control'].value.title()}",
                    callback_data="scroll",
                )
            ],
        ]
    )
    _split = _settings["split"]
    _resolution = _settings["resolution"]
    if _split or  _resolution != "Letter":
        markup.extend(
            [
                [InlineKeyboardButton(text="Ek ayarları kapat/ Hide additional options ˄", callback_data="options")],
                [
                    InlineKeyboardButton(text=f"resolution | {_resolution}", callback_data="res"),
                ],
                [
                    InlineKeyboardButton(
                        text=f"Split - {'Yes' if _split else 'No'}",
                        callback_data="splits",
                    )
                ]
                if _settings["render_type"] != RenderType.PDF
                else [],
            ]
        )
    else:
        markup.append([InlineKeyboardButton(text="Ek ayarları göster / Show additional options ˅", callback_data="options")])
    markup.extend(
        [
            [InlineKeyboardButton(text="▫️ start render ▫️", callback_data="render")],
            [InlineKeyboardButton(text="cancel", callback_data="cancel")],
        ]
    )
    await msg.edit(
        text="Choose the prefered settings",
        reply_markup=InlineKeyboardMarkup(markup),
    )


@WebshotBot.on_message(filters.command(["start"]))
async def start(_, message: Message) -> None:
    await message.reply_text(
        f"<b> {message.from_user.first_name} 👋\n\n"
        "Belirli bir bağlantının web sitesini PDF veya PNG/JPEG'ye dönüştürebilirim."
        "I can render website of a given link to either PDF or PNG/JPEG</b>",
        quote=True,
        reply_markup=InlineKeyboardMarkup
        (
        [
        [
        InlineKeyboardButton("❓ About", callback_data="about_cb"),
        InlineKeyboardButton("❓ Hakkımda", callback_data="support_cb"),
        ],
        ]
        ),
    )


@WebshotBot.on_message(filters.command(["about", "feedback"]))
async def feedback(_, message: Message) -> None:
    await message.reply_text(
        text="This project is open ❤️ source",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "❓ Hata Raporlama / Bug Report",
                        url="https://t.me/DolunayDestekBot",
                    ),
                ],
                
            ]
        ),
    )


@WebshotBot.on_message(filters.command(["support", "feedback", "help"]) & filters.private)
async def help_handler(_, message: Message) -> None:
    if Config.SUPPORT_GROUP_LINK is not None:
        await message.reply_text(
        text="Nasıl kullanılır?\How is it used?",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Türkçe",
                        callback_data="",
                    ),
                    InlineKeyboardButton(
                        "English",
                        callback_data="",
                    ),
                ],
                
            ]
        ),
    )
        
@WebshotBot.on_message(filters.command(["support_en", ]) & filters.private)
async def help_handler(_, message: Message) -> None:
    if Config.SUPPORT_GROUP_LINK is not None:
        await message.reply_text(
        text=
            "__Frequently Asked Questions__:\n\n"
            "** A. How to use the bot to render a website?\n\n"
            "Answer:** Just send the link to the website you want to create, "
            "select the desired setting and click on `Start`.\n\n"
            "** B. How does this bot work?**\n\n"
            "**Answer**: This bot uses a real browser under the hood to create websites.\n\n"
            "**C. How to report a bug or request a new feature?\n\n"
            "**Answer**: For feature requests or error reports"
            "launch the [Dolunay Raport](https://t.me/DolunayDestekBot) bot and follow the steps or contact [Nihilanth](https://t.me/nihilanth0) privately",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Support group", url=Config.SUPPORT_GROUP_LINK)]]
            ),
            disable_web_page_preview=True,
        )
        

@WebshotBot.on_message(filters.command(["support_tr", ]) & filters.private)
async def help_handler(_, message: Message) -> None:
    if Config.SUPPORT_GROUP_LINK is not None:
        await message.reply_text(
        text=
            "__Sıkça Sorulan Sorular__:\n\n"
            "** A. Bir web sitesinin çıktısı için bot nasıl kullanılır?\n\n"
            "**Cevap**:Oluşturmak istediğiniz web sitesinin bağlantısını göndermeniz yeterli,"
            "istediğiniz ayarı seçin ve `Başlat'a'` tıklayın.\n\n"
            "** B. Bu bot nasıl çalışır**?\n\n"
            "**Cevap**:Bu bot, web sitelerini oluşturmak için kaputun altında gerçek bir tarayıcı kullanır.\n\n"
            "** C. Bir hata nasıl bildirilir veya yeni bir özellik nasıl istenir?**\n\n"
            "**Cevap**: Özellik istekleri veya hata raporları için"
            "[Dolunay Raporlama](https://t.me/DolunayDestekBot) botunu başlatıp adımları izleyin veya [Nihilanth](https://t.me/nihilanth0)'a özelden ulaşın",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Support group", url=Config.SUPPORT_GROUP_LINK)]]
            ),
            disable_web_page_preview=True,
        )

@WebshotBot.on_message(filters.command(["debug", "log"]) & filters.private)
async def send_log(_, message: Message) -> None:
    try:
        sudo_user = int(os.environ["SUDO_USER"])
        if sudo_user != message.chat.id:
            raise Exception
    except Exception:
        return
    if os.path.exists("debug.log"):
        await message.reply_document("debug.log")
    else:
        await message.reply_text("Dosya bulunamadı\nFile not found.")
