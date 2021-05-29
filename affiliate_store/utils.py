import os
import secrets
from PIL import Image
from affiliate_store import app
from affiliate_store.models import Blog


def delete_image(file_name):
    current_dir_path = os.getcwd()
    file_path = os.path.join(current_dir_path, file_name)
    try:
        os.remove(file_path)
    except OSError:
        pass


def save_image(form_img):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_img.filename)
    image_fname = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/images', image_fname)
    output_size = (1080, 1080)
    i = Image.open(form_img)
    i.thumbnail(output_size)
    i.save(image_path)

    return image_fname


def get_related_blogs(search):
    blogs = Blog.query.all()
    sorting_list = []
    ranked_blogs = []
    for b in blogs:
        ranking_value = 0

        # ranking pased on tags
        tags = b.tags
        # the thing between tags
        tags = tags.split(' ')
        for word in search.split(' '):
            for tag in tags:
                if word != 'watch':
                    for idx, litter in enumerate(word):
                        if idx == tag.find(litter):
                            ranking_value += 5

        # ranking pased on title
        title = b.title
        for word in search.split(' '):
            if word in title:
                ranking_value += 1
        sorting_list.append((b.id, ranking_value))

    # sorting
    largest_RV = 0
    for l in sorting_list:
        if l[1] > largest_RV:
            largest_RV = l[1]
    sorting_RV = 0

    # sorting the sorting list form larg RV to small RV
    while True:
        if sorting_RV > largest_RV:
            break
        for t in sorting_list:
            if t[1] == sorting_RV:
                sorting_list.pop(sorting_list.index(t))
                sorting_list.insert(0, t)
        sorting_RV += 1

    # adding the blogs in order of the sorting list
    for b in sorting_list:
        blog = Blog.query.filter_by(id=b[0]).first()
        ranked_blogs.append(blog)
    return ranked_blogs

