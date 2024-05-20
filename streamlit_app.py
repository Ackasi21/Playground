import requests
from bs4 import BeautifulSoup
import streamlit as st
import re
from fuzzywuzzy import process

# Dictionary to map state abbreviations to full names
states_dict = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", 
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA", 
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", 
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", 
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", 
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", 
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", 
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", 
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", 
    "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA", 
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

states_abbr_dict = {abbr: name for name, abbr in states_dict.items()}

def get_state_name(input_state):
    match_full, score_full = process.extractOne(input_state, states_dict.keys())
    match_abbr, score_abbr = process.extractOne(input_state.upper(), states_abbr_dict.keys())
    
    if score_full > score_abbr and score_full > 80:
        return match_full
    elif score_abbr > 80:
        return states_abbr_dict[match_abbr]
    else:
        return None

def format_description(description):
    description = description.replace("  ", " ").replace("\n", " ").strip()
    
    patterns = {
        "ID": r"^(\d{3,4} \w+)",
        "Type": r"(Tropical Weather Outlook)",
        "Location": r"(NWS National Hurricane Center Miami FL)",
        "Summary": r"(For the North Atlantic...Caribbean Sea and the Gulf of Mexico: [^$]+)"
    }
    
    formatted_desc = []

    for label, pattern in patterns.items():
        match = re.search(pattern, description)
        if match:
            formatted_desc.append(f"- **{label}:** {match.group(1)}")
    
    forecaster_match = re.search(r"\$\$ ([A-Za-z/]+)$", description)
    if forecaster_match:
        formatted_desc.append(f"- **Forecaster:** {forecaster_match.group(1)}")

    return "\n".join(formatted_desc)

def check_for_hurricanes(state, update_type):
    url = "https://www.nhc.noaa.gov/index-at.xml"
    response = requests.get(url)
    if response.status_code != 200:
        st.write("Failed to fetch data.")
        return

    soup = BeautifulSoup(response.content, features="html.parser")
    entries = soup.find_all('item')

    if update_type == "country":
        st.write("## General Hurricane Updates")
        for entry in entries:
            title = entry.title.get_text()
            description_text = BeautifulSoup(entry.description.get_text(), "html.parser").text
            st.markdown(f"### {title}")
            st.markdown(format_description(description_text))
    elif update_type == "state":
        state_alert = False
        hurricane_locations = []
        for entry in entries:
            title = entry.title.get_text()
            description_text = BeautifulSoup(entry.description.get_text(), "html.parser").text
            if state.lower() in description_text.lower() or states_dict[state].lower() in description_text.lower():
                state_alert = True
                hurricane_locations.append((title, description_text))
        
        if state_alert:
            st.markdown(f"<h1 style='color:red; font-size:32px;'>**Alert: Hurricane conditions relevant to {state} detected.**</h1>", unsafe_allow_html=True)
        
        st.write(f"## Specific State Updates for {state}")
        if hurricane_locations:
            st.write(f"### Hurricanes potentially affecting {state}:")
            for title, location in hurricane_locations:
                st.markdown(f"**{title}**")
                st.markdown(format_description(location))
        else:
            st.write(f"No hurricanes currently affecting {state}.")

st.title("Hurricane Monitoring Application")

hurricane_image_url = "https://ca-times.brightspotcdn.com/dims4/default/4ab00bb/2147483647/strip/true/crop/1173x892+0+0/resize/1200x913!/format/webp/quality/75/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2F8c%2Fd4%2F8c27b1054d66b867600166ab1614%2Fhurricane-hilary-satellite-noaa.jpg"  # Provided URL
st.image(hurricane_image_url, caption='', use_column_width=True)

user_state = st.text_input("Enter the state you want to monitor for hurricanes (e.g., Florida or FL):")

if st.button("Show Country-Wide Updates"):
    check_for_hurricanes(user_state, "country")

if st.button("Show State-Specific Updates"):
    if user_state:
        matched_state = get_state_name(user_state)
        if matched_state:
            check_for_hurricanes(matched_state, "state")
        else:
            st.write("State not recognized. Please enter a valid U.S. state name or abbreviation.")
    else:
        st.write("Please enter a state to monitor.")
