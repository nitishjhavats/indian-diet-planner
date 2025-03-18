# Indian Vegetarian Diet & Fitness Planner

A comprehensive web application that generates personalized Indian vegetarian diet plans based on user metrics, preferences, and budget constraints. The app also provides customized exercise routines, hydration guidelines, and general health tips.

## Features

- **Personalized Diet Plans**: Generate meal plans tailored to your age, gender, weight, height, activity level, and dietary preferences
- **Budget-Conscious Options**: Choose from low, medium, or high budget levels
- **Authentic Indian Vegetarian Foods**: Focus on traditional Indian vegetarian dishes
- **Exercise Recommendations**: Get customized workout routines based on your activity level
- **Hydration Guidelines**: Personalized water intake recommendations and scheduling
- **Health Tips**: General advice for nutrition, sleep, and stress management

## How It Works

The application uses the Mifflin-St Jeor equation to calculate your Basal Metabolic Rate (BMR) and then adjusts it based on activity level to determine daily calorie needs. It then generates a balanced meal plan from a database of Indian vegetarian foods, respecting your dietary preferences, allergies, and budget constraints.

## Technologies Used

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation
- **Matplotlib**: Data visualization
- **Custom Diet Planning Algorithm**: Food selection based on nutritional requirements and preferences

## Installation and Usage

1. Clone this repository
2. Install the required packages: `pip install -r requirements.txt`
3. Run the app: `streamlit run app.py`

## Screenshots



## Diet Plan Generation Logic

- Protein-rich foods are prioritized for active individuals
- Portion sizes are adjusted based on age (smaller portions for seniors and children)
- Meals are distributed throughout the day based on age group
- Food selections respect dietary preferences and avoid allergens
- Variety is ensured across food categories

## Data Sources

The application uses a custom food database (foods.csv) with information on:
- Food items
- Calories per 100g
- Protein, carbs, and fat content
- Food categories
- Meal suitability
- Diet type (vegan, vegetarian, non-vegetarian)
- Potential allergens

## Future Extensions

- Integration with food image recognition
- Machine learning for improved recommendations based on user feedback
- Weekly meal planning with shopping lists
- Integration with fitness tracking
- Recipe suggestions for meal combinations 
