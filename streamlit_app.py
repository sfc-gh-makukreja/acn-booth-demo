import streamlit as st
from PIL import Image
import base64
import io

# Page configuration
st.set_page_config(
    page_title="Age Guesser with Snowflake Cortex",
    page_icon="📸",
    layout="wide"
)

# Get Snowflake session (native to Streamlit in Snowflake)
session = st.connection('snowflake').session()

def image_to_base64(image):
    """Convert PIL image to base64 string"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def guess_age_with_cortex(image_base64):
    """Use Snowflake AI_COMPLETE to guess age from image"""
    try:
        # Prepare the prompt for AI vision analysis
        prompt = "Analyze this image and estimate the age of the person. Look at facial features and skin texture. Provide an age estimate with a brief explanation."
        
        # Create a unique filename for this session
        import uuid
        filename = f"age_photo_{uuid.uuid4().hex[:8]}.jpg"
        
        # Convert base64 to binary and upload to stage
        import base64
        image_binary = base64.b64decode(image_base64)
        
        # Create stage with proper configuration for AI_COMPLETE
        session.sql("""
            CREATE STAGE IF NOT EXISTS temp_images_stage
            ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
            COMMENT = 'Temporary stage for AI image processing'
        """).collect()
        
        # Upload image to stage (using PUT command)
        # First save the image temporarily
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            tmp_file.write(image_binary)
            temp_path = tmp_file.name
            temp_file_name = os.path.basename(temp_path)
        try:
            # Upload to Snowflake stage with better error handling
            st.write(temp_path, filename)
            upload_result = session.file.put(temp_path, f"@temp_images_stage/{filename}", auto_compress=False, overwrite=True)
            st.write(f"Debug: Upload result: {upload_result}")  # Debug info
            
            # Verify file exists in stage
            verify_query = f"LIST '@temp_images_stage/{filename}/{temp_file_name}'"
            verify_result = session.sql(verify_query).collect()
            st.write(f"Debug: File verification: {verify_result}")  # Debug info
            
            if not verify_result:
                return "Error: Failed to upload image to stage"
            
            # Use AI_COMPLETE with the uploaded image - escape prompt properly
            escaped_prompt = prompt.strip().replace("'", "''")  # Escape single quotes
            
            query = f"""
            SELECT AI_COMPLETE(
                'claude-3-5-sonnet',
                '{escaped_prompt}',
                TO_FILE('@temp_images_stage', '{filename}/{temp_file_name}')
            ) as age_prediction
            """
            
            st.write(f"Debug: Executing query: {query}")  # Debug info
            result = session.sql(query).collect()
            
            if result and len(result) > 0:
                return result[0]['AGE_PREDICTION']
            else:
                return "Unable to analyze the image"
                
        finally:
            # Clean up temporary file and stage file
            os.unlink(temp_path)
            try:
                session.sql(f"rm '@temp_images_stage/{filename}/{temp_file_name}'").collect()
            except:
                pass  # Ignore cleanup errors
            
    except Exception as e:
        st.error(f"Error using AI_COMPLETE: {str(e)}")
        return f"Error analyzing image: {str(e)}"

def main():
    # Header with company logos
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        # Accenture logo
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Accenture.svg/320px-Accenture.svg.png", 
                width=200)
    
    with col2:
        st.markdown("<h1 style='text-align: center; margin-top: 20px;'>📸 Age Guesser</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #666;'>Powered by Snowflake Cortex AI</h3>", unsafe_allow_html=True)
    
    with col3:
        # Snowflake logo
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Snowflake_Logo.svg/320px-Snowflake_Logo.svg.png", 
                width=200)
    
    st.markdown("---")
    
    # Booth presentation subtitle
    st.markdown("<h4 style='text-align: center; color: #0066cc;'>🎪 Live Demo at Snowflake World Tour</h4>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 18px;'>Take a photo and let AI guess your age using advanced computer vision!</p>", unsafe_allow_html=True)
    
    # Info about the app
    with st.sidebar:
        st.header("🎪 Snowflake World Tour Demo")
        st.markdown("**Built by Accenture + Snowflake**")
        
        st.markdown("---")
        st.header("💡 Technology Stack")
        st.write("🤖 **Snowflake Cortex AI** - Claude 3.5 Sonnet")
        st.write("📸 **Streamlit Camera** - Real-time capture")
        st.write("⚡ **Native Snowflake** - Zero-ETL processing")
        st.write("🔒 **Secure by Design** - Data never leaves Snowflake")
        
        st.markdown("---")
        st.markdown("**🚀 Demo Flow:**")
        st.markdown("""
        1. 📱 **Take Photo** → Camera captures image
        2. 🔄 **Upload Stage** → Secure Snowflake storage  
        3. 🧠 **AI Analysis** → Cortex vision processing
        4. 📊 **Results** → Age estimate + explanation
        5. 🧹 **Auto Cleanup** → Temporary data removed
        """)
        
        st.markdown("---")
        st.info("🎯 **Use Case**: Computer vision for retail, healthcare, security applications")
        
        st.markdown("---")
        st.markdown("**Learn More:**")
        st.markdown("• [Snowflake Cortex](https://docs.snowflake.com/en/user-guide/snowflake-cortex)")
        st.markdown("• [Accenture + Snowflake](https://www.accenture.com/us-en/services/snowflake)")
        st.markdown("• [Streamlit in Snowflake](https://docs.snowflake.com/en/developer-guide/streamlit)")

    # Main app layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("📷 Take a Photo")
        
        # Camera input
        camera_image = st.camera_input("Take a picture")
        
        if camera_image is not None:
            # Display the captured image
            image = Image.open(camera_image)
            st.image(image, caption="Captured Image", use_column_width=True)
            
            # Convert to base64
            image_base64 = image_to_base64(image)
            
            # Enhanced button for booth demo
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🤖 **GUESS MY AGE!**", type="primary", use_container_width=True, help="Click to analyze your photo with Snowflake Cortex AI"):
                with st.spinner("Analyzing your photo with Snowflake Cortex..."):
                    # Get age prediction
                    age_prediction = guess_age_with_cortex(image_base64)
                    
                    # Store result in session state
                    st.session_state.age_result = age_prediction
                    st.rerun()
    
    with col2:
        st.header("🎯 Age Prediction")
        
        # Display results
        if 'age_result' in st.session_state:
            st.success("🎉 **SNOWFLAKE CORTEX AI ANALYSIS COMPLETE!**")
            
            # Display the prediction in a nice format with enhanced styling
            st.markdown("### 🧠 **AI Prediction Results:**")
            st.markdown(f"""
            <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #0066cc;'>
                <h3 style='color: #0066cc; margin-top: 0;'>🎯 {st.session_state.age_result}</h3>
                <p style='margin-bottom: 0; color: #666;'><em>Powered by Claude 3.5 Sonnet via Snowflake Cortex</em></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Add some fun elements
            st.balloons()
            
            # Enhanced call-to-action for booth visitors
            st.markdown("<br>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            
            with col_a:
                if st.button("🔄 **TRY AGAIN**", use_container_width=True, help="Take another photo!"):
                    if 'age_result' in st.session_state:
                        del st.session_state.age_result
                    st.rerun()
            
            with col_b:
                st.markdown("**🤔 How accurate was it?**")
                accuracy = st.select_slider("Rate the accuracy:", ["😞 Way off", "🤷 Close", "😊 Pretty good", "🎯 Spot on!"], key="accuracy_rating")
        else:
            st.info("📸 Take a photo and click 'Guess My Age!' to see the AI prediction.")
            
            # Placeholder content
            st.markdown("""
            ### 🌟 Features:
            - **🎯 Accurate AI Analysis**: Uses advanced Cortex models
            - **📱 Real-time Camera**: Instant photo capture
            - **⚡ Fast Processing**: Native Snowflake performance  
            - **🔒 Secure**: All processing within Snowflake
            
            *Note: This is for entertainment purposes only.*
            """)

    # Professional footer for booth demo
    st.markdown("---")
    
    footer_col1, footer_col2, footer_col3 = st.columns(3)
    
    with footer_col1:
        st.markdown("**🤝 Partnership**")
        st.markdown("Accenture × Snowflake")
        st.markdown("*Leading the Data Cloud Revolution*")
    
    with footer_col2:
        st.markdown("**🎪 Event**")
        st.markdown("Snowflake World Tour 2025")
        st.markdown("*Live AI Demo*")
        
    with footer_col3:
        st.markdown("**🚀 Technology**")
        st.markdown("Streamlit in Snowflake")
        st.markdown("*Native AI Applications*")
    
    st.markdown("<p style='text-align: center; color: #888; margin-top: 20px;'>Built with ❤️ using Snowflake Cortex AI • Secure • Scalable • Serverless</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main() 