#!/usr/bin/env python3
"""
ShopSavvy - Telegram Bot for Finding Deals Across Indian E-commerce Platforms
"""
import logging
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, 
    ConversationHandler, MessageHandler, filters
)

from config import BOT_TOKEN, PLATFORM_SELECTION, PRODUCT_SEARCH, CATEGORY_SEARCH
from bot_handlers import (
    start, help_command, deals_command, button_callback,
    handle_product_search, handle_invalid_input, cancel_conversation,
    handle_text_message, error_handler
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the bot"""
    
    # Validate bot token
    if BOT_TOKEN == "your_bot_token_here":
        logger.error("Please set TELEGRAM_BOT_TOKEN environment variable")
        return
    
    # Create application
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Create conversation handler
    conversation_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CallbackQueryHandler(button_callback, pattern='^(search_products|browse_categories|platform_|category_).*$')
        ],
        states={
            PLATFORM_SELECTION: [
                CallbackQueryHandler(button_callback, pattern='^platform_.*$')
            ],
            PRODUCT_SEARCH: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_product_search)
            ],
            CATEGORY_SEARCH: [
                CallbackQueryHandler(button_callback, pattern='^category_.*$')
            ]
        },
        fallbacks=[
            CommandHandler('cancel', cancel_conversation),
            MessageHandler(filters.TEXT, handle_invalid_input)
        ],
        allow_reentry=True
    )
    
    # Add handlers
    app.add_handler(conversation_handler)
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('deals', deals_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))
    
    # Add error handler
    app.add_error_handler(error_handler)
    
    logger.info("🤖 ShopSavvy Bot is starting...")
    logger.info("🔍 Ready to help users find the best deals!")
    
 # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 8443))
            
    # Start the bot
    try:
        if 'RENDER' in os.environ:
            # Webhook configuration for Render
            webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{BOT_TOKEN}"
            app.run_webhook(
                listen="0.0.0.0",
                port=port,
                webhook_url=webhook_url,
                url_path=BOT_TOKEN,
                allowed_updates=['message', 'callback_query'],
                drop_pending_updates=True
            )
            logger.info(f"🌐 Webhook configured at {webhook_url}")
        else:
            # Use polling for local development
            app.run_polling(
                allowed_updates=['message', 'callback_query'],
                drop_pending_updates=True
            )
            logger.info("🔌 Using polling method (local development)")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        logger.info("Make sure TELEGRAM_BOT_TOKEN is set correctly")

if __name__ == '__main__':
    main()
