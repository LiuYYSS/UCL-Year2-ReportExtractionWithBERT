import docQuery_utils


def query(NGOName, model, context, nBestProbability):
    content = reportContent()
    content.information["ngo"]["NGO_NAME"] = NGOName

    if NGOName is not None:
        Questions = ["When was NAME founded?",
                     "what is the address of NAME", "What is the Phone Number",
                     "What is NAME’s mission",
                     "who is the contact for NAME",
                     "What is the name of our programme?",
                     "Which SDG (sustainable development goal) does NAME trying to achieve",
                     "who is funding NAME?", "Who is working for NAME?"]
        for i in range(len(Questions)):
            Questions[i] = Questions[i].replace("NAME", NGOName)

        bestPredictionText, nBestAnswerPredictionsText, nBestAnswerPredictionsProbability = docQuery_utils.getPredictions(
            context, Questions, model, nBestProbability)

        # Start data
        content.information["ngo"]["NGO_SINCE"] = bestPredictionText[0]

        # NGO location
        content.information["ngo"]["NGO_STREET_ADDRESS"] = bestPredictionText[1]

        # NGO Contact
        content.information["ngo"]["NGO_PHONE"] = bestPredictionText[2]

        # NGO Mission
        content.information["ngo"]["MISSION"] = bestPredictionText[3]
        content.information["ngo"]["FOCUS_AREA"] = bestPredictionText[6]

        # NGO contact
        content.information["ngo"]["NGO_CONTACT_NAME"] = bestPredictionText[4]

        # NGO Programme
        content.information["ngo"]["PROJECT_TITLE"] = nBestAnswerPredictionsText[5]

        content.information["sponsors"]["SPONSOR_NAME"] = bestPredictionText[7]

        content.information["ngo_staff"]["PERSON_NAME"] = nBestAnswerPredictionsText[8]

        # Project Part
        projectQuestions = []
        for project in content.information["ngo"]["PROJECT_TITLE"]:
            if project is not None and project != "":
                Questions = ["What is PNAME?", "When did PNAME start?",
                             "When will PNAME finish?",
                             "What is the status of PNAME?",
                             "who are PNAME trying to support?", "Which country is PNAME located?",
                             "which goal does PNAME support?", "who is PNAME trying to help?",
                             "how many people dose PNAME want to help?", "how many people has PNAME helped?",
                             "How much money did PNAME receive?"]
                for i in range(len(Questions)):
                    Questions[i] = Questions[i].replace("PNAME", project)
                projectQuestions+=Questions

        bestPredictionText, nBestAnswerPredictionsText, nBestAnswerPredictionsProbability = docQuery_utils.getPredictions(
            context, projectQuestions, model, nBestProbability)

        content.information["projects"]["PROJECT_DESCRIPTION"] = []
        content.information["projects"]["PROJECT_STATUS"] = []
        content.information["projects"]["PROJECT_START_DATE"] = []
        content.information["projects"]["PROJECT_END_DATE"] = []
        content.information["projects"]["PROJECT_SCOPE"] = []
        content.information["project_geo_info"]["PROJECT_ADDRESS"] = []
        content.information["classifications"]["SECTOR"] = []
        content.information["project_impact"]["PROJECT_TARGET_GROUPS"] = []
        content.information["project_impact"]["PROJECT_REACH_TARGET"] = []
        content.information["project_impact"]["PROJECT_REACH_ACTUAL"] = []
        content.information["project_finance"]["CURRENCY"] = []
        for i in range(len(bestPredictionText)):
            if i % len(Questions) == 0:
                content.information["projects"]["PROJECT_DESCRIPTION"].append(bestPredictionText[i])
            elif i % len(Questions) == 1:
                content.information["projects"]["PROJECT_START_DATE"].append(bestPredictionText[i])
            elif i % len(Questions) == 2:
                content.information["projects"]["PROJECT_END_DATE"].append(bestPredictionText[i])
            elif i % len(Questions) == 3:
                content.information["projects"]["PROJECT_STATUS"].append(bestPredictionText[i])
            elif i % len(Questions) == 4:
                content.information["projects"]["PROJECT_SCOPE"].append(bestPredictionText[i])
            elif i % len(Questions) == 5:
                content.information["project_geo_info"]["PROJECT_ADDRESS"].append(bestPredictionText[i])
            elif i % len(Questions) == 6:
                content.information["classifications"]["SECTOR"].append(bestPredictionText[i])
            elif i % len(Questions) == 7:
                content.information["project_impact"]["PROJECT_TARGET_GROUPS"].append(bestPredictionText[i])
            elif i % len(Questions) == 8:
                content.information["project_impact"]["PROJECT_REACH_TARGET"].append(bestPredictionText[i])
            elif i % len(Questions) == 9:
                content.information["project_impact"]["PROJECT_REACH_ACTUAL"].append(bestPredictionText[i])
            elif i % len(Questions) == 10:
                content.information["project_finance"]["CURRENCY"].append(bestPredictionText[i])

        # Staff
        staffQuestions = []
        for staff in content.information["ngo_staff"]["PERSON_NAME"]:
            Questions = ["What is PERSON’s role?", "What department does PERSON work in", "What are PERSON’s contact details"]
            for i in range(len(Questions)):
                Questions[i] = Questions[i].replace("PERSON", staff)
            staffQuestions.append(Questions)
        bestPredictionText, nBestAnswerPredictionsText, nBestAnswerPredictionsProbability = docQuery_utils.getPredictions(
            context, staffQuestions, model, nBestProbability)
        for i in range(len(bestPredictionText)):
            if i % len(Questions) == 0:
                content.information["ngo_staff"]["JOB_TITLE"] = bestPredictionText[i]
            elif i % len(Questions) == 1:
                content.information["ngo_staff"]["DEPARTMENT"] = bestPredictionText[i]
            elif i % len(Questions) == 2:
                content.information["ngo_staff"]["EMAIL"] = bestPredictionText[i]

        financeQuestions = []
        for currency in content.information["project_finance"]["CURRENCY"]:
            if currency is not None and currency != "":
                Questions = ["When did PNAME receive MONEY?", "When did PNAME stop receiving MONEY?"]
                for i in range(len(Questions)):
                    Questions[i] = Questions[i].replace("MONEY", currency)
                financeQuestions += Questions

        bestPredictionText, nBestAnswerPredictionsText, nBestAnswerPredictionsProbability = docQuery_utils.getPredictions(
            context, financeQuestions, model, nBestProbability)

        for i in range(len(bestPredictionText)):
            if i % len(Questions) == 0:
                content.information["project_finance"]["PERIOD_START"].append(bestPredictionText[i])
            elif i % len(Questions) == 1:
                content.information["project_finance"]["PERIOD_END"].append(bestPredictionText[i])
    return content


class reportContent(object):
    ngodict = {}
    projectdict = {}
    sponsorsdict = {}
    ngo_staffdict = {}
    project_geo_infodict = {}
    classificationsdict = {}
    project_impactdict = {}
    project_financedict = {}
    information = {"ngo": ngodict, "projects": projectdict, "sponsors":sponsorsdict, "ngo_staff":ngo_staffdict, "project_geo_info": project_geo_infodict, "classifications": classificationsdict, "project_impact": project_impactdict, "project_finance": project_financedict}