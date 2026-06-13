import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Configuration
BOT_TOKEN = "8918914057:AAGoajYd1afX-aAvFLwHI2toeJ4pS1J0_R4"
CHANNEL_USERNAME = "@VALXOfficial"

logging.basicConfig(level=logging.INFO)

async def check_membership(bot, user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    is_member = await check_membership(context.bot, user.id)
    
    if not is_member:
        keyboard = [[InlineKeyboardButton("👑 Join VALX Official", url=f"https://t.me/VALXOfficial")],
                    [InlineKeyboardButton("✅ I Joined", callback_data="check_membership")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "👑 *Welcome to VALX Bot*\n\n"
            "To access VALX information, you must first join our official channel.\n\n"
            "Click the button below to join, then press ✅ I Joined",
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    else:
        await send_valx_info(update.message.reply_text)

async def send_valx_info(reply_func):
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
        "• Contract Address: 🔜 Coming Soon\n\n"
        "⚡ *Why $VALX?*\n"
        "• Real Value. Real Wealth.\n"
        "• Early believers always win.\n"
        "• Built for those who recognize opportunity.\n\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "📢 *Stay Updated:*\n"
        "• Telegram: @VALXOfficial\n"
        "• Twitter: @VALX\\_SOL\n\n"
        "🚀 *Launch is coming. Stay close.* 🔱",
        parse_mode="Markdown"
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "check_membership":
        is_member = await check_membership(context.bot, query.from_user.id)
        if is_member:
            await query.message.delete()
            await send_valx_info(query.message.reply_text)
        else:
            await query.answer("❌ You haven't joined yet! Please join first.", show_alert=True)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("VALX Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
