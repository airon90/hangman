#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
from SPARQLWrapper import SPARQLWrapper, JSON


def get_results(endpoint_url, query):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


loop = True

query = """SELECT ?item ?code WHERE {
    ?item wdt:P31 wd:Q1288568;
          wdt:P218 ?code
} ORDER BY ?code"""

endpoint_url = "https://query.wikidata.org/sparql"
data = get_results(endpoint_url, query)
base = data["results"]["bindings"]

lang = {}
for elem in base:
    lang[elem["code"]["value"]] = elem["item"]["value"][31:]

langcode = ""
while langcode not in lang.keys():
    langcode = input("Insert language code: ")

query = """SELECT ?lexeme ?lemma WHERE {
    ?lexeme <http://purl.org/dc/terms/language> wd:""" + lang[langcode] + """.
    ?lexeme wikibase:lemma ?lemma .
}"""

endpoint_url = "https://query.wikidata.org/sparql"
data = get_results(endpoint_url, query)
base = data["results"]["bindings"]

words = []
for elem in base:
    vorto = {"w": elem["lemma"]["value"], "q": elem["lexeme"]["value"][31:]}
    word = vorto["w"]
    if (len(word) > 2 and word.isalpha()):
        words.append(vorto)

if len(words) == 0:
    print("No words for this language")
    loop = False
else:
    print(str(len(words)), "words found for this language")

points = 0
while loop:
    vorto = words[random.randint(0, len(words))]
    word = vorto["w"].lower()

    guess = [word[0]]

    for i in range(1, len(word) - 1):
        guess.append("_")

    guess.append(word[len(word) - 1])

    guesses = 10
    letters = [""]

    loop2 = True
    while (guesses > 0 and "_" in guess and loop2):
        letter = ""
        print(" ".join(guess))
        while letter in letters:
            letter = input("Letter: ").lower()
        if letter == "quit!" or letter == "exit!":
            loop = False
            loop2 = False
            print("Total points:", str(points))
            print("Bye bye")
        elif len(letter) > 1:
            if letter == word:
                print("You won! The word was", word, "(" + vorto["q"] + ")")
                points = points + 1
            else:
                print("You lose! The word was", word, "(" + vorto["q"] + ")")
                points = points - 1
            ok = input("Press Enter to continue.")
            loop2 = False
        else:
            letters.append(letter)

            if letter not in word[1:-1]:
                print("No letter found!")
                guesses = guesses - 1
            else:
                for i in range(1, len(word) - 1):
                    if word[i] == letter:
                        guess[i] = letter

    if loop2:
        if guesses == 0:
            print("You lose! The word was", word, "(" + vorto["q"] + ")")
            points = points - 1
        else:
            print("You won! The word was", word, "(" + vorto["q"] + ")")
            points = points + 1
        ok = input("Press Enter to continue.")
