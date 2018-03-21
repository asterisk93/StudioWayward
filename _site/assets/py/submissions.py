import shutil
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
        tk.Tk.wm_title(self, "Wayward's Son")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (SiteSelect, Model, Photo, Review, Success, Photoset, Photographs):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SiteSelect)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def request_file(self, cont):
        cont.file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

    def request_dir(self, cont):
        cont.file_dir = filedialog.askdirectory()
    
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

        #create filename, frontmatter and send image to appropriate assets subfolder
        

        if rating == "meal":
            front = '---\n layout: post\n title: "' + title + '"\n date:  ' + year + '-' + month + '-' + day + '\n categories: opinion\n image: "' + keyword + '.jpg"\n permalink: /:title\n---'
            filename = year + '-' + month + '-' + day + '-MEAL-' + str.replace(str.replace(title, ' ', '-'), ':', '-') + '.markdown'
            img_path = bsr_local + '/assets/article-images/'
            shutil.move(poster, img_path + keyword + '.jpg')
            
        else:
            front = '---\n layout: post\n title: "' + title + '"\n date:  ' + year + '-' + month + '-' + day + '\n categories: review\n rating: "' + rating + '"\n light: "' + color + '"\n poster: "' + keyword + '.jpg"\n permalink: /:title\n---'
            filename = year + '-' + month + '-' + day + '-' + str.replace(str.replace(title, ' ', '-'), ':', '-') + '.markdown'
            img_path = bsr_local + '/assets/posters/'
            shutil.move(poster, img_path + keyword + '.jpg')
            
        review_path = bsr_local + '/_posts/'

        write_path = os.path.join(review_path, filename)
        
        #write to file
        fp = open((write_path), 'x')
        fp.write(str(front + '\n\n\n' + text))
        fp.close()

        #tracking
        print(title + ' created')

        self.show_frame(Success)

    def set_gen(self, cont):

        #get field values
        title = cont.set_title.get()
        year = cont.set_year.get()
        month = cont.set_month.get()
        day = cont.set_day.get()
        keyword = cont.set_keyword.get()
        text = cont.set_desc.get("1.0",'end-1c')

        #create filename
        filename = year + '-' + month + '-' + day + '-' + str.replace(str.replace(title, ' ', '-'), ':', '-') + '.markdown'

        #frontmatter
        front = '---\n layout: post\n type: photography, photoset\n permalink: /photography/:title\n title: ' + title + '\n date:  ' + year + '-' + month + '-' + day + '\n keyword: ' + keyword + '\n---'
                
        set_path = wayward_local + '/_posts/photography/sets/'

        write_path = os.path.join(set_path, filename)
        
        #write to file
        fp = open((write_path), 'x')
        fp.write(str(front + '\n\n\n' + text))
        fp.close()

        #tracking
        print(title + ' created')

        set_asset_folder = wayward_local + '/assets/images/photography/' + keyword +'/'
        if not os.path.exists(set_asset_folder):
            os.makedirs(set_asset_folder)

        set_post_folder = wayward_local + '/_posts/photography/photos/' + keyword +'/'
        if not os.path.exists(set_post_folder):
            os.makedirs(set_post_folder)

        self.show_frame(Success)

    def model_gen(self, cont):

        #field values
        title = cont.model_title.get()
        scale = cont.model_scale.get()
        year = cont.model_year.get()
        month = cont.model_month.get()
        day = cont.model_day.get()
        src_dir = cont.file_dir
        img_preview = cont.file
        animate = cont.model_animate.get()
        preview = cont.model_pre.get()
        keyword = cont.model_keyword.get()
        text = cont.model_desc.get("1.0",'end-1c')

        dest_asset_dir = wayward_local + '/assets/images/models/' + keyword + '/'
        dest_post_dir = wayward_local + '/_posts/models/'

        os.makedirs(dest_asset_dir)
        
        #filename and frontmatter, file migration
        filename = year + '-' + month + '-' + day + '-' + str.replace(str.replace(title, ' ', '-'), ':', '-') + '.markdown'
        front = '---\nlayout: post\ntype: model\npermalink: /models/:title\ntitle: ' + title + '\nscale: ' + scale +'\ndate:  ' + year + '-' + month + '-' + day + '\nfolder: ' + keyword +'\nanimate: ' + animate + '\npreview: ' + preview + '\nphotos:\n'

        shutil.move(img_preview, (dest_asset_dir + 'preview.png'))

        increment = 1
        for photo in os.listdir(src_dir):
            shutil.move((src_dir + '/' + photo), dest_asset_dir + str(increment) + '.jpg')
            front = front + '- path: ' + str(increment) + '.jpg\n'
            increment += 1
        front = front + '---\n\n\n'

        #write to file
        write_path = os.path.join(dest_post_dir, filename)
        fp = open((write_path), 'x')
        fp.write(str(front + text))
        fp.close()

        self.show_frame(Success)
        
    def add_photos(self, cont):
        
        #get field values
        photoset = cont.photoset
        year = cont.photo_year.get()
        month = cont.photo_month.get()
        day = cont.photo_day.get()
        keyword = cont.photo_keyword.get()
        src_dir = cont.file_dir
        desc = cont.model_desc.get()

        #move and rename photo files, markdown generation
        dest_asset_dir = wayward_local + '/assets/images/photography/' + keyword +'/'
        dest_post_dir = wayward_local + '/_posts/photography/photos/' + keyword +'/'
        offset = len(os.listdir(dest_asset_dir))
        src_files = os.listdir(src_dir)
        for photo in src_files:
            offset += 1
            shutil.move((src_dir + '/' + photo), dest_asset_dir + str(offset) + '.jpg')
            

            #filename and frontmatter
            base_date = year + '-' + month + '-' + day
            filename = base_date + '-' + keyword + '-' + str(offset) + '.markdown'
            front = '---\n' + 'layout: post\n' + 'type: photography, picture\n' + 'permalink: /photography/:title\n' + 'title: ' + keyword + '-' + str(offset) + '\n' + 'date: ' + base_date + '\n' + 'keyword: ' + keyword + '\n' + 'imgpath: ' + str(offset) + '.jpg\n' + '---'

            write_path = os.path.join(dest_post_dir, filename)
            fp = open((write_path), 'x')
            fp.write(str(front + '\n\n\n'))
            fp.close()

            #tracking
            print(keyword + '-' + str(offset) + ' created')

        self.show_frame(Success)
         
    def quit(self):
        self.destroy()

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

        label = ttk.Label(self, text="Title:", font=LABEL_FONT)
        label.pack()
        model_title = tk.Entry(self)
        model_title.pack(pady=10,padx=10)
        self.model_title = model_title

        label = ttk.Label(self, text="Model Scale:", font=LABEL_FONT)
        label.pack()
        model_scale = tk.Entry(self)
        model_scale.pack(pady=10,padx=10)
        self.model_scale = model_scale

        label = ttk.Label(self, text="Date:", font=LABEL_FONT)
        label.pack()

        model_year=tk.StringVar(self)
        model_month=tk.StringVar(self)
        model_day=tk.StringVar(self)
        
        year = ttk.OptionMenu(self, model_year, "Year", "2017", "2018", "2019", "2020", "2021")
        model_year.set("Year")
        year.pack()
        self.model_year = model_year

        month = ttk.OptionMenu(self, model_month, "Month", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")
        model_month.set("Month")
        month.pack()
        self.model_month = model_month
        
        day = ttk.OptionMenu(self, model_day, "Day", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
        model_day.set("Day")
        day.pack()
        self.model_day = model_day

        button = ttk.Button(self, text="Select Image Source Folder",
                            command=lambda: controller.request_dir(self))
        button.pack(pady=5,padx=10)

        preview = ttk.Button(self, text="Select Preview Thumbnail",
                            command=lambda: controller.request_file(self))
        preview.pack(pady=10,padx=10)

        label = ttk.Label(self, text="Link to animate.gif", font=LABEL_FONT)
        label.pack()
        model_animate = tk.Entry(self)
        model_animate.pack(pady=10,padx=10)
        self.model_animate = model_animate

        label = ttk.Label(self, text="Link to preview.gif", font=LABEL_FONT)
        label.pack()
        model_pre = tk.Entry(self)
        model_pre.pack(pady=10,padx=10)
        self.model_pre = model_pre

        label = ttk.Label(self, text="Keyword:", font=LABEL_FONT)
        label.pack()
        model_keyword = tk.Entry(self)
        model_keyword.pack(pady=10,padx=10)
        self.model_keyword = model_keyword

        label = ttk.Label(self, text="Description:", font=LABEL_FONT)
        label.pack()
        model_desc = tk.Text(self)
        model_desc.pack(pady=10,padx=10)
        self.model_desc = model_desc

        button = ttk.Button(self, text="Create",
                            command=lambda: controller.model_gen(self))
        button.pack(pady=5,padx=10)

        button = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(Model))
        button.pack()        

        

class Photo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Studio Wayward Photography: Add Content", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="New Photoset",
                            command=lambda: controller.show_frame(Photoset))
        button.pack(pady=5,padx=10)

        button = ttk.Button(self, text="New Photographs",
                            command=lambda: controller.show_frame(Photographs))
        button.pack(pady=5,padx=10)

        button = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(SiteSelect))
        button.pack()

