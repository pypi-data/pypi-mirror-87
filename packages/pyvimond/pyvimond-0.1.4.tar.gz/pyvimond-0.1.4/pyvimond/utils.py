def create_api_metadata(metadata):
    api_metadata = {
        'entries': {},
        'empty': True,
    }
    for key in metadata:
        value = metadata[key]
        api_metadata['entries'][key] = [
            {'value': value, 'lang': '*'}
        ]
    return api_metadata
