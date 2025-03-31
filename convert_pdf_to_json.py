import pdfplumber
import pandas as pd
import json

pdf_path = "/Users/kankofski/Desktop/Tech/MRDC/card_details.pdf"

data = []
with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        table = page.extract_table()
        if table:
            df = pd.DataFrame(table)
            data.append({"page": page_num, "content": df.to_dict(orient="records")})


with open("card_details.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("PDF successfully converted to JSON!")
