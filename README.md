# Progression

1. Telephone -> email
2. Coffee Shop index.html
3. Coffee Shop menu.html
4. Admin Site cookies
5. Admin Site (WIP)

# Coffee Shop Website

## `index.html`: Hidden in plain sight

**Clue:** We've gained some intel on the criminals. They operate a coffee shop in Dana Point, CA. Their website looks pretty normal, which seems suspicious. Take a good look around to see if you can find anything unusual.

**Hint:** Selecting text can reveal things you might not normally see.

### Solution

The flag is hidden in plain sight

Flag: `Y!!q2f~xq*:m_~&e3.ee9,C5`

## `menu.zip`: Zipped

**Clue:** Great job, Agent! We also noticed on the menu page that one of the product photos has an abnormality. There might be a flag which will help us gain more info.

**Hint:** Look at the "Zippy Orange Tea" image. Did you know that you can hide `.zip`s in many normal files, like JPEG images?

### Solution

- The picture of the `insert something here` has a `.zip` file embedded in it.
- Inside the `.zip` is the script of the Bee Movie

Flag: `e44B,%y]_5:bNK&*<KD"*Tuj`

# Internal Panel

## Insecure State Mangement (Cookies)

**Clue:** We've intercepted the logins for their secure internal panel. The username is `steve`, password is `P@$$word`. (Talk about "secure"!) Unfortunately, they don't have admin privileges, so all we can find is that their secret Double Chocolate Chip Cookie recipie. Maybe you should login and take a look around.

**Hint:** There might be something stored in the cookies. Use your browser's developer tools or an extension (try Cookie-Editor on Chrome) to view your cookies.

### Solution

- Log in using the combo above
- Analyze the cookie data using an extension or developer tools.
- Change the `admin` value of the from `0` to `1` and refresh.

## Internal Memos (URL Parameters)

Work in Progress

### Solution

- Change URL parameter from X to Y, revealing other memo with flag.

# Mainframe Endpoint

## TCP Service

**Clue:** We ran a port scan on their server and discovered a TCP service running on port 9648. Try connecting to it to see what you find. You can use the `telnet` or `nc` utilities to connect to TCP services.

**Hint:** This might be trickier for many, compared to the previous challenges. When you connect to the TCP service using `telnet` or `nc`, you are presented with a math problem that you probably won't be able to do in your head. However, if you take too long, it will either reject your answer or timeout. You're going to need to automate this process somehow. Try writing a program. The `socket` library for Python is a good start.
