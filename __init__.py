from flask import Flask, render_template, request, \
    flash, send_file, send_from_directory, abort
from linked_list_simulator.linked_list import *
from huffman_compressor.engine import *
import os
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

garbage_files = []

scheduler = BackgroundScheduler()
scheduler.start()

app = Flask(__name__)

app.config["FILE_UPLOADS"] = \
    r"C:\Users\Hassan\Documents\GitHub\djerty_website\client_files"


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/huffman", methods=["POST", "GET"])
def huffman():
    if request.method == "POST":
        if request.files:
            try:
                file = request.files['file']
                file.save(os.path.join(app.config["FILE_UPLOADS"],
                                       file.filename))
                compress_file(os.path.join(app.config["FILE_UPLOADS"],
                                           file.filename),
                              os.path.join(app.config["FILE_UPLOADS"],
                                           file.filename.split('.')[0] +
                                           '.djerty'))
                garbage_files.append(os.path.join(app.config['FILE_UPLOADS'],
                                                  file.filename.split('.')[0] +
                                                  '.djerty'))
                scheduler.add_job(func=clear_garbage_files,
                                  next_run_time=datetime.now() +
                                                timedelta(seconds=10))
                os.remove(os.path.join(app.config["FILE_UPLOADS"],
                                       file.filename))
                return send_file(os.path.join(app.config["FILE_UPLOADS"],
                                              file.filename.split('.')[0] +
                                              '.djerty'))
            except FileNotFoundError:
                return render_template("huffman.html", error='NoFileError')
    return render_template("huffman.html")


def clear_garbage_files():
    for path in garbage_files:
        try:
            os.remove(path)
        except FileNotFoundError:
            continue


# @app.route("/get_file/<file_name>")
# def get_file(file_name):
#
#     try:
#         temp = send_from_directory(app.config["FILE_UPLOADS"], file_name)
#         return temp
#     except FileNotFoundError:
#         abort(404)

@app.route("/linked-list", methods=["POST", "GET"])
def linked():
    if request.method == "POST":
        split = request.form['linkedlist'].split(',')
        if '' in split:
            split.remove('')
        linkedlist = LinkedList(split)
        if request.form["operation"] == 'Append':
            linkedlist.insert(len(linkedlist), request.form['value'])
            return render_template("linked_list.html", ans=str(linkedlist),
                                   list=linkedlist.join())

        if request.form["operation"] == 'Insert at the beginning':
            linkedlist.insert(0, request.form['value'])
            return render_template("linked_list.html", ans=str(linkedlist),
                                   list=linkedlist.join())

        elif request.form["operation"] == 'Remove first instance of':
            try:
                linkedlist.delete_one(request.form['value'])
                return render_template("linked_list.html", ans=str(linkedlist),
                                       list=linkedlist.join())
            except ValueError:  # if the item is not in the list
                return render_template("linked_list.html", ans=str(linkedlist),
                                       list=linkedlist.join(),
                                       error='ValueError')
        elif request.form["operation"] == 'Remove all instances of':
            try:
                linkedlist.delete_all(request.form['value'])
                return render_template("linked_list.html", ans=str(linkedlist),
                                       list=linkedlist.join())
            except ValueError:  # if the item is not in the list
                return render_template("linked_list.html", ans=str(linkedlist),
                                       list=linkedlist.join(),
                                       error='ValueError')

        elif request.form["operation"] == 'Remove item at index':
            try:
                linkedlist.delete_at_index(int(request.form['value']))
                return render_template("linked_list.html", ans=str(linkedlist),
                                       list=linkedlist.join())
            except IndexError:  # if the item is not in the list
                return render_template("linked_list.html", ans=str(linkedlist),
                                       list=linkedlist.join(),
                                       error='IndexError')
    else:
        return render_template("linked_list.html", empty=True,
                               list='[]', error='')


if __name__ == "__main__":
    app.run()
