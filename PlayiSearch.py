#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tkinter import *
from pygame import mixer
import requests
import base64
import json
from tkhtmlview import HTMLLabel
from secrets import *
import sqlite3
con = sqlite3.connect("spotify.db")
c = con.cursor()
import webbrowser
master = Tk()
mixer.init()
mixer.music.load("song.mp3")

class Spotify :
    def __init__(self,master,title,labeltxt):
        self.master = master
        self.master.title = title
        self.master.geometry("600x500")
        self.back = PhotoImage(file = "music.png")
        bgimage = Label(self.master,image = self.back).place(x = 0,y = 0)
        w = Label ( self.master, text = labeltxt,font = ("Arial",30))
        w.grid(row = 0,column = 2)
        self.counter = 0
        y = Button(self.master,text = "Back",command = lambda:Window(master)).place(x=0,y=0)
        
    def search(self,keyword,endpoint,param1,param2):
        global entry
        global olist
        global res
        if endpoint == None :
            c.execute(f'SELECT * FROM {param1} LIMIT {param2}')
            data = c.fetchall()
            print(data)
            f = Frame(self.master)
            f.place(x = 50 , y = 250 , width = 300)
            scroll_bar = Scrollbar(f)

            scroll_bar.pack( side = RIGHT,fill = Y )
            olist = Listbox(f,yscrollcommand = scroll_bar.set)
            olist.pack( fill = BOTH )
            scroll_bar.config(command = olist.yview)
            for i in range(len(data)) :
                olist.insert(i,data[i][2])
        else:
            
            searchtext = entry.get()
            print(searchtext)


            # Step 1 - Authorization 
            url = "https://accounts.spotify.com/api/token"
            headers = {}
            data = {}

            # Encode as Base64

            clientId = "<Enter your client Id>"
            clientSecret =  "<Enter your Client Secret>"

            message = f"{clientId}:{clientSecret}"
            messageBytes = message.encode('ascii')
            base64Bytes = base64.b64encode(messageBytes)
            base64Message = base64Bytes.decode('ascii')

            headers['Authorization'] = f"Basic {base64Message}"
            data['grant_type'] = "client_credentials"

            r = requests.post(url, headers=headers, data=data)

            token = r.json()['access_token']
            #print(token)

            token = r.json()['access_token']

            # Step 2 - Use Access Token to call playlist endpoint


            print(keyword)
            print(searchtext)

            from googlesearch import search
            query = "spotify" + keyword + searchtext 
            for i in search(query,num = 1, stop = 1):
              print(i)
            spotifyId = i.split("/")[-1]
            print(spotifyId)

            #playlistId = "7nYJDIm5nHyNTS2KugaD4w"
            if endpoint == "https://api.spotify.com/v1/artists":
                spotifyUrl = f"{endpoint}/{spotifyId}/top-tracks?market=ES"

            else:
                spotifyUrl = f"{endpoint}/{spotifyId}"

            print(spotifyUrl)

            headers = {
                "Authorization": "Bearer " + token
            }

            res = requests.get(url=spotifyUrl, headers=headers)
            f = Frame(self.master)
            f.place(x = 50 , y = 250 , width = 300)
            scroll_bar = Scrollbar(f)

            scroll_bar.pack( side = RIGHT,fill = Y )
            olist = Listbox(f,yscrollcommand = scroll_bar.set)
            olist.pack( fill = BOTH )
            scroll_bar.config(command = olist.yview)

            print(res.json())
  
            
        
            if endpoint == "https://api.spotify.com/v1/artists":
                
                for i in res.json()["tracks"] :
                    olist.insert(END,i[param1][param2])
                    
                    
                    c.execute('INSERT INTO artisearch(id,Artist_Searched,Songs) VALUES(?,?,?)',(self.counter,searchtext,i[param1][param2]))
                    self.counter+=1
                    con.commit()

            elif endpoint == "https://api.spotify.com/v1/tracks":
                
                for i in (res.json()["artists"]):
                    olist.insert(END,i[param1][param2])
                    
                    webbrowser.open(i[param1][param2])
                    c.execute('INSERT INTO songisearch(id,Song_Searched,Url) VALUES(?,?,?)',(self.counter,searchtext,i[param1][param2]))
                    self.counter+=1
                    con.commit()
            else:
                for i in range(len(res.json()["tracks"]['items'])):

                    olist.insert(END, res.json()["tracks"]['items'][i][param1][param2])
                    
                    c.execute('INSERT INTO playlisearch(id,Playlist_Searched,Songs) VALUES(?,?,?)',(self.counter,searchtext,res.json()["tracks"]['items'][i][param1][param2]))
                    self.counter+=1
                    con.commit()
            
            my_label = HTMLLabel(self.master, html=f"""
            <a style = "text-align : center;" href ="https://open.spotify.com/embed/{keyword}/{spotifyId}" width="50%" height="10" frameborder="0" allowtransparency="true" allow="encrypted-media">LISTEN NOW</a>
            """)
            # Adjust label
            my_label.place(x = 400 , y = 250, width = 100 , height = 27)
               

    def home(self,keyword,endpoint,param1,param2):
        global entry
        label = Label(self.master,text = f"Enter {keyword} : ",font = ("Arial",20)).grid(row = 2,column = 1,pady = 15)
        entry = Entry(self.master)
        entry.grid(row = 2, column = 2, pady = 5)
