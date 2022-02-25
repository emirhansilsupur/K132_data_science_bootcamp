from requests_html import HTMLSession
import pandas as pd


# Creating a session object that will allow us to send requests to the website.
session = HTMLSession()
# Extracting the title, description and date of the news article.
def scraping(topic):
    """
    The function is scraping the website and extracting the data.

    :param topic: The topic of the blog
    :return: A list of dictionaries. Each dictionary contains the title, description, date, topic and
    link of the news article.
    """

    # Sending a GET request to the website and storing the response in `r`.
    r = session.get(f"https://www.kdnuggets.com/tag/{topic}")

    # Rendering the page and scrolling down the page to load all the data.
    r.html.render(sleep=1, scrolldown=5)

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


topics = [
    "artificial-intelligence",
    "career-advice",
    "computer-vision",
    "data-science",
    "machine-learning",
    "natural-language-processing",
]

dataset = list()

# This is a for loop that is iterating through the list of topics and calling the function
# topic_name() for each topic.
for i in topics:
    dataset += scraping(i)

# Creating a dataframe from the list of dictionaries and saving it as a csv file.
df = pd.DataFrame(dataset)
df.drop_duplicates(subset="title", inplace=True)
df.to_csv("KDnuggets_data.csv", index=False)
