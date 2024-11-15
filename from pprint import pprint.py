from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
pprint(contacts_list)

for contact in contacts_list:
    name_parts = contact[0].split()
    
    if len(name_parts) == 3:
        contact[0], contact[1], contact[2] = name_parts[0], name_parts[1], name_parts[2]
    elif len(name_parts) == 2:  
        contact[0], contact[1], contact[2] = name_parts[0], name_parts[1], ''
    elif len(name_parts) == 1:
        contact[0], contact[1], contact[2] = name_parts[0], '', ''
phone_pattern = re.compile(r'(\+7|7|8)?(\(?\d{3}\)?)(\d{3})(\d{2})(\d{2})(\s?доб.(\d+))?')

for contact in contacts_list:
    phone = contact[5]
    match = phone_pattern.match(phone)
    if match:
        formatted_phone = f"+7{match.group(2).replace('(','').replace(')','')}({match.group(3)}){match.group(4)}-{match.group(5)}"
        
        if match.group(6):
            formatted_phone += f" {match.group(6)}"
        
        contact[5] = formatted_phone
    else:
        contact[5] = phone

unique_contacts = {}

for contact in contacts_list:
    full_name = f"{contact[0]} {contact[1]} {contact[2]}"

    if full_name not in unique_contacts:
        unique_contacts[full_name] = contact
    else:
        existing_contact = unique_contacts[full_name]
        if existing_contact[5] != contact[5]:
            existing_contact[5] = existing_contact[5] if existing_contact[5] else contact[5]
        if existing_contact[6] != contact[6]:
            existing_contact[6] = existing_contact[6] if existing_contact[6] else contact[6]


with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(unique_contacts)