class Photoset(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Studio Wayward Photography: New Photoset", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        label = ttk.Label(self, text="Title:", font=LABEL_FONT)
        label.pack()
        set_title = tk.Entry(self)
        set_title.pack(pady=10,padx=10)
        self.set_title = set_title

        label = ttk.Label(self, text="Date:", font=LABEL_FONT)
        label.pack()

        set_year=tk.StringVar(self)
        set_month=tk.StringVar(self)
        set_day=tk.StringVar(self)
        
        year = ttk.OptionMenu(self, set_year, "Year", "2017", "2018", "2019", "2020", "2021")
        set_year.set("Year")
        year.pack()
        self.set_year = set_year

        month = ttk.OptionMenu(self, set_month, "Month", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")
        set_month.set("Month")
        month.pack()
        self.set_month = set_month
        
        day = ttk.OptionMenu(self, set_day, "Day", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
        set_day.set("Day")
        day.pack()
        self.set_day = set_day

        label = ttk.Label(self, text="Keyword:", font=LABEL_FONT)
        label.pack()
        set_keyword = tk.Entry(self)
        set_keyword.pack(pady=10,padx=10)
        self.set_keyword = set_keyword

        label = ttk.Label(self, text="Description:", font=LABEL_FONT)
        label.pack()
        set_desc = tk.Text(self)
        set_desc.pack(pady=10,padx=10)
        self.set_desc = set_desc

        button = ttk.Button(self, text="Create",
                            command=lambda: controller.set_gen(self))
        button.pack(pady=5,padx=10)

        button = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(Photo))
        button.pack()

class Photographs(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Add Photographs to Existing Photoset", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        photosets = ['']
        asset_dir = wayward_local +'/assets/images/photography/'
        for pset in os.listdir(asset_dir):
            if os.path.isdir(asset_dir + pset):
                photosets.append(pset)

        photoset = tk.StringVar(self)
        
        set_select = ttk.OptionMenu(self, photoset, *photosets)
        photoset.set("Choose a Set")
        set_select.pack()
        self.photoset = photoset

        label = ttk.Label(self, text="Photoset Keyword:", font=LABEL_FONT)
        label.pack()
        photo_keyword = tk.Entry(self)
        photo_keyword.pack(pady=10,padx=10)
        self.photo_keyword = photo_keyword

        label = ttk.Label(self, text="Date:", font=LABEL_FONT)
        label.pack()

        photo_year=tk.StringVar(self)
        photo_month=tk.StringVar(self)
        photo_day=tk.StringVar(self)
        
        year = ttk.OptionMenu(self, photo_year, "Year", "2016", "2017", "2018", "2019", "2020", "2021")
        photo_year.set("Year")
        year.pack()
        self.photo_year = photo_year

        month = ttk.OptionMenu(self, photo_month, "Month", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12")
        photo_month.set("Month")
        month.pack()
        self.photo_month = photo_month
        
        day = ttk.OptionMenu(self, photo_day, "Day", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31")
        photo_day.set("Day")
        day.pack()
        self.photo_day = photo_day

        button = ttk.Button(self, text="Select Source Folder",
                            command=lambda: controller.request_dir(self))
        button.pack(pady=5,padx=10)

        button = ttk.Button(self, text="Submit",
                            command=lambda: controller.add_photos(self))
        button.pack()
        
        button = ttk.Button(self, text="Back",
                            command=lambda: controller.show_frame(Photo))
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

class Success(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Post Created!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        label = ttk.Label(self, text="Please restart app to see changes.", font=LABEL_FONT)
        label.pack(pady=10,padx=10)

        button = ttk.Button(self, text="Continue",
                            command=lambda: controller.show_frame(SiteSelect))
        button.pack() 

        button = ttk.Button(self, text="Finish",
                            command=lambda: controller.quit())
        button.pack()  
        

app = SW_submit()
app.mainloop()
        
            
