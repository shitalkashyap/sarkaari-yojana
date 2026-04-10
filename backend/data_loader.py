import csv


def normalize_key(key):
    return key.strip().lower()


def load_schemes_from_csv(file_path):
    schemes = []

    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        # ✅ normalize headers
        reader.fieldnames = [normalize_key(h) for h in reader.fieldnames if h]

        for row in reader:
            row = {normalize_key(k): v for k, v in row.items() if k}

            scheme = {
                "scheme_name": row.get("scheme_name", ""),
                "scheme_id": row.get("slug", ""),
                "description": row.get("details", ""),
                "benefits": row.get("benefits", ""),
                "eligibility": row.get("eligibility", ""),
                "application_process": row.get("application", ""),
                "documents": row.get("documents", ""),
                "level": row.get("level", ""),
                "category": row.get("schemecategory", ""),
                "tags": row.get("tags", "")
            }

            # ✅ skip bad rows
            if not scheme["scheme_name"]:
                continue

            schemes.append(scheme)

    print(f"✅ Loaded {len(schemes)} CLEAN schemes")

    return schemes