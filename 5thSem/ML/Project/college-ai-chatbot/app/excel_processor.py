import pandas as pd


def process_excel(file_path):
    documents = []

    excel_file = pd.ExcelFile(file_path)

    for sheet_name in excel_file.sheet_names:

        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name
        )

        # Remove completely empty rows and columns
        df = df.dropna(how="all")
        df = df.dropna(axis=1, how="all")

        for _, row in df.iterrows():

            parts = []

            for column in df.columns:

                value = row[column]

                if pd.notna(value):
                    parts.append(
                        f"{column}: {value}"
                    )

            if parts:

                text = " | ".join(parts)

                documents.append({
                    "text": text,
                    "source": file_path,
                    "sheet": sheet_name
                })

    return documents