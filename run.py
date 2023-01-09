import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('WeighingData')


def get_inweight():
    """
    Get inweight from user
    """
    while True:
        print("Please enter inweight for 5 vehicles, seperated by commas.")
       
        data_str = input("Enter value here: ")
   
        inweight = data_str.split(",")

        if validate_data(inweight):
            break

    return inweight


def get_outweight():
    """
    Get outweight from user
    """
    while True:
        print("Please enter outweight for 5 vehicles, seperated by commas.")
       
        data_str = input("Enter value here: ")
   
        outweight = data_str.split(",")

        if validate_data(outweight):
            break

    return outweight


def validate_data(values):
    """
    Check values are intergers and 5 values given
    """
    try:
        [int(value) for value in values]
        if len(values) != 5:
            raise ValueError("Please enter 5 values")
    except ValueError as e:
        print(f"Invalid data: {e}, try again.")
        return False

    return True


def update_inweight_worksheet(data):
    """
    Update inweight worksheet and add new row with csv data input
    """
    print("Updating inweight worksheet...")
    inweight_worksheet = SHEET.worksheet("inweight")
    inweight_worksheet.append_row(data)
    print("Inweight worksheet updated successfully")


def update_outweight_worksheet(data_two):
    """
    Update outweight worksheet and add new row with csv data input
    """
    print("Updating outweight worksheet...")
    outweight_worksheet = SHEET.worksheet("outweight")
    outweight_worksheet.append_row(data_two)
    print("Outweight worksheet updated successfully")
    

def calculate_netweight_row():
    """
    Calculate netweight by subtracting inweight from outweight.
    """
    outweight_data = SHEET.worksheet("outweight").get_all_values()
    outweight_row = outweight_data[-1]
    inweight_data = SHEET.worksheet("inweight").get_all_values()
    inweight_row = inweight_data[-1]
    print("Calculating netweight...")

    netweight_row = []
    for outweight, inweight in zip(outweight_row, inweight_row):
        netweight = int(outweight) - int(inweight)
        netweight_row.append(netweight)

    return netweight_row


def update_netweight_worksheet(data_three):
    """
    Update netweight worksheet and add new row with csv data input
    """
    print("Updating netweight worksheet...")
    netweight_worksheet = SHEET.worksheet("netweight")
    netweight_worksheet.append_row(data_three)
    print("Netweight worksheet updated successfully")


def main():
    data = get_inweight()
    inweight = [int(num) for num in data]
    update_inweight_worksheet(inweight)
    data_two = get_outweight()
    outweight = [int(num) for num in data_two]
    update_outweight_worksheet(outweight)
    data_three = calculate_netweight_row()
    netweight = [int(num) for num in data_three]
    update_netweight_worksheet(netweight)

    print(f"outweight: {outweight}")
    print(f"inweight: {inweight}")
    print(f"netweight: {data_three}")


print("Weighing Control System")
main()