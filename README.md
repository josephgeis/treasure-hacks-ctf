# Treasure Hacks CTF Challenges

Designed by Joseph Geis ([@josephgeis](https://github.com/josephgeis)).
Licensed under the MIT license

# Progression

1. Audio/morse challenge
2. Coffee Shop index.html
3. Coffee Shop menu.html
4. Admin Site cookies
5. Admin Site memo
6. Mainframe

# Audio Challenge

**Clue:** Welcome aboard agent! We have been tracking some criminals who have been committing crimes around Southern California. We need more cybersecurity agents like you to help gain intel. Join the `Audio Flag` voice channel to hear a secret message, which is your first flag. (To submit it as a flag, type it as `\flag{<message>}`, replacing `<message>` with the secret message.)

If you are hearing impaired, please DM josephDaCoder to get a transcription.

**Hint:** .... .- -.-. -.- -- . (also give if hearing impaired)

**Flag:** `hackme`

# Coffee Shop Website

## `index.html`: Hidden in plain sight

**Clue:** We've gained some intel on the criminals. They operate a coffee shop in Dana Point, CA. Their website looks pretty normal, which seems suspicious. Take a good look around to see if you can find anything unusual. Go to https://a.ctf.treasurehacks.dev/index.html.

**Hint:** Selecting text can reveal things you might not normally see. You could also try using the source code.

**Flag:** `pdmRgS4ScTeWRhrp`

### Solution

The flag is hidden in plain sight

## `menu.zip`: Zipped

**Clue:** We also noticed on the menu page that one of the product photos has an abnormality. There might be a flag which will help us gain more info. Go to https://a.ctf.treasurehacks.dev/menu.html.

**Hint:** Look at the image file sizes. Notice that one of them is abnormally larger. Did you know that you can hide `.zip`s in many normal files, like JPEG images? Also, remember that flags start with `\flag`.

**Flag:** `LOZqJxitPnkw5tyi`

### Solution

- The picture of the `insert something here` has a `.zip` file embedded in it.
- Inside the `.zip` is the script of the Bee Movie

# Internal Panel

## Insecure State Mangement (Cookies)

**Clue:**
We've intercepted the logins for their secure internal panel. The username is `steve`, password is `P@$$word`. (Talk about "secure"!) Unfortunately, they don't have admin privileges, so all we can find is that their secret Double Chocolate Chip Cookie recipie. Maybe you should login and take a look around.

Access the admin panel at https://b.ctf.treasurehacks.dev/

**Hint:** There might be something stored in the cookies. Use your browser's developer tools or an extension (try Cookie-Editor on Chrome) to view your cookies.

**Flag:** `ok8mWDVCS36Caipa`

### Solution

- Log in using the combo above
- Analyze the cookie data using an extension or developer tools.
- Change the `admin` value of the from `0` to `1` and refresh.

## Internal Memos (URL Parameters)

**Clue:**
We obtained this email from what appears to be the internal criminals' internal message board system. We imagine that they have used it in the past to coordinate their plots. Examine it and see what you can find.

```
Date: October 13, 2021
From: noreply@danaptcoffee.com
To: steve@danaptcoffee.com
Subject: New memo available

A new memo is available for your viewing. Please access it at https://b.ctf.treasurehacks.dev/memo/3
```

**Hint**: Take a look at the ID in the URL. What would happen if you changed it from `3` to something lower?

**Flag:** `XXUWpamNQqxYk98D`

### Solution

- Change URL parameter from 3 to 1, revealing other memo with flag.

# Mainframe Endpoint

## TCP Service

**Clue:** We ran a port scan on their admin panel server (b.ctf.treasurehacks.dev) and discovered a TCP service running on port 9648. Try connecting to it to see what you find. (You can use the `telnet` or `nc` utilities to connect to TCP services.)

**Hint:** This might be trickier for many, compared to the previous challenges. When you connect to the TCP service using `telnet` or `nc`, you are presented with a math problem that you probably won't be able to do in your head. However, if you take too long, it will either reject your answer or timeout. You're going to need to automate this process somehow. Try writing a program. The `socket` library for Python is a good start.

**Flag:** `qKdZJ24VdvOg0Ji0`
