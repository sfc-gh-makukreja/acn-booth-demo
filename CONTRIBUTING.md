# Contributing to Snowflake World Tour 2025 Age Guesser Demo

## 🎪 Project Overview

This is a **Streamlit in Snowflake** application showcasing AI-powered age estimation using **Snowflake Cortex** for the **Snowflake World Tour 2025** booth demo.

**Partnership**: Accenture × Snowflake

## 🛠️ Development Setup

### Prerequisites
- [Snowflake CLI](https://docs.snowflake.com/en/developer-guide/snowflake-cli-v2/installation/installation) installed
- Snowflake account with **Cortex enabled**
- Git for version control

### Quick Start
```bash
# Clone the repository
git clone <repo-url>
cd acn-booth-demo

# Configure Snowflake connection
snow connection add

# Deploy the app
./deploy.sh
```

## 📁 Project Structure

```
acn-booth-demo/
├── streamlit_app.py        # Main Streamlit application
├── environment.yml         # Snowflake Anaconda packages
├── snowflake.yml          # Snowflake CLI configuration
├── deploy.sh              # Deployment script
├── README.md              # Project documentation
├── CONTRIBUTING.md        # This file
└── .gitignore            # Git ignore patterns
```

## 🔄 Development Workflow

### Making Changes

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Edit `streamlit_app.py` for app functionality
   - Update `environment.yml` for new packages
   - Modify `README.md` for documentation

3. **Test locally** (if possible)
   ```bash
   # Deploy to your dev environment
   ./deploy.sh
   ```

4. **Commit changes**
   ```bash
   git add .
   git commit -m "feat: describe your changes"
   ```

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Deployment

**Production Deployment**:
```bash
./deploy.sh
```

**Manual Deployment**:
```bash
snow streamlit deploy --replace
```

## 🎯 Key Components

### Streamlit App (`streamlit_app.py`)
- **Main function**: Camera capture and AI analysis
- **Branding**: Accenture + Snowflake logos
- **AI Integration**: Uses `AI_COMPLETE` with `claude-3-5-sonnet`
- **Stage Management**: Temporary image storage with cleanup

### Environment (`environment.yml`)
- **Snowflake Anaconda Channel** packages only
- **Pinned versions** for consistency
- **Minimal dependencies** for fast deployment

### Configuration (`snowflake.yml`)
- **Streamlit app definition** for Snowflake CLI
- **Warehouse specification** for compute
- **Deployment settings**

## 🐛 Debugging

### Common Issues

**1. Connection Errors**
```bash
# Test connection
snow connection test

# Add new connection
snow connection add
```

**2. Stage Upload Issues**
```bash
# Check stage exists
snow sql -q "SHOW STAGES LIKE 'temp_images_stage'"

# List stage contents
snow sql -q "LIST '@temp_images_stage'"
```

**3. AI_COMPLETE Errors**
```bash
# Test basic AI function
snow sql -q "SELECT AI_COMPLETE('claude-3-5-sonnet', 'Hello test')"
```

### Debug Mode
Enable debug output in the app by setting debug flags in `streamlit_app.py`.

## 📊 Booth Demo Guidelines

### For Booth Staff

**Demo Script**:
1. 🎪 **"Welcome to our AI demo powered by Snowflake Cortex!"**
2. 📸 **"Let's take your photo and see how accurate our AI is!"**
3. 🤖 **"This uses Claude 3.5 Sonnet running natively in Snowflake"**
4. 📊 **"Notice how fast it processes - no external APIs needed!"**
5. 🔄 **"Want to try again or bring a friend?"**

**Key Talking Points**:
- ✅ **Native Snowflake**: No external dependencies
- ✅ **Secure**: Data never leaves Snowflake
- ✅ **Scalable**: Enterprise-ready architecture
- ✅ **Partnership**: Accenture + Snowflake innovation

## 🔒 Security

- **No sensitive data** in version control
- **Temporary image processing** with automatic cleanup
- **Stage-based storage** with server-side encryption
- **Credentials** managed via Snowflake CLI

## 📈 Future Enhancements

**Potential Features**:
- [ ] Multiple model comparison
- [ ] Batch image processing
- [ ] Analytics dashboard
- [ ] Export results to Snowflake tables
- [ ] Multi-language support

## 🆘 Support

**For Issues**:
1. Check this CONTRIBUTING.md
2. Review project README.md
3. Contact the Accenture + Snowflake team

**For Booth Support**:
- Test deployment before events
- Have backup demo ready
- Know the talking points
- Understand the technical architecture

---

**Happy Coding!** 🚀 Let's showcase the power of Snowflake Cortex at World Tour 2025! 