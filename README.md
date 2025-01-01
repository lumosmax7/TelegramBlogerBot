# Auto Github Page generator by tg-bot
## Usage
1. Clone this project and assure your blog can be correctly deployed on GitHub.
2. Fill two environment variables in the config.py file: `TOKEN` and `GP_URL`. `TOKEN` is your tg-bot token, `GP_URL` is the url of your github page.
3. Run `docker-compose up --build`
4. Enjoy your tg-bot with command `/start` 


## Requirement
1. python3
2. pip3
3. Node.js
4. npm
5. tg-bot python api
6. hexo
7. git

## TODO
- [x] Add a command to change a previous post
- [x] Package the code into a docker image.
- [x] Hexo init --> turn to mount volume
- [x] Hexo setting(Focusing on Github deploy)
- [x] Using docker to deploy the bot service.
- [ ] code optimization 
- [ ] pics optimization
