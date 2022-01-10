import pandas
import json
Not_done = True
while Not_done:
    option = input("Do you want to add stock or email or exit program?(enter: stock or email or exit): ")
    if option.lower() == "stock":
        stock_name = input("Enter Stock name (eg.TSLA AAPL): ")
        company_name = input("Enter company name of that stock (eg. tesla, apple): ")
        confirm = input("Double check the data entered for spelling errors, are you sure you want to enter data?(enter: y or n): ")
        if confirm.lower() == 'y':
            with open("stocks.json", "r+") as file:
                try:
                    data = json.load(file)
                except json.decoder.JSONDecodeError:
                    data = {}
                stock = {stock_name: company_name}
                data.update(stock)
                file.seek(0)
                json.dump(data, file)
    elif option.lower() == "email":
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        confirm = input("Double check the data entered for spelling errors, are you sure you want to enter data?(enter: y or n): ")
        if confirm.lower() == "y":
            with open("email.json", "r+") as file:
                try:
                    data = json.load(file)
                except json.decoder.JSONDecodeError:
                    data = {}
                person = {name: email}
                data.update(person)
                file.seek(0)
                json.dump(data, file)
    else:
        Not_done = False
