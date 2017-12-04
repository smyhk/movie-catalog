#!/usr/bin/env python3

import db
import tkinter as tk
import tkinter.simpledialog as tkSimpleDialog
from tkinter import ttk
from objects import Movie


class MovieFrames(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)

        MovieInputFrame(parent).grid(column=0, row=0, sticky=tk.W)
        MovieOutputFrame(parent).grid(column=0, row=1, sticky=tk.W)


class MovieOutputFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")

        self.tree = ttk.Treeview(height=10, columns=("name", "year", "mins", "genre"))
        self.tree.grid(row=1, column=0, padx=(10, 10))

        self.tree.heading('#0', text="ID", anchor=tk.W)
        self.tree.column('#0', minwidth=0, width=0, stretch=tk.NO)
        self.tree.heading("name", text="Name", anchor=tk.W)
        self.tree.heading("year", text="Year", anchor=tk.W)
        self.tree.heading("mins", text="Minutes", anchor=tk.W)
        self.tree.heading("genre", text="Category", anchor=tk.W)

        self.refresh_record_view()

        ttk.Button(parent, text="Delete", command=self.deleteMovie).grid(
            column=0, row=2, sticky=tk.W, padx=10, pady=(10, 10))

        ttk.Button(parent, text="Year", command=self.view_movies_by_year).grid(
            column=0, row=3, sticky=tk.W, padx=10, pady=(10, 10))

    def refresh_record_view(self):
        # currently display all records in the database
        movies = db.get_all_movies()
        self.viewRecords(movies)

    def viewRecords(self, movies):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        for movie in movies:
            self.tree.insert('', 0, text=movie.id, values=(movie.name,
                                                           movie.year,
                                                           movie.minutes,
                                                           movie.category.name))

    def view_movies_by_year(self):
        year = self.get_year_from_user()
        movies = db.get_movies_by_year(year)
        self.viewRecords(movies)

    def get_year_from_user(self):
        year = tkSimpleDialog.askinteger("List by Year", "Enter year:")
        return year

    def deleteMovie(self):
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            print("Please record select a record")
            # self.message[text] = 'Please select record'
            return
        movie_id = self.tree.item(self.tree.selection())['text']
        db.delete_movie(movie_id)

        self.viewRecords()


class MovieInputFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent

        # define string variables for text fields
        self.movieTitle = tk.StringVar()
        self.year = tk.StringVar()
        self.category = tk.StringVar()
        self.minutes = tk.StringVar()

        # initialize gui components
        self.initComponents()

    def initComponents(self):
        # self.pack()

        ttk.Label(self, text="Movie Title:").grid(
            column=0, row=0, sticky=tk.E)
        ttk.Entry(self, width=45, textvariable=self.movieTitle).grid(
            column=1, row=0)

        ttk.Label(self, text="Year Released:").grid(
            column=0, row=1, sticky=tk.E)
        ttk.Entry(self, width=10, textvariable=self.year).grid(
            column=1, row=1, sticky=tk.W)

        ttk.Label(self, text="Category:").grid(
            column=0, row=2, sticky=tk.E)
        ttk.Combobox(self, values=self.populateCombo(), textvariable=self.category).grid(
            column=1, row=2, sticky=tk.W)

        ttk.Label(self, text="Minutes:").grid(
            column=0, row=3, sticky=tk.E)
        ttk.Entry(self, width=10, textvariable=self.minutes).grid(
            column=1, row=3, sticky=tk.W)

        self.makeButtons()

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    def makeButtons(self):
        # create a frame to store three buttons
        buttonFrame = ttk.Frame(self)
        buttonFrame.grid(column=1, row=4, columnspan=3, sticky=tk.W)

        ttk.Button(buttonFrame, text="Clear",
                   command=self.clear).grid(column=0, row=0, pady=5)
        ttk.Button(buttonFrame, text="Save",
                   command=self.saveMovie).grid(column=1, row=0, padx=(5, 5))
        ttk.Button(buttonFrame, text="Exit", command=self.close).grid(
            column=2, row=0)

    # populate the drop down list from the database
    def populateCombo(self):
        cat_list = []
        categories = db.get_categories()
        for category in categories:
            cat_list.append(str(category.name))
        return cat_list

    def saveMovie(self):
        movieTitle = self.movieTitle.get()
        year = int(self.year.get())
        category = self.category.get()
        minutes = int(self.minutes.get())

        category = db.get_category_by_name(category)

        movie = Movie(name=movieTitle, year=year, minutes=minutes, category=category)
        db.add_movie(movie)

        self.confirmMovieAdd(movieTitle)

        mof = MovieOutputFrame(self)
        mof.refresh_record_view()

    def confirmMovieAdd(self, title):
        toplevel = tk.Toplevel()
        toplevel.title("Movie Add Confirmation")
        ttk.Label(toplevel, text=title + " was added.").grid(
            column=0, row=0, padx=(45, 45), pady=(10, 10))
        ttk.Button(toplevel, text="OK", command=toplevel.destroy).grid(
            column=0, row=1, pady=(10, 20))

    def clear(self):
        self.movieTitle.set("")
        self.year.set("")
        self.minutes.set("")
        self.category.set("")

    def close(self):
        db.close()
        self.parent.destroy()


def main():
    db.connect()
    root = tk.Tk()
    root.title("Movie Catalog")
    MovieFrames(root)
    root.mainloop()


if __name__ == '__main__':
    main()
