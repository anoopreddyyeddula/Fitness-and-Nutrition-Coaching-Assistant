
import streamlit as st
import google.generativeai as genai
import os

# MUST be the first Streamlit command
st.set_page_config(
    page_title="Fitness and Nutrition Coaching Chatbot",
    page_icon="🏋️‍♂️",
    layout="wide"
)

# Initialize Gemini with API key
GOOGLE_API_KEY = st.secrets["google"]["api_key"]
genai.configure(api_key=GOOGLE_API_KEY)

# Configure safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Initialize the model with configuration
generation_config = {
    "temperature": 0.7,
    "top_p": 0.8,
    "top_k": 40,
    "max_output_tokens": 1024,  # Reduced for faster responses
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",  # Updated to use an available model
    generation_config=generation_config,
    safety_settings=safety_settings
)

def get_gemini_response(messages):
    try:
        # Optimize prompt construction
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        
        # Add streaming for faster initial response
        response = model.generate_content(
            prompt,
            stream=True,
            generation_config={
                "temperature": 0.7,
                "top_p": 0.8,
                "top_k": 40,
                "max_output_tokens": 1024,  # Reduced for faster response
            }
        )
        
        # Stream the response
        full_response = ""
        for chunk in response:
            if chunk.text:
                full_response += chunk.text
        return full_response
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return "I encountered an error. Please try again."

# Custom CSS
st.markdown("""
    <style>
    /* Main container styles */
    .main {
        background-color: #f5f5f5;
        overflow-y: hidden;
    }

    /* Chat interface layout */
    .stChatFloatingInputContainer {
        position: fixed !important;
        bottom: 0 !important;
        padding: 1rem !important;
        background: white !important;
        border-top: 1px solid #ddd !important;
        z-index: 999 !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 100% !important;
        max-width: 800px !important;
    }

    .stChatContainer {
        height: calc(100vh - 100px) !important;
        overflow-y: auto !important;
        padding-bottom: 100px !important;
    }

    /* Message styles */
    .stChatMessage {
        margin-bottom: 1rem !important;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Optimize performance with hardware acceleration */
    .stChatFloatingInputContainer {
        transform: translateZ(0);
        -webkit-transform: translateZ(0);
        backface-visibility: hidden;
    }
    
    /* Smooth animations */
    .stChatMessage {
        transition: all 0.2s ease-in-out;
    }
    
    /* Edit button styling */
    .edit-button {
        opacity: 0.6;
        transition: opacity 0.2s ease-in-out;
    }
    
    .edit-button:hover {
        opacity: 1;
    }
    </style>
    """, unsafe_allow_html=True)

# Add tabs for different features
tab1, tab2, tab3 = st.tabs(["Chat", "BMI Calculator", "Workout Generator"])

