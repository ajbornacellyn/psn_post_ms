

from bson import ObjectId


def getPostPipeline(postId):
    pipeline = [
  {
    "$match": {
      "_id": postId
    }
  },
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
      "from": "content_element",
      "localField": "_id",
      "foreignField": "postId",
      "as": "contentelement"
    }
  },
  {
  "$sort": {
            "createdDate": -1
            }
    }
]

    return pipeline

def getPostsByOwner(owner_id):
    pipeline = [
        {
            "$match": {
                "ownerId": int(owner_id)
            }
        },
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
                "from": "content_element",
                "localField": "_id",
                "foreignField": "postId",
                "as": "contentelement"
            }
        },
        {
            "$sort": {
            "createdDate": -1
            }
        }
    ]

    return pipeline

    
    
    


def getPostContentElementPipeline():
    pipeline =pipeline = [
    {
    "$lookup": {
                "from": "content_element",
                "localField": "_id",
                "foreignField": "postId",
                "as": "content_elements"
            }
        },
        {
        "$lookup": {
            "from": "comment",
            "localField": "_id",
            "foreignField": "postId",
            "as": "comments"
        }
    },
    {
        "$unwind": {
            "path": "$comments",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$lookup": {
            "from": "reaction",
            "localField": "comments._id",
            "foreignField": "commentId",
            "as": "comments.reactions"
        }
    },
    {
        "$group": {
            "_id": "$_id",
            "idOriginalPost": {"$first": "$idOriginalPost"},
            "createdDate": {"$first": "$createdDate"},
            "updatedDate": {"$first": "$updatedDate"},
            "ownerId": {"$first": "$ownerId"},
            "location": {"$first": "$location"},
            "description": {"$first": "$description"},
            "contentElement": {"$first": "$content_elements"},
            "num_comments": {"$sum": 1},
            "num_reactions": {"$sum": {"$size": "$comments.reactions"}}
        }
    }
]

    return pipeline

def getCommentsPostPipeline(post_id):
    pipeline = [
         {
            "$match": {
                "postId": post_id
            }
        },

        {
            "$lookup": {
                "from": "reaction",
                "localField": "_id",
                "foreignField": "commentId",
                "as": "Reactions"
            }
        },
        {
            "$lookup": {
                "from": "report",
                "localField": "_id",
                "foreignField": "commentId",
                "as": "reports"
            }
        },
        {
            "$lookup": {
                "from": "contentelement",
                "localField": "_id",
                "foreignField": "commentId",
                "as": "contentElements"
            }
        }
    ]

    return pipeline



def getCommentPipeline(Post_id):
    pipeline = [
        {
            "$match": {
                "_id": Post_id
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