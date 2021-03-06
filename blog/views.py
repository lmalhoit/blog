from flask import render_template

from blog import app
from .database import session
from .models import Post

import mistune
from flask import request, redirect, url_for

from flask import flash
from flask.ext.login import login_user
from werkzeug.security import check_password_hash
from .models import User

from flask.ext.login import login_required, current_user, logout_user


#@app.route("/")
#def posts():
#    posts = session.query(Post)
#    posts = posts.order_by(Post.datetime.desc())
#    posts = posts.all()
#    return render_template("posts.html",
#        posts=posts
#    )

@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
        posts=posts,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

#route to see only one post by clicking on title
@app.route("/post/<id>", methods=["GET"])
def one_post(id):
	post = session.query(Post).get(id)
	return render_template("one_post.html",
		post=post)


@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    print "hello"
    return render_template("add_post.html")

@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
        author=current_user
    )
    session.add(post)
    session.commit()

    return redirect(url_for("posts"))

@app.route("/post/<id>/edit", methods=["GET"])
@login_required
def edit_post_get(id):
    post = session.query(Post).get(id)
   #Building a view using render_template which is using edit_post.html to build the view and passing the argument post
   #Tryng to see if the current_user is the same as the author. If so, should allow edit, if not redirects to login
   #Why is post.author?
    print post.__dict__
    if post.author == current_user:
       return render_template("edit_post.html", post=post)
    else:
        return redirect(url_for("login_get"))


@app.route("/post/<id>/edit", methods=["POST"])
@login_required
def edit_post_put(id):
    #Retrieving the post with id
    post = session.query(Post).get(id)
    #Assigning new edits
    post.title = request.form["title"]
    post.content = mistune.markdown(request.form["content"])
    #Commits Edits
    session.commit()
    #Redirecting our app to another route - posts.html
    return redirect(url_for("posts"))

@app.route("/post/<id>/confirm", methods=["GET"])
def confirm(id):
    return render_template("confirm.html", postid=id)

@app.route("/post/<id>/delete", methods=["GET"])
@login_required
def delete_post(id):
    #Retrieve the post with ID
    post = session.query(Post).get(id)
    #Use session.delete to delete the post we just retrieved with variable post
    if post.author == current_user:
        session.delete(post)
    #Give a prompt to either confirm or cancel the delete
    #If user confirms, do the session.commit()
    #Commit the session
        session.commit()
    #Redirect back to the main posts site
        return redirect(url_for("posts"))
    #If user cancels, just redirect to "edit_post_put(id)"
    else:
        return redirect(url_for("posts"))


@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("posts"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("posts"))

