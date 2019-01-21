

def _save_screenshots(screenshots):
    for filename, png in screenshots:
        with open(filename, 'wb') as f:
            f.write(png)


def _exact_result_and_save_screenshots(result):
    screenshots = result['screenshots']
    _save_screenshots(screenshots)
    result = result['origin_result']
    return result
