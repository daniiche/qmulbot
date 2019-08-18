import telebot
from telebot import types
import sqlite3
from twitterscraper import query_tweets
from datetime import timedelta, datetime
import datetime as dt
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
import joblib
import time


bot = telebot.TeleBot('798457983:AAEPhKpIIBDz8ulAUcxltiZ0Jd5cQbqUdkA')

category_name =  {'1':'Events','2':'Career','3':'Sport','4':'Science','5':'Politics','6':'Education','7':'Culture','8':'Freebies'}
bot_condition = {'1': 'New user', '2': 'News as post', '3': 'Evening QMUL', '4': 'Feedback'}

# command start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    
    database = sqlite3.connect('bot_db.sqlite')
    db = database.cursor()

    db.execute("SELECT user_id FROM users WHERE user_id = ?", (message.chat.id,))
    check_user = db.fetchall()

    if not check_user:
        db.execute("INSERT INTO users (user_id, reg_date, bot_cond, user_name, first_name, last_name) VALUES "
                   "(?, datetime('now', 'localtime'), 1, ?, ?, ?)",
                   (message.chat.id, message.chat.username, message.chat.first_name, message.chat.last_name,))
        database.commit()

        bot.send_message(
            message.chat.id,
            "Hi, I'm a bot! \n"
                 "I'll help you to monitor news about your University! \n"
                 "I can send you news from QMUL Twitter. \n"
                 "I also have an evening newsletter of popular news. \n\n\n"
                 "Please choose the type of the subscription. \n"
                 "Evening QMUL is an evening newsletter with 5 most popular news. It is sent everyday at 9 p.m.\n"
                 "Or I can send you news as they post.\n",
            reply_markup=start_keyboard())
    else:
        bot.send_message(message.chat.id, 'Welcome to the main menu!', reply_markup=menu_keyboard()) 

# command stop
@bot.message_handler(commands=['stop'])
def send_goodbye(message):

    database = sqlite3.connect('bot_db.sqlite')
    db = database.cursor()

    db.execute("SELECT user_id FROM users WHERE user_id = ?", (message.chat.id,))
    check_user = db.fetchall()

    if check_user:
        db.execute("DELETE * FROM users, Usersgroups WHERE uid = ?", (message.chat.id,))
        database.commit()

        bot.send_message(
            message.chat.id, 
            "Very sorry that you decided to unsubscribe from all QMUL news. \U0001F614\n"
            "If you want to join QMUL_bot again, press /start \U0001F609")

# command help
@bot.message_handler(commands=['help'])  
def send_help(message):   
    bot.send_message(  
        message.chat.id,  
        '1) To receive a list of available currencies press /exchange.\n' +  
        '2) Click on the currency you are interested in.\n' +  
        '3) You will receive a message containing information regarding the source and the target currencies, ' +  
        'buying rates and selling rates.\n' +  
        '4) Click “Update” to receive the current information regarding the request. ' +  
        'The bot will also show the difference between the previous and the current exchange rates.\n' +  
        '5) The bot supports inline. Type @<botusername> in any chat and the first letters of a currency.',  
        reply_markup=menu_keyboard()  
    )

@bot.message_handler(content_types=["text"])
def main_menu(message):
    database = sqlite3.connect('bot_db.sqlite')
    database.row_factory = lambda cursor, row: row[0]
    db = database.cursor()
#1 screen with subscription types
    if message.text == 'Evening QMUL':
        db.execute("UPDATE users SET bot_cond = 3 WHERE user_id = ?", (message.chat.id,))
        database.commit()
        text = 'You are subscribed to Evening QMUL. \n Please choose categories you are interested in: '
        bot.send_message(message.chat.id, text,reply_markup=cat_keyboard())

    if message.text == 'News as they post':
        db.execute("UPDATE users SET bot_cond = 2 WHERE user_id = ?", (message.chat.id,))
        database.commit()
        text = 'You are subscribed to QMUL news as they post. \n Please choose categories you are interested in: '
        bot.send_message(message.chat.id, text,reply_markup=cat_keyboard())

