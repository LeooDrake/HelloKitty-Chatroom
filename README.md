# README




## Leo's Chat room
Built to recreate a basic 2000s chat room.




![the homepage ](chatroomhomepage.png)
## usage
Communication is an essential part to living in a complex society. Technology allows us to be better connected than ever,
messaging is an essential part to modern communication and its implications are exponential.

## version
Leo's Chatroom version `1.` </br>
[Leo's Chat room](https://project2-siaj.onrender.com) </br>
[Git repository](https://github.com/LeooDrake/project2) </br>



## instructions

- 1. simply create an account.
- 2. Select search from the menu and type in your friends email address.
- 3. if it exists in database then you will be able to leave them messages.
- 4. If your friend is loggedin then you can send messages in realtime.

## Data

chat_room database contains 2 tables. `users` and `messages`.

### `users`
![Users table ](users.png)
### `messages`
![Messages table ](messages.png)




## strengths

- uses web sockets which allows for realtime chatting.
- css formated to work on mobile devices and desktop


## limitations

- render can be extremely slow.
- satisfys basic chatroom functionality.
- still very minimal viable product for a basic chatroom.
- With these sockets I wanna make it so it goes into db automatically and doesn’t refresh page to update form to send.
- internal database error if search isnt a valid email

## extensions 

- groupchats.
- adding friends.
- sending more than just raw text.


### libraries
- Flask
- Gunicorn
- psycopg2
- bcrypt
- datetime
- flask_socketio

### License

`MIT License`

`Copyright (c) 2018 Render Developers`

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
