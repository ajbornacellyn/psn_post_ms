

def getPostPipeline():
    pipeline = [
    {
        "$lookup": {
            "from": "comment",
            "localField": "_id",
            "foreignField": "postId",
            "as": "comments"
        }
    },
    {
        "$lookup": {
            "from": "report",
            "localField": "_id",
            "foreignField": "postId",
            "as": "reports"
        }
    },
    {
        "$lookup": {
            "from": "reaction",
            "localField": "_id",
            "foreignField": "postId",
            "as": "reactions"
        }
    },
    {
        "$lookup": {
            "from": "contentelement",
            "localField": "_id",
            "foreignField": "postId",
            "as": "contentElements"
        }
    },
    {
        "$addFields": {
            "id_str": {"$toString": "$_id"}
        }
    },
    {
        "$project": {
            "_id": 0,
            "id_str": 1,
            "createdDate": 1,
            "updatedDate": 1,
            "ownerId": 1,
            "location": 1,
            "description": 1,
            "comments": 1,
            "reports": 1,
            "reactions": 1,
            "contentElements": 1
        }
    }
]

    return pipeline
