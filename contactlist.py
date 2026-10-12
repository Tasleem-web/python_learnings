from pathlib import Path
import time
import json

CONTACTS_FILE = Path(__file__).with_name("contactList.json")

contact_list = []


def contact_menu():
    name = input("Enter your name=")
    age = int(input("Enter your age="))
    phone = int(input("Enter your phone="))
    return name, age, phone


def create_contact(contact):
    contact_list.append(contact)
    write_mode_contact_file(contact_list)
    print("Contact saved successfully to JSON file!")


def write_mode_contact_file(contact_list, indent=2):
    if not CONTACTS_FILE.exists():
        return []

    with CONTACTS_FILE.open("w", encoding="utf-8") as file:
        json.dump(contact_list, file, indent=indent)


def read_mode_contact_file():
    if not CONTACTS_FILE.exists():
        return []

    with CONTACTS_FILE.open("r", encoding="utf-8") as file:
        try:
            contact_list = json.load(file)
            return contact_list
        except json.JSONDecodeError:
            return []


def display_contacts_table(contact_list_ext=[]):
    # 1. Load the contacts from your existing read function
    if len(contact_list_ext) > 0:
        contact_list = contact_list_ext
    else:
        contact_list = read_mode_contact_file()

    if not contact_list:
        print("\nNo contacts found to display.")
        return

    # 2. Define column widths for alignment (adjust numbers to change column sizes)
    # {:<20} means left-align with a width of 20 characters
    header_format = "{:<5} | {:<20} | {:<5} | {:<5} | {:<20}"
    row_format = "{:<5} | {:<20} | {:<5} | {:<5} | {:<20}"

    # 3. Print the table Header
    print("\n" + "=" * 65)
    print(header_format.format("S.No", "ID", "Name", "Age", "Phone"))
    print("=" * 65)

    # 4. Print each contact as a row in the table
    for index, contact in enumerate(contact_list, start=1):
        id = contact.get("id", "N/A")
        name = contact.get("name", "N/A")
        age = contact.get("age", "N/A")
        phone = contact.get("phone", "N/A")

        print(row_format.format(index, id, name, age, phone))

    print("=" * 65 + "\n")


def update_contact():
    search_query = input("Please enter the id you want to update it=").strip().lower()

    find_index = next(
        (i for i, item in enumerate(contact_list) if item.get("id") == search_query), -1
    )

    contact_id = contact_list[find_index]["id"]

    if find_index != -1:
        print("Please enter your updated fields below=")
        name, age, phone = contact_menu()

        contact_list[find_index]["name"] = name
        contact_list[find_index]["age"] = age
        contact_list[find_index]["phone"] = phone

        write_mode_contact_file(contact_list)
        print(f"Contact with ID {contact_id} updated successfully.")
    else:
        print(f"No contact found with ID {contact_id}.")


def delete_contact():
    contact_id = input("Enter the contact id you want to delete it=").strip().lower()

    find_index = next(
        (i for i, item in enumerate(contact_list) if item.get("id") == contact_id), -1
    )

    if find_index != -1:
        del contact_list[find_index]
        write_mode_contact_file(contact_list)
        print(f"Record has been deleted by provided {contact_id}")
    else:
        print("No contact found by provided ID")

    display_contacts_table()


def search_contact():
    id = input("Please enter the id you want to search it=")

    find_index = next(
        (i for i, item in enumerate(contact_list) if item.get("id") == id), -1
    )

    if find_index != -1:
        try:
            display_contacts_table([contact_list[find_index]])
        except Exception as e:
            print(f"An error occurred while displaying the contact: {e}")
    else:
        print(f"No contact found with this {id}")


def fetch_data(firstTime=False):
    global contact_list
    if not CONTACTS_FILE.exists():
        return []

    with CONTACTS_FILE.open("r", encoding="utf-8") as file:
        try:
            contact_list = json.load(file)
            print("Data successfully fetched from JSON!")
            if firstTime == True:
                main()
        except Exception as e:
            print(f"An error occurred while displaying the contact: {e}")


def main():

    while True:
        print("\nContact Book App")
        print("1. Create contact")
        print("2. Update contact")
        print("3. Delete contact")
        print("4. View contact")
        print("5. Search contact")
        print("6. Count contact")
        print("7. Delete all contacts")
        print("0. Exit")

        user_input = input("Enter your choice=")

        match user_input:
            case "1":
                contact = {}
                name, age, phone = contact_menu()
                id = hex(int(time.time() * 1000000))[2:]
                contact["id"] = id
                contact["name"] = name
                contact["age"] = age
                contact["phone"] = phone
                create_contact(contact)

            case "2":
                update_contact()

            case "3":
                delete_contact()

            case "4":
                display_contacts_table()

            case "5":
                search_contact()

            case "exit" | "0":
                print("Exiting from the Contact Book Application...")
                print("Exited.")
                break


if __name__ == "__main__":
    # main()
    fetch_data(True)
