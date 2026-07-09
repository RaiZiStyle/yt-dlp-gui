# References : 

- https://github.com/yt-dlp/yt-dlp

Supported site : https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md


# TODO : 
- [x] Better info in size (limit to 2 decimals, and handle MB, GB)
- [x] Cancel Btn when downloading   
    - [x] Make the statusBar update acordingly
- [x] GUI HELP : 
- [ ] Better handle the output (user can't overwrite the name of the file currently & the input is a dir, but the output is a file)
- [ ] Make a Icon ? 


## ISSUE - Error handler
- [x]  If i query twice, some info stack
- [x]  No url given
- [x]  Handle playlist (see `URL_THAT_FAILED`) (pretty simple, clean the url)
- [x]  No output given
- [x] Handle timeout/no Internet, no youtube video
- [x] Reset info when error in download



# How to launch CI/CD : 
`git tag -a vx.y.z -m "message"`