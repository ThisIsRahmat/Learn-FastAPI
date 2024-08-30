from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

# schemas are used for data validation
class Post(BaseModel):
    title: str
    content: str
    # this is an optional schema field, if user doesn't provide a value, defaults to True
    published: bool = True
    #this is a fully optional field and if 
    #the user doesn't provide it, it defaults to Optional
    rating: Optional[int] = None

# an array of posts for savign things in memeory ( if you don't want to use a db)
my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "title of post 2", "content": "content of post 2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p 

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 
# this is path operation - it's the function + the path decorator e.g @app.get()

# the @ is decorator, app referneces our FastAPi instance, .get is the method  - it turns the function 
# from a plain old function to a FastAPI function
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get('/posts')
def get_posts():
    return {"data":  my_posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # .dict() converts the pydantic model to dictonary 
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": my_posts}


# becareful with the order of the routes
#fastapi works tops down and sticks with the first match

# @app.get("/posts/latest")
# def get_latest_post():
#     post = my_posts[len(my_posts)-1]
#     return {"detail": post}


#if you want to get an individual post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):


    #anytime we have a path parameter e.g {id}
    # it is always returned as a string so you have to first 
    # convert it to int before fetching the post

     
    # post = find_post(int(id))

    # however you can work around havign to convert the int by including the
    # paramter type in the function e.g (id: int)
    # this will do the valuation and converting for us
 
    post = find_post(id)
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found" }
    return {"data": post }

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    #find index in the array that has the specific id
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    # convert data recived from frontend to regular python dictonary 
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] =post_dict
    return { "data": post_dict}
