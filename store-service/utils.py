def clean_data(data, needed_data):
    cleaned_data = {}

    for col in needed_data:
        if col in data:
            cleaned_data[col] = data[col]

    return cleaned_data
