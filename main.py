import requests, re, time
from bs4 import BeautifulSoup
import pandas as pd

def user_input():
    user_input = str(input('Enter Item to search: '))
    user_input = format_search(user_input)
    return user_input

def format_search(search):
    search = re.sub(r"\s+", '+', search)
    return(search)

def create_csv(products):
    '''
        future additions:
        - let user choose name of the file 
        - let user choose location of file
    '''
    df = pd.DataFrame(products)
    df.to_csv('results.csv', index=False)
    print('Done CSV')


def get_html(search):
    headers ={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={search}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1'
    '''
    url with pages to allow mulipage scraping for future update
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={search}&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1&_pgn={page_num}'
    '''
    r = requests.get(url,headers=headers)

    if r.status_code != 200:
        print('Error',r.status_code)
        new_search = user_input()
        get_html(new_search)
    else:
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup

def parse_data(soup):
    results = soup.find_all('div',{'class':'s-item__info clearfix'})
    products = []

    for listing in results:
        bid = listing.find('span',{'class':'s-item__bids s-item__bidCount'})
        
        if bid:
            bid = bid.text
        else:
            bid = 0

        product = {
            'tite':listing.find('h3',{'class':'s-item__title s-item__title--has-tags'}).text,
            'soldprice':float(listing.find('span',{'class':'s-item__price'}).text.replace('$','').replace(',','')),
            'bids':bid,
            'link':listing.find('a',{'class':'s-item__link'})['href'],
        }
        products.append(product)

    create_csv(products)

def main():
    search = user_input()
    soup = get_html(search)
    parse_data(soup)


if __name__ == '__main__':
    main()