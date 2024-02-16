import json
from openai import OpenAI
import os
import sqlite3
from time import time

print("Running dbai_proj.py!")

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

sqliteDbPath = getPath("GardenDB.db")
setupSqlPath = getPath("create_tables.sql")
setupSqlDataPath = getPath("dummy_data.sql")

if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath) 

sqliteCon = sqlite3.connect(sqliteDbPath)
sqliteCursor = sqliteCon.cursor()
with (
        open(setupSqlPath) as setupSqlFile,
        open(setupSqlDataPath) as setupSqlDataFile
    ):

    setupSqlScript = setupSqlFile.read()
    setupSQlDataScript = setupSqlDataFile.read()

sqliteCursor.executescript(setupSqlScript)
sqliteCursor.executescript(setupSQlDataScript)

def runSql(query):
    result = sqliteCursor.execute(query).fetchall()
    return result

########
configPath = getPath("config.json")
print(configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(
    api_key = config["openaiKey"],
    organization = config["orgId"]
)
########

def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)

    result = "".join(responseList)
    return result

commonSqlOnlyRequest = " Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not expalin it!"
strategies = {
    "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    "single_domain_double_shot": (setupSqlScript + 
                   " How many tomato plants are there? " + 
                   "\nSELECT COUNT(*) AS TotalTomatoPlants\nFROM Plant\nWHERE Name = 'Tomato';" +
                   commonSqlOnlyRequest)
}

questions = [
    "How many tomato plants are there?",
    "How many plants are in the butterfy garden?",
    "Which plants does John Smith care for?",
    "Which plants need to be watered every other day?",
    "Which plants have been watered in the last 3 days?",
    "Where are the carrots?",
    "What species of plants were planted in 2022?"
]

def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    return value

for strategy in strategies:
    print("-"*30 + strategy + "-"*30)
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    for question in questions:
        print(question)
        error = "None"
        try:
            sqlSyntaxResponse = getChatGptResponse(strategies[strategy] + " " + question)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print(sqlSyntaxResponse)
            queryRawResponse = str(runSql(sqlSyntaxResponse))
            print(queryRawResponse)
            friendlyResultsPrompt = "I asked a question \"" + question +"\" and the response was \""+queryRawResponse+"\" Please, just give a concise response in a more friendly way? Please do not give any other suggests or chatter."
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print(friendlyResponse)
        except Exception as err:
            error = str(err)
            print("AN ERROR OCCURED:", err)

        questionResults.append({
            "question": question, 
            "sql": sqlSyntaxResponse, 
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })
        print("-"*60)

    responses["questionResults"] = questionResults

    with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent = 2)
            

sqliteCursor.close()
sqliteCon.close()
print("Done!")