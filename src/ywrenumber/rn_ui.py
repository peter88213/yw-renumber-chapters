"""Provide a user interface for chapter renumbering: Tkinter facade

Copyright (c) 2020 Peter Triesberger
For further information see https://github.com/peter88213/yw-renumber
Published under the MIT License (https://opensource.org/licenses/mit-license.php)
"""
import os
import webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk

from pywriter.ui.ui_tk import UiTk


class RnUi(UiTk):
    """Tkinter based GUI.
    Extend the superclass.
    """

    def __init__(self, title, sourcePath=None, **kwargs):
        """Make the converter object visible to the user interface 
        in order to make method calls possible.
        Add the widgets needed to invoke the converter manually.
        """
        self.kwargs = kwargs
        self.converter = None
        self.infoWhatText = ''
        self.infoHowText = ''

        self.root = Tk()
        self.root.title(title)

        self.successInfo = Label(self.root)
        self.successInfo.config(height=1, width=75)
        self.processInfo = Label(self.root, text='')
        self.appInfo = Label(self.root, text='')
        self.appInfo.config(height=2, width=75)

        self.hdTypes = Label(self.root, text='Chapters')
        self.renParts = BooleanVar(value=kwargs['ren_parts'])
        self.renUnused = BooleanVar(value=kwargs['ren_unused'])

        self.hdOptions = Label(self.root, text='NumberingStyle')
        self.numberingStyle = IntVar(value=kwargs['numberingStyle'])
        self.numberingCase = IntVar(value=kwargs['numberingCase'])

        self.hdAdd = Label(self.root, text='Add to number')
        self.hdPrefix = Label(self.root, text='Heading prefix')
        self.headingPrefix = StringVar(value=kwargs['headingPrefix'].replace('|', ''))
        self.hdSuffix = Label(self.root, text='Heading suffix')
        self.headingSuffix = StringVar(value=kwargs['headingSuffix'].replace('|', ''))

        self.root.partsCheckbox = ttk.Checkbutton(
            text='Include Section beginnings', variable=self.renParts, onvalue=True, offvalue=False)
        self.root.unusedCheckbox = ttk.Checkbutton(
            text='Include "unused" chapters', variable=self.renUnused, onvalue=True, offvalue=False)

        self.root.arabicCheckbox = ttk.Radiobutton(text='Arabic numbers', variable=self.numberingStyle, value=0)
        self.root.romanCheckbox = ttk.Radiobutton(text='Roman numbers', variable=self.numberingStyle, value=1)
        self.root.englishCheckbox = ttk.Radiobutton(
            text='Written out in English', variable=self.numberingStyle, value=2)

        self.root.upcaseCheckbox = ttk.Radiobutton(text='Uppercase', variable=self.numberingCase, value=0)
        self.root.capitalizeCheckbox = ttk.Radiobutton(text='Capitalized', variable=self.numberingCase, value=1)
        self.root.lowercaseCheckbox = ttk.Radiobutton(text='Lowercase', variable=self.numberingCase, value=2)

        self.root.prefixEntry = Entry(textvariable=self.headingPrefix)
        self.root.suffixEntry = Entry(textvariable=self.headingSuffix)

        self.root.selectButton = Button(text="Select file", command=self.select_file)
        self.root.selectButton.config(height=1, width=20)

        self.root.runButton = Button(text='Renumber chapters', command=self.convert_file)
        self.root.runButton.config(height=1, width=20)
        self.root.runButton.config(state='disabled')

        self.root.quitButton = Button(text='Quit', command=self.stop)
        self.root.quitButton.config(height=1, width=20)

        row1Cnt = 1
        self.hdTypes.grid(row=row1Cnt, column=1, sticky=W, padx=20)
        row1Cnt += 1
        self.root.partsCheckbox.grid(row=row1Cnt, column=1, sticky=W, padx=20)
        row1Cnt += 1
        self.root.unusedCheckbox.grid(row=row1Cnt, column=1, sticky=W, padx=20)

        row2Cnt = 1
        self.hdOptions.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.arabicCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.romanCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.englishCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.upcaseCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.capitalizeCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)
        row2Cnt += 1
        self.root.lowercaseCheckbox.grid(row=row2Cnt, column=2, sticky=W, padx=20)

        row3Cnt = 1
        self.hdAdd.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.hdPrefix.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.prefixEntry.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.hdSuffix.grid(row=row3Cnt, column=3, sticky=W, padx=20)
        row3Cnt += 1
        self.root.suffixEntry.grid(row=row3Cnt, column=3, sticky=W, padx=20)

        if row3Cnt > row2Cnt:
            rowCnt = row3Cnt

        else:
            rowCnt = row2Cnt

        if row1Cnt > rowCnt:
            rowCnt = row1Cnt

        rowCnt += 1
        self.appInfo.grid(row=rowCnt, column=1, columnspan=3, pady=10)

        rowCnt += 1
        self.root.selectButton.grid(row=rowCnt, column=1, padx=10, pady=10, sticky=W)
        self.root.runButton.grid(row=rowCnt, column=2, padx=10, pady=10, sticky=E)
        self.root.quitButton.grid(row=rowCnt, column=3, padx=10, pady=10, sticky=E)

        rowCnt += 1
        self.successInfo.grid(row=rowCnt, column=1, columnspan=3)

        rowCnt += 1
        self.processInfo.grid(row=rowCnt, column=1, columnspan=3, pady=10)

        self.sourcePath = None

        if kwargs['yw_last_open']:

            if os.path.isfile(kwargs['yw_last_open']):
                self.sourcePath = kwargs['yw_last_open']

        if sourcePath:

            if os.path.isfile(sourcePath):
                self.sourcePath = sourcePath

        if self.sourcePath is not None:
            self.set_info_what('File: ' + os.path.normpath(self.sourcePath))
            self.root.runButton.config(state='normal')

        else:
            self._sourcePath = None
            self.set_info_what('No file selected')
            self.startDir = os.getcwd()

    def start(self):
        """Start the user interface.
        Note: This can not be done in the __init__() method.
        """
        self.root.mainloop()

    def stop(self):
        """Stop the user interface.
        """
        self.root.destroy()

    def select_file(self):
        """Open a file dialog in order to set the sourcePath property.
        """
        self.processInfo.config(text='')
        self.successInfo.config(bg=self.root.cget("background"))

        if self.sourcePath is not None:
            self.startDir = os.path.dirname(self.sourcePath)

        file = filedialog.askopenfile(initialdir=self.startDir)

        if file:
            self.sourcePath = file.name

        if self.sourcePath:
            self.set_info_what('File: ' + os.path.normpath(self.sourcePath))
            self.root.runButton.config(state='normal')

        else:
            self.set_info_what('No file selected')
            self.root.runButton.config(state='disabled')

    def convert_file(self):
        """Call the converter's conversion method, if a source file is selected.
        """
        self.processInfo.config(text='')
        self.successInfo.config(bg=self.root.cget("background"))

        if self.sourcePath:
            self.kwargs = dict(
                yw_last_open=self.sourcePath,
                ren_parts=self.renParts.get(),
                ren_unused=self.renUnused.get(),
                numberingStyle=str(self.numberingStyle.get()),
                numberingCase=str(self.numberingCase.get()),
                headingPrefix='|' + self.headingPrefix.get() + '|',
                headingSuffix='|' + self.headingSuffix.get() + '|',
            )
            self.converter.run(self.sourcePath, **self.kwargs)

            if self.converter.newFile is not None:
                webbrowser.open(self.converter.newFile)
