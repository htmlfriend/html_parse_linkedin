import os
import csv
from lxml import html, etree

# text that precedes the info we're after
PARSE_NAME = '"title":{"textDirection":"FIRST_STRONG","text":"'
PARSE_HEADLINE = '"primarySubtitle":{"textDirection":"USER_LOCALE","text":"'
PARSE_LOCATION = '"secondarySubtitle":{"textDirection":"USER_LOCALE","text":"'
# text that comes right after the info we're after
END_PARSE = ',"attributesV2":'


def main():
    employee_list = []  # will store employee data -> [(name, headline, location), ()]
    # file path to 'html_files' folder
    file_path = os.path.dirname(os.path.dirname(__file__)).replace("\\", "/") + '/html_files'
    # get list of our '.html' files
    file_list = os.listdir(file_path)

    for file in file_list:
        html_path = file_path + '/' + file

        # Load the HTML file and parse it
        with open(html_path, "r", encoding="utf-8") as file:
            htmldoc = html.fromstring(file.read())

        # Open a output.xml file and write the element/document to an encoded string representation of its XML tree.
        with open("output.xml", 'wb') as file:
            file.write(etree.tostring(htmldoc))

        # Read the 'xml' file of the 'html' webpage
        with open("output.xml", 'r') as file:
            x_file = file.read()

        while x_file.find(PARSE_NAME) != -1:  # '-1' when no match
            find_name = x_file.find(PARSE_NAME)  # returns index position of 'PARSE_NAME'
            # redefine so that it excludes this loop's instance of the 'PARSE_NAME' text
            x_file = x_file[find_name+48:]
            name = x_file[:x_file.find(END_PARSE)-1]

            find_headline = x_file.find(PARSE_HEADLINE)
            if find_headline != -1:
                x_file = x_file[find_headline+57:]
                headline = x_file[:x_file.find(END_PARSE)-1]
                headline = headline.replace("amp;", "")  # remove unnecessary text

            find_location = x_file.find(PARSE_LOCATION)
            if find_location != -1:
                x_file = x_file[find_location+59:]
                location = x_file[:x_file.find(END_PARSE)-1]

            employee_list.append((name, headline, location))

    # write 'employee_list' to a 'csv' file
    with open("employee_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        for i in range(len(employee_list)):
            try:
                writer.writerow(employee_list[i])
            except UnicodeEncodeError:
                # try to remove the text that had the error and re-try to write to CSV
                try:
                    for x_i in range(len(employee_list[i])):
                        employee_list[i][x_i] = employee_list[i][x_i].encode("utf-8").decode("ascii", "ignore")
                    writer.writerow(employee_list[i])
                except Exception as x_exception:
                    print(f"ERROR adding row to CSV: {x_exception}")
                    pass


if __name__ == "__main__":
    main()
