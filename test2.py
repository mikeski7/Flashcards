import requests

def translate_with_pons(word, source_language='es', target_language='en', api_key='b8fba6eeb495da3683253c64f47a8ebb3eb21074df920e17e6efeeec8b92c5f7'):
    url = f'https://api.pons.com/v1/dictionary?l={source_language}{target_language}&q={word}'
    headers = {'X-Secret': api_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        translations = []
        for set in data['arabs']:
            translations.append(set['target'])
        print(translations)
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

# Example usage
spanish_word = "hola"
translations = translate_with_pons(spanish_word)
