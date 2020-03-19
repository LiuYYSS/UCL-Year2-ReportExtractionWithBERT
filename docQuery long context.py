import io
import json
import os
import sys
from simpletransformers.question_answering import QuestionAnsweringModel
import platform
import requests
import pdf2image as pdf2image
import Questions
import getDataFromDB
import submitDataToDB

# ms cognitive service configs
endpoint = 'https://uksouth.api.cognitive.microsoft.com/'
ocr_url = 'https://uksouth.api.cognitive.microsoft.com/vision/v2.1/ocr'
subscription_key = 'ffcc4bbd174c4b6e97d0a945aebf8b98'

# transformer configs
model = QuestionAnsweringModel('albert', 'ahotrod/albert_xxlargev1_squad2_512',
                               args={'max_seq_length': 512, "eval_batch_size": 3, "version_2_with_negative": True,
                                     'reprocess_input_data': True, 'overwrite_output_dir': True, 'silent': True})

# input dir configs
projectPath = os.path.abspath(os.path.dirname(sys.argv[0]))
inputPath = projectPath + os.path.sep + "input"

# program configs
nBestProbability = 0.1

pdfs = []
for filename in os.listdir(inputPath):
    if filename.endswith(".pdf"):
        pdfs.append(os.path.join(inputPath, filename))
    else:
        continue

for pdf in pdfs:
    pages = None
    outputString = ""
    pageNum = 0

    NGOName = getDataFromDB(pdf)

    if NGOName is "":
        continue

    if platform.system() == 'Windows':
        pathname = projectPath + os.path.sep + "poppler_win" + os.path.sep + "bin"
        pages = pdf2image.convert_from_path(pdf, 200, poppler_path=pathname, fmt="jpeg")
    else:
        pages = pdf2image.convert_from_path(pdf, 200, fmt="jpeg")

    while pageNum < len(pages):
        # pic to json
        imgByteArr = io.BytesIO()
        pages[pageNum].save(imgByteArr, format=pages[pageNum].format)
        imgByteArr = imgByteArr.getvalue()
        headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
        params = {'language': 'unk', 'detectOrientation': 'true'}
        response = requests.post(ocr_url, headers=headers, params=params, data=imgByteArr)
        response.raise_for_status()
        ocrResult = response.json()
        ocrResult = json.dumps(eval(str(ocrResult)))

        # json to string
        resultJSONObject = json.loads(ocrResult)
        regions = resultJSONObject['regions']
        for region in regions:
            lines = region['lines']

            for line in lines:
                words = line['words']
                for word in words:
                    text = word.get('text')
                    outputString += text + " "
        pageNum += 1

    information = Questions.query(NGOName, model, outputString, nBestProbability)
    submitDataToDB.submit(information, pdf)
