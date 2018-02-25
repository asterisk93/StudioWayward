from git import Repo,remote
import os.path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


LARGE_FONT = ("Verdana, 12")
LABEL_FONT = ("Verdana, 10")
##########CONFIG##########

#wayward local repo dir
wayward_local = "C:/Users/Kevin D/JK2/StudioWayward"

#BSR local repo dir
bsr_local = "C:/Users/Kevin D/JK1/BiteSizeReviews"

##########################

class SW_submit(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default="favicon.ico")
        tk.Tk.wm_title(self, "Studio Wayward Submission App")
        #tk.Tk.geometry(self, newGeometry="800x500")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (SiteSelect, Model, Photo, Review):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SiteSelect)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def request_file(self, cont):
        cont.file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

    def review_gen(self, cont):

        #get field values
        title = cont.review_title.get()
        rating = cont.review_rating.get()
        color = cont.review_color.get()
        keyword = cont.review_keyword.get()
        year = cont.review_year.get()
        month = cont.review_month.get()
        day = cont.review_day.get()
        text = cont.review_text.get("1.0",'end-1c')
        poster = cont.file

        #create filename
        filename = year + '-' + day + '-' + month + '-' + str.replace(str.replace(title, ' ', '-'), ':', '-') + '.markdown'

        if rating == "meal":
            front = '---\n layout: post\n title: "' + title + '"\n date:  ' + year + '-' + month + '-' + day + '\n categories: opinion\n image: "' + keyword + '.jpg"\n permalink: /:title\n---'

        else:
            front = '---\n layout: post\n title: "' + title + '"\n date:  ' + year + '-' + month + '-' + day + '\n categories: review\n rating: "' + rating + '"\n light: "' + color + '"\n poster: "' + keyword + '.jpg"\n permalink: /:title\n---'

        review_path = bsr_local + '/_posts/'

        write_path = os.path.join(review_path, filename)
        
        #write to file
        fp = open((write_path), 'x')
        fp.write(str(front + '\n\n\n' + text))
        fp.close()

        #tracking
        print(title + ' created')

class SiteSelect(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Choose a Site!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Model Works",
                            command=lambda: controller.show_frame(Model))
        button.pack(pady=10, padx=10, side=tk.TOP)

        button = ttk.Button(self, text="Photography",
                            command=lambda: controller.show_frame(Photo))
        button.pack(pady=10, padx=10, side=tk.TOP)

        button = ttk.Button(self, text="BS Reviews",
                            command=lambda: controller.show_frame(Review))
        button.pack(pady=10, padx=10, side=tk.TOP)

class Model(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Studio Wayward Model Works: New Model", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Submit",
                            command=lambda: controller.show_frame(SiteSelect))
        button.pack() 

        button = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(SiteSelect))
        button.pack()  

class Photo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Studio Wayward Photography: Add Content", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Continue",
                            command=lambda: controller.show_frame(SiteSelect))
        button.pack() 

        button = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(SiteSelect))
        button.pack()  

class Review(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Bite-Size Reviews: New Post", font=LARGE_FONT)
        label.pack(pady=15,padx=10)

        label = ttk.Label(self, text="Title:", font=LABEL_FONT)
        label.pack()
        review_title = tk.Entry(self)
        review_title.pack(pady=10,padx=10)
        self.review_title = review_title

        label = ttk.Label(self, text="Rating: (set to 'meal' for long-post)", font=LABEL_FONT)
        label.pack()
        review_rating = tk.Entry(self)
        review_rating.pack(pady=10,padx=10)
        self.review_rating = review_rating

        label = ttk.Label(self, text="Rating Color:", font=LABEL_FONT)
        label.pack()
        review_color = tk.Entry(self)
        review_color.pack(pady=10,padx=10)
        self.review_color = review_color

        label = ttk.Label(self, text="Keyword:", font=LABEL_FONT)
        label.pack()
        review_keyword = tk.Entry(self)
        review_keyword.pack(pady=10,padx=10)
        self.review_keyword = review_keyword

        label = ttk.Label(self, text="Review Date:", font=LABEL_FONT)
        label.pack()

        review_year=tk.StringVar(self)
        review_month=tk.StringVar(self)
        review_day=tk.StringVar(self)
        
        year = ttk.OptionMenu(self, review_year, "Year", "2017", "2018", "2019", "2020", "2021")
        review_year.set("Year")
        year.pack()
        self.review_year = review_year

        month = ttk.OptionMenu(self, review_month, "Month", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")
        review_month.set("Month")
        month.pack()
        self.review_month = review_month
        
        day = ttk.OptionMenu(self, review_day, "Day", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
        review_day.set("Day")
        day.pack()
        self.review_day = review_day

        label = ttk.Label(self, text="Review Text:", font=LABEL_FONT)
        label.pack()
        review_text = tk.Text(self)
        review_text.pack(pady=10,padx=10)
        self.review_text = review_text

        poster = ttk.Button(self, text="Select Poster",
                            command=lambda: controller.request_file(self))
        poster.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Submit",
                            command=lambda: controller.review_gen(self))
        button.pack(pady=10,padx=10) 

        button = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(SiteSelect))
        button.pack(pady=10,padx=10)

        

##Post-Gen Functions##

    

app = SW_submit()
app.mainloop()
        
            
