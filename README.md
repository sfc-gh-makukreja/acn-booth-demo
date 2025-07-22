# 📸 Age Guesser with Snowflake Cortex

A **Streamlit in Snowflake** app that uses Snowflake Cortex AI to guess a person's age from a camera photo. Runs natively within Snowflake!

## 🌟 Features

- 📷 **Camera Integration**: Take photos directly from your browser
- 🤖 **AI Age Estimation**: Uses Snowflake Cortex vision models
- ⚡ **Native Performance**: Runs entirely within Snowflake
- 🔒 **Secure**: No external dependencies or data transfer
- 🎯 **Simple Interface**: Clean, intuitive design

## 🚀 Quick Deploy

### Prerequisites
- Snowflake account with **Cortex enabled**
- **Snowflake CLI** installed ([Installation guide](https://docs.snowflake.com/en/developer-guide/snowflake-cli-v2/installation/installation))
- Required Snowflake privileges for creating Streamlit apps

### Method 1: Deploy with Snowflake CLI

1. **Login to Snowflake**:
   ```bash
   snow connection add
   snow connection test
   ```

2. **Deploy the app** (includes environment.yml automatically):
   ```bash
   snow streamlit deploy --replace
   ```

3. **Open your app** in Snowsight!

### Method 2: Deploy via Snowsight UI

1. **Login to Snowsight**
2. Go to **Data > Streamlit**
3. Click **+ Streamlit App**
4. **Name**: `age_guesser_app`
5. **Copy and paste** the content from `streamlit_app.py`
6. **Upload environment.yml**: Click "Upload Files" and add the `environment.yml`
7. **Deploy!**

### Method 3: SQL Command

```sql
-- First upload files to stage
PUT file://streamlit_app.py @mystage;
PUT file://environment.yml @mystage;

-- Create Streamlit app
CREATE OR REPLACE STREAMLIT age_guesser_app
  ROOT_LOCATION = '@mystage'
  MAIN_FILE = 'streamlit_app.py'
  QUERY_WAREHOUSE = 'my_warehouse';
```

## 📱 How to Use

1. **Open the app** in Snowsight
2. **Allow camera access** when prompted by browser
3. **Take a photo** using the camera input
4. **Click "🤖 Guess My Age!"** for AI analysis
5. **View results** and try again!

## 🛠️ App Architecture

```
📁 Your Snowflake Account
├── 🎯 Streamlit App (age_guesser_app)
│   ├── 📄 streamlit_app.py
│   └── 🐍 environment.yml (Snowflake Anaconda packages)
├── 🤖 Cortex AI Models (llama3.1-405b)
├── 📸 Camera Integration
└── ⚡ Native Session Management
```

## 🔧 Configuration

The app uses **native Snowflake session** - no external credentials needed!

Key components:
- `st.connection('snowflake').session()` - Native session
- `SNOWFLAKE.CORTEX.COMPLETE()` - AI vision analysis
- `st.camera_input()` - Browser camera integration

## 📦 Package Management

The app uses `environment.yml` for package management (not requirements.txt):

```yaml
name: sf_env
channels:
  - snowflake
dependencies:
  - streamlit=1.31.1
  - pillow
```

**Important Notes:**
- ✅ Uses **Snowflake Anaconda Channel** only
- ✅ Streamlit version is **pinned** for consistency  
- ✅ Packages auto-installed during deployment
- ❌ External Anaconda channels **not supported**

## 📋 Requirements

- **Snowflake Account** with Cortex enabled
- **Browser** with camera support
- **Snowflake privileges**: 
  - `CREATE STREAMLIT` on schema
  - `USAGE` on Cortex functions

## 🎯 Features Explained

### 🤖 AI Vision Analysis
Uses Snowflake Cortex's `llama3.1-405b` model with vision capabilities to analyze:
- Facial features and bone structure
- Skin texture and appearance  
- Age-related visual indicators
- Provides reasoning for estimates

### 📸 Camera Integration
- **Real-time capture**: Direct browser camera access
- **Image processing**: Converts to base64 for Cortex
- **Instant preview**: See your photo before analysis

### 🔒 Security & Privacy
- **No external APIs**: Everything runs in Snowflake
- **Secure processing**: Images processed within your account
- **Session-based**: Temporary storage only

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Cortex Error** | Ensure Cortex is enabled in your account |
| **Camera Not Working** | Check browser camera permissions |
| **Deploy Failed** | Verify CLI connection and privileges |
| **App Not Loading** | Check warehouse is running |

## 📚 Learn More

- [Streamlit in Snowflake Docs](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- [Snowflake Cortex Guide](https://docs.snowflake.com/en/user-guide/snowflake-cortex/llm-functions)
- [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli-v2/index)

---

Built with ❤️ using **Streamlit in Snowflake** and **Snowflake Cortex** 