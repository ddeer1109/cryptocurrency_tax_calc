import csv
import pathlib


europln_exchange_rates = {
    "14-08-2020": 4.4011,
    "17-08-2020": 4.3988,
    "18-08-2020": 4.3892,
    "04-09-2020": 4.4181,
    "21-11-2020": 4.4679,
    "22-11-2020": 4.4679
}


FILE_PATH = {"1": pathlib.Path("transactions_files/1.csv"),
             "2": pathlib.Path("transactions_files/2.csv"),
             "3": pathlib.Path("transactions_files/3.csv"),
             "4": pathlib.Path("transactions_files/4.csv"),
             "5": pathlib.Path("transactions_files/5.csv")}

DATE = "\ufeffData operacji"
DATE_INDEX = 0
TYPE = "Rodzaj"
TYPE_INDEX = 1
VALUE = "Wartość"
VALUE_INDEX = 2
CURRENCY = "Waluta"
CURRENCY_INDEX = 3
ACCOUNT = "Saldo całkowite po operacji"
ACCOUNT_INDEX = 4


def read_file(path):
    dictionaries_list = []
    with open(path, encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';', quotechar='"')
        for row in csv_reader:
            dictionaries_list.append(dict(row))

        return dictionaries_list


def get_listed_csv_data(file_path):
    return read_file(file_path)


def get_transactions_in_PLN(file_path):
    all_data = get_listed_csv_data(file_path)

    filtered_data = []

    for data in all_data:
        if 'transakc' in data[TYPE]:
            data[TYPE] = data[TYPE][:30]
            if data[CURRENCY] == "PLN":
                filtered_data.append(data)
            elif data[CURRENCY] == "EUR":
                date = data[DATE].split(" ")[0]
                rate = europln_exchange_rates[date]
                data[VALUE] = round(float(data[VALUE]) * rate)
                data[CURRENCY] = 'PLN'

                filtered_data.append(data)

    return filtered_data


def get_euro_transactions(file_path):
    all_data = get_listed_csv_data(file_path)

    filtered_data = []

    for data in all_data:
        if 'transakc' in data[TYPE]:
            if data[CURRENCY] == "EUR":
                filtered_data.append(data)

    return filtered_data


def print_transactions(transactions_list):
    if len(transactions_list) != 0:
        keys = list(transactions_list[0].keys())
        cols_lens = [len(transactions_list[0][DATE])+2,
                     len(transactions_list[0][TYPE])+2,
                     max([len(str(entry[VALUE])) for entry in transactions_list])+2,
                     len(keys[CURRENCY_INDEX]) + 2,
                     len(keys[ACCOUNT_INDEX]) + 2]
        header_str_list = []
        for key, length in zip(keys, cols_lens):
            header_str_list.append(key.center(length))

        print(" " + "|".join(header_str_list))

        for transaction in transactions_list:
            data = "|".join([str(value).center(length) for value, length in zip(transaction.values(), cols_lens)])
            print(data)

        print()
        print(get_balance_after_transactions(transactions_list))


def get_balance_after_transactions(list_of_transactions):
    transactions_values = [float(entry[VALUE]) for entry in list_of_transactions]
    return sum(transactions_values)


def get_income_from_transactions(transactions_in_pln):
    income = 0

    for transaction in transactions_in_pln:
        if float(transaction[VALUE]) > 0:
            income += float(transaction[VALUE])

    return income


def get_cost_of_transactions(transactions_in_pln):
    cost = 0

    for transaction in transactions_in_pln:
        if float(transaction[VALUE]) < 0:
            cost += float(transaction[VALUE])

    return cost


def get_2020():
    year2020 = [get_transactions_in_PLN(FILE_PATH['1']),
                get_transactions_in_PLN(FILE_PATH['2']),
                get_transactions_in_PLN(FILE_PATH['3']),
                get_transactions_in_PLN(FILE_PATH['4'])]

    income = sum([get_income_from_transactions(entry) for entry in year2020])
    cost = sum([get_cost_of_transactions(entry) for entry in year2020])

    balance2020 = sum(list(map(get_balance_after_transactions, year2020)))

    return year2020, balance2020, income, cost


def print_2020():
    tables, balance, income, cost = get_2020()

    for table in tables:
        print_transactions(table)

    print(f"Income: {income}")
    print(f"Cost: {cost}\n")
    print(f"Balance: {balance}")


print_2020()

