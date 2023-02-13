from tkinter import *
from tkinter import ttk
from tkinter import filedialog, simpledialog,messagebox
from PIL import Image, ImageTk
from urllib.request import urlopen
from pytube import YouTube
from io import BytesIO
import re,os,threading,platform

class downloader(Tk):
    def __init__(self):
        super().__init__()
        self.style = ttk.Style(self)

        #chosing theme on the basis of system
        if platform.system()=='Windows':
            self.style.theme_use('winnative')
        else:
            self.style.theme_use('default')

        self.resizable(False, False)
        self.title("Youtube Video Downloader")
        self.iconbitmap("icon.ico")
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1,column=0)

        thumb_img = ImageTk.PhotoImage(file=r'movie.png')
        thumb_img1 = ImageTk.PhotoImage(file=r'sound.png')

        #Some colours for Notebook Tab -Reference
        _bgcolor = '#B0D3EE'  
        _fgcolor = '#000000'  
        _compcolor = '#8FC3EA' 
        _ana2color = 'beige' 
       
        #Canvas for Banner
        self.canvas=Canvas(self,width=600,height=100)
        self.canvas.grid(row=0,column=0)

        self.Banner=ImageTk.PhotoImage(Image.open("youtube.jpg"))
        self.canvas.create_image(0,0,image=self.Banner,anchor=NW)

        # creating tabs for Notebook and adding them in Dictionary
        self.tab = dict()
        self.img = list()
        self.tab["VIDEO"] = Frame(self.notebook, width=600, height=600)
        self.tab["AUDIO"] = Frame(self.notebook)
        self.img.append(thumb_img)
        self.img.append(thumb_img1)

        i = 0
        for x in self.tab.keys():
            self.notebook.add(self.tab[x], text=x,
                              image=self.img[i], compound=LEFT)
            i = i+1

        # Creating Default Path
        Directory = "Yotube Downloader By Coder Community"
        Dir_Name = "C:/"
        self.path = os.path.join(Dir_Name, Directory)
        try:
            os.mkdir(self.path)
            os.mkdir("C:/Yotube Downloader By Coder Community/Video")
            os.mkdir("C:/Yotube Downloader By Coder Community/Audio")
        except OSError as error:
            pass

        def path_loc():
            global filename
            filename = filedialog.askdirectory()
            self.output_entry.delete(0, END)
            self.output_entry.insert(END, filename)
            if filename == "":
                self.output_entry.insert(
                    END, "C:/Yotube Downloader By Coder Community")

        def fetch():
            #Preparing Window For Fetching the Video ( inculdes deleting older data etc.)
            try:
                for widget in self.container_3.winfo_children():
                    widget.grid_forget()
                self.container_2.grid()
                self.percent.grid_forget()
                self.my_progress.config(mode="indeterminate")
            except Exception as e:
                pass

            self.my_progress.grid(row=0, column=0)
            self.my_progress.start(10)

            # Fetching Video Title
            self.url = self.urlbox.get()
            self.yt = YouTube(self.url)
            self.label4.config(text=self.yt.title,wraplength=500, justify="center")

            self.label4.grid(row=0, column=0, columnspan=2, pady=10)

            # Fetching Video Thumbnail using both pytube and Extracting using regex
            try:
                self.vid_id = re.search(
                    r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", self.url)
                self.img_url = urlopen(
                    f"https://img.youtube.com/vi/{self.vid_id.group(1)}/maxresdefault.jpg").read()
                self.image = Image.open(BytesIO(self.img_url))
                self.resize = self.image.resize(
                    (300, 200), Image.Resampling.LANCZOS)
                self.image1 = ImageTk.PhotoImage(self.resize)
                self.canvas.create_image(0, 0, image=self.image1, anchor=NW)

            except Exception as error:
                self.img_url = urlopen(self.yt.thumbnail_url).read()
                self.image = Image.open(BytesIO(self.img_url))
                self.resize = self.image.resize((300, 200), Image.Resampling.LANCZOS)
                self.image1 = ImageTk.PhotoImage(self.resize)
                self.canvas.create_image(0, 0, image=self.image1, anchor=NW)

            self.canvas.grid(row=1, column=0, rowspan=7, pady=6,padx=3)

            self.Length = self.yt.length
            if self.Length > 60 and self.Length < 3600:
                minute = self.Length//60
                second = self.Length % 60
                self.video_length.config(
                    text=f"Length: {minute} minutes {second} seconds")

            elif self.Length >= 3600:
                hour = (self.Length//60)//60
                minute = (self.Length//60) % 60
                second = self.Length % 60
                self.video_length.config(
                    text=f"Length: {hour} hour {minute} minutes {second} seconds")

            elif self.Length < 60:
                self.video_length.config(text=f"Length: {self.Length} seconds")

            self.video_length.grid(row=2, column=1, sticky=W)

            self.author.config(text=f"Author: {self.yt.author}")
            self.views.config(text="Views: {:,}".format(self.yt.views))
            self.author.grid(row=3, column=1, sticky=W)
            self.views.grid(row=4, column=1, sticky=W)

            if name == "VIDEO":
                self.notebook.tab(1, state="disabled")
                self.reso.grid(row=5, column=1, sticky=E)

                # Getting All Available Resolutions
                self.clicked = StringVar()
                self.resolution = [stream.resolution for stream in self.yt.streams.filter(file_extension="mp4", progressive=True)]
                self.clicked.set("Select Video Resolution")

                # Dropdown for selecting resolution
                self.dropdown = OptionMenu(self.container_3, self.clicked, *self.resolution)
                self.dropdown.config(bg="#c2dcf0",cursor="hand2", activebackground="#c2dcf0", activeforeground="black",font=("Arial Bold",10))
                self.dropdown.grid(row=6, column=1, ipady=5, ipadx=10)
                self.reso.config(
                    text=f"Available Resolutions: {self.resolution[:]}")
                self.download_button.grid(row=7, column=1, ipadx=50, ipady=15, pady=5, padx=5, sticky=EW)
    
                self.container_2.grid_forget()

            if name == "AUDIO":
                self.notebook.tab(0, state="disabled")
                self.reso.grid(row=5, column=1, sticky=W)
                self.reso.config(text=f"Audio Format: MP3")
                self.extra_label.config(text="Audio Is Ready To Download")
                self.extra_label.grid(row=6, column=1)
                self.download_button.grid(row=7, column=1, ipadx=50, ipady=15, pady=5, padx=5, sticky=EW)
                self.container_2.grid_forget()

        def on_progress(stream, chunk, bytes_remaining):
            global inc,my_progress,label2,filename
            self.total_size = stream.filesize
            bytes_downloaded = self.total_size - bytes_remaining
            percentage_of_completion = bytes_downloaded / self.total_size * 100
            inc=int(percentage_of_completion)

            #Upating Progress Bar
            self.my_progress["value"]+=inc-self.my_progress["value"]
            self.percent.config(text=f"{inc}%")
            if self.my_progress["value"]==100:
                self.container_2.grid_forget()
                self.percent["text"]="0%"
                messagebox.showinfo("Youtube Downloader",f"Downloaded Successfully...\nPath: {self.output_entry.get()}")   
                self.notebook.tab(1, state="normal")
                self.notebook.tab(0, state="normal")


        def download():

            if name == "VIDEO":
                if self.output_entry.get() == "C:/Yotube Downloader By Coder Community":
                    os.chdir("C:/Yotube Downloader By Coder Community/Video")
                else:
                    os.chdir(f"{filename}")

                try:
                    file=self.yt.streams.filter(res=self.clicked.get()).first()
                    self.size=file.filesize
                    ask=messagebox.askyesno("Do You Want To Download",f"File Size: {round(self.size* 0.000001, 2)} MegaBytes")
                    if ask==True:
                        self.container_2.grid(row=3, column=0)
                        self.my_progress.config(mode="determinate")
                        self.my_progress.stop()
                        self.percent.grid(row=0, column=1)
                        self.yt.register_on_progress_callback(on_progress)  
                        self.yt.streams.filter(res=self.clicked.get()).first().download()

                except Exception as e:
                    messagebox.showerror("Error","Error Raised Due To!\n#UnSelected Resolution  \n#Your Internet Connectivity")
                
            if name == "AUDIO":
                if self.output_entry.get() == "C:/Yotube Downloader By Coder Community":
                    os.chdir("C:/Yotube Downloader By Coder Community/Audio")
                else:
                    os.chdir(f"{filename}")
                try:
                    mp3=self.yt.streams.filter(only_audio=True).first()
                    self.size=mp3.filesize
                    get=messagebox.askyesno("Do You Want To Download",f"File Size: {round(self.size* 0.000001, 2)} MegaBytes")
                    if get==True:
                        self.container_2.grid(row=3, column=0)
                        self.my_progress.config(mode="determinate")
                        self.my_progress.stop()
                        self.percent.grid(row=0, column=1)
                        self.yt.register_on_progress_callback(on_progress)  
                        audio=self.yt.streams.filter(only_audio=TRUE).first().download()
                        base, ext = os.path.splitext(audio)
                        converted=base +'.mp3'  
                        os.rename(audio,converted)
                      
                except Exception as e:
                    messagebox.showerror("Error ","Error Raised Due To!\n\n>Your Internet Connectivity")


        # Creating Thread for fetching Video
        def thread():
            self.thread=threading.Thread(target=fetch)
            self.thread.start()

        # Creating Thread for Downloading Video
        def thread1():
            self.thread=threading.Thread(target=download)
            self.thread.start()

        # container for urlbox and Browse File
        self.container_1 = Frame(self,width=800,height=500,highlightbackground="grey",highlightthickness=2,highlightcolor="grey")
        
        # container for progress bar
        self.container_2 = Frame(self,highlightbackground="grey",highlightthickness=2,highlightcolor="grey")
        
        # container for thumbnail and information
        self.container_3 = Frame(self,highlightbackground="grey",highlightthickness=2,highlightcolor="grey")


        self.label1 = Label(self.container_1,text="Enter URL and download location",font=("Arial bold",10))
        self.label1.grid(column=0,row=0,columnspan=3,sticky=W)    

        # Url Box/Button/Label Creation
        self.label2=Label(self.container_1,text="Video url:",font=("Arial bold",9))
        self.label2.grid(column=0,row=1)

        self.urlbox=Entry(self.container_1,width=63,font=("Arial Bold",10),borderwidth=2,highlightbackground="black",highlightthickness=2, relief=SUNKEN)
        self.urlbox.grid(row=1,column=1,ipady=1,columnspan=2,pady=6)

        img1=ImageTk.PhotoImage(file=r"fetch.png")
        self.fetch_button=Button(self.container_1,text="",image=img1,font=("Arial Bold",9),bg="#c2dcf0",cursor="hand2",compound=LEFT,command=thread)
        self.fetch_button.image=img1
        self.fetch_button.grid(row=1,column=3,padx=2)
  
        # Browse File Box/Button/Label Creation
        self.label3=Label(self.container_1,text="Save to:",font=("Arial bold",9))
        self.label3.grid(column=0,row=2)

        self.output_entry=Entry(self.container_1,width=63,font=("Arial bold",10),borderwidth=2)
        self.output_entry.grid(row=2,column=2,ipady=3)
        self.output_entry.insert(END,"C:/Yotube Downloader By Coder Community")
         
        img2=ImageTk.PhotoImage(file=r"browse.png")
        self.browse_loc=Button(self.container_1,text="Browse",image=img2,font=("Arial Bold",9),bg="#c2dcf0",cursor="hand2",compound=LEFT,command=path_loc)
        self.browse_loc.image=img2
        self.browse_loc.grid(row=2,column=3,ipadx=10,pady=3,padx=2)

        # Progress Bar
        self.my_progress=ttk.Progressbar(self.container_2,orient=HORIZONTAL,length=550,mode="indeterminate")
          
        # Video title
        self.label4=Label(self.container_3,text="",font=("Arial Bold",14),relief="solid")

        # canvas for thumbnail
        self.canvas=Canvas(self.container_3,width=300,height=200,bg="grey")
        
        # labels for video information

        self.video_length=Label(self.container_3,text="",font=("Arial Bold",13)) 

        self.author=Label(self.container_3,text="",font=("Arial Bold",13))
        
        self.views=Label(self.container_3,text="",font=("Arial Bold",13))

        self.reso=Label(self.container_3,text="",font=("Arial Bold",13))

        self.extra_label=Label(self.container_3,text="",font=("Arial Bold",13),fg="green")
        
        # Label For Progress Bar(To show Percentage)
        self.percent=Label(self.container_2,text="0%",font=("Arial Bold",15))

        # Download Button
        img=ImageTk.PhotoImage(file=r"download.png")
        self.download_button=Button(self.container_3,text="Download",image=img,font=("Arial Bold",10),bg="#c2dcf0",cursor="hand2",command=thread1,compound=LEFT)
        self.download_button.image=img

        
        self.style.configure("TNotebook", tabposition='n')
        self.style.configure("TNotebook.Tab",  font=('Arial Bold','12'))
        self.style.configure('TNotebook.Tab',background=_bgcolor)
        self.style.configure('TNotebook.Tab',foreground=_fgcolor)
        self.style.map('TNotebook.Tab',background=[('selected', _compcolor), ('active',_ana2color)])
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_change)

        
    def tab_change(self, event):
            global name
            id = self.notebook.select()
            name = self.notebook.tab(id, "text")
            self.container_1.grid(row=0,column=0,in_= self.tab[name],pady=2)
            self.container_3.grid(row=1,column=0,in_= self.tab[name],pady=2)
            self.container_2.grid(row=3,column=0,in_= self.tab[name],pady=2)
            
            self.urlbox.focus_force()
            
            if name=="VIDEO":
                self.container_2.grid_forget()
                self.fetch_button.config(text="Fetch Video")
            elif name=="AUDIO":
                self.container_2.grid_forget()
                self.fetch_button.config(text="Fetch Audio")
            

if __name__ == '__main__':
    window=downloader()
    window.mainloop()
