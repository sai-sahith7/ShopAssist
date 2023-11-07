from bs4 import BeautifulSoup
import requests, re, json
from flask import Flask,render_template,url_for,request,redirect
from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def amazon(searches):
    result = list()
    for search in searches:
        headers = {"User-Agent": "Defined"}
        while True:
            source = requests.get("https://www.amazon.in/s?k="+search,headers=headers).text
            soup = BeautifulSoup(source,"html.parser").prettify()
            if "It's rush hour and traffic is piling up on that page. Please try again in a short while." not in str(soup):
                break
        soup2 = BeautifulSoup(soup,"html.parser")
        parent_tag = soup2.find_all("div", attrs={"data-component-type" : "s-search-result"})
        price = list();link = list();image = list();title = list()
        for tag in parent_tag:
            try:
                price.append(tag.findChild("span", attrs={"class" : "a-price-whole"}).text.strip())
                link.append(tag.findChild("a", attrs={"class" : "a-link-normal s-no-outline"})["href"])
                image.append(tag.findChild("img", attrs={"class" : "s-image" })["src"])
                title.append(tag.findChild("img", attrs={"class" : "s-image" })["alt"])
            except:
                continue
        for i in range(len(link)):
            result.append([image[i],"https://www.amazon.in"+link[i],title[i],"Rs. "+price[i]])
    return result

def url_list_for_flipkart(input_text):
    link_list = list()
    while True:
        temp_list = list()
        img_link = ""
        link=""
        price = ""
        try:
            index_img = input_text.index('"media"') + input_text[input_text.index('"media"'):].index("http://")
            index_link = input_text.index('"baseUrl":"') + 11
            index_price = input_text.index('"finalPrice":{"a') + 69
        except:
            break
        while True:
            img_link += input_text[index_img]
            index_img +=1
            if ".jpeg?" in img_link:
                img_link = img_link.replace("{@width}","500")[:-1]
                img_link = img_link.replace("{@height}","1000")
                temp_list.append(img_link)
                break
        while True:
            link += input_text[index_link]
            index_link +=1
            if "," in link:
                link = link[:-2]
                temp_list.append("https://www.flipkart.com"+link)
                temp_list.append(link[1:link[1:].index("/")+1].replace("-"," ").title())
                break
        while True:
            price += input_text[index_price]
            index_price += 1
            if "," in price:
                price = price[:-2]
                temp_list.append("Rs. "+price)
                break
        input_text = input_text.replace('"media"', "", 1)
        input_text = input_text.replace('"baseUrl":"', "", 1)
        input_text = input_text.replace('"finalPrice":{"a', "", 1)
        link_list.append(temp_list)
    return link_list


def flipkart(searches):
    result = list()
    for search in searches:
        headers = {"User-Agent": "Edge/90.0.818.46"}
        source = requests.get("https://www.flipkart.com/search?q="+search,headers=headers).text
        soup = BeautifulSoup(source,"html.parser").prettify()
        return soup
        for i in url_list_for_flipkart(str(soup)):
            result.append(i)
    return result

def get_json_repsone(input):
    result = list()
    for i in input:
        if i[2] == "Ttps:":
            continue
        result.append({"image":i[0],"link":i[1],"title":i[2],"price":i[3]})
    return result

@app.get('/')
def index():
    return "API is up and running."

@app.get('/amazon/{search}')
def amazonroute(search: str):
    return get_json_repsone(amazon([search]))

@app.get('/flipkart/{search}')
def flipkartroute(search: str):
    # return get_json_repsone(flipkart([search]))
    return flipkart([search])

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)