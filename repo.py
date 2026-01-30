# Install FPDF
!pip install fpdf

# Upload CSV
from google.colab import files
uploaded = files.upload()

# Script begins
import pandas as pd
from fpdf import FPDF

# Load data
df = pd.read_csv("/content/Zomato data .csv")

# Clean data
df["rate"] = df["rate"].str.extract(r"(\d+\.\d+)").astype(float)
df["approx_cost(for two people)"] = (
    df["approx_cost(for two people)"].astype(str).str.replace(",", "")
)
df["approx_cost(for two people)"] = pd.to_numeric(
    df["approx_cost(for two people)"], errors="coerce"
)
df_clean = df.dropna(subset=["rate", "approx_cost(for two people)", "votes"])

# Analyze
top_rated = df_clean.sort_values(by="rate", ascending=False).head(5)
most_voted = df_clean.sort_values(by="votes", ascending=False).head(5)
average_cost = df_clean["approx_cost(for two people)"].mean()
category_summary = df_clean["listed_in(type)"].value_counts().head(5)

# Format results
avg_cost_str = f"Rs. {average_cost:.2f}"
top_rated_list = [f"{i+1}. {row['name']} - {row['rate']}/5" for i, row in top_rated.iterrows()]
most_voted_list = [f"{i+1}. {row['name']} - {row['votes']} votes" for i, row in most_voted.iterrows()]
category_list = [f"{cat} - {count}" for cat, count in category_summary.items()]

# PDF Class
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Zomato Data Analysis Report", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def section(self, title, content_list):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, title, ln=True)
        self.set_font("Arial", "", 12)
        for line in content_list:
            self.cell(0, 10, line, ln=True)
        self.ln(5)

# Generate PDF
pdf = PDF()
pdf.add_page()
pdf.section("1. Average Cost for Two", [avg_cost_str])
pdf.section("2. Top Rated Restaurants", top_rated_list)
pdf.section("3. Most Voted Restaurants", most_voted_list)
pdf.section("4. Top Categories by Listing Type", category_list)

# Save and download PDF
pdf.output("Zomato_Report.pdf")

# Download the PDF
files.download("Zomato_Report.pdf")
