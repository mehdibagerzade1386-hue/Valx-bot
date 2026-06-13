import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8918914057:AAGoajYd1afX-aAvFLwHI2toeJ4pS1J0_R4")
CHANNEL_USERNAME = "@VALXOfficial"

logging.basicConfig(level=logging.INFO)

async def check_membership(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    is_member = await check_membership(context.bot, update.effective_user.id)
    if not is_member:
        keyboard = [
            [InlineKeyboardButton("👑 Join VALX Official", url="https://t.me/VALXOfficial")],
            [InlineKeyboardButton("✅ I Joined", callback_data="check")]
        ]
        await update.message.reply_text(
            "👑 *Welcome to VALX Bot*\n\nTo access VALX information, join our channel first.",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await send_info(update.message.reply_text)

async def send_info(reply_func):
    await reply_func(
        "👑 *Welcome to VALX — The New Standard*\n\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "🔱 *What is $VALX?*\n"
        "VALX is not just a token. It's a standard.\n"
        "Built on Solana for those who recognize real value.\n\n"
        "💰 *Token Info:*\n"
        "• Name: VALX\n"
        "• Ticker: $VALX\n"
        "• Blockchain: Solana\n"
        "• Contract: 🔜 Coming Soon\n\n"
        "⚡ *Why $VALX?*\n"
        "• Real Value. Real Wealth.\n"
        "• Early believers always win.\n\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "📢 Telegram: @VALXOfficial\n"
        "🐦 Twitter: @VALX\\_SOL\n\n"
        "🚀 *Launch is coming. Stay close.* 🔱",
        parse_mode="Markdown"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "check":
        is_member = await check_membership(context.bot, query.from_user.id)
        if is_member:
            await query.message.delete()
            await send_info(query.message.reply_text)
        else:
            await query.answer("❌ Please join the channel first!", show_alert=True)

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

print("VALX Bot is running...")
app.run_polling()
