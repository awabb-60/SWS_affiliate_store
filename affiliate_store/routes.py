from affiliate_store import app, db, bc
from affiliate_store.forms import AdminRegistrationForm, AdminLoginForm, AddBlogForm, UpdateBlogForm, AddTopicForm
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from affiliate_store.models import Admin, Blog, Topic, AdminLogs
from affiliate_store.utils import save_image, get_related_blogs, delete_image


@app.route("/")
@app.route("/home", methods=['POST', 'GET'])
def home():
    if request.method == 'POST' and request.form.get('search-term'):
        search_data = request.form.get('search-term')
        return redirect(url_for('search', search_data=search_data))

    number_of_TR = 5
    per_page = 7
    title = 'Smart Watch Sensei'
    topics = Topic.query.all()
    page = request.args.get('page', 1, type=int)
    trending_blogs = Blog.query.order_by(Blog.clicks.desc())
    recent_blogs = Blog.query.order_by(Blog.date_posted.desc()).paginate(per_page=per_page, page=page)

    return render_template('home.html', title=title, trending_blogs=trending_blogs[:number_of_TR], recent_blogs=recent_blogs, topics=topics)


@app.route("/about")
def about():
    title = 'SWS-About'

    return render_template('about.html', title=title)


@app.route("/search_query=<string:search_data>", methods=['POST', 'GET'])
def search(search_data):
    search_blogs = get_related_blogs(search_data)
    topics = Topic.query.all()

    title = 'Smart Watch Sensei'

    return render_template('search.html', title=title, search_blogs=search_blogs, topics=topics)


@app.route('/topics')
def topics():
    topics = Topic.query.all()
    return render_template('topics.html', topics=topics)


@app.route('/edit_topic<int:topic_id>', methods=['POST','GET'])
def update_topic(topic_id):
    topic = Topic.query.filter_by(id=topic_id).first()
    form = AddTopicForm()
    if form.validate_on_submit():
        log_info = f'{current_user.username} has updated the topic: {form.name.data}'.title()
        log = AdminLogs(admin_name=current_user.username, log_info=log_info)
        db.session.add(log)

        topic.name = form.name.data
        topic.topic_tags = form.topic_tags.data

        db.session.commit()
        return redirect(url_for('admin_control'))

    form.name.data = topic.name
    form.topic_tags.data = topic.topic_tags
    return render_template('update_topic.html', topic=topic, form=form)


@app.route('/delete_topic')
def delete_topic():
    id = request.args.get('topic_id')
    topic = Topic.query.filter_by(id=id).first()
    db.session.delete(topic)
    db.session.commit()
    return redirect(url_for('admin_control'))


@app.route('/add_topic', methods=['POST', 'GET'])
def add_topic():
    form = AddTopicForm()
    if form.validate_on_submit():
        log_info = f'{current_user.username} has added the topic: {form.name.data}'.title()
        log = AdminLogs(admin_name=current_user.username, log_info=log_info)
        db.session.add(log)

        name = form.name.data
        topic_tags = form.topic_tags.data
        topic = Topic(name=name, topic_tags=topic_tags)
        db.session.add(topic)
        db.session.commit()
        return redirect(url_for('admin_control'))
    return render_template('add_topic.html', form=form)


@app.route("/kookariakook")
def admin():
    return render_template('admin.html')


@app.route("/read_blog/<int:blog_id>")
def read_blog(blog_id):

    blog = Blog.query.get_or_404(blog_id)
    blog.clicks += 1
    db.session.commit()

    search_data = f'{blog.title} {blog.tags}'
    related_blogs = get_related_blogs(search_data.lower())
    related_blogs.remove(blog)

    related_blogs_number = 4
    title = f'SWS-{blog.title}'
    return render_template('read_blog.html', title=title, blog=blog, related_blogs=related_blogs[:related_blogs_number])


@app.route("/addblog", methods=['GET', 'POST'])
# @login_required
def add_blog():
    form = AddBlogForm()
    if request.method == 'POST':
        content = request.form.get('editordata')
        if form.validate_on_submit():
            log_info = f'{current_user.username} has added the Blog: {form.title.data}'.title()
            log = AdminLogs(admin_name=current_user.username, log_info=log_info)
            db.session.add(log)

            title = form.title.data.title()
            first_par = form.first_par.data
            tags = form.tags.data

            blog = Blog(title=title, first_par=first_par, content=content, tags=tags)
            db.session.add(blog)
            db.session.commit()
            return redirect(url_for('admin_control'))
    return render_template('add_blog.html', form=form)


