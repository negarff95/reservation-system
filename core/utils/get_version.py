def get_version(file_path):
    try:
        with open(file_path) as version:
            return version.read()
    except Exception as e:
        return "0.0.0"