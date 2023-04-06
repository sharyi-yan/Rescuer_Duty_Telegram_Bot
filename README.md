                                     The specification of Duty_Rescuer_Bot

 
 
 General Information:

1. Duty_Rescuer_Bot is a bot created to ensure that each group member always knows the date of his duty. No more confusion and disputes:

"I was on duty last time!!! Now it's your turn!"
"Don't lie!!! No, it's yours!"

These conflicts will be resolved automatically now,  the bot will take care of everything for you!



2. What this bot can do:

Calculate the dates of all your work days several years ahead
Create a database with people's names, add and delete new people on duty
Control the queue of “who is on duty”, and monitor the queue even if the person is on vacation or sick leave
Іdentify the date when a specific person is on duty



3. This bot is scalable! Separate tables are created in the database for each user, and the number of days off between shifts can be easily adjusted (suitable for different work schedules). It was created using the PyTelegramBotAPI library, the Flask web framework, the MySQL database, webhooks, and hosted on Heroku in combination with the ClearDB database service. The GitHub repository and free Dino hours were used for deployment on Heroku (where else would a rescuer get the money?)



4. What isn’t in the current version, but is planned for the next version:

A calendar with marked dates of duty
Rating of quantity and quality of duties, assignment of ranks (soap lieutenant, toilet plunger sergeant, shithouse general)





Interaction with the bot:

1. The user сlicks the "Start" and the brand image appears in front of them.
The message states that the user needs to send the response "begin" to start the program. Then, a table with duty dates is created in the database. The list of dates is created depending on the date the "begin" message was sent. For this reason, the message should be sent on the day of duty!!! If the user enters any other text, they will receive a message: "Follow the instructions above!!!" Such a message is sent in all cases when the user writes to the bot at the wrong time.
 
2. After sending “ start “ to our bot, the main menu with Telegram buttons (InLineButtons) appears on the screen. The menu includes the following buttons
"Add to duty list".
"Remove from duty list"
"Find out when you're on duty."
"On duty today."

Note: If a user is not using the bot for the first time, they do not need to enter "start". They simply continue from where they left off last time.

3. If the user is using the bot for the first time, the lists with the names of those on duty will be empty. If the user selects any button except "Add to the on-duty list", they will receive the message: "The on-duty list is still empty! Add people to the on-duty list!!!"

4. When the user clicks the "Add to the on-duty list" button, they receive the message: "Provide the name of the person you want to add to the on-duty list." After entering the name and sending the message, the bot sends another message: "Please enter the name of the person one more time." This is done so that the user does not accidentally add a misspelled name to the on-duty list.
If the names match, the user receives a message that the name they entered has been added to the database. If they do not match, a warning is sent: "Names do not match!!!" In both cases, buttons appear on the screen: "Main Menu" and "Enter the Name".
Clicking the "Main Menu" button displays the main menu on the screen. Clicking "Enter Name" repeats the process of adding to the database.

Note: Adding the same name to the list twice is not allowed!!! It is not possible to secretly joke about someone like "Johnny" being on duty twice as often as everyone else!!! For this reason, when adding a name, the bot checks if it is already in the database.

5. If someone has "bothered" you and you have decided to remove them from the list, use the "Remove from on-duty list" button. When you click this button, you receive the message: "Enter the name of the person you want to remove from the on-duty list." Send a message to the bot with the name, and it will check if the person with that name is in the database.
If a person with that name is found in the database, the user will be asked to confirm their deletion by pressing the "Confirm" button. After clicking "Confirm," the user receives the message: "The entered_name has been removed from the on-duty list!" Following this message, buttons for the main menu appear.
If the user realizes that they made a mistake and the person is actually useful, they can click the "Cancel" button. If the person with that name is not in the database, the message "The entered_name is not in the on-duty list! Try entering the name again!" is sent. In this case, two buttons appear: "Main Menu" and "Try Again."

6. The "Find out when you're on duty" button is used to find out when you're on duty! When clicked, the user receives the message: "Enter the name of the person to find out their duty date:" The user needs to send a message with the person's name, and the program will provide their duty date according to the queue. If the user's fingers are too thick to hit the right buttons, or if they're pretty (or extremely) drunk - "The entered_name is not in the duty list!" Try entering the name again by clicking the "Try Again" button.

7. Oh my god, that's the last button from the main menu!!! The most important button!!! The "On Duty Today" button. When you click this button, a message appears on the screen with the name of the person who is first in the queue to be on duty. If that person is at work, he is out of luck!!! Click the "Confirm" button and he will be assigned to be on duty today! After the confirmation of the duty person, that date can no longer be changed!!! Be attentive! If a person is sick, on vacation, breastfeeding, or just lazy - click the "No duty" button. The "No duty" button makes that person first in the queue for the next time, and the name of the second in the queue appears on the screen. The queue shifts until the person on duty is assigned (Confirm button!!!) Once the person on duty is assigned, their name is attached to that date. The data are entered in a separate table "Archive" in the database.

Note: You can only assign the duty person on the day of duty!!! On all other days, when you click the "On Duty Today" button, you will receive the message: "Wait for the next shift!!! You can only assign  another duty person  on the day of duty!!!"
