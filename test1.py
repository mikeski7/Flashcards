import requests

def translate(word, source_language='en', target_language='es', api_key='b8fba6eeb495da3683253c64f47a8ebb3eb21074df920e17e6efeeec8b92c5f7'):
    url = f'https://api.pons.com/v1/dictionary?l={source_language}{target_language}&q={word}'
    headers = {'X-Secret': api_key}

    response = requests.get(url, headers=headers)
    translations = []

    if response.status_code == 200:
        data = response.json()
        for dict in data[0]["hits"][0]["roms"][0]["arabs"][0]["translations"]:
            translations.append(dict["target"].split(" ")[0])
        return(translations)

    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

# Example usage
print(translate("language"))