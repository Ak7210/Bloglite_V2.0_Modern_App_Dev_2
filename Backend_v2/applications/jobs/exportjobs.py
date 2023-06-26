from applications.models.blogdb import Blog

from . import celery
import os


@celery.task
def export_blog_as_csv(blogId):
    blog = Blog.query.get(blogId)
    file = open("applications/static/exportCsv/download_blog_{}.csv".format(blogId), "w")
    file.write("Title, Caption, Image URL, Private, Creation \n")
    if blog:
        blogImageURL = "No image for this blog"
        if(blog.blogImageURL):  
            blogImageURL = os.path.join("http://localhost:5000/image/"+blog.blogImageURL)
        
        a = "No"
        if(blog.blogArchive == True):
            a = "Yes"

        creation = blog.blogCreation.strftime("%b %d %Y %H:%M:%S")

        file.write("{},{},{},{},{} \n".format(blog.blogTitle, blog.blogCaption, blogImageURL,a, creation))
    file.close()
    return "done"