#2 screen with categories
    if message.text == 'Events':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==1", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 1)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Events to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Events', False)

    if message.text == 'Career':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==2", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 2)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Career to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Career', False)

    if message.text == 'Sport':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==3", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 3)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Sport to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Sport', False)

    if message.text == 'Science':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==4", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 4)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Science to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Science', False)

    if message.text == 'Politics':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==5", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 5)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Politics to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Politics', False)
    
    if message.text == 'Education':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==6", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 6)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Education to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Education', False)

    if message.text == 'Culture':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==7", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 7)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Culture to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Culture', False)

    if message.text == 'Freebies':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==8", (message.chat.id,))
        check_user = db.fetchall()
        if not check_user:
            db.execute("INSERT INTO Usersgroups (uid, gid) VALUES "
                   "(?, 8)",
                   (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You added Freebies to your categories', False)
        else:
        	bot.send_message(message.chat.id, 'You already subscribed to Freebies', False)
       

    if message.text == 'Back to main menu':
        bot.send_message(message.chat.id, 'Welcome to the main menu!', reply_markup=menu_keyboard())

#4 screen with main menu    
    if message.text == 'About the project':
        bot.send_message(message.chat.id, 'QMUL_bot is the final project of QMUL EECS MSc student Polina Zhuchkova.\n'
                                      'It is the first news bot of Queen Mary University of London!\n'
                                      'Plagiarism and copying are prosecuted.', reply_markup=menu_keyboard())

    if message.text == 'Leave feedback':
        database = sqlite3.connect('bot_db.sqlite')
        db = database.cursor()

        db.execute("UPDATE users SET bot_cond = 4 WHERE user_id = ?", (message.chat.id,))
        database.commit()
        bot.send_message(message.chat.id, 'Type and send feedback like in a regular chat', reply_markup=done_keyboard())

        db.execute("INSERT INTO Reviews (uid, rev_text, rev_date) VALUES (?, ?, datetime('now', 'localtime'))",
                           (message.chat.id, message.text))
        db.execute("UPDATE Users SET bot_cond = 0 WHERE id = ?", (message.chat.id,))
        database.commit()
        markup = press_done(message)
        send_message(message.chat.id, 'Thanks for your feedback! \U0001F64F', markup)
        

#7 screen to manage subscriptions
    if message.text == 'Manage subscriptions':
        bot.send_message(message.chat.id, 'Please, choose what you want to do', reply_markup=manage_keyboard())   

    if message.text == 'My categories':
        db.execute("SELECT gid FROM Usersgroups WHERE uid = ?", (message.chat.id,))
        categories_id = db.fetchall()
        categories = []

        if categories_id:
            for category in categories_id:
                categories.append(category_name.get(category))

            bot.send_message(message.chat.id, 'You are subscribed to : '+str(categories), reply_markup=manage_keyboard())
        else:
            bot.send_message(message.chat.id, 'You are not subscribed to any category', reply_markup=manage_keyboard())

    if message.text == 'Change subscription type':
        db.execute("SELECT bot_cond FROM users WHERE user_id = ?", (message.chat.id,))
        subtype = db.fetchall()[0]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        if subtype==3:
        	markup.add(types.KeyboardButton('Change to News as post'))
        if subtype==2:
        	markup.add(types.KeyboardButton('Change to Evening QMUL'))
        markup.add(types.KeyboardButton('Back to main menu'))

        bot.send_message(message.chat.id, 'Your type of subscription '+bot_condition.get(str(subtype)), reply_markup=markup)

    if message.text == 'Change to News as post':

        db.execute("UPDATE users SET bot_cond = 2 WHERE user_id = ?", (message.chat.id,))
        database.commit()

        bot.send_message(message.chat.id, 'Your type of subscription changed to News as post', reply_markup=menu_keyboard())

    if message.text == 'Change to Evening QMUL':

        db.execute("UPDATE users SET bot_cond = 3 WHERE user_id = ?", (message.chat.id,))
        database.commit()

        bot.send_message(message.chat.id, 'Your type of subscription changed to Evening QMUL', reply_markup=menu_keyboard())

    if message.text == 'Change categories':
        db.execute("SELECT gid FROM Usersgroups WHERE uid = ?", (message.chat.id,))
        categories_id = db.fetchall()
        categories = []

        if categories_id:
            for category in categories_id:
                categories.append(category_name.get(category))
            bot.send_message(message.chat.id, 'You are already subscribed to : \n'+str(categories), None)
        else:
        	bot.send_message(message.chat.id, 'You are not subscribed to any category', None)


        bot.send_message(message.chat.id, 'Choose what you want to do: ', reply_markup=mancat_keyboard())


    # 11 screen choose categories to subscribe 
    if message.text == 'Choose categories to subscribe':
        db.execute("SELECT gid FROM Usersgroups WHERE uid = ?", (message.chat.id,))
        categories_id = db.fetchall()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        check_if_all = 0
        for category in category_name:
            if category not in categories_id:
                markup.add(types.KeyboardButton(category_name.get(str(category[0]))))
                check_if_all += 1

        markup.add(types.KeyboardButton('Back to main menu'))
        
        if check_if_all > 0:
            bot.send_message(message.chat.id, 'Please, select topics to add to your subscription.\n', reply_markup=markup)
            bot.send_message(message.chat.id, 'You are not subscribed to:', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'You are subscribed to all categories', False) 

    # 11 screen choose categories to unsubscribe 
    if message.text == 'Unsubscribe from category':
        db.execute("SELECT gid FROM Usersgroups WHERE uid = ?", (message.chat.id,))
        categories_id = db.fetchall()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        check_if_all = 0
        for category in category_name:
            if category in categories_id:
                markup.add(types.KeyboardButton("No more "+category_name.get(str(category[0]))))
                check_if_all += 1
        
        markup.add(types.KeyboardButton('Back to main menu'))

        if check_if_all > 0:
            bot.send_message(message.chat.id, 'Choose topics to unsubscribe: ', reply_markup=markup)

        else:
            bot.send_message(message.chat.id, 'You have no subscriptions yet', reply_markup=markup)

    #2 categories
    if message.text == 'No more Events':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==1", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==1", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Events category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Events', False)

    if message.text == 'No more Career':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==2", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==2", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Career category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Career', False)

    if message.text == 'No more Sport':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==3", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==3", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Sport category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Sport', False)

    if message.text == 'No more Science':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==4", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==4", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Science category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Science', False)

    if message.text == 'No more Politics':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==5", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==5", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Politics category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Politics', False)
    
    if message.text == 'No more Education':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==6", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==6", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Education category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Education', False)

    if message.text == 'No more Culture':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==7", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==7", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Culture category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Culture', False)

    if message.text == 'No more Freebies':
        db.execute("SELECT uid FROM Usersgroups WHERE uid = ? AND gid ==8", (message.chat.id,))
        check_user = db.fetchall()
        if check_user:
            db.execute("DELETE FROM Usersgroups WHERE uid = ? AND gid ==8", (message.chat.id,))
            database.commit()
            bot.send_message(message.chat.id, 'You have unsubscribed from Freebies category', False)
        else:
        	bot.send_message(message.chat.id, 'You already unsubscribed from Freebies', False)
       

    database.close()   

def categories_list():
    database = sqlite3.connect('bot_db.sqlite')
    db = database.cursor()

    db.execute("SELECT * FROM Groups")
    categories = db.fetchall()

    database.close()
    return categories

# back to mm
def done_keyboard ():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    back_btn = types.KeyboardButton('Back to main menu')
    markup.add(done_btn)
    return markup 

# main menu keyboard
def menu_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton('About the project'))
    markup.add(types.KeyboardButton('Leave feedback'))
    markup.add(types.KeyboardButton('Manage subscriptions'))
    return markup  

# welcome scr keyboard
def start_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    evnews_btn = types.KeyboardButton('Evening QMUL')
    dnews_btn = types.KeyboardButton('News as they post')
    markup.add(evnews_btn)
    markup.add(dnews_btn)
    return markup  

# buttons as categories 
def cat_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for i in categories_list():
        markup.add(types.KeyboardButton(i[0]))
    markup.add(types.KeyboardButton('Back to main menu'))
    '''ev_btn = types.KeyboardButton('Events')
    car_btn = types.KeyboardButton('Career')
    sp_btn = types.KeyboardButton('Sport')
    sc_btn = types.KeyboardButton('Science')
    pol_btn = types.KeyboardButton('Politics')
    ed_btn = types.KeyboardButton('Education')
    cul_btn = types.KeyboardButton('Culture')
    fr_btn = types.KeyboardButton('Freebies')
    markup.add(ev_btn, car_btn, sp_btn, sc_btn, pol_btn, ed_btn, cul_btn, fr_btn)'''

    return markup

# manage categories keyboard
def mancat_keyboard():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton('Unsubscribe from category'))
    markup.add(types.KeyboardButton('Choose categories to subscribe'))
    markup.add(types.KeyboardButton('Back to main menu'))

    return markup 

