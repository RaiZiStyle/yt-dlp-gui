# References : 

- https://github.com/yt-dlp/yt-dlp

Supported site : https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md


# TODO : 
- [x] Better info in size (limit to 2 decimals, and handle MB, GB)
- [ ] Cancel Btn when downloading   
- [ ] Make the statusBar update acordingly
- [ ] Better handle the output (user can't overwrite the name of the file currently & the input is a dir, but the output is a file)
- [ ] Make a Icon ? 
- [ ] GUI HELP : 
Prompt : 
```
Comment je pourrais faire une help a mon GUI ? C'est très rapide en vrai y'a X etapes : 

1. Charger une URL dans le champs "URL"
2. Selectionner le type , video ou audio.
3. Clique sur charger
(techniquement y'a un cas ici ou ca plante mais on le met de coté)
4. Choisir la qualité dans la liste déroulante
5. Sélectionner dans quel dossier il va aller (le nom du fichier sera crée automatiquement)
```

## ISSUE - Error handler
- [x]  If i query twice, some info stack
- [x]  No url given
- [x]  Handle playlist (see `URL_THAT_FAILED`) (pretty simple, clean the url)
- [x]  No output given
- [x] Handle timeout/no Internet, no youtube video
- [x] Reset info when error in download



# How to launch CI/CD : 
`git tag -a vx.y.z -m "message"`