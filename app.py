from connection2 import SpoonacularMetadataConnectionProvider
import streamlit as st
from connection import SpoonacularConnectionProvider
from requests import get
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

# Custom CSS styles
st.markdown(
    """
    <style>
    .stApp {
        max-width: 700px;
        margin: 0 auto;
        color: white;
        background-color: #008080; /* Background color */
    }
    .stTextInput>div>div>input {
        background-color: #f0f0f0;
        color: black;  /* Keep the user input text as black */
        font-size: 16px;
        padding: 12px 15px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    .stButton>button {
        background-color: #0078E7;
        color: white;
        font-size: 16px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .stMarkdown {
        color: white;
    }
    .footer {
        background-color: #444444; /* Footer background color */
        padding: 20px 0;
        text-align: center;
    }
    .footer p {
        color: white;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    """
    The main function to run the recipe information web app.

    This function sets up the Streamlit app, connects to the Spoonacular API,
    and handles user interactions to fetch and display recipe data.
    """
    api_connection = SpoonacularConnectionProvider(connection_name='recipeProvider')

    st.title("Recipedia")
    st.markdown("Enter your desired food name and we'll find you a recipe! :)")

    recipes_input = st.text_input("Enter your preferred food choice")

    if st.button("Get Recipes"):
        try:
            recipes = [city.strip() for city in recipes_input.split(",")]
            recipes_data = api_connection.query(recipes)
            if(len(recipes_data) != 0):
                st.success("Recipes fetched successfully!")
                display_recipes_data(recipes_data)
            else:
                st.error("No recipes found for the given query.")    
        except Exception as e:
            st.error(f"Error occurred: {e}")

def display_recipes_data(recipes_data):
    for city, data in recipes_data.items():
        if isinstance(data, str):
            st.markdown(data)
        else:
            st.image(data['image'])
            st.markdown(f"## Recipe Name: {data['title']}")
            st.markdown(f"## Recipe ID: {data['id']}")
            api_connection = SpoonacularMetadataConnectionProvider(connection_name='recipeProvider')

            with st.expander("See Recipe Details"):
                try:
                    recipe_data = api_connection.query(data['id'])

                    # Display recipe details
                    st.image(recipe_data['image'])
                    st.markdown(f"## Price per Serving: {recipe_data['pricePerServing']}")
                    st.markdown(f"## Health Score: {recipe_data['healthScore']}")
                    st.markdown(f"## Gluten Free: {recipe_data['glutenFree']}")
                    st.markdown(f"## Instructions:")
                    st.markdown(recipe_data['instructions'], unsafe_allow_html=True)
                    st.markdown(f"## Source URL:")
                    st.markdown(f"{recipe_data['sourceUrl']}")
                    st.markdown(f"## Ready in Minutes: {recipe_data['readyInMinutes']}")
                except Exception as e:
                    st.error(f"Error occurred while fetching recipe details: {e}")

    st.markdown("---")

def footer():
    st.markdown(
        """
        <div class="footer">
            <p><b>About Us:</b> Recipedia is your go-to platform for finding delicious recipes. We provide a wide range of recipes for every taste!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def layout(*args):
    for arg in args:
        if isinstance(arg, HtmlElement):
            st.markdown(str(arg), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
    footer()
