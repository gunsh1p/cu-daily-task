import httpx

async def get_daily() -> str:
    data = {
        "query": "\n    query questionOfToday {\n  activeDailyCodingChallengeQuestion {\n    date\n    userStatus\n    link\n    question {\n      acRate\n      difficulty\n      freqBar\n      frontendQuestionId: questionFrontendId\n      isFavor\n      paidOnly: isPaidOnly\n      status\n      title\n      titleSlug\n      hasVideoSolution\n      hasSolution\n      topicTags {\n        name\n        id\n        slug\n      }\n    }\n  }\n}\n    ",
        "variables": {},
        "operationName": "questionOfToday",
    }
    async with httpx.AsyncClient() as client:
        r = await client.post("https://leetcode.com/graphql/", json=data)
        r_json = r.json()
    link = r_json["data"]["activeDailyCodingChallengeQuestion"]["link"]
    return "https://leetcode.com" + link