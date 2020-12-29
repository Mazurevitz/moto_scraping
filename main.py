import requests
from bs4 import BeautifulSoup
import re
from csv import DictWriter
import time

def price_finder(car_offer):
    price_string = car_offer.find('span', class_='offer-price__number ds-price-number').findChild().text
    price = int(price_string.replace(' ', ''))
    return {'price': price}

def find_params(element):
    params = element.find('ul', class_="ds-params-block").find_all('li')
    year = params[0].findChild().text
    mileage = params[1].findChild().text
    engine_capacity = params[2].findChild().text
    fuel_type = params[3].findChild().text
    return {
        "year": int(year.strip()),
        "mileage": int(mileage.replace(' km', '').replace(' ','')),
        "engine_capacity": int(engine_capacity.replace(' cm3', '').replace(' ','')),
        "fuel_type": fuel_type
    }

def find_name(element):
    full_name = element.find('a', class_='offer-title__link').text.strip()
    name_array = re.split('\s+', full_name)

    name = name_array[0]
    model = ' '.join(name_array[1:])

    if(name == 'Alfa'):
        name = ' '.join(name_array[0:2])
        model = model = ' '.join(name_array[2:])
    
    return {
        'name': name,
        'model': model
    } 

def find_photo(element):
    return {'photo': element.find('a', class_='offer-item__photo  ds-photo-container')}

def append_dict_as_row_to_csv(file_name, dict_of_elem, field_names):
    with open(file_name, 'a+', newline='') as write_obj:
        dict_writer = DictWriter(write_obj, fieldnames=field_names)
        if write_obj.tell() == 0:
            dict_writer.writeheader()
        dict_writer.writerow(dict_of_elem)


def get_number_of_pages(element):
    return int(element.find_all('span', class_='page')[-1].text)

def find_car(offer):
        price = price_finder(offer)
        params = find_params(offer)
        name = find_name(offer)
        photo = find_photo(offer)
        return {**price, **params, **name, **photo}



def main():
    link = "https://www.otomoto.pl/osobowe/seg-city-car--seg-combi--seg-compact/?search%5Bfilter_enum_fuel_type%5D%5B0%5D=petrol-lpg&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_features%5D%5B0%5D=front-heated-seats&search%5Bfilter_enum_registered%5D=1&search%5Bfilter_enum_no_accident%5D=1&search%5Bprivate_business%5D=private&search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=&page={}"
    field_names = ['price', 'year', 'mileage', 'engine_capacity', 'fuel_type', 'name', 'model', 'photo']
    cars_file_name = 'cars.csv'

    page = requests.get(link.format(1))
    soup = BeautifulSoup(page.text, "html.parser")
    number_of_pages = get_number_of_pages(soup)
    print(number_of_pages)

    time.sleep(5)

    for page_number in range(1, 1+1):
        print("PROGRESS: ", page_number)
        page = requests.get(link.format(page_number))

        soup = BeautifulSoup(page.text, "html.parser")
        all_offers = soup.find_all('article')
        for offer in all_offers:
            car = find_car(offer)
            append_dict_as_row_to_csv(cars_file_name, car, field_names)

        time.sleep(5)



# page = requests.get("https://www.otomoto.pl/osobowe/seg-city-car--seg-combi--seg-compact/?search%5Bfilter_enum_fuel_type%5D%5B0%5D=petrol-lpg&search%5Bfilter_enum_damaged%5D=0&search%5Bfilter_enum_features%5D%5B0%5D=front-heated-seats&search%5Bfilter_enum_registered%5D=1&search%5Bfilter_enum_no_accident%5D=1&search%5Bprivate_business%5D=private&search%5Border%5D=created_at%3Adesc&search%5Bbrand_program_id%5D%5B0%5D=&search%5Bcountry%5D=&page=1")
# soup = BeautifulSoup(page.content, 'html.parser')
# print(soup.prettify())

if __name__ == "__main__":
    # execute only if run as a script
    main()
