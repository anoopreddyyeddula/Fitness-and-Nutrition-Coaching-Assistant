---
title: Fitness & Nutrition AI Coach
emoji: 🏋️‍♂️
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.42.1
app_file: app.py
pinned: false
short_description: 'An AI-powered Fitness and Nutrition Coach for personalized health guidance'
---

# Fitness & Nutrition AI Coach

## Overview
An intelligent chatbot that provides personalized fitness and nutrition guidance using the Google Gemini API and Streamlit. Get expert advice on workouts, meal planning, and healthy lifestyle choices.

## Features
- 💪 Personalized workout recommendations
- 🥗 Nutrition and diet guidance
- 📊 Goal-based advice (weight loss, muscle gain, general fitness)
- 💬 Interactive chat interface with real-time responses
- 📝 Chat history with edit functionality
- 🎯 BMI Calculator with personalized recommendations
- 💪 Custom workout plan generator

## Setup
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Google API key in `.streamlit/secrets.toml`:
   ```toml
   [google]
   api_key = "your-api-key-here"
   ```
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage
- Start a conversation by asking any fitness or nutrition-related question
- Use the BMI calculator for personalized health insights
- Generate custom workout plans based on your goals and equipment
- Edit previous messages to refine your queries
- Get evidence-based advice for your health journey

## Technologies
- Streamlit
- Google Gemini API
- Python
- Gemini 1.5 Pro Model

## Features in Detail

### Chat Interface
- Real-time conversation with AI fitness coach
- Edit functionality for previous messages
- Clean, modern interface similar to ChatGPT/Gemini

### BMI Calculator
- Instant BMI calculation
- Health status indication
- Personalized recommendations based on results

### Workout Generator
- Customizable workout plans
- Equipment-based exercises
- Difficulty level adjustment
- Downloadable workout plans

## License
MIT License