# manage keyboard
def manage_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('My categories'))
    markup.add(types.KeyboardButton('Change subscription type'))
    markup.add(types.KeyboardButton('Change categories'))
    markup.add(types.KeyboardButton('Back to main menu'))
    return markup

def categories_list():
    database = sqlite3.connect('bot_db.sqlite')
    db = database.cursor()

    db.execute("SELECT name FROM Categories")
    categories = db.fetchall()

    database.close()
    return categories

# get tweets from twitter 
def scrap_tweets():
    
    date_N_days_ago = datetime.now() - timedelta(days=1)
    y = int(date_N_days_ago.strftime("%Y"))
    m = int(date_N_days_ago.strftime("%m"))
    d = int(date_N_days_ago.strftime("%d"))

    # Import of classification model
    filename1 = 'model.sav'
    filename2 = 'tfidf.sav'
    model = joblib.load(filename1)
    tfidf = joblib.load(filename2)

    # Connection with database 
    database = sqlite3.connect('bot_db.sqlite')
    database.row_factory = lambda cursor, row: row[0]
    db = database.cursor()

    # Tweets from chosen 8 QMUL accounts will be returned
    for tweet in query_tweets("from%3AQMUL%20OR%20from%3AQMSU%20OR%20from%3Aqmcareers%20OR%20from%3AQMLibrary%20OR%20from%3AQMSU_Events%20OR%20from%3AEngageQM%20OR%20from%3AQMULSciEng%20OR%20from%3AQMSUsocieties", begindate=dt.date(y, m, d)):
        (category_name.get(str(model.predict(tfidf.transform([tweet.text])))))
        if tweet.tweet_id not in db.execute('SELECT id FROM Posts').fetchall():
            category = int((model.predict(tfidf.transform([tweet.text]))[0]))
            text = tweet.text.replace('http', ' http')
            text = text.replace('pic.', ' pic.')
            db.execute("INSERT INTO Posts (id, gid, p_date, p_text, p_likes, p_reposts, class_group, date_month) VALUES "
                   "(?, ?, ?, ?, ?, ?, ?, ?)",
                   (tweet.tweet_id, tweet.user_id, tweet.timestamp, text, tweet.likes, tweet.retweets,
                    category, datetime.now().strftime("%d")))
            send_as_scrap(text, category)
    database.commit()
    database.close()

