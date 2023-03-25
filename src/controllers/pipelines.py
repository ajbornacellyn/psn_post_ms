

from bson import ObjectId


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

def getCommentsPostPipeline(post_id):
    pipeline = [
        {
            "$match": {
                "postId": ObjectId(post_id)
            }
        },
        {
            "$addFields": {
                "postId": { "$toString": "$postId" },
                "_id": { "$toString": "$_id" }
            }
        },
        {
            "$project": {
                "_id": 1,
                "ownerId": 1,
                "description": 1,
                "createdDate": 1,
                "updatedDate": 1
            }
        }
    ]
    return pipeline

def getCommentPipeline(commentId):
    pipeline = [
        {
            "$match": {
                "_id": ObjectId(commentId)
            }
        },
        {
            "$addFields": {
                "postId": { "$toString": "$postId" },
                "_id": { "$toString": "$_id" }
            }
        },
        {
            "$project": {
                "postId": 1,
                "ownerId": 1,
                "createdDate": 1,
                "updatedDate": 1,
                "infraction": 1,
                "description": 1
            }
        }
    ]
    return pipeline

def getReactionPipeline():
    pipeline = [
        {
            "$addFields": {
                "postId": { "$toString": "$postId" },
                "commentId": { "$toString": "$commentId" },
                "_id": { "$toString": "$_id" }
            }
        },
        {
            "$project": {
                "postId": 1,
                "commentId": 1,
                "ownerId": 1,
                "type": 1,
                "createdDate": 1,
                "updatedDate": 1,
            }
        }
    ]
    return pipeline