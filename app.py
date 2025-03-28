import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
BLOG_POSTS_FILE = 'blog_posts.json'

def load_blog_posts():
    """Load blog posts from JSON file."""
    if not os.path.exists(BLOG_POSTS_FILE):
        posts = [
            {'id': 1, 'author': 'John Doe', 'title': 'First Post', 'content': 'This is my first post.'},
            {'id': 2, 'author': 'Jane Doe', 'title': 'Second Post', 'content': 'This is another post.'},
            {'id': 3, 'author': 'Alice Smith', 'title': 'Third Post', 'content': 'Welcome to my blog!'}
        ]
        with open(BLOG_POSTS_FILE, 'w') as file:
            json.dump(posts, file, indent=4)
        return posts
    try:
        with open(BLOG_POSTS_FILE, 'r') as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        return []

def save_blog_posts(posts):
    """Save blog posts to JSON file."""
    with open(BLOG_POSTS_FILE, 'w') as file:
        json.dump(posts, file, indent=4)

def fetch_post_by_id(post_id):
    """Fetch a single post by ID."""
    blog_posts = load_blog_posts()
    for post in blog_posts:
        if post['id'] == post_id:
            return post
    return None

@app.route('/')
def index():
    """Display all blog posts."""
    return render_template('index.html', posts=load_blog_posts())

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new blog post."""
    if request.method == 'POST':
        blog_posts = load_blog_posts()
        new_id = max([post['id'] for post in blog_posts], default=0) + 1
        new_post = {
            'id': new_id,
            'author': request.form.get('author', 'Anonymous'),
            'title': request.form.get('title', 'Untitled'),
            'content': request.form.get('content', '')
        }
        blog_posts.append(new_post)
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Delete a blog post by ID."""
    blog_posts = load_blog_posts()
    updated_posts = [post for post in blog_posts if post['id'] != post_id]
    save_blog_posts(updated_posts)
    return redirect(url_for('index'))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Update a blog post by ID."""
    blog_posts = load_blog_posts()
    post = fetch_post_by_id(post_id)
    if not post:
        return "Post not found", 404
    if request.method == 'POST':
        post['author'] = request.form.get('author', post['author'])
        post['title'] = request.form.get('title', post['title'])
        post['content'] = request.form.get('content', post['content'])
        save_blog_posts(blog_posts)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)