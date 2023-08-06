
def __setup__ (pref):
    import tfserver

    if "MODEL_DIR" in pref.config:
        tfserver.add_models_from_directory (pref.config.MODEL_DIR)
