import sqlite3
import requests
import time
import json

requestURL_Pluralizer = "http://classify.at.northwestern.edu/maserver/pluralizer"
requestURL_Conjugator = "http://classify.at.northwestern.edu/maserver/verbconjugator"


def pluralizer(noun):
    print(f"Pluralizer has been called for noun: {noun}")
    pluralizerSet = set()
    pluralTypes = ["singular", "plural"]
    payload = {"singular": noun, "media": "json"}
    response = requests.post(requestURL_Pluralizer, data=payload)
    result = json.loads(response.text)
    for pluralType in pluralTypes:
        pluralizerSet.add(result["PluralizerResult"][pluralType])

    time.sleep(2)
    return list(pluralizerSet)


# ['expensed', 'expense', 'expenses', 'expensing']
def conjugator(verb):
    print(f"Conjugator has been called for verb: {verb}")
    conjugatorSet = set()
    verbTenses = ["present", "presentParticiple", "past", "pastParticiple"]
    verbConjugations = ["firstPersonSingular", "secondPersonSingular", "thirdPersonSingular",
                        "firstPersonPlural", "secondPersonPlural", "thirdPersonPlural"]
    conjugatorSet.add(verb)
    for verbTense in verbTenses:
        payload = {"infinitive": verb, "verbTense": verbTense, "media": "json"}
        response = requests.post(requestURL_Conjugator, data=payload)
        result = json.loads(response.text)
        for conjugation in verbConjugations:
            conjugatorSet.add(result["VerbConjugatorResult"][conjugation])

    time.sleep(2)
    return list(conjugatorSet)
