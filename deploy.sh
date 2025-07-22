#!/bin/bash

# Snowflake World Tour 2025 - Age Guesser Demo
# Deployment script for Streamlit in Snowflake

set -e

echo "🎪 Deploying Snowflake World Tour 2025 Age Guesser Demo..."
echo "================================================"

# Check if Snowflake CLI is installed
if ! command -v snow &> /dev/null; then
    echo "❌ Snowflake CLI not found. Please install it first:"
    echo "   brew install snowflake-cli"
    exit 1
fi

# Test connection
echo "🔗 Testing Snowflake connection..."
if ! snow connection test; then
    echo "❌ Snowflake connection failed. Please check your credentials:"
    echo "   snow connection add"
    exit 1
fi

echo "✅ Connection successful!"

# Deploy the app
echo "🚀 Deploying Streamlit app..."
snow streamlit deploy --replace

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "📱 Your app is live at:"
echo "   https://app.snowflake.com/[YOUR_ACCOUNT]/#/streamlit-apps/[DATABASE].[SCHEMA].AGE_GUESSER_APP"
echo ""
echo "🎪 Ready for Snowflake World Tour 2025 booth demo!"
echo "   • Professional Accenture + Snowflake branding"
echo "   • AI-powered age estimation using Cortex"  
echo "   • Interactive camera integration"
echo "" 