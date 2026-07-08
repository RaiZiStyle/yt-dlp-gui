# References : 

- https://github.com/yt-dlp/yt-dlp


# TODO : 
- [x] Get format list
- [x] Find a way to make a "formulaire" since we need to select video or audio, perhaps it's not really usefull ? will see
- [x] Make the query in a thread.
- [x] make an equivalent of `yt-dlp -f bestvideo+bestaudio URL`
- [x] Make an .exe installer via pyinstaller
- [x] Think how to handle FFMPEG
- [x] Logging system ? 
- [ ] Cancel Btn when downloading   
- [ ] Make a Icon ? 

## TODO - Error handler
- [x]  If i query twice, some info stack
- [x]  No url given
- [x]  Handle playlist (see `URL_THAT_FAILED`) (pretty simple, clean the url)
- [x]  No output given
- [x] Handle timeout/no Internet, no youtube video
- [ ] Reset info when error in download

# Issues : 
- setFixedSize & setMinimumSize not working.



# Gui : 

```txt
┌──────────────────────────────────────────────────────────────┐
│ URL                                                         │
│ ┌──────────────────────────────────────────────┐ [ Charger ]│
│ │ https://youtube.com/watch?v=xxxx             │            │
│ └──────────────────────────────────────────────┘            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ ┌──────────────┐  Titre de la vidéo                          │
│ │              │  Chaîne Youtube                             │
│ │  Miniature   │  Durée : 12:34                              │
│ │              │                                              │
│ └──────────────┘                                              │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ Type                                                        │
│ ○ Vidéo                                                     │
│ ○ Audio                                                     │
│                                                              │
│ Qualité                                                     │
│ ┌────────────────────┐                                      │
│ │ 1080p MP4          ▼│                                      │
│ └────────────────────┘                                      │
│                                                              │
│ Dossier                                                     │
│ ┌─────────────────────────────┐ [ Parcourir ]               │
│ │ C:\Downloads                │                             │
│ └─────────────────────────────┘                             │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ [====================          ] 62 %                        │
│ Téléchargement : 3.2 MB/s                                   │
│ Temps restant : 00:12                                       │
│                                                              │
│                          [ Télécharger ]                    │
│                                                              │
└──────────────────────────────────────────────────────────────┘

```


# How to launch CI/CD : 
`git tag -a vx.y.z -m "message"`