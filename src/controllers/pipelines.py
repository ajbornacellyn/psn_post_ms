

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
      "as": "contentElement"
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
                "as": "contentElement"
            }
        },
        {
            "$sort": {
            "createdDate": -1
            }
        }
    ]

    return pipeline

    
    
    


def getPostcontentElementPipeline():
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
            "$lookup": {
                "from": "reaction",
                "localField": "_id",
                "foreignField": "postId",
                "as": "post.reactions"
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "idOriginalPost": { "$first": "$idOriginalPost" },
                "createdDate": { "$first": "$createdDate" },
                "updatedDate": { "$first": "$updatedDate" },
                "ownerId": { "$first": "$ownerId" },
                "location": { "$first": "$location" },
                "description": { "$first": "$description" },
                "contentElement": { "$first": "$content_elements" },
                "num_comments": { "$sum": { "$size": "$comments" } },
                "num_reactions": { "$sum": { "$size": "$post.reactions" } },
            }
        },
        {
            "$sort": {
                "num_reactions": -1,
                "num_comments": -1
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
                "from": "contentElement",
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

def getCommentsThreadPipeline(postId):
    pipeline = [
  {
    "$match": { "postId": postId }
  },
  {
    "$graphLookup": {
      "from": "comment",
      "startWith": "$_id",
      "connectFromField": "_id",
      "connectToField": "parentCommentId",
      "as": "commentTherad"
    }
  },
  {
    "$lookup": {
      "from": "content_element",
      "localField": "_id",
      "foreignField": "commentId",
      "as": "content_elements"
    }
  },
  {
    "$lookup": {
      "from": "reaction",
      "localField": "_id",
      "foreignField": "commentId",
      "as": "reactions"
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
    "$unwind": "$commentTherad"
  },
  {
    "$lookup": {
      "from": "content_element",
      "localField": "commentTherad._id",
      "foreignField": "commentId",
      "as": "commentTherad.content_elements"
    }
  },
  {
    "$lookup": {
      "from": "reaction",
      "localField": "commentTherad._id",
      "foreignField": "commentId",
      "as": "commentTherad.reactions"
    }
  },
  {
    "$lookup": {
      "from": "report",
      "localField": "commentTherad._id",
      "foreignField": "commentId",
      "as": "commentTherad.reports"
    }
  },
  {
    "$group": {
      "_id": "$_id",
      "post": { "$first": "$$ROOT" },
      "commentTherad": { "$push": "$commentTherad" }
    }
  },
  {
    "$project": {
      "_id": "$post._id",
      "idOriginalPost": "$post.idOriginalPost",
      "createdDate": "$post.createdDate",
      "updatedDate": "$post.updatedDate",
      "ownerId": "$post.ownerId",
      "location": "$post.location",
      "description": "$post.description",
      "content_elements": "$post.content_elements",
      "reactions": "$post.reactions",
      "reports": "$post.reports",
      "commentTherad": 1
    }
  }
]

    return pipeline


