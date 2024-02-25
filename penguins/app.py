# IMPORT the packages we need (or might want to use) first.
# NOTE: Each package should be added to requirements.txt,
#       so the packages can be INSTALLED into the project virtual environment.

import faicons as fa  # For using font awesome in cards
import palmerpenguins  # This package provides the Palmer Penguins dataset
import pandas as pd
import plotly.express as px
import seaborn as sns  # Seaborn for making Seaborn plots
from shiny import App, ui, reactive, req
from shinywidgets import output_widget, render_widget  


# --------------------------------------------------------
# Get the Data
# --------------------------------------------------------

penguins_df = palmerpenguins.load_penguins()

# --------------------------------------------------------
# Define User Interface (ui)
# --------------------------------------------------------

app_ui = ui.page_fluid(
    ui.h1("PyShiny Penguins Dashboard (Core)"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.h2("Sidebar"),
            ui.input_select(
                "selected_attribute",
                "Select Plotly Attribute",
                ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g", "year"]),
            ui.input_numeric("plotly_bin_count", "Number of Plotly bins", 30),
            ui.input_slider("seaborn_bin_count", "Number of Seaborn bins", 1, 100, 20),
            ui.hr(),
            ui.input_checkbox_group(
                "selected_species",
                "Species in Scatterplot",
                ["Adelie", "Gentoo", "Chinstrap"],
                selected=["Adelie", "Gentoo", "Chinstrap"],
                inline=False,
            ),
            ui.hr(),
            ui.h6("Links:"),
            ui.a(
                "GitHub Source",
                href="https://github.com/denisecase/pyshiny-penguins-dashboard-core",
                target="_blank",
            ),
            ui.a(
                "GitHub App",
                href="https://denisecase.github.io/pyshiny-penguins-dashboard-core/",
                target="_blank",
            ),
            ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank"),
        ),
        ui.panel_main(
            ui.h2("Main Panel"),
            output_widget("plotly_scatterplot"), # Output widget
        )
    ),
    title="PyShiny Penguins", # Browser tab name
)

# --------------------------------------------------------
# Define Server function
# --------------------------------------------------------

def server(input, output, session):

    @output
    @render_widget  
    def plotly_scatterplot():
        return px.scatter(
            filtered_data(), 
            x="flipper_length_mm", 
            y="body_mass_g", 
            color="species", 
            title="Penguins Plot (Plotly Express)",
            labels={
                "flipper_length_mm": "Flipper Length (mm)",
                "body_mass_g": "Body Mass (g)",
            },
            size_max=8, # set the maximum marker size
        )

    # --------------------------------------------------------
    # Reactive calculations and effects
    # --------------------------------------------------------

    @reactive.calc
    def filtered_data():

        # The required function req() is used to ensure that
        # the input.selected_species() function is not empty.
        # req(input.selected_species())

        # If not empty, filter the data otherwise, just return the original data

        # Use the isin() method to filter the DataFrame
        # The method returns a boolean Series with the same index as the original DataFrame
        # Each row is:
        #   True if the species is in the input.selected_species() list
        #   False if the species is not
        isSpeciesMatch = penguins_df["species"].isin(input.selected_species())

        # Use the boolean filter mask in square brackets to filter the DataFrame
        # Return the filtered DataFrame when the function is triggered
        # Filter masks can be combined with the & operator for AND and the | operator for OR
        return penguins_df[isSpeciesMatch]


# Create the Shiny app from the UI and the server
app = App(app_ui, server, debug=True)
