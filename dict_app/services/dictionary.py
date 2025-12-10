import json
from urllib import request, error


class DictionaryEntry:
    def __init__(self, meanings, synonyms, antonyms, examples, pronunciation, pronunciation_audio):
        self.meanings = meanings
        self.synonyms = synonyms
        self.antonyms = antonyms
        self.examples = examples
        self.pronunciation = pronunciation
        self.pronunciation_audio = pronunciation_audio


def lookup_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    try:
        with request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        if isinstance(data, dict) and data.get("title") == "No Definitions Found":
            return None

        meanings_list = []
        synonyms_list = []
        antonyms_list = []
        examples_list = []
        pronunciation_text = ""
        pronunciation_audio = ""

        for phonetic in data[0].get("phonetics", []):
            text_value = phonetic.get("text")
            audio_value = phonetic.get("audio")
            if text_value:
                pronunciation_text = text_value
            if audio_value and not pronunciation_audio:
                pronunciation_audio = audio_value
            if pronunciation_text and pronunciation_audio:
                break

        for meaning in data[0]["meanings"]:

            # 🔥 FIX 1: synonyms/antonyms at meaning level
            synonyms_list.extend(meaning.get("synonyms", []))
            antonyms_list.extend(meaning.get("antonyms", []))

            for definition in meaning["definitions"]:

                # meaning
                meanings_list.append(definition.get("definition", ""))

                # example
                if definition.get("example"):
                    examples_list.append(definition["example"])

                # 🔥 FIX 2: synonyms/antonyms at definition level
                synonyms_list.extend(definition.get("synonyms", []))
                antonyms_list.extend(definition.get("antonyms", []))

        return DictionaryEntry(
            meanings=meanings_list,
            synonyms=sorted(list(set(synonyms_list))),
            antonyms=sorted(list(set(antonyms_list))),
            examples=examples_list,
            pronunciation=pronunciation_text,
            pronunciation_audio=pronunciation_audio,
        )

    except error.HTTPError:
        return None
    except Exception:
        return None



