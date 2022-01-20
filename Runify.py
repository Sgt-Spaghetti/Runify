from tkinter import PhotoImage
import IntroStuff, ConversionStuff, os, sys, json, re
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

active = True
graphical = False
is_custom = False
conversion_type = "b"

custom_word = {}
custom_letter = {}

def start():

    loop = True
    global conversion_type

    if len(sys.argv) > 1 and sys.argv[1] == "c":

        IntroStuff.startup()

        while active == True:
            print("Please past the entire path to the input file below: ")
            input_file_path = os.path.abspath(input())

            print("\nOK! the input path is " + input_file_path + "\n" + \
            "The output file will be created in the same directory\n")

            print("\nWould you like to transliterate letters, translate words or both? (l/w/b)")
            while loop == True:
                answer = input()
                if answer == "b" or answer == "w" or answer == "l":
                    conversion_type = answer
                    loop = False
                else:
                    print("Whoops, didn't get that")
            
            conversion(input_file_path)
    else:
        global graphical
        graphical = True
        gui()

def word_conversion(inputstring):

    inputstring = inputstring.lower()
    global custom_word

    word_converted_string = ""
    word_list = (line.split() for line in inputstring.splitlines())
    for lines in word_list:
        if custom_word:
            for word in lines:
                word_converted_string += custom_word.get(word,word) + " "
        else:
            for word in lines:
                processed_word = re.findall( r'\w+|[^\s\w]+', word)
                for section in processed_word:
                    if section in ConversionStuff.symbols:
                        word_converted_string += section
                    else:
                        word_converted_string += ConversionStuff.Word_Dictionary.get(section,section)
                word_converted_string += " "

        word_converted_string += "\n"

    return word_converted_string

def letter_conversion(inputstring):
    global custom_letter

    letter_converted_string = ""
    if custom_letter:
        for character in inputstring:
            letter_converted_string += custom_letter.get(character,character)
    else:
        for character in inputstring:
            letter_converted_string += ConversionStuff.letter_dictionary.get(character,character)

    return letter_converted_string

def save(output,outputfilepath=None,):
    global is_custom
    global graphical

    if graphical == True:

            if is_custom == False:
                with open(outputfilepath,"w") as output_file:
                        output_file.write(output)
                        gui.output_window["state"] = "normal"
                        gui.output_window.delete("0.0",tk.END)
                        gui.output_window.insert("0.0",output)
                        gui.output_window["state"] = "disabled"
            else:
                gui.output_window["state"] = "normal"
                gui.output_window.delete("0.0",tk.END)
                gui.output_window.insert("0.0",output)
                gui.output_window["state"] = "disabled"

    else:
        with open(os.path.split(outputfilepath)[0] + "/Runify_Output.txt","w") as output_file:
            output_file.write(output)


def conversion(inputfilepath=None):
    
    global is_custom
    global graphical
    global _type

    if graphical == True:
        if is_custom == False:

            try:

                inputfilepath = gui.input_text_field.get()

                if inputfilepath == "" or inputfilepath == None:
                    tk.messagebox.showinfo("File not found", "Please select a valid input file")
                    return
                
                outputfilepath = browse_output()

                if outputfilepath == "" or outputfilepath == None:
                    return
                else:

                    with open(inputfilepath,"r") as input_file:
                        input_string = input_file.read()

                    if conversion_type == "l":
                        output_string = letter_conversion(input_string).strip()
                    elif conversion_type == "w":
                        output_string = word_conversion(input_string).strip()
                    else:
                        output_string = letter_conversion(word_conversion(input_string)).strip()
                    save(output_string, outputfilepath)

            except FileNotFoundError:
                tk.messagebox.showinfo("File not found", "Please select a valid file")
            except PermissionError:
                tk.messagebox.showinfo("File not found", "Please select a valid file")

        else:
            text_input = gui.input_window.get("0.0",tk.END)
            if conversion_type == "l":
                output_string = letter_conversion(text_input).strip()
            elif conversion_type == "w":
                output_string = word_conversion(text_input).strip()
            else:
                output_string = letter_conversion(word_conversion(text_input)).strip()
            save(output_string)


    else:
        try:
            input_file = open(inputfilepath)
        except:
            print("Sorry, the input file could not be opened!\n"+\
            "Please make sure the path is correct and includes the file extention\n")
            inputfilepath == ""
            return

        input_string = input_file.read()
        if conversion_type == "l":
            output_string = letter_conversion(input_string).strip()
        elif conversion_type == "w":
            output_string = word_conversion(input_string).strip()
        else:
            output_string = letter_conversion(word_conversion(input_string)).strip()
        input_file.close()
        save(output_string,inputfilepath)
        global active
        active = False