#         background_img = PhotoImage(file="transparent.png")
        button = Button(self.master,text = "Search",command = lambda:self.search(keyword,endpoint,param1,param2), borderwidth = 0).grid(row = 3,column = 2,pady = 20)
    
    def getData(self,keyword,endpoint,param1,param2):
        button = Button(self.master,text = "Get Top Playlists",command = lambda:self.search(keyword,endpoint,param1,param2), borderwidth = 0).grid(row = 3,column = 1,pady = 20)
        button = Button(self.master,text = "Get Top Artists",command = lambda:self.search(keyword,endpoint,"artisearch",param2), borderwidth = 0).grid(row = 3,column = 2,pady = 20)
        button = Button(self.master,text = "Get Top Songs",command = lambda:self.search(keyword,endpoint,"songisearch",1), borderwidth = 0).grid(row = 3,column = 3,pady = 20)
        
#         c.execute('SELECT * FROM playlisearch LIMIT 10')
#         data = c.fetchall()
#         print(data)
#         f = Frame(self.master)
#         f.place(x = 50 , y = 250 , width = 300)
#         scroll_bar = Scrollbar(f)
  
#         scroll_bar.pack( side = RIGHT,fill = Y )
#         olist = Listbox(f,yscrollcommand = scroll_bar.set)
#         olist.pack( fill = BOTH )
#         scroll_bar.config(command = olist.yview)
#         for i in range(len(data)) :
#             olist.insert(i,data[i][2])

class Window :
    def __init__(self,master):
        self.master = master
        self.master.title = "Spotify"
        self.master.geometry("600x400")
        self.back = PhotoImage(file = "music.png")
        bgimage = Label(self.master,image = self.back).place(x = 0,y = 0)
        
        
        w = Label ( self.master, text = "Choose one of the following :",font = ("Arial",17))

        w.grid(row = 1,column = 2,pady = 10)
        b1 = Button(self.master,text = "Search Playlist",command = self.playlisearch).grid(row = 3,column = 1, pady = 40,padx = 30)
        b2 = Button(self.master,text = "Search Artist", command = self.artisearch).grid(row = 3,column = 2,pady = 40)
        b3 = Button(self.master,text = "Search Song", command = self.songisearch).grid(row = 3,column = 3,pady = 40)
        b4 = Button(self.master,text = "See Top 5 Searched Songs",command = self.user).grid(row = 4,column = 2,pady = 30)
        
#         self.f = Frame(self.master).place(x = 20, y = 60, bordermode = OUTSIDE, height = 50, width = 100)
        b5 = Button(self.master,text = "Play",command = mixer.music.play).grid(row = 7 , column = 0, pady = 40)
        b6 = Button(self.master,text = "Pause",command = mixer.music.pause).grid(row = 7, column = 1, pady = 40)
        b7 = Button(self.master,text = "Stop",command = mixer.music.stop).grid(row = 7, column = 2, pady = 40)
        b8 = Button(self.master,text = "Resume",command = mixer.music.unpause).grid(row = 7 , column = 3, pady = 40)
        
    def playlisearch(self):
        x = Spotify(master,"PlayliSearch","PlayliSearch")
        x.home("playlist","https://api.spotify.com/v1/playlists","track","name")
        
    def artisearch(self):
        x = Spotify(master,"ArtiSearch","ArtiSearch")
        x.home("artist","https://api.spotify.com/v1/artists","album","name")
    
    def songisearch(self):
        x = Spotify(master,"SongiSearch","SongiSearch")
        x.home("track","https://api.spotify.com/v1/tracks","external_urls","spotify")
        
    def user(self):
        x = Spotify(master,"Favourites","Favourites")
        x.getData("Songs",None,"playlisearch",10)
        
#https://api.spotify.com/v1/artists/{id}
#f"https://api.spotify.com/v1/playlists/{playlistId}"
#<iframe src="https://open.spotify.com/embed/album/4PwSDqUwhh4sZUHyi7UzXb" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
main = Window(master)
master.mainloop()
con.close()





