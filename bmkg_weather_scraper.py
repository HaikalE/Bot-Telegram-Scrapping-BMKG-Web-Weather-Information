import requests
from bs4 import BeautifulSoup

def scrape_weather_info(url):
    """
    Scrapes weather data from the BMKG website.

    Args:
    url (str): The URL of the webpage containing weather data.

    Returns:
    list: A list containing all the scraped weather data.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            tabs = soup.find('ul', class_='nav-tabs')
            dates = [tab.text.strip() for tab in tabs.find_all('a')]

            tables = soup.find_all('table')

            if tables:
                all_tables_data = []
                for date, table in zip(dates, tables):
                    table_data = []
                    table_data.append([date])
                    headers = []
                    th_row = table.find('tr')
                    for th in th_row.find_all('th'):
                        if th.has_attr('rowspan'):
                            rowspan = int(th['rowspan'])
                            if rowspan > 1:
                                for i in range(rowspan - 1):
                                    headers.append(th.text.strip())
                            headers.append(th.text.strip() + " : " + th_row.find_all('th')[1].text.strip())
                        else:
                            headers.append(th.text.strip())
                    table_data.append(headers)
                    for row in table.find_all('tr')[1:]:
                        row_data = [cell.text.strip() for cell in row.find_all(['th', 'td'])]
                        table_data.append(row_data)
                    all_tables_data.append(table_data)

                return all_tables_data
            else:
                print("No tables found on the webpage.")
                return []
        else:
            print("Failed to retrieve the webpage. Status code:", response.status_code)
            return []
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return []

if __name__ == "__main__":
    url = "https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg"
    weather_data = scrape_weather_info(url)
    print(weather_data)
