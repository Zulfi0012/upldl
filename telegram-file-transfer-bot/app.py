import os
import logging
from flask import Flask, request, render_template, jsonify, flash, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
import json
from bot_handlers import BotHandler
from config import Config

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize bot handler
bot_handler = BotHandler()

@app.route('/')
def index():
    """Main page with bot setup instructions"""
    return render_template('index.html', 
                         bot_token=Config.TELEGRAM_BOT_TOKEN,
                         webhook_url=Config.WEBHOOK_URL)

@app.route('/config')
def config():
    """Configuration page for API keys and settings"""
    return render_template('config.html', 
                         telegram_token_configured=bool(Config.TELEGRAM_BOT_TOKEN),
                         google_drive_configured=bool(Config.GOOGLE_DRIVE_CREDENTIALS),
                         webhook_url=Config.WEBHOOK_URL,
                         max_file_size=Config.MAX_FILE_SIZE // (1024*1024))

@app.route('/dashboard')
def dashboard():
    """Dashboard to monitor bot activity"""
    stats = bot_handler.get_stats()
    return render_template('dashboard.html', stats=stats)

@app.route('/webhook', methods=['POST'])
def webhook():
    """Telegram webhook endpoint"""
    try:
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = json.loads(json_string)
            logger.debug(f"Received update: {update}")
            
            # Process the update
            response = bot_handler.process_update(update)
            
            if response:
                return jsonify(response)
            return jsonify({"ok": True})
        else:
            logger.error("Invalid content type")
            return jsonify({"error": "Invalid content type"}), 400
            
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/set_webhook', methods=['POST'])
def set_webhook():
    """Set up the Telegram webhook"""
    try:
        result = bot_handler.set_webhook()
        if result:
            flash("Webhook set successfully!", "success")
        else:
            flash("Failed to set webhook", "error")
    except Exception as e:
        flash(f"Error setting webhook: {str(e)}", "error")
    
    return redirect(url_for('index'))

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "bot_configured": bool(Config.TELEGRAM_BOT_TOKEN),
        "google_drive_configured": bool(Config.GOOGLE_DRIVE_CREDENTIALS)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
