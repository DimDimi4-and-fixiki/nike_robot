from nike_bot import NikeBot

SPECIAL_LINK = "https://www.nike.com/ru/launch/t/dunk-low-ceramic?size=9.5&productId=4ccdea17-4ce4-5211-ab32-d2e93590209c"

NUMBER_OF_ACCOUNTS = 1
START_NUMBER = 17
SUBMIT_TIME = "13:59:57.99"


def read_txt(path):
    file = open(path, "r")
    data = str(file.read())
    accounts = data.split("\n")
    return accounts


accounts = read_txt("accounts.txt")  # file with accounts
for i in range(START_NUMBER, START_NUMBER + NUMBER_OF_ACCOUNTS):  # runs several bots
    cur_account = accounts[i]  # takes current account
    login = str(cur_account.split(":")[0])  # gets login
    password = str(cur_account.split(":")[1])  # gets password
    address = str(cur_account.split(":")[-2])  # gets address
    last_name = str(cur_account.split(":")[-1])  # gets last name
    bot = NikeBot(login=login,
                  password=password,
                  main_page="https://www.nike.com/ru/launch",
                  special_link=SPECIAL_LINK,
                  address=address,
                  submit_time=SUBMIT_TIME,
                  last_name=last_name)
