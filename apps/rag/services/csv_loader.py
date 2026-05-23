import pandas as pd


def load_csv_data():
    """
    Load college data from CSV and convert each row into
    a structured document dict for embedding.
    Handles NaN values cleanly so they don't pollute context.
    """

    df = pd.read_csv("data/College_Fees_Master_2026-27.csv")

    # Normalise column names - strip whitespace to avoid subtle mismatches
    df.columns = df.columns.str.strip()

    print(f"\nCSV Columns: {df.columns.tolist()}")
    print(f"Total rows loaded: {len(df)}")

    documents = []

    for _, row in df.iterrows():

        college_name    = str(row.get("College", "")).strip()
        location        = str(row.get("Location", "")).strip()
        state           = str(row.get("State", "")).strip()
        program_level   = str(row.get("Program Level", "")).strip()
        course          = str(row.get("Course / Specialization", "")).strip()
        fees            = str(row.get("Total Fee (INR)", "")).strip()

        raw_notes = row.get("Notes", "")
        notes = str(raw_notes).strip() if pd.notna(raw_notes) else ""

        lines = [
            f"College Name: {college_name}",
            f"Location: {location}",
            f"State: {state}",
            f"Program Level: {program_level}",
            f"Course / Specialization: {course}",
            f"Total Fee (INR): {fees}",
        ]
        if notes:
            lines.append(f"Notes: {notes}")

        content = "\n".join(lines)

        documents.append(
            {
                "college_name": college_name,
                "location": location,
                "state": state,
                "content": content,
            }
        )

    print(f"Documents built: {len(documents)}")
    return documents