with tab1:
    # Session state for chats and editing
    if "chats" not in st.session_state:
        st.session_state.chats = [{"first_query": None, "history": []}]
    if "current_chat_index" not in st.session_state:
        st.session_state.current_chat_index = 0
    if "editing_query_index" not in st.session_state:
        st.session_state.editing_query_index = None

    def truncate_query(query, max_len=40):
        return f"{query[:max_len]}..." if len(query) > max_len else query

    def handle_submit(user_input, is_edit=False):
        if user_input:
            current_chat = st.session_state.chats[st.session_state.current_chat_index]
            try:
                system_prompt = """You are a knowledgeable, friendly, and professional Fitness and Nutrition Coach. 
                Your goal is to provide evidence-based, practical, and personalized advice on fitness, nutrition, and overall health.
                Focus on providing accurate, science-backed information while keeping responses concise and actionable."""
                
                chat_completion = get_gemini_response([
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ])

                if is_edit:
                    original_response = current_chat["history"][st.session_state.editing_query_index]["response"]
                    current_chat["history"][st.session_state.editing_query_index].update({
                        "query": user_input,
                        "response": chat_completion,
                        "original_response": original_response
                    })
                    st.session_state.editing_query_index = None
                else:
                    current_chat["history"].append({
                        "query": user_input,
                        "response": chat_completion
                    })
                    if current_chat["first_query"] is None:
                        current_chat["first_query"] = user_input
                        st.rerun()

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.stop()

    # Chat management functions
    def create_new_chat():
        st.session_state.chats.append({"first_query": None, "history": []})
        st.session_state.current_chat_index = len(st.session_state.chats) - 1

    def switch_chat(index):
        st.session_state.current_chat_index = index

    def delete_chat(index):
        del st.session_state.chats[index]
        if st.session_state.current_chat_index >= len(st.session_state.chats):
            st.session_state.current_chat_index = len(st.session_state.chats) - 1
        st.rerun()

    def delete_message(chat_index, message_index):
        del st.session_state.chats[chat_index]["history"][message_index]
        st.rerun()

    # Sidebar
    st.sidebar.header("Instructions")
    st.sidebar.markdown("""
    Welcome to the Fitness and Nutrition Coaching AI Chatbot!
    - Ask any fitness or nutrition-related questions
    - Get personalized advice and tips
    """)

    # Chat management UI
    st.sidebar.title("Chats")
    if st.sidebar.button("Create New Chat", key="create_new_chat"):
        create_new_chat()

    # Display existing chats
    for i, chat in enumerate(st.session_state.chats):
        chat_title = chat["first_query"] if chat["first_query"] else f"Chat {i + 1}"
        col1, col2 = st.sidebar.columns([1, 1])
        with col1:
            if st.button(truncate_query(chat_title), key=f'chat_{i}'):
                switch_chat(i)
        with col2:
            if st.button("🗑️", key=f'delete_chat_{i}'):
                delete_chat(i)

    # Initialize chat container
    chat_placeholder = st.container()
    
    # Fixed input at bottom
    with st.container():
        user_input = st.chat_input("Ask something about fitness or nutrition...")
    
    # Display messages in chat container
    with chat_placeholder:
        for i, entry in enumerate(st.session_state.chats[st.session_state.current_chat_index]["history"]):
            with st.chat_message("user"):
                # Add edit button and message
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
                    if "editing" in st.session_state and st.session_state.editing == i:
                        edited_message = st.text_input("Edit message", value=entry["query"], key=f"edit_{i}")
                        if st.button("Save", key=f"save_{i}"):
                            entry["query"] = edited_message
                            st.session_state.editing = None
                            # Regenerate response
                            with st.spinner("Updating response..."):
                                new_response = get_gemini_response([
                                    {"role": "system", "content": "You are a fitness expert providing brief, actionable advice."},
                                    {"role": "user", "content": edited_message}
                                ])
                                entry["response"] = new_response
                            st.rerun()
                    else:
                        st.write(entry["query"])
                with col2:
                    if st.button("✏️", key=f"edit_btn_{i}"):
                        st.session_state.editing = i
                        st.rerun()
            
            with st.chat_message("assistant"):
                st.write(entry["response"])
    
    # Handle new messages
    if user_input:
        with chat_placeholder:
            with st.chat_message("user"):
                st.write(user_input)
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = get_gemini_response([
                        {"role": "system", "content": "You are a fitness expert providing brief, actionable advice."},
                        {"role": "user", "content": user_input}
                    ])
                    st.write(response)
                    
                    # Add to chat history
                    st.session_state.chats[st.session_state.current_chat_index]["history"].append({
                        "query": user_input,
                        "response": response
                    })

with tab2:
    st.header("BMI Calculator")
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=300.0, value=70.0)
        height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0, value=170.0)
        
    if st.button("Calculate BMI"):
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        
        st.write(f"Your BMI is: {bmi:.1f}")
        
        if bmi < 18.5:
            st.warning("Underweight")
        elif 18.5 <= bmi < 25:
            st.success("Normal weight")
        elif 25 <= bmi < 30:
            st.warning("Overweight")
        else:
            st.error("Obese")
            
        bmi_prompt = f"Given a BMI of {bmi:.1f}, provide a short, personalized recommendation for improving health. Include one nutrition tip and one exercise tip. Keep it within 3 sentences."
        
        recommendation = get_gemini_response([
            {"role": "system", "content": "You are a fitness expert providing brief, actionable advice."},
            {"role": "user", "content": bmi_prompt}
        ])
        st.info(recommendation)

with tab3:
    st.header("Workout Plan Generator")
    
    goal = st.selectbox("What's your primary goal?", 
                       ["Weight Loss", "Muscle Gain", "General Fitness", "Endurance"])
    
    level = st.selectbox("What's your fitness level?",
                        ["Beginner", "Intermediate", "Advanced"])
    
    equipment = st.multiselect("Available equipment",
                             ["None", "Dumbbells", "Resistance Bands", "Pull-up Bar", "Full Gym"])
    
    duration = st.slider("Workout duration (minutes)", 15, 120, 45)
    
    if st.button("Generate Workout Plan"):
        workout_prompt = f"""Create a {duration}-minute workout plan for a {level} level person focusing on {goal}.
        Available equipment: {', '.join(equipment)}.
        Include:
        1. Warm-up
        2. Main exercises with sets and reps
        3. Cool-down
        Format the response with clear sections and bullet points."""
        
        try:
            workout_plan = get_gemini_response([
                {"role": "system", "content": "You are a professional fitness trainer creating personalized workout plans."},
                {"role": "user", "content": workout_prompt}
            ])
            st.markdown(workout_plan)
            
            st.download_button(
                label="Download Workout Plan",
                data=workout_plan,
                file_name="workout_plan.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Google Gemini")
