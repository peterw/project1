# Import necessary libraries and modules
import os
import replicate
import streamlit as st
from dotenv import load_dotenv
from elevenlabs import generate
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import OpenAI

# Load environment variables from a .env file
load_dotenv()

# Retrieve the OpenAI and Elevenlabs API keys from the environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
eleven_api_key = os.getenv("ELEVEN_API_KEY")

# Instantiate OpenAI object with a specific temperature for randomness
llm = OpenAI(temperature=0.9)

# Define a function to generate a recipe given a food and calories
def generate_recipe(food, calories):
    # Define a prompt for the language model to generate the recipe
    prompt = PromptTemplate(
        input_variables=["food", "calories"],
        template=""" 
         You are an experienced chef, create a recipe for the following food {food} that is under {calories} calories.
        """
    )
    # Instantiate a chain for the language model and prompt, and generate the recipe
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run({
    'food': food,
    'calories': calories
    })

# Define a function to generate audio given some text and a voice
def generate_audio(text, voice):
    audio = generate(text=text, voice=voice, api_key=eleven_api_key)
    return audio

# Define a function to generate images given a food
def generate_images(food):
    output = replicate.run(
        "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf",
        input={"prompt": food}
    )
    return output

# Define the streamlit app
def app():
    # Display a title
    st.title("Recipe Generator")

    # Form for user input
    with st.form(key='my_form'):
        food = st.text_input(label="Enter what you want to cook.", placeholder="Enter a food you want to cook")
        calories = st.number_input(label="Enter the calorie limit.", min_value=1, max_value=3000, value=200)

        options = ["Bella", "Antoni", "Arnold", "Adam", "Domi", "Elli", "Josh", "Rachel", "Sam"]
        voice = st.selectbox("Select a voice", options)

        submit_button = st.form_submit_button("Generate Recipe")

    # If user has submitted the form
    if submit_button:
        # Generate a recipe, audio and images and display them
        recipe = generate_recipe(food, calories) 
        audio = generate_audio(recipe, voice)

        st.markdown(recipe)

        st.audio(audio, format='audio/mp3')

        images = generate_images(food)
        st.image(images[0])

# Run the app
if __name__ == '__main__':
    app()
