import requests
import webbrowser


def query(title):
    try:
        parameters = {'action': 'query', 'prop': 'extracts', 'titles': title, 'exintro': 'true', 'exsentences': '2',
                      'explaintext': 'true', 'redirects': 'true', 'formatversion': '2'}
        response = requests.get("https://en.wikipedia.org/w/api.php", params=parameters)

        # Separates definition from the rest of the response
        intro = response.content.decode("utf-8").split('</span> <span class="s2">')[1].split(
            '</span>')[0]

        # For readability
        intro = intro.replace('&quot;', '"').replace('&#39;', "'").replace('\\n', '')

        # Splits definition in to two lines
        words = intro.split()
        mid = len(words) // 2
        intro = '\n' + ' '.join(words[0:mid]) + '\n' + ' '.join(words[mid:]) + '\n'

        return intro

    except IndexError:
        return "IndexError"


def show_image(title):
    try:
        parameters = {'action': 'query', 'prop': 'pageimages', 'format': 'json', 'piprop': 'original', 'titles': title}
        response = requests.get("http://en.wikipedia.org/w/api.php")

        # Separates url from the rest of the response
        pic = response.content.decode("utf-8").split('"source":"')[1].split('"')[0]
        webbrowser.open(pic)

    except IndexError:
        print("No main image available for this article")


if __name__ == '__main__':
    while (True):
        search = input("What would you like wikipedia to define?\n").replace(" ", "%20")
        result = query(search)
        if ('may refer to:' in result):
            print("Multiple articles: Please be more specific\n")
        elif (result == 'IndexError'):
            print("Page not found. Please try again\n")
        else:
            print(result)
            break

    if input("Would you like to view an image in your browser?\n") in 'yes':
        show_image(search)
