from this import d
from requests_html import HTMLSession
import pandas as pd


# Creating a session object that will allow us to send requests to the website.
session = HTMLSession()
# Extracting the title, description and date of the news article.
def web_scraping():
    """
    This function is used to scrape the data from the website and store it in a list
    :return: A list of dictionaries.
    """

    # Sending a GET request to the website and storing the response in `r`.
    r = session.get("https://www.kdnuggets.com/tag/machine-learning")

    # Rendering the page and scrolling down the page to load all the data.
    r.html.render(sleep=1, scrolldown=1)

    # Finding all the `ul` tags in the page.
    blogs = r.html.find("ul")

    # Creating an empty list and storing the data in it.
    data = list()

    for i in blogs:
        for j in r.html.find("li"):
            try:
                blog_title = j.find("a", first=True)
                blog_desc = j.find("div", first=True)
                blog_date = j.find("font", first=True)
                blog_tag = j.find("p", first=True)
                blog_link = blog_title.absolute_links

                blog_data = {
                    "title": blog_title.text.strip(),
                    "description": blog_desc.text.strip(),
                    "topic": blog_tag.text.strip().split(",")[0],
                    "date": blog_date.text.lstrip("-").rstrip("."),
                    "link": list(blog_link)[0],
                }
                data.append(blog_data)
            except:
                pass
    return data


dataset = list()
dataset = web_scraping()

# Creating a dataframe from the list of dictionaries and saving it as a csv file.
df = pd.DataFrame(dataset)

df.to_csv("KDnuggets_data_v1.csv", index=False)
