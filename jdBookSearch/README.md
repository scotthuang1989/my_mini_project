# Intro
A small app that search book on jd.com (one of china's biggest online shopping site)
by taking photo of book cover

# Project Structure

## web crawler

`jdBookScrapy`

This crawler collect data from jd.com. For the simplicity, I only crawl 25 books.
But this crawler is very scalable.

The data will be store at `jdBookData`

## Image Search Engine

`searchEngine`

This is the image search engine build on opencv.

## search app

`search.py`

This is the main app file. It will invoke the function in search engine. and do the image search.

## Test file

`queryImage`

This is the test image I took.

# How to return

## Run the crawler to collect data

`
cd jdBookScrapy
scrapy crawl jdBookSpider
`
Now you should have the data in `jdBookData` folder.

## Run image searcher

change directory to project main directory

`cd ..`

run it

`python search.py -d ./jdBookData/jdbookexporter.csv -c ./jdBookData -q queryImage/5.jpg
`

There are 5 test image, I took the photo with different background and angle. The search app will find correct match for all the test image but with different score which is understandable.
