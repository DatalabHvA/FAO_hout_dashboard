import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Forestry_E_Europe.csv")
    return df

df = load_data()

# Melt time-series columns into long format
year_cols = [col for col in df.columns if col.startswith('Y') and col[1:5].isdigit()]
df_long = df.melt(
    id_vars=["Area", "Item", "Element", "Unit"],
    value_vars=year_cols,
    var_name="Year",
    value_name="Value"
)
df_long["Year"] = df_long["Year"].str[1:5].astype(int)
df_long["Value"] = pd.to_numeric(df_long["Value"], errors='coerce')

# Sidebar filters
st.sidebar.header("Filter Data")
selected_country = st.sidebar.selectbox("Select Country", sorted(df_long["Area"].unique()),30)
selected_item = st.sidebar.selectbox("Select Type of Wood", sorted(df_long[df_long["Area"] == selected_country]["Item"].unique()),32)
selected_element = st.sidebar.selectbox("Select Element (e.g. Production, Import Value)", 
                                        sorted(df_long[(df_long["Area"] == selected_country) & (df_long["Item"] == selected_item)]["Element"].unique()),3)

# Filter based on selection
filtered = df_long[
    (df_long["Area"] == selected_country) &
    (df_long["Item"] == selected_item) &
    (df_long["Element"] == selected_element)
]

# Display
st.title("European Forestry Production and Trade Dashboard")
st.write(f"**{selected_element}** for **{selected_item}** in **{selected_country}**")

# Plotting
fig, ax = plt.subplots()
ax.plot(filtered["Year"], filtered["Value"], marker='o')
ax.set_xlabel("Year")
ax.set_ylabel(f"{selected_element} ({filtered['Unit'].iloc[0]})")
ax.grid(True)
st.pyplot(fig)

# Show raw data
with st.expander("📄 Show raw data"):
    st.dataframe(filtered)
