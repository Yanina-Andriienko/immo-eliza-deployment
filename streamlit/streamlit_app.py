import streamlit as st
import requests
from PIL import Image


# Custom CSS

image_path = 'image.jpeg'
image = Image.open(image_path)

st.markdown("""
    <style>
    /* Background color */
    body, .stApp {
        background-color: #f0f2f6 !important;
    }
    
    /* Title color */
    h1 {
        color: green !important;
    }
    </style>
    """, unsafe_allow_html=True)

# App title
st.title('Immo Eliza Property Price Prediction')

# Create two columns for the image and the text with a new layout
col1, col2 = st.columns([2, 3])  # Adjust the column ratios here as needed

# Load and display image in the first column
image_path = 'image.jpeg'
image = Image.open(image_path)

with col1:
    st.image(image)

with col2:
    st.markdown("""
    Welcome to the Immo Eliza Property Price Prediction tool! This application allows you to estimate the market value of a property based on various factors such as the area, number of bedrooms, amenities, and more.

    Simply enter the details about the property in the form below and hit "Predict Price" to see the estimated value. This tool is designed to help both real estate professionals and individuals get a quick price estimate for properties in Belgium.

    **Instructions:**
    - Fill in the property details in the form.
    - Click on "Predict Price" to get the estimation.

    If you have any questions or feedback, please feel free to reach out.
    """)

district_options = [
    'Aalst', 'Antwerp', 'Arlon', 'Ath',
    'Bastogne', 'Brugge', 'Brussels',
    'Charleroi', 'Dendermonde', 'Diksmuide',
    'Dinant', 'Eeklo', 'Gent',
    'Halle-vilvoorde', 'Hasselt', 'Huy',
    'Ieper', 'Kortrijk', 'Leuven',
    'Liège', 'Maaseik', 'Marche-en-Famenne',
    'Mechelen', 'Mons', 'Mouscron',
    'Namur', 'Neufchâteau', 'Nivelles',
    'Oostend', 'Oudenaarde', 'Philippeville',
    'Roeselare', 'Sint-Niklaas', 'Soignies',
    'Thuin', 'Tielt', 'Tongeren',
    'Tournai', 'Turnhout', 'Verviers',
    'Veurne', 'Virton', 'Waremme'
]


#  fields expander
with st.form("property_details", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        state_construction = st.selectbox('State of Construction', options=[
                                          "New", "Good", "To renovate"])
        living_area = st.number_input('Living Area (in sqm)', min_value=10)
        bedrooms = st.number_input('Number of Bedrooms', min_value=1, step=1)
        bathrooms = st.number_input('Number of Bathrooms', min_value=1, step=1)
        epc = st.selectbox('EPC Rating', options=[
                           "A", "B", "C", "D", "E", "F"])
        area_total = st.number_input('Total Area (in sqm)', min_value=10)
        district = st.selectbox('District', options=district_options)

    with col2:
        has_garden = st.checkbox('Has Garden')
        kitchen = st.checkbox('Has Kitchen')
        fireplace = st.checkbox('Has Fireplace')
        swimmingpool = st.checkbox('Has Swimming Pool')
        has_terrace = st.checkbox('Has Terrace')
        has_attic = st.checkbox('Has Attic')
        has_basement = st.checkbox('Has Basement')

    submitted = st.form_submit_button("Predict Price")

if submitted:
    # Construct the request payload
    payload = {
        "state_construction": state_construction,
        "living_area": living_area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "has_garden": has_garden,
        "kitchen": kitchen,
        "fireplace": fireplace,
        "swimmingpool": swimmingpool,
        "has_terrace": has_terrace,
        "has_attic": has_attic,
        "has_basement": has_basement,
        "epc": epc,
        "area_total": area_total,
        "district": district.lower()
    }

    # Endpoint of API

    url = 'http://localhost:8000/predict'

    # Make the POST request
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        prediction = response.json()['prediction']
        st.success(f"Estimated Property Price: €{prediction}")
    else:
        st.error("Error in prediction")