def browse_output():
    filepath = str(asksaveasfilename(
        filetypes = [("Text","*.txt"), ("All Files","*.*")],
        initialfile = "Runify-Output"
        ))
    if not filepath or filepath == "()":
        return
    else:
        return filepath

def gui():
    
    window = tk.Tk()


    # FUNCTIONS GO HERE

    def check_button_states():
        # Check for invalid configurations

        global is_custom
        global conversion_type

        if checkbox_letters.get() == False and checkbox_words.get() == False:
            submit_button["state"] = "disabled"
        else:
            submit_button["state"] = "normal"

            if checkbox_letters.get() == True and checkbox_words.get() == True:
                conversion_type = "b"
            elif checkbox_letters.get() == True:
                conversion_type = "l"
            elif checkbox_words.get() == True:
                conversion_type = "w"


        if checkbox_input.get() == True:

            gui.input_window.grid(row=0,column=0,sticky="nsew", padx=2,pady=2)
            gui.output_window.grid(row=0,column=1, sticky="nsew", padx=2,pady=2)


            is_custom = True
            gui.input_window["state"] = "normal"
            gui.input_text_field["state"] = "disabled"
            input_browse_btn["state"] = "disabled"
        
        else:

            gui.input_window.grid_remove()
            gui.output_window.grid(row=0,column=0, columnspan=2, sticky="nsew", padx=2,pady=2)

            is_custom = False
            gui.input_text_field["state"] = "normal"
            input_browse_btn["state"] = "normal"
            input_browse_btn["disabledforeground"] = theme[0]
            gui.input_window["state"] = "disabled"


    def change_theme(theme, configurable):

        icons = [input_browse_btn, window]
        frames = [box_container,window,input_files_container]
        boxes = [gui.output_window,gui.input_window,gui.input_text_field]
        checkboxes = [letters_checkbox,words_checkbox,window_checkbox]
        menu = [menubar,filemenu,thememenu,load_dictionary_bar,csv_bar]

        gui.active_theme = theme[8]
        
        for widget in configurable:
            if widget in frames:
                widget.configure(bg=theme[0])
            elif widget in boxes:
                if widget == gui.input_text_field:
                    widget["disabledbackground"] = theme[7]
                widget.configure(bg=theme[2], fg=theme[1])
            elif widget in checkboxes:
                widget.configure(selectcolor=theme[5],bg=theme[0], fg=theme[1])
            elif widget in icons:
                if widget == icons[0]:
                    filephoto = theme[3]
                    widget.configure(image=filephoto, bg=theme[0],disabledforeground=theme[0],activebackground = theme[2])
                if widget == icons[1]:
                    photoicon = theme[4]
                    widget.iconphoto(True,photoicon)
            elif widget in menu:
                if widget == menubar:
                    widget.config(bg=theme[0],fg=theme[1])
                else:
                    widget.config(bg=theme[2], fg=theme[1])
                    
            else:
                widget.configure(bg = theme[0], fg=theme[1])

    def save_theme(theme):
        with open("config.txt", "w") as file:
            if theme == "light":
                file.write("Theme: light")

            elif theme == "dark":
                file.write("Theme: dark")

    def browse_input_btn():
        filepath = str(askopenfilename(
            filetypes=[("Text Files","*.txt"),("All Files","*.*")],
            ))
        if not filepath or filepath == "()":
            return
        else:
            gui.input_text_field.delete(0,tk.END)
            gui.input_text_field.insert(0, filepath)
            

    def create_custom_dictionary():
        subwindow = tk.Toplevel(window)
        subwindow.title("Dictonary Wizard")
        subwindow["background"] = "dark grey"

        create_custom_dictionary.entries = []
        create_custom_dictionary.added_rows = 1
        create_custom_dictionary.added_columns = 0

        def save_dic(entries):
            dic = {}
            for i in range(len(entries)):
                if entries[i][0] != None and entries[i][1] != None:
                    dic[entries[i][0].get()] = entries[i][1].get()
                    
            data = json.dumps(dic, indent=4)

            filepath = str(asksaveasfilename(
                filetypes = [("Text Files","*.txt"),("All Files","*.*")]))
            if filepath != None or filepath != "" or filepath != "()":

                with open(filepath,"w") as file:
                    file.write(data)

        def add_entry():
            added_rows = 0
            added_columns = 0

            added_rows = create_custom_dictionary.added_rows
            added_columns = create_custom_dictionary.added_columns
            added_rows += 1
            if added_rows % 30 == 0 and added_rows != 0:
                added_columns += 3
                added_rows = 1
            
            entry1 = tk.Entry(master=subwindow, highlightthickness=0)
            entry1.grid(row=added_rows,column=added_columns)
            tk.Label(master=subwindow, text="\u27fc",bg="dark grey").grid(row=added_rows,column=added_columns+1)
            entry2 = tk.Entry(master=subwindow, highlightthickness=0)
            entry2.grid(row=added_rows,column=added_columns+2)


            create_custom_dictionary.entries.append((entry1,entry2))

            create_custom_dictionary.added_rows = added_rows
            create_custom_dictionary.added_columns = added_columns

        ent1 = tk.Entry(master=subwindow, highlightthickness=0)
        ent1.grid(row=1,column=0)
        lbl = tk.Label(master=subwindow, text="\u27fc", bg="dark grey").grid(row=1,column=1)
        ent2 = tk.Entry(master=subwindow, highlightthickness=0)
        ent2.grid(row=1,column=2)

        create_custom_dictionary.entries.append((ent1,ent2))

        create_btn = tk.Button(master=subwindow, text="Add Entry", command=lambda: add_entry())
        save_btn = tk.Button (master = subwindow, text="save", command = lambda: save_dic(create_custom_dictionary.entries))

        create_btn.grid(row=0, column=0)
        save_btn.grid(row=0, column=2)



    def load_custom_dictionary(_type):

        global custom_word
        global custom_letter

        if _type == "word" or _type == "letter":
            file_path = askopenfilename(
                filetypes=[("Text Files","*.txt"),("All Files","*.*")]
            )
        if _type == "wcsv" or _type == "lcsv":
            file_path = askopenfilename(
                filetypes=[("CSV files","*.csv"),("All Files","*.*")]
            )
            
        try:
            with open(file_path,"r") as input_file:

                if _type == "word" or _type == "letter":
                    data = input_file.read()
                    data = json.loads(data)
                    if _type == "word":
                        custom_word = data
                    else:
                        custom_letter = data
                if _type == "wcsv" or _type == "lcsv":
                    
                    dic = {}
                    data = input_file.readlines()
                    
                    for line in data:
                        line = re.split(",|\n",line,2)
                        del line[2]
                        dic[line[0]] = line[1]

                    if _type == "wcsv":
                        custom_word = dic
                    else:
                        custom_letter = dic

        except TypeError:
            pass
        except FileNotFoundError:
            pass
        except ValueError:
            tk.messagebox.showinfo("Invalid file", "Could not parse file data")

    def clear_custom_dictionaries():
        global custom_word, custom_letter
        custom_word = {}
        custom_letter = {}

    # Load images
    photo1dark = tk.PhotoImage(file= "FileIcon.png")
    photo1light = tk.PhotoImage(file="FileIconLight.png")
    filephoto = photo1dark

    photo2light = tk.PhotoImage(file = "RunifyIcon.png")
    photo2dark = tk.PhotoImage(file = "RunifyIconDark.png")
    photoicon = photo2light

    window.iconphoto(True,photoicon)

    # Set themes
    dark_theme_background = "#142427"
    light_theme_background = "#ebdbd8"

    light_theme_text = "black"
    dark_theme_text = "white"

    light_theme_box = "white"
    dark_theme_box = "#606060"

    dark_theme = (dark_theme_background, dark_theme_text,dark_theme_box,photo1light,
                  photo2dark,"#142427","#142427","black","dark")
    light_theme = (light_theme_background, light_theme_text,light_theme_box,photo1dark,
                   photo2light,"white","light grey","light grey","light")
    gui.active_theme = "light"

    try:
        with open("config.txt","r") as file:
            data = file.read()
            if data == "Theme: light":
                theme = light_theme
            elif data == "Theme: dark":
                theme = dark_theme
            else:
                raise TypeError
    except:
        theme = light_theme

    # set main window config
    window.title("Runify - Graphical mode")
    window.geometry("750x600")
    window.columnconfigure(0, weight=1,minsize=600)
    window.rowconfigure(0,weight=0,minsize=200)
    window.rowconfigure(1,weight=1,minsize=400)
    window["background"] = theme[0]

    # Create the dropdown menubar
    menubar = tk.Menu(master=window, borderwidth=1, relief="flat", bg=theme[0],fg=theme[1])
    filemenu = tk.Menu(master=menubar, tearoff=0,relief="flat",bg=theme[2],fg=theme[1])
    thememenu = tk.Menu(master=menubar, tearoff = 0, relief="flat",bg=theme[2],fg=theme[1])
    load_dictionary_bar = tk.Menu(master=filemenu, tearoff=0,bg=theme[2],relief="flat",fg=theme[1])
    csv_bar = tk.Menu(master=load_dictionary_bar, tearoff=0,bg=theme[2], relief="flat",fg=theme[1])

    
    filemenu.add_command(label="Create Custom Dictionary", command=create_custom_dictionary)
    filemenu.add_cascade(label="Load Custom Dictionary", menu=load_dictionary_bar)
    filemenu.add_command(label="Clear Loaded Dictionaries", command = clear_custom_dictionaries)

    load_dictionary_bar.add_command(label="Word Dictionary", command=lambda:load_custom_dictionary("word"))
    load_dictionary_bar.add_command(label="Letter Dictionary", command=lambda:load_custom_dictionary("letter"))
    load_dictionary_bar.add_cascade(label = "Load from CSV", menu = csv_bar)

    csv_bar.add_command(label = "Use as Word Dictionary", command = lambda: load_custom_dictionary("wcsv"))
    csv_bar.add_command(label = "Use as Letter Dictionary", command = lambda: load_custom_dictionary("lcsv"))

    thememenu.add_command(label = "Light Theme", command= lambda: change_theme(light_theme,themed_widgets))
    thememenu.add_command(label = "Dark Theme", command = lambda: change_theme(dark_theme,themed_widgets))
    thememenu.add_command(label = "Set Default", command = lambda: save_theme(gui.active_theme))

    menubar.add_cascade(label = "Options", menu = filemenu)
    menubar.add_cascade(label = "Theme", menu = thememenu)

    # Create the special texbox variables
    checkbox_letters = tk.BooleanVar(value=True)
    checkbox_words = tk.BooleanVar(value=False)
    checkbox_input = tk.BooleanVar(value=False)

    # Frame for the file input/output paths
    input_files_container = tk.Frame(master=window, background=theme[0])
    input_files_container.rowconfigure([0,1,2,3],weight=1)
    input_files_container.columnconfigure([0,1,2],weight=1)

    # Frame for the input boxes
    box_container = tk.Frame(master=window, background=theme[0])
    box_container.columnconfigure([0,1],weight=1)
    box_container.rowconfigure(0,weight=1)

    # All the widgets to do with file input/output paths + translation choice
    
    input_path_label = tk.Label(master=input_files_container, text="Path to input file:",background=theme[0], fg=theme[1])
    gui.input_text_field = tk.Entry(master=input_files_container,borderwidth=1,highlightthickness=0)
    
    input_browse_btn = tk.Button(master=input_files_container, image=theme[3],bg=theme[0], fg=theme[1],borderwidth=0,
                                     highlightthickness=0,command=browse_input_btn, width=70, height=40,
                                     activebackground = theme[2])

    letters_checkbox = tk.Checkbutton(master=input_files_container, variable=checkbox_letters, text="Transliterate letters",command=check_button_states,
                                      bg= theme[0],borderwidth=0,highlightthickness=0, fg=theme[1])

    
    words_checkbox = tk.Checkbutton(master=input_files_container, variable=checkbox_words, text="Translate words",command=check_button_states, bg=theme[0],
                                    borderwidth=0,highlightthickness=0, fg=theme[1])

    submit_button = tk.Button(master=input_files_container, text="Submit", bg="#F0BE19",borderwidth=0,highlightthickness=0, command=conversion)


    # The two big text windows for manual text entry and preview
    gui.input_window = tk.Text(master=box_container, state="disabled", bg=theme[2],borderwidth=0,highlightthickness=0)
    gui.output_window = tk.Text(master=box_container, state="disabled",borderwidth=0,highlightthickness=0)


    # Widgets associated to the big text windows
    window_checkbox = tk.Checkbutton(master=input_files_container,variable=checkbox_input, text="Custom Input", command=check_button_states,
    borderwidth=0,bg=theme[0],highlightthickness=0, fg=theme[1])
    window_lbl_output = tk.Label(master = input_files_container, text="Output preview:",borderwidth=0,bg=theme[0], fg=theme[1])

    # Grid all of the subwidgets correctly for the file input/output paths + translation choice
    input_path_label.grid(row=0, column=0, pady=5)
    gui.input_text_field.grid(row=0, column=1, padx=5,pady=5)
    input_browse_btn.grid(row=0, column=2, pady=5)

    letters_checkbox.grid(row=2, column=0, pady=5)
    words_checkbox.grid(row=2, column=2, pady=5)

    submit_button.grid(row=3, column=1)

    # Grid the widgets associated with the big text entry boxes


    window_checkbox.grid(row=4, column=0)
    window_lbl_output.grid(row=4, column=2)

    gui.output_window.grid(row=0,column=0,columnspan=2,sticky="nsew", padx=2,pady=2)

    # Grid the frames and the big text entry boxes
    input_files_container.grid(row=0,column=0, columnspan=2)
    box_container.grid(row=1, column=0,columnspan=2,sticky="nsew")

    themed_widgets = [input_path_label,input_browse_btn,box_container,window,input_files_container,menubar,gui.input_text_field,load_dictionary_bar,
                      letters_checkbox,words_checkbox,window_checkbox,window_lbl_output,gui.output_window,gui.input_window,filemenu,thememenu,csv_bar]

    window.config(menu=menubar)

    
    window.mainloop()

start()
