INSERT INTO treasure_ctf.flags (id, title, clue, hints, flag, points_remaining) VALUES (1, 'Audio', 'Welcome aboard agent! We have been tracking some criminals who have been committing crimes around Southern California. We need more cybersecurity agents like you to help gain intel. Join the `Audio Flag` voice channel to hear a secret message, which is your first flag. (To submit it as a flag, type it as `\\flag{<message>}`, replacing `<message>` with the secret message.)

If you are hearing impaired, please DM josephDaCoder to get a transcription.', '[".... .- -.-. -.- -- ."]', 'hackme', 20);
INSERT INTO treasure_ctf.flags (id, title, clue, hints, flag, points_remaining) VALUES (2, 'Plain sight', 'We''ve gained some intel on the criminals. They operate a coffee shop in Dana Point, CA. Their website looks pretty normal, which seems suspicious. Take a good look around to see if you can find anything unusual. Go to https://a.ctf.treasurehacks.dev/index.html.', '["Selecting text can reveal things you might not normally see. You could also try using the source code."]', 'pdmRgS4ScTeWRhrp', 20);
INSERT INTO treasure_ctf.flags (id, title, clue, hints, flag, points_remaining) VALUES (3, 'Zipped', 'We also noticed on the menu page that one of the product photos has an abnormality. There might be a flag which will help us gain more info. Go to https://a.ctf.treasurehacks.dev/menu.html.', '["Look at the image file sizes. Notice that one of them is abnormally larger. Did you know that you can hide `.zip`s in many normal files, like JPEG images? Also, remember that flags start with `\\flag`."]', 'LOZqJxitPnkw5tyi', 20);
INSERT INTO treasure_ctf.flags (id, title, clue, hints, flag, points_remaining) VALUES (4, 'Admin Cookie', 'We''ve intercepted the logins for their secure internal panel. The username is `steve`, password is `P@$$word`. (Talk about "secure"!) Unfortunately, they don''t have admin privileges, so all we can find is that their secret Double Chocolate Chip Cookie recipie. Maybe you should login and take a look around.

Access the admin panel at https://b.ctf.treasurehacks.dev/', '["There might be something stored in the cookies. Use your browser''s developer tools or an extension (try Cookie-Editor on Chrome) to view your cookies."]', 'ok8mWDVCS36Caipa', 20);
INSERT INTO treasure_ctf.flags (id, title, clue, hints, flag, points_remaining) VALUES (5, 'URL parameters', 'We obtained this email from what appears to be the internal criminals'' internal message board system. We imagine that they have used it in the past to coordinate their plots. Examine it and see what you can find.

```
Date: October 13, 2021
From: noreply@danaptcoffee.com
To: steve@danaptcoffee.com
Subject: New memo available

A new memo is available for your viewing. Please access it at https://b.ctf.treasurehacks.dev/memo/3
```', '["Take a look at the ID in the URL. What would happen if you changed it from `3` to something lower?"]', 'XXUWpamNQqxYk98D', 20);
INSERT INTO treasure_ctf.flags (id, title, clue, hints, flag, points_remaining) VALUES (6, 'Mainframe', 'We ran a port scan on their admin panel server (b.ctf.treasurehacks.dev) and discovered a TCP service running on port 9648. Try connecting to it to see what you find. (You can use the `telnet` or `nc` utilities to connect to TCP services.)', '["This might be trickier for many, compared to the previous challenges. When you connect to the TCP service using `telnet` or `nc`, you are presented with a math problem that you probably won''t be able to do in your head. However, if you take too long, it will either reject your answer or timeout. You''re going to need to automate this process somehow. Try writing a program. The `socket` library for Python is a good start."]', 'qKdZJ24VdvOg0Ji0', 20);