# send tweets to users
def send_as_scrap(text, category):

	database = sqlite3.connect('bot_db.sqlite')
	database.row_factory = lambda cursor, row: row[0]
	db = database.cursor()

	db.execute("SELECT uid FROM Usersgroups WHERE gid == ?", (category,))
	for user in db.fetchall():
		print(user)
		bot.send_message(user, "Message from category: "+category_name.get(str(category))+"\n\n"+text, False)

def evening_qmul():

	database = sqlite3.connect('bot_db.sqlite')
	database.row_factory = lambda cursor, row: row[0]
	db = database.cursor()
	today = datetime.now().strftime("%d")

	today_posts = []

	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 1 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 1)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 2 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 2)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 3 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 3)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 4 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 4)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 5 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 5)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 6 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 6)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 7 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 7)",
	 (today, today,))
	today_posts.append(db.fetchall())
	db.execute("SELECT id FROM posts WHERE date_month == ? AND class_group == 8 AND p_likes=(SELECT MAX(p_likes) FROM posts WHERE date_month == ? AND class_group == 8)",
	 (today, today,))
	today_posts.append(db.fetchall())
	
	db.execute("SELECT user_id FROM users WHERE bot_cond == 3")

	for user in db.fetchall():
		db.execute("SELECT gid FROM Usersgroups WHERE uid == ?", (user,))

		for group in db.fetchall():
			if today_posts[int(group)-1]:
				db.execute("SELECT p_text FROM posts WHERE id == ?", (today_posts[int(group)-1][0],))
				ptext = db.fetchall()
				bot.send_message(user, "Evening QMUL for category: "+category_name.get(str(group))+"\n\n"+ptext[0], False)

			else:
				bot.send_message(user, "Sorry, no news today for category: "+category_name.get(str(group)), False)

def main():
	bot.remove_webhook()
	bot.polling(none_stop=True)

if __name__ == "__main__":

	main()






