from flask import Flask, redirect, url_for, render_template, request, flash
from linked_list_simulator.linked_list import *

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


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
                               list='', error='')


if __name__ == "__main__":
    app.run(debug=True)
