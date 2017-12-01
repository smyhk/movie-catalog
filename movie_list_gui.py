#!/usr/bin/env python3

import db
import tkinter as tk
from tkinter import ttk


class MovieInputFrame(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.parent = parent

        # define string variables for text fields
        self.movieTitle = tk.StringVar()
        self.year = tk.StringVar()
        self.category = tk.StringVar()

        # initialize gui components
        self.initComponents()

    def initComponents(self):
        self.pack()

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
        ttk.Combobox(self, values=self.populateCombo()).grid(
            column=1, row=2, sticky=tk.W)

        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    def makeButtons(self):
        # create a frame to store two buttons
        buttonFrame = ttk.Frame(self)
        buttonFrame.grid(column=0, row=3, columnspan=2, sticky=tk.E)

        ttk.Button(buttonFrame, text="Clear",
                   command=self.clear).grid(column=0, row=0, padx=5)
        ttk.Button(buttonFrame, text="Save",
                   command=self.saveMovie).grid(column=1, row=0)

    # populated to drop down list from the database
    def populateCombo(self):
        cat_list = []
        categories = db.get_categories()
        for category in categories:
            cat_list.append(str(category.name))
        return cat_list

    def saveMovie(self):
        movieTitle = self.movieTitle.get()
        year = self.year.get()


def main():
    db.connect()
    root = tk.Tk()
    root.title("Movie Catalog")
    MovieInputFrame(root)
    root.mainloop()
    db.close()


if __name__ == '__main__':
    main()
