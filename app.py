import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from diet_planner import calculate_bmr, calculate_daily_calories, generate_diet_plan
import base64
from io import BytesIO
import os

# Set page config with a more engaging theme
st.set_page_config(
    page_title="Indian Vegetarian Diet & Fitness Planner",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark mode and better UI
st.markdown("""
    <style>
    /* Dark mode styles */
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .css-1d391kg {
        background-color: #0E1117;
    }
    .st-bq {
        background-color: #1E2128;
    }
    .st-c0 {
        background-color: #0E1117;
    }
    .st-c1 {
        background-color: #0E1117;
    }
    .st-c2 {
        background-color: #1E2128;
    }
    .st-c3 {
        background-color: #0E1117;
    }
    .st-c4 {
        background-color: #1E2128;
    }
    .stTabs [data-baseweb="tab-panel"] {
        background-color: #0E1117;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E2128;
        color: white;
        border-radius: 4px 4px 0px 0px;
        padding: 0.5rem 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    .stTabs [data-baseweb="tab-list"] {
        background-color: #0E1117;
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"]:focus {
        background-color: #3B4357;
        color: white;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #3B4357;
    }
    div.stButton > button {
        background-color: #3B4357;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    div.stButton > button:hover {
        background-color: #4B5675;
        color: white;
    }
    .stMetric {
        background-color: #1E2128;
        padding: 1rem;
        border-radius: 5px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        color: white;
    }
    .stMetric label {
        color: #8C94A6;
    }
    /* Table styles */
    .stTable {
        background-color: #1E2128;
        color: white;
    }
    table {
        background-color: #1E2128;
        color: white;
    }
    thead tr th {
        background-color: #3B4357;
        color: white;
    }
    tbody tr:nth-child(odd) {
        background-color: #1E2128;
    }
    tbody tr:nth-child(even) {
        background-color: #262B36;
    }
    .css-1pxazr7 {
        color: white;
    }
    /* Expander */
    .streamlit-expanderHeader {
        background-color: #1E2128;
        color: white;
    }
    .streamlit-expanderContent {
        background-color: #1E2128;
        color: white;
    }
    /* Sidebar */
    .css-1d391kg {
        background-color: #0E1117;
    }
    section[data-testid="stSidebar"] {
        background-color: #1E2128;
    }
    section[data-testid="stSidebar"] .css-1cpxqw2 {
        background-color: #1E2128;
    }
    /* Form */
    .css-12oz5g7 {
        background-color: #1E2128;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    /* Info boxes */
    .stAlert {
        background-color: #2D3648;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description with emojis
st.title("🌱 Indian Vegetarian Diet & Fitness Planner")
st.markdown("""
    Get your personalized diet plan, exercise routine, and health recommendations based on your profile.
    Let's work together to achieve your health goals! 🎯
""")

# Sidebar for additional information
with st.sidebar:
    st.header("💡 Quick Tips")
    st.markdown("""
        - Stay hydrated throughout the day 💧
        - Take regular breaks during work 🧘‍♂️
        - Practice mindful eating 🍽️
        - Get adequate sleep 😴
        - Stay consistent with your routine ⏰
    """)
    
    st.header("📱 Track Your Progress")
    st.markdown("""
        - Log your daily water intake
        - Record your exercise minutes
        - Track your meals
        - Monitor your weight
    """)

# Load food data
@st.cache_data
def load_food_data():
    try:
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Create the path to the CSV file
        csv_path = os.path.join(current_dir, "foods.csv")
        return pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error("Food database not found. Please make sure foods.csv exists.")
        return None
    except Exception as e:
        st.error(f"Error loading food database: {e}")
        return None

food_data = load_food_data()

# Main form for user input with improved layout
with st.form("user_info"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        weight = st.number_input("Weight (kg)", min_value=30, value=70)
        height = st.number_input("Height (cm)", min_value=100, value=170)
    
    with col2:
        activity = st.selectbox("Activity Level", ["Sedentary", "Moderate", "Active"])
        dietary_preference = st.selectbox("Dietary Preference", ["Vegetarian", "Vegan"], index=0)
        allergies = st.multiselect("Allergies", options=["Dairy", "Nuts", "Gluten", "Soy"])
        health_goal = st.selectbox("Health Goal", ["Maintain Weight", "Lose Weight", "Gain Weight"])
        budget = st.selectbox("Budget", ["Low", "Medium", "High"], index=1, 
                              help="Low: ≤₹15 per 100g, Medium: ≤₹25 per 100g, High: All foods")
    
    submitted = st.form_submit_button("Generate Plan")

# Process form submission
if submitted and food_data is not None:
    # Calculate BMR
    bmr = calculate_bmr(weight, height, age, gender)
    
    # Calculate daily calorie needs
    daily_calories = calculate_daily_calories(bmr, activity, health_goal)
    
    # Calculate water intake (30ml per kg of body weight)
    water_intake = weight * 30
    
    # Display user stats with improved metrics
    st.subheader(f"👋 Hello, {name}!")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Basal Metabolic Rate (BMR)", f"{bmr:.0f} calories")
    with col2:
        st.metric("Daily Calorie Needs", f"{daily_calories:.0f} calories")
    with col3:
        protein = (daily_calories * 0.15) / 4
        carbs = (daily_calories * 0.60) / 4
        fats = (daily_calories * 0.25) / 9
        st.metric("Protein Needs", f"{protein:.0f}g per day")
    with col4:
        st.metric("Water Intake", f"{water_intake:.0f}ml per day")
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🍽️ Diet Plan", "💪 Exercise Guide", "💧 Hydration & Health"])
    
    with tab1:
        # Generate and display diet plan
        diet_plan = generate_diet_plan(
            food_data,
            daily_calories,
            age,
            dietary_preference,
            allergies,
            activity,
            budget,
            "Indian"
        )
        
        if diet_plan:
            st.subheader("Your Personalized Diet Plan")
            
            # Display total cost
            total_cost = diet_plan.get("total_cost", 0)
            st.info(f"Estimated Daily Food Cost: ₹{total_cost:.0f}")
            
            # Create tabs for each meal
            meal_keys = [key for key in diet_plan.keys() if key != "total_cost"]
            meal_tabs = st.tabs(meal_keys)
            
            for i, meal_name in enumerate(meal_keys):
                with meal_tabs[i]:
                    meal_items = diet_plan[meal_name]
                    
                    if "foods" in meal_items:
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write(f"Total Calories: {meal_items['calories']:.0f}")
                            meal_df = pd.DataFrame(meal_items["foods"])
                            
                            if "price" in meal_df.columns:
                                meal_df["price"] = meal_df["price"].apply(lambda x: f"₹{x:.0f}")
                                st.table(meal_df[["food", "portion", "calories", "protein", "carbs", "fats", "price"]])
                            else:
                                st.table(meal_df[["food", "portion", "calories", "protein", "carbs", "fats"]])
                        
                        with col2:
                            # Adjust plot style for dark mode
                            plt.style.use("dark_background")
                            fig, ax = plt.subplots(figsize=(4, 4))
                            fig.patch.set_facecolor("#1E2128")
                            ax.set_facecolor("#1E2128")
                            
                            labels = ["Protein", "Carbs", "Fats"]
                            sizes = [
                                meal_items["macros"]["protein"],
                                meal_items["macros"]["carbs"],
                                meal_items["macros"]["fats"]
                            ]
                            colors = ["#FF9999", "#66B3FF", "#99FF99"]
                            ax.pie(sizes, labels=labels, colors=colors, autopct="%1.1f%%", startangle=90,
                                  textprops={'color': 'white'})
                            ax.axis("equal")
                            st.pyplot(fig)
                            
                            if "cost" in meal_items:
                                st.metric("Meal Cost", f"₹{meal_items['cost']:.0f}")
    
    with tab2:
        st.subheader("🏃‍♂️ Personalized Exercise Guide")
        
        # Exercise recommendations based on activity level
        if activity == "Sedentary":
            st.markdown("""
                ### Beginner's Exercise Routine
                
                **Morning (15-20 minutes):**
                1. Light stretching (5 minutes)
                2. Walking in place (5 minutes)
                3. Basic yoga poses (10 minutes)
                
                **Evening (20-30 minutes):**
                1. Brisk walking (15 minutes)
                2. Simple bodyweight exercises:
                   - 10 squats
                   - 10 push-ups (knee push-ups if needed)
                   - 10 lunges
                   - 30-second plank
                
                **Weekly Goals:**
                - 3-4 days of exercise
                - Gradually increase duration
                - Focus on consistency
            """)
        elif activity == "Moderate":
            st.markdown("""
                ### Intermediate Exercise Routine
                
                **Morning (30 minutes):**
                1. Dynamic stretching (5 minutes)
                2. Cardio (15 minutes):
                   - Jumping jacks
                   - High knees
                   - Mountain climbers
                3. Strength training (10 minutes):
                   - 15 squats
                   - 15 push-ups
                   - 15 lunges
                   - 45-second plank
                
                **Evening (30-40 minutes):**
                1. Brisk walking or jogging (20 minutes)
                2. Circuit training (15-20 minutes):
                   - 3 rounds of:
                     - 20 squats
                     - 20 push-ups
                     - 20 mountain climbers
                     - 1-minute plank
                
                **Weekly Goals:**
                - 4-5 days of exercise
                - Mix of cardio and strength
                - Include rest days
            """)
        else:  # Active
            st.markdown("""
                ### Advanced Exercise Routine
                
                **Morning (45-60 minutes):**
                1. Dynamic warm-up (10 minutes)
                2. High-intensity cardio (20 minutes):
                   - Burpees
                   - Jump squats
                   - Mountain climbers
                   - High knees
                3. Strength training (20-30 minutes):
                   - 3 sets of:
                     - 20 squats
                     - 20 push-ups
                     - 20 lunges
                     - 1-minute plank
                
                **Evening (45-60 minutes):**
                1. Running or cycling (30 minutes)
                2. Advanced circuit training (20-30 minutes):
                   - 4 rounds of:
                     - 25 burpees
                     - 25 squats
                     - 25 push-ups
                     - 1.5-minute plank
                
                **Weekly Goals:**
                - 5-6 days of exercise
                - High-intensity workouts
                - Active recovery on rest days
            """)
        
        # Cardio health tips
        st.subheader("❤️ Cardio Health Tips")
        st.markdown("""
            1. **Start Gradually:**
               - Begin with low-impact exercises
               - Increase intensity over time
               - Listen to your body
            
            2. **Proper Form:**
               - Maintain good posture
               - Keep movements controlled
               - Breathe properly
            
            3. **Recovery:**
               - Stay hydrated
               - Get adequate sleep
               - Include rest days
            
            4. **Progression:**
               - Track your progress
               - Set realistic goals
               - Celebrate small wins
        """)
    
    with tab3:
        st.subheader("💧 Hydration & Health Guidelines")
        
        # Water intake tracking
        st.markdown(f"""
            ### Daily Water Intake Goal: {water_intake:.0f}ml
            
            **Water Intake Schedule:**
            1. Morning (500ml):
               - 250ml on waking up
               - 250ml with breakfast
            
            2. Mid-morning (500ml):
               - Sip water throughout
            
            3. Lunch (500ml):
               - 250ml before lunch
               - 250ml with lunch
            
            4. Afternoon (500ml):
               - Regular sips
            
            5. Evening (500ml):
               - 250ml before dinner
               - 250ml with dinner
            
            6. Night (500ml):
               - Sip water as needed
        """)
        
        # Health tips
        st.subheader("🌿 General Health Tips")
        st.markdown("""
            **Nutrition:**
            - Eat mindfully
            - Include variety in meals
            - Practice portion control
            
            **Sleep:**
            - Aim for 7-9 hours
            - Maintain regular sleep schedule
            - Create a bedtime routine
            
            **Stress Management:**
            - Practice deep breathing
            - Take regular breaks
            - Stay connected with loved ones
            
            **Regular Check-ups:**
            - Monitor blood pressure
            - Check blood sugar
            - Regular health screenings
        """)
    
    # Add download button for complete plan
    def get_download_link():
        plan_text = f"Personalized Health & Fitness Plan for {name}\n\n"
        plan_text += f"BMR: {bmr:.0f} calories\n"
        plan_text += f"Daily Calorie Needs: {daily_calories:.0f} calories\n"
        plan_text += f"Water Intake: {water_intake:.0f}ml\n"
        plan_text += f"Budget Level: {budget}\n"
        plan_text += f"Estimated Daily Food Cost: ₹{total_cost:.0f}\n\n"
        
        # Add diet plan
        plan_text += "=== Diet Plan ===\n"
        for meal_name in meal_keys:
            meal_items = diet_plan[meal_name]
            plan_text += f"\n{meal_name}:\n"
            if "foods" in meal_items:
                for food in meal_items["foods"]:
                    price_str = f" (₹{food['price']:.0f})" if "price" in food else ""
                    plan_text += f"- {food['food']}: {food['portion']} ({food['calories']:.0f} calories){price_str}\n"
        
        # Add exercise plan
        plan_text += "\n=== Exercise Plan ===\n"
        if activity == "Sedentary":
            plan_text += "Beginner's Exercise Routine\n"
        elif activity == "Moderate":
            plan_text += "Intermediate Exercise Routine\n"
        else:
            plan_text += "Advanced Exercise Routine\n"
        
        # Add health tips
        plan_text += "\n=== Health Tips ===\n"
        plan_text += "- Stay hydrated throughout the day\n"
        plan_text += "- Follow the exercise routine regularly\n"
        plan_text += "- Maintain a balanced diet\n"
        plan_text += "- Get adequate sleep\n"
        plan_text += "- Practice stress management\n"
        
        b64 = base64.b64encode(plan_text.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="health_fitness_plan.txt" style="color: #66B3FF; text-decoration: none; padding: 0.5rem 1rem; background-color: #1E2128; border-radius: 5px; border: 1px solid #66B3FF;">Download Complete Plan</a>'
        return href
    
    st.markdown(get_download_link(), unsafe_allow_html=True)

# Add information about the planner
with st.expander("ℹ️ About This Planner"):
    st.markdown("""
        ### How it works
        
        This comprehensive health and fitness planner provides personalized recommendations based on:
        - Age and gender
        - Weight and height
        - Activity level
        - Dietary preferences and allergies
        - Health goals
        - Budget constraints
        
        ### Features
        - Personalized diet plan with Indian vegetarian options
        - Customized exercise routine based on activity level
        - Water intake recommendations
        - Cardio health tips
        - Complete health and fitness guidelines
        
        ### Budget Levels
        - **Low Budget**: Foods costing ₹15 or less per 100g
        - **Medium Budget**: Foods costing ₹25 or less per 100g
        - **High Budget**: All foods regardless of price
        
        ### Nutritional Balance
        The recommended diet follows a balanced macronutrient distribution:
        - 15% protein (beans, lentils, dairy, paneer)
        - 60% carbohydrates (rice, roti, vegetables)
        - 25% fats (oils, ghee, nuts)
    """) 