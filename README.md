# References : 

- https://github.com/yt-dlp/yt-dlp


# TODO : 
- [x] Get format list
- [x] Find a way to make a "formulaire" since we need to select video or audio, perhaps it's not really usefull ? will see
- [x] Make the query in a thread.
- [ ] Make an .exe installer via pyinstaller
- [ ] Logging system ? 
- [ ] make an equivalent of `yt-dlp -f bestvideo+bestaudio URL`

## TODO - Error handler
- [ ]  No url given
- [ ]  Handle playlist (see `URL_THAT_FAILED`) (pretty simple, clean the url)
- [ ]  No output given
- [ ]  If i query twice, some info stack

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