from pydantic import BaseModel


class Blog(BaseModel):
    title: str
    body: str


# serializer
# class ShowBlog(BaseModel):
class ShowBlog(Blog):
    # title: str
    # body: str

    class Config():
        orm_mode = True
