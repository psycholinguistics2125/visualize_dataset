import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import tempfile
import base64

from src.utils import (
    load_config,
    load_features_and_meta,
    get_binary_file_downloader_html,
)


# Page title
st.title("Visualization of research dataset")
st.markdown(
    """
    This application was develop to help you interact with the dataset associated with this publication:
    
    ```
    Towards Unlocking the Linguistic Code of Post-Traumatic Stress Disorder: A Comprehensive Analysis and Diagnostic Approach.
    ```

    The code associated with this application is available on GitHub:  [github](https://github.com/psycholinguistics2125/vizualise_dataset)
    
    **contact:** psycholinguistic2125@gmail.com

    You can filter the data using the sidebar on the left. You can also visualize the data and export the filtered data to a CSV file.


    """
)


# Sidebar filters
st.sidebar.title("Filters")

# Load data

data = load_features_and_meta(load_config())


# Filter by sexe

sexe_all = st.sidebar.checkbox("Select All Sexe", value=True)
if sexe_all:
    sexe = data["sexe"].unique()
else:
    sexe = st.sidebar.selectbox("Select Sexe", data["sexe"].unique())

# Filter by age
age_range_all = st.sidebar.checkbox("Select All Ages", value=True)
if age_range_all:
    age_range = (min(data["age"]), max(data["age"]))
else:
    age_range = st.sidebar.slider(
        "Select Age Range",
        min(data["age"]),
        max(data["age"]),
        (min(data["age"]), max(data["age"])),
    )

# Filter by profession
profession_all = st.sidebar.checkbox("Select All Professions", value=True)
if profession_all:
    selected_profession = data["code_insee"].unique()
else:
    selected_profession = st.sidebar.selectbox(
        "Select Profession", data["code_insee"].unique()
    )


# Filter by degree
education_all = st.sidebar.checkbox("Select All Education", value=True)
if education_all:
    selected_education = data["education_degree"].unique()
else:
    selected_education = st.sidebar.selectbox(
        "Select education_degree", data["education_degree"].unique()
    )

# Filter by symptom
symptom_all = st.sidebar.checkbox("Select All Symptoms", value=True)
if symptom_all:
    selected_symptom = data.columns[5:]  # Assuming symptoms start from column 6
else:
    selected_symptom = st.sidebar.selectbox(
        "Select Symptom",
        data.filter(regex=r"probable").columns.tolist() + ["full_or_partial_PTSD"],
    )  # Assuming symptoms start from column 6

# Apply filters to the data
if age_range_all and profession_all:
    filtered_data = data  # No need to filter if all ages and professions are selected
else:
    filtered_data = data[
        (data["age"] >= age_range[0])
        & (data["age"] <= age_range[1])
        & (data["code_insee"].isin(selected_profession))
        & (data["education_degree"].isin(selected_education))
        & (data["sexe"].isin(sexe))
    ]

# Display filtered data
st.header("Filtered Data")
st.write(filtered_data)


# Display basic statistics
st.header("Basic Statistics for Filtered Data")
st.write(f"Total Number of People: {len(filtered_data)}")

st.header('Count of "critere A" Values')
exp_critereA_counts = filtered_data["exp_critereA"].value_counts()
st.write(exp_critereA_counts)

# Data visualization
st.header("Box Plot visualization")

# Select measure for y-axis
selected_measure = st.selectbox(
    "Select Measure for Y-axis", data.columns[18:], index=72
)  # Assuming measures start from column 9

# Select variable for hue
selected_hue = st.selectbox(
    "Select Variable for Hue", data.columns[1:7].tolist() + [None], index=6
)  # Assuming variables start from column 11

# Select symptom for x-axis
selected_symptom_2 = st.selectbox(
    "Select Symptom",
    data.filter(regex=r"probable").columns.tolist() + ["full_or_partial_PTSD"],
    index=7,
)

plt.figure(figsize=(12, 6))
sns.boxplot(data=data, x=selected_symptom_2, y=selected_measure, hue=selected_hue)
plt.title(
    f"Box Plot of {selected_measure} by {selected_symptom_2} (Hue: {selected_hue})"
)
plt.xticks(rotation=45)
st.pyplot(plt)

# Add more visualizations as needed

# Summary statistics
st.header("Summary Statistics")

# Display summary statistics for measures
selected_measure = st.selectbox(
    "Select Measure", data.columns[18:]
)  # Assuming measures start from column 9
st.write(f"Summary Statistics for {selected_measure}:")
st.write(filtered_data[selected_measure].describe().round(3))


export_format = st.selectbox("Select Export Format", ["CSV", "Excel"])
# Export filtered data
if st.button(f"Export Filtered Data as {export_format}"):
    with tempfile.TemporaryDirectory() as tmpdirname:
        export_path = os.path.join(tmpdirname, "filtered_data." + export_format.lower())
        if export_format == "CSV":
            filtered_data.to_csv(export_path, index=False)
        elif export_format == "Excel":
            filtered_data.to_excel(export_path, index=False)

        st.success(
            f"Filtered data exported as {export_format}! Click below to download."
        )
        with open(export_path, "rb") as f:
            st.download_button(
                f"Download {export_format}",
                f.read(),
                key=f"download_{export_format.lower()}.{export_format.lower()}",
                file_name=f"filtered_data.{export_format.lower()}",
            )


# About section
st.sidebar.markdown("### About")
st.sidebar.info("This Streamlit app allows you to interact with a research dataset.")

# Data source information
st.sidebar.markdown("### Data Source")
st.sidebar.info(
    "Dataset source: Programme 13-Novembre, https://www.memoire13novembre.fr/"
)


# Add an image at the end
st.sidebar.image("data/logo_13nov_program.png", use_column_width=True)
