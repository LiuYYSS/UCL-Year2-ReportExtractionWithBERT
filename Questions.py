import docQuery_utils


def query(NGOName, model, context):
    content = reportContent(NGOName)

    if NGOName is not None:
        Questions = ["When was NAME founded?",
                     "what is the address of NAME", "What is the Phone Number",
                     "What is the E-mail", "What is NAME’s mission", "what is the NAME's goal",
                     "who is the contact for NAME",
                     "What is the name of our programme?",
                     "Which SDG (sustainable development goal) does NAME trying to achieve"]
        for Question in Questions:
            Question.replace("NAME", NGOName)
        bestPredictionText, nBestAnswerPredictionsText, nBestAnswerPredictionsProbability = docQuery_utils.getPredictions(
            context, Questions, model)


        # Start data
        content.NGOStartDate = docQuery_utils.getBestAnswer(nBestAnswerPredictionsText,
                                                            nBestAnswerPredictionsProbability, 0, 2)
        # NGO location
        content.NGOLocation = docQuery_utils.getBestAnswer(nBestAnswerPredictionsText,
                                                           nBestAnswerPredictionsProbability, 3, 4)

        # NGO Contact
        content.NGOPhoneNumber = bestPredictionText[6]
        content.NGOEMail = bestPredictionText[7]


        # NGO Mission
        content.NGOMission = bestPredictionText[8]
        content.NGOGoal = docQuery_utils.getBestAnswer(nBestAnswerPredictionsText,
                                                       nBestAnswerPredictionsProbability, 9, 10)



class reportContent(object):
    NGOName = ""
    NGOStartDate = ""
    NGOLocation = ""
    NGOPhoneNumber = ""
    NGOEMail = ""
    NGOMission = ""
    NGOGoal = ""
    Contact = []

    def __init__(self, name):
        self.NGOName = name
