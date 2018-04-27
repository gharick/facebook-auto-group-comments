from selenium import webdriver
from facebookbot import FacebookBot


def main():
    usr = raw_input('Username: ')
    pwd = raw_input('Password: ')

    # Initiate webdriver - PhantomJS
    print("Iniatiating PhantomJS")
    driver = webdriver.PhantomJS()

    myBot = FacebookBot(driver)
    myBot.login(str(usr), str(pwd))

    groups = myBot.collect_groups()

    post = """ Sample Post """ # change this to what you will post to each group
    myBot.post_to_groups(post, 500, groups)

if __name__ == '__main__':
    main()