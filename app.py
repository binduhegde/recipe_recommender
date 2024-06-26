
import streamlit as st
import pandas as pd
# Import the recommend function from your recommender.py file
from recommender import recommend

# # * BG IMAGE
# page_bg_img = '''
# <style>
# body {
# background-image: url("https://images.pexels.com/photos/1939485/pexels-photo-1939485.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
# background-size: cover;
# }
# </style>
# '''
# st.markdown(page_bg_img, unsafe_allow_html=True)


def main():
    # title html
    title = '<div style="background: linear-gradient(to right,#FC5C7D,#6A82FB); color: transparent; color: white; font-family: Helvetica; font-weight: bold; font-size: 40px; text-align: center; padding: 30px; letter-spacing:1px; width: 100%; margin-bottom: 20px;"><h2>Vegan Recipe Recommender</h2></div>'
    st.markdown(title, unsafe_allow_html=True)
    # subheading html
    subhead = '<p style="color: #FC5C7D;">Please choose your preferences and allergies in the sidebar</p>'
    st.markdown(subhead, unsafe_allow_html=True)

    # Sidebar for user input
    st.sidebar.header('User Preferences')
    pref_options = ['Fruits', 'Vegetables', 'Grains',
                    'Vegan Milk', 'Herbs and Spices',
                    'Sweeteners', 'Oils',
                    'Condiments and Sauces',
                    'Cereals']
    user_pref = st.sidebar.multiselect(
        'Select your favorite categories:', pref_options)
    allergy_options = ['Soy', 'Glutten']
    user_allergies = st.sidebar.multiselect(
        'Select your allergies if any:', allergy_options)
    # slider to set preferred time
    time = st.sidebar.slider('Preferred cook time in mins', 5, 130, 30, 10)

    # Empty element to keep sidebar open
    st.sidebar.markdown('---')  # Add a horizontal line

    # Button to trigger recommendation
    if st.sidebar.button('Get Recommendations'):
        # Call the recommend function with user preferences and allergies
        recommendations = get_recommendations(
            user_pref, user_allergies, time, top_n=20)

       # Display recommendations
        top_rec = '<p style="background: linear-gradient(to right,#FC5C7D, transparent); color: transparent; color: white; font-size: 100%; text-align: left; padding: 8px; letter-spacing:1px; width: 100%; margin-bottom: 20px;">Top Recommendations</p>'
        st.markdown(top_rec, unsafe_allow_html=True)
        for index, row in recommendations.iterrows():
            # Display recipe name with clickable link
            recipe_link = f"[{row['name']}]({row['link']})"

            # Format likes as percentage
            likes_percentage = f"{int(100*(row['likes']))}% likes"

            # Align likes to the right side of the page
            st.write(f"{recipe_link} - {likes_percentage}", anchor='right')

# since the df has column names with lowercase letters and userscores, 
# we convert them to the desired names
def get_recommendations(user_pref, user_allergies, time, top_n):
    for i, pref in enumerate(user_pref):
        if pref == 'Vegan Milk':
            user_pref[i] = 'dairy_alternatives'
        elif pref == 'Herbs and Spices':
            user_pref[i] = 'herbs_and_spices'
        elif pref == 'Condiments and Sauces':
            user_pref[i] = 'condiments_and_sauces'
        elif pref == 'Cereals':
            user_pref[i] = 'grains_and_cereals'
        else:
            user_pref[i] = user_pref[i].lower()
    # all allergies start with 'contains_' followed by the lowercase name
    for i, allergy in enumerate(user_allergies):
        user_allergies[i] = f'contains_{user_allergies[i].lower()}'

    return recommend(user_pref, user_allergies, time, top_n)


# Entry point of the Streamlit app
if __name__ == '__main__':
    main()
