import json
import os


def removeIncludePredictions(predictions):
    for i in reversed(range(len(predictions))):
        for j in reversed(range(len(predictions))):
            if i != j and i < len(predictions) and j < len(predictions) and (predictions[j] in predictions[i]):
                predictions.remove(predictions[j])
    return predictions


def getPredictions(context, questions, model, nBestProbability):
    print(questions)
    qasJSONs = []
    for i in range(len(questions)):
        qasJSON = {
            'id': str(i),
            'is_impossible': False,
            'question': questions[i],
            'answers': []
        }
        qasJSONs.append(qasJSON)
    to_predict = [{'context': context, 'qas': qasJSONs}]

    os.makedirs('data', exist_ok=True)
    with open('data/train.json', 'w') as f:
        json.dump(to_predict, f)
    f.close()
    bestPrediction, nBestPredictions = model.eval_model('data/train.json')

    # Extract answer
    bestPredictionText = []
    for i in range(len(bestPrediction)):
        bestPredictionText.append(bestPrediction[str(i)])
    nBestAnswerPredictionsText = []
    nBestAnswerPredictionsProbability = []
    for i in range(len(nBestPredictions)):
        nBestAnswerPredictionText = []
        nBestAnswerPredictionProbability = []
        for BestPrediction in nBestPredictions[str(i)]:
            if BestPrediction['probability'] >= nBestProbability:
                nBestAnswerPredictionText.append(BestPrediction['text'])
                nBestAnswerPredictionProbability.append(BestPrediction['probability'])
        nBestAnswerPredictionsText.append(nBestAnswerPredictionText)
        nBestAnswerPredictionsProbability.append(nBestAnswerPredictionProbability)

    return bestPredictionText, nBestAnswerPredictionsText, nBestAnswerPredictionsProbability


def getBestOneAnswer(allAnswers, allProbability, starts, ends):
    bestAnswer = None
    bestProbability = 0
    for i in range(starts, ends + 1):
        if allProbability[i][0] > bestProbability and allAnswers[i][0] != " ":
            bestAnswer = allAnswers[i][0]
            bestProbability = allProbability[i][0]
    return bestAnswer
