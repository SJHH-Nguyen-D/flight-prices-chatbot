import chatterbot
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
import unirest

# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)

"""
Application feature requirements:

Statement:
	Travel related question about flight circuits/destinations, and hotels
Response: 
	Flights:
		flight price, 
		airline and 
		times and for 
	Hotels:
		hotel name and 
		price per night or 
		total price for the stay.
"""


bot = ChatBot(
    "Terminal",
    storage_adapter="chatterbot.storage.SQLStorageAdapter",
    logic_adapters=[
        {
            "import_path": "chatterbot.logic.BestMatch",
            "default_response": "I am sorry, but I do not understand.",
            "maximum_similarity_threshold": 0.90,
        },
        "chatterbot.logic.MathematicalEvaluation",
        "chatterbot.logic.TimeLogicAdapter",
        {
            "import_path": "chatterbot.logic.SpecificResponseAdapter",
            "input_text": "Google it",
            "output_text": "Ok, here is a link: https://google.com",  # doesn't quite work yet
        },
    ],
    database_uri="sqlite:///database.sqlite3",
)

booking_flight_convo = [
    "Hi, can I help you?",
    "I'd like to book a flight to Iceland.",
    "Your flight to Iceland has been booked. Is there anything else you want to know concerning flights?",
    "No. That is all, thank you.",
    "Thank you for using our services. It has been a pleasure. Please feel free to ask me anything anytime. You can call our offices at 1-800-999-7685 to talk to a human representative.",
]

flight_training_corpus_path = "/home/dennis/Documents/datascience_adventures/pythonscripts/datascience_job_portfolio/travel_chat_bot/app/flight_recommender.yml"


def do_the_training_thing():
    trainer = ListTrainer(bot)
    trainer.train(booking_flight_convo)
    trainer = ChatterBotCorpusTrainer(bot)
    trainer.train(flight_training_corpus_path)


def ceate_skyscan_session():
    """
	Using unirest and the skyscanner api to get live ticket quotes directly from flight agencies.
	A successful response contains no content. The session key to poll the results are provided in the Location header of the response. The last value of the location header contains the session key which is required when polling the session
	"""
    response = unirest.post(
        "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/v1.0",
        headers={
            "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
            "X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        params={
            "inboundDate": "2019-09-10",
            "cabinClass": "business",
            "children": 0,
            "infants": 0,
            "country": "US",
            "currency": "USD",
            "locale": "en-US",
            "originPlace": "SFO-sky",
            "destinationPlace": "LHR-sky",
            "outboundDate": "2019-09-01",
            "adults": 1,
        },
    )


def poll_skyscan_session_results(sessionkey):
    """
	Get itineraries from a created session.
	"""
    response = unirest.get(
        f"https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/pricing/uk2/v1.0/{sessionkey}?pageIndex=0&pageSize=10",
        headers={
            "X-RapidAPI-Host": "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
            "X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
        },
    )


def test(user_input="I would like to book a flight to Iceland."):
    """
	Opens conversation with a bot in terminal and can be closed by pressing ctrl-C
	"""
    print("Hi, how can I help you?")
    # The following loop will execute each time the user enters input in the terminal
    while True:
        try:
            user_input = input()

            bot_response = bot.get_response(user_input)

            print(bot_response)

        # Press ctrl-c or ctrl-d on the keyboard to exit
        except (KeyboardInterrupt, EOFError, SystemExit):
            break


if __name__ == "__main__":
    do_the_training_thing()
    test()


############ Useful ###################

# trainer = ChatterBotCorpusTrainer(bot)
# trainer.train("chatterbot.corpus.english")
# trainer.export_for_training('./my_trained_corpus_export.json') # outputs the training corpus to share with other bots

# if you have your training corpus stored at an address you can specify it as such
# trainer.train(
#     "./data/greetings_corpus/custom.corpus.json",
#     "./data/my_corpus/"
# )

# below uses a subset of the training corpus for faster and more specific responses
# trainer.train("chatterbot.corpus.english.conversations",
# 			  "chatterbot.corpus.english.greetings"
# )


# while True:
#     try:
#         bot_input = bot.get_response(input())
#         print(bot_input)

#     except(KeyboardInterrupt, EOFError, SystemExit):
#         break