@app.route("/editblog", methods=['POST', 'GET'])
# @login_required
def edit_blog():
    blogs = Blog.query.order_by(Blog.date_posted.desc())

    if request.method == 'POST' and request.form.get('edit-search'):
        search_data = request.form.get('edit-search')
        blogs = get_related_blogs(search_data)
        return render_template('edit_blog.html', blogs=blogs)

    return render_template('edit_blog.html', blogs=blogs)


@app.route("/deleteblog/<int:blog_id>")
# @login_required
def delete_blog(blog_id):
    blog = Blog.query.filter_by(id=blog_id).first()

    log_info = f'{current_user.username} has deleted the blog: {blog.title}'.title()
    log = AdminLogs(admin_name=current_user.username, log_info=log_info)
    db.session.add(log)

    db.session.delete(blog)
    db.session.commit()
    return redirect(url_for('edit_blog'))


@app.route("/yn/<int:blog_id>", methods=['GET', 'POST'])
# @login_required
def y_n(blog_id):
    return render_template('y_n.html', id=blog_id)


@app.route("/updateblog/<int:blog_id>", methods=['GET', 'POST'])
# @login_required
def update_blog(blog_id):
    form = UpdateBlogForm()
    blog = Blog.query.filter_by(id=blog_id).first()
    if request.method == 'POST':
        if form.validate_on_submit():
            log_info = f'{current_user.username} has updated the blog: {form.title.data}'.title()
            log = AdminLogs(admin_name=current_user.username, log_info=log_info)
            db.session.add(log)

            if form.image_file.data:
                old_file_name = blog.image_file
                if old_file_name != 'test_img.jpg':
                    delete_image(f'affiliate_store\\static\\images\\{old_file_name}')
                image_file = save_image(form.image_file.data)
                blog.image_file = image_file

            blog.title = form.title.data.title()
            blog.first_par = form.first_par.data
            blog.content = request.form.get('editordata')
            blog.tags = form.tags.data
            db.session.commit()
            return redirect(url_for('admin_control'))

    elif request.method == 'GET':
        form.title.data = blog.title
        form.first_par.data = blog.first_par
        form.tags.data = blog.tags
        form.content_holder.data = blog.content
    return render_template('Update_blog.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():

        # name = os.environ('AF_NAME')
        # pass1 = os.environ('AF_PASS1')
        # pass2 = os.environ('AF_PASS2')
        name = 'awab'
        pass1 = 'pass1'
        pass2 = 'pass2'
        if form.username.data == name and form.password1.data == pass1 and form.password2.data == pass2:
            admin = Admin.query.filter_by(id=1).first()
            login_user(admin)

            log_info = f'{admin.username} has login!!'
            log = AdminLogs(admin_name=current_user.username, log_info=log_info)
            db.session.add(log)
            db.session.commit()

            return redirect(url_for('admin_control'))
        else:
            flash('something is wrong!')

    return render_template('admin_login.html', title='Admin Login', form=form)


@app.route('/register', methods=['GET', 'POST'])
# @login_required
def register():
    form = AdminRegistrationForm()
    if form.validate_on_submit():
        log_info = f'{form.username.data} has registered as a new admin !!'
        log = AdminLogs(admin_name=current_user.username, log_info=log_info)
        db.session.add(log)

        username = form.username.data
        password1 = bc.generate_password_hash(form.password1.data).decode('utf-8')
        password2 = bc.generate_password_hash(form.password2.data).decode('utf-8')
        admin = Admin(username=username, password1=password1, password2=password2)
        db.session.add(admin)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template('admin_register.html', form=form, title='Register')


@app.route("/logout")
def logout():
    log_info = f'{current_user.username} has logout !!'
    log = AdminLogs(admin_name=current_user.username, log_info=log_info)
    db.session.add(log)
    db.session.commit()

    logout_user()
    return redirect(url_for('admin'))


@app.route("/logs")
@login_required
def logs():
    logs = AdminLogs.query.order_by(AdminLogs.log_date.desc())
    return render_template('logs.html', logs=logs)


@app.route("/adminc")
# @login_required
def admin_control():
    user = current_user
    return render_template('adminc.html', user=user)
