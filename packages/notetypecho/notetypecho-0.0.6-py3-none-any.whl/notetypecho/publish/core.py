# coding=utf-8
import os

import nbformat
import yaml
from nbconvert import MarkdownExporter
from notetypecho import Category, Post, Typecho


class FileTree:
    def __init__(self, name="默认分类"):
        self.name = name
        self.categories = []
        self.files = []

    def __str__(self):
        return "{}  {}  {}".format(self.name, ';'.join([i.__str__() for i in self.categories]), len(self.files))


def get_all_file(path_root):
    file_tree = FileTree(os.path.basename(path_root))
    for path in os.listdir(path_root):
        path = os.path.join(path_root, path)

        if os.path.isdir(path):
            filename = os.path.basename(path)
            if filename in ('.ipynb_checkpoints', 'pass') or 'pass' in filename:
                continue
            file_tree.categories.append(get_all_file(path))
        else:
            filename, filetype = os.path.splitext(os.path.basename(path))
            if filetype in ('.ipynb', '.md'):
                file_tree.files.append(path)

    return file_tree


def coalesce(params: list):
    if params is None or len(params) == 0:
        return None
    for param in params:
        if param is not None:
            return param
    return None


class PostAll:
    typecho: Typecho = None

    def __init__(self):
        self.categories = [entry['categoryName']
                           for entry in self.typecho.get_categories()]

    def post(self, path, categories):
        filename, filetype = os.path.splitext(os.path.basename(path))

        post = None
        if filetype == '.ipynb':
            jake_notebook = nbformat.reads(
                open(path, 'r').read(), as_version=4)
            mark = MarkdownExporter()
            content, _ = mark.from_notebook_node(jake_notebook)
            # check title
            if len(jake_notebook.cells) >= 1:
                source = str(jake_notebook.cells[0].source)
                if source.startswith('- '):
                    s = yaml.load(source)
                    res = {}
                    [res.update(i) for i in s]

                    title = res.get("title", filename)
                    tags = res.get("tags", '')
                    categories = categories or res.get(
                        "category", '').split(',')

                    del jake_notebook.cells[0]
                    content, _ = mark.from_notebook_node(jake_notebook)
                    post = Post(title=title,
                                description=content,
                                mt_keywords=tags,
                                categories=categories, )

            post = post or Post(title=filename,
                                description=content,
                                categories=categories,)
        elif filetype == '.md':
            content = open(path, 'r').read()
            post = Post(title=filename,
                        description=content,
                        categories=categories,)
        else:
            print("error {}".format(filetype))
            return

        self.typecho.new_post(post, publish=True)

    def category_manage(self, categories):
        for category in categories:
            if category not in self.categories:
                cate = Category(name=category)
                self.typecho.new_category(cate)
                self.categories.append(category)

    def post_tree(self, file_tree: FileTree, categories, parent_id=0):
        self.category_manage(categories)

        for path in file_tree.files:
            self.post(path, categories=categories)
        for tree in file_tree.categories:
            self.post_tree(tree, categories=categories)

    def post_all(self, path_root):
        res = get_all_file(path_root)

        for path in res.categories:
            self.post_tree(path, categories=[path.name])
            # break
