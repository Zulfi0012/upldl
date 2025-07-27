#!/bin/bash

# Telegram File Transfer Bot Deployment Script

set -e

echo "🚀 Starting deployment of Telegram File Transfer Bot..."

# Check if environment variables are set
check_env_var() {
    if [ -z "${!1}" ]; then
        echo "❌ Error: $1 environment variable is not set"
        echo "Please set all required environment variables before deployment"
        exit 1
    fi
}

echo "📋 Checking required environment variables..."
check_env_var "TELEGRAM_BOT_TOKEN"
check_env_var "GOOGLE_DRIVE_CREDENTIALS"

echo "✅ Environment variables check passed"

# Create temp directory if it doesn't exist
echo "📁 Creating temporary storage directory..."
mkdir -p temp_files

# Install dependencies
echo "📦 Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    pip install -e .
fi

# Set webhook if WEBHOOK_URL is provided
if [ ! -z "$WEBHOOK_URL" ]; then
    echo "🔗 Setting up Telegram webhook..."
    curl -X POST "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/setWebhook" \
         -H "Content-Type: application/json" \
         -d "{\"url\": \"$WEBHOOK_URL\"}"
    echo ""
fi

# Start the application
echo "🎯 Starting the application..."
if [ "$1" = "dev" ]; then
    echo "🔧 Running in development mode..."
    python app.py
else
    echo "🏭 Running in production mode..."
    gunicorn --bind 0.0.0.0:${PORT:-5000} --reuse-port --reload main:app
fi