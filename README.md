# References : 

- https://github.com/yt-dlp/yt-dlp


# TODO : 
1. Get format list
2. Make an .exe installer via pyinstaller
3. Find a way to make a "formulaire" since we need to select video or audio, perhaps it's not really usefull ? will see
X. Make the query in a thread. 

X. Logging system ? 

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