
LINK: https://github.com/jyrikangas/csbproject1
Flaws from the 2021 OWASP Top 10

Application description: A simple website where users can register, log in, and post notes. Notes can be set to be private, and private notes can only be viewed from the users personal account page, which only they can access, if they are logged in. In addition to django, the application uses dotenv, which can be installed with `pip install python-dotenv`



FLAW 1: AO7 Identification and Authentication failures
exact source link pinpointing flaw 1: https://github.com/jyrikangas/csbproject1/blob/548fea93df1ba4337da3857b3891824f8ca542eb/notes/views.py#L30
description of flaw 1:
The website does not include sufficient measures to confirm the users identity. Users are allowed to choose a weak password, which opens them and the website up to a credential stuffing attack. This is an example of CWE-521, weak password requirements.
how to fix it:
This could be fixed by checking the strength of the users password during user creation, and only allowing passwords that are sufficiently strong. Here is an example function in the code: https://github.com/jyrikangas/csbproject1/blob/548fea93df1ba4337da3857b3891824f8ca542eb/notes/views.py#L42 . The function checks that the password provided by the user is at least 8 characters long and includes an uppercase letter, a lowercase letter, a number and a special character. This will make it much more difficult to guess passwords.

FLAW 2: AO3 Injection
exact source link pinpointing flaw 2:
https://github.com/jyrikangas/csbproject1/blob/7eb3ab01ef4aa28c5b7554d8688192afabcd758c/notes/views.py#L67
description of flaw 2:
The application does not sufficiently prevent user inputted data from tampering with the application. For example, it is possible to include javascript code in a note. When the page is loaded, the web browser will execute the code. (Try for example <script> alert(" a s d f "); </script>). This could be used maliciously by an attacker to for example break the website. By inputting a note with the script <script> while(True) </script> the website will be stuck executing the javascript code and thus it will be unusable.
how to fix it:
To prevent this we use the Djangos escape() function to escape any code in the note, before storing them in the database. (Line 73)

FLAW 3: AO5 Security Misconfiguration
exact source link pinpointing flaw 3: https://github.com/jyrikangas/csbproject1/blob/548fea93df1ba4337da3857b3891824f8ca542eb/csbproject2/settings.py#L18
description of flaw 3:
The cryptographic key used to hash passwords in this application is available in the settings.py file, which is uploaded to github. An attacker can find this key, and use it to break the encryption of the passwords. This is an example of CWE-260, password in configuration file.
how to fix it:
We can fix this problem by using a .env file. The .env file is used to insert the sensitive keys into the correct place while not uploading them to the version control system. (In this case though the .env file is uploaded to version control for demonstration purposes.)

FLAW 4: AO1 Broken Access Control
exact source link pinpointing flaw 4: https://github.com/jyrikangas/csbproject1/blob/548fea93df1ba4337da3857b3891824f8ca542eb/notes/views.py#L86
description of flaw 4:
Users personal pages are located on the path /accounts/{username}. Because the app does not follow the principle of deny by default, attackers can use URL manipulation to access other users private account pages. They can also view notes which the user has set as private. This is an example of CWE-284, improper access control. 
how to fix it:
Before allowing the user access to the account page, the application should check that the user has the required authorization to view the content. In this case we use the @login_required tag to restrict access to logged in users, and make sure that the user accessing the page is the owner by checking the request_user against the page owner in the handler. 


FLAW 5: AO4 Insecure design
exact source link pinpointing flaw 5: https://github.com/jyrikangas/csbproject1/blob/548fea93df1ba4337da3857b3891824f8ca542eb/notes/views.py#L86
description of flaw 5:
This application includes an example of CWE-73, external control of path. Because the path of the user page is the username chosen by the user, an attacker may use a username to manipulate the application in unintended ways. For example a user may choose make their username delete/username. Because the website has an account deletion handler (conviniently not using GET instead of POST) located at /accounts/delete/{username}, this will cause the account with the name 'username' to be deleted when the attacker visits their own account page.
how to fix it:
To avoid this issue, the path should be determined by the application and its programmers, not by the user. In this example we will simply use the user id number instead. This is not a great solution, since it still reveals information about the inner functioning of the application that could be used by an attacker. But since it fixes the issue of giving the user direct control of the path, I consider it good enough for this example. Other ways of fixing this could be by restricting the usernames in such a way that they could not manipulate the path, or using a separate url identifier randomly generated by the application. Relevant links for this fix: 
Handler: https://github.com/jyrikangas/csbproject1/blob/548fea93df1ba4337da3857b3891824f8ca542eb/notes/views.py#L96
urls.py: https://github.com/jyrikangas/csbproject1/blob/548fea93df1ba4337da3857b3891824f8ca542eb/csbproject2/urls.py#L28
index.html: https://github.com/jyrikangas/csbproject1/blob/548fea93df1ba4337da3857b3891824f8ca542eb/notes/templates/index.html#L14

