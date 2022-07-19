import requests
import json
import random

class TriviaQuestion:
    correct_answer = ""
    list_of_answers = []
    question = ""
    def get_data(self):
        #Get Questions
        response = requests.get("https://opentdb.com/api.php?amount=1&type=multiple")
        data = response.json()

        #Get Question
        self.question = self.replace_invalid_characters(data["results"][0]["question"])

        #Get Answer List
        self.list_of_answers = self.parse_answers(data)

        #Get Correct answer
        self.correct_answer = self.replace_invalid_characters(data["results"][0]["correct_answer"])

    def parse_answers(self, data):
        list = []
        for answer in data["results"][0]["incorrect_answers"]:
            answer = self.replace_invalid_characters(answer)
            list.append(answer)
        list.append(data["results"][0]["correct_answer"])
        random.shuffle(list)
        return list

    def replace_invalid_characters(self, string):
        string = string.replace("&#039;", "\'")
        string = string.replace("&quot;", "\"")
        string = string.replace("&amp;", "&")
        string = string.replace("&shy;", "-")
        string = string.replace("&eacute;", "é")
        string = string.replace("&deg;", "°")
        string = string.replace("&auml;", "ä")
        string = string.replace("&Auml;", "Ä")
        string = string.replace('&Uuml;', "Ü")
        string = string.replace("&uuml;", "ü")
        return string
