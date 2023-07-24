### PURPOSE

- Parse html data from LinkedIn's employee search results
- LinkedIn is tough to scrape so this is a quick ad-hoc solution to get high-level employee data (Name, Headline, Location) for a company

### STEPS

- Go to LinkedIn and search for people
- In your web browser, download the html file for each pages search results and save in the `html_files` folder
- Run the `parse_html.py` file, which will create a CSV file with rows for each person and columns for their name, headline, and location
