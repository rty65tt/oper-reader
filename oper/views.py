# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.cache import cache_page

import requests
from bs4 import BeautifulSoup

import os, time
from oper.settings import BASE_DIR

# Create your views here.

from lxml import html, etree
import re

from lxml.html.clean import Cleaner

cleaner = Cleaner()
cleaner.javascript = False
cleaner.scripts = False
cleaner.style = True
cleaner.safe_attrs_only = False

url = 'https://oper.ru'

def cleanhtml(o):
    rattr = ['style', 'width', 'height']
    for a in rattr:
        p = '//*[@' + a + ']'
        for s in o.xpath(p):
            s.attrib.pop(a)

def get_page(u, clean=True):
    r = requests.get(u)
    soup = BeautifulSoup(r.text)
    o = html.fromstring(soup.encode('UTF-8'))
    if clean:
        cleanhtml(o)
    return o

def format_news(md):
    md = md.replace(u'»','')
    md = md.replace(u'href="/static/','href="https://oper.ru/static/')
    md = md.replace(u'src="/static/','src="https://oper.ru/static/')
    md = md.replace(u'href="/donate/','href="https://oper.ru/donate/')
    md = md.replace(u'src="/video/','src="https://oper.ru/video/')
    md = re.sub(r'\<iframe.+name=(\".+?\").+?>([\s\S]+?)\</iframe>', 
            r'<div class="youtube" data-embed=\1>\2</div>' , md)
    return md

@cache_page(60)
def main(request):

    if request.method == "GET" and "page" in request.GET:
        u = url + '?page=%s' % request.GET['page']
    else:
        u=url
    
    o = get_page(u)
    
    arch = o.xpath('//p[@class="categories"]')[0]
    etree.strip_tags(arch,'b')
    p = etree.tostring(arch, encoding='unicode')

    for i in o.xpath('//dd[@class="banner"]'):
        i.getparent().remove(i)

    m = o.xpath('//dl')[0]
    etree.strip_tags(m,'font')
    etree.strip_tags(m,'b')

    me = o.xpath('//p[@class="meta"]')
    for i in me:
        etree.strip_tags(i,'a')

    b1 = o.xpath('//td/div[@id="right"]/div[@class="block"]')[0]
    b2 = o.xpath('//td/div[@id="right"]/div[@class="block"]')[1]

    for bad in o.xpath('//*[@id="right"]/div[@class="block"]/h3'):
        bad.getparent().remove(bad)

    md = etree.tostring(m, encoding='unicode')
    md = format_news(md)

    e1 = etree.tostring(b1, encoding='unicode')
    e2 = etree.tostring(b2, encoding='unicode')
    e2 = e2.replace('src="/','src="https://oper.ru/')

    return render(request, "main.html", 
            {'m':md, 'p':p, 'b1':e1, 'b2':e2})


def comments_format(comments, com):
    for i in comments:
        nick = i.xpath('./tr/td[@class="text13"]/a/font/b')[0].text_content()
        color = i.xpath('./tr/td[@class="text13"]/a/font')[0].get('color')
        posted = i.xpath('./tr/td[2]/table/tr/td[1]/span/span[@class="posted"]')[0].text_content()
        posted = posted.replace(u'отправлено ','')
        num = i.xpath('./tr/td[2]/table/tr/td[2]/a')[0].get('href')
        num = num.replace('#','')
        comment = etree.tostring(i.xpath('./tr/td[2]/font/div')[0], encoding='unicode')
        com.append({'nick':nick,'color':color,'posted':posted,'num':num,'comment':comment})
    return com

def comm(c,p,link):
    i = 1
    if p > 20:
        p = 20
    while i<p:
        u = link + '&page=%s' % i
        o = get_page(u)
        comments = o.xpath('//table[@class="comment"]')
        c = comments_format(comments, c)
        i = i+1
    return c


def get_comments(o, u):
    cs = []
    comments = o.xpath('//table[@class="comment"]')
    cs = comments_format(comments, cs)

    plc = o.xpath('//div[@id="middle"]/table/tr[@valign="middle"]/td[1]/font/b/a[last()]')
    if plc:
        plc = int(plc[0].text_content())
        cs = comm(cs,plc,u)

    return cs

@cache_page(60)
def forum(request):
    if request.method == "GET" and "t" in request.GET:
        u = url + '/news/read.php?t=%s' % request.GET['t']
        o = get_page(u)
        title = o.xpath('//h1')[0]
        n = o.xpath('//dl')[0]
        etree.strip_tags(n,'font')
        etree.strip_tags(n,'b')
        me = o.xpath('//p[@class="meta"]')
        for i in me:
            etree.strip_tags(i,'a')
        
        h1 = etree.tostring(title, encoding='unicode')
        n = etree.tostring(n, encoding='unicode')
        n = format_news(n)

        cs = get_comments(o, u)

        return render(request, "news.html", 
            {'h1':h1, 'n':n, 'cs':cs, 'u':u})
    else:
        return redirect('/')

@cache_page(60)
def stenogramma(request):
    u = url + '/video/view.php'
    if request.method == "GET" and "t" in request.GET:
        u = u + '?t=%s' % request.GET['t']
    
        #o = get_page(u)
        r = requests.get(u)
        o = html.fromstring(r.text.encode('UTF-8'))

        h1 = o.xpath('//h1')[0].text_content()
        text = o.xpath('//div[@class="body"]')[0]
        etree.strip_tags(text,'font')

        for s in text.xpath('//a'):
            etree.strip_tags(s, 'b')
            #tt = s.text.rstrip()
            #s.append(tt)

        n = etree.tostring(text, encoding='unicode')

        cs = []# get_comments(o, u)

        return render(request, "text.html", 
            {'h1':h1, 'n':n, 'cs':cs, 'u':u})

    return redirect('https://catalog.oper.ru/')

@cache_page(60)
def gallery(request):
    if request.method == "GET" and "t" in request.GET:
        u = url + '/gallery/view.php?t=%s' % request.GET['t']

        o = get_page(u)
        
        title = o.xpath('//h1')[0]
        h1 = etree.tostring(title, encoding='unicode')

        n = o.xpath('//div[@id="middle"]/table/tr/td/a/img')[0].get('src')
        cs = get_comments(o, u)

        il = u'https://oper.ru/static/data/gallery/l%s.jpg' % request.GET['t']
        
        n = u'<img src="%s">' % il
        n = u'<a href="%s" target="_blank">%s</a>' % (il,n)
        n = u'<div class="image">' + n + '</div>'

        return render(request, "news.html", 
            {'h1':h1, 'n':n, 'cs':cs, 'u':u})

    if request.method == "GET" and "div" in request.GET:
        u = url + '/gallery/list.php?div=%s' % request.GET['div']
    else:
        u = url + '/gallery/'

    o = get_page(u, clean=False)
    
    title = o.xpath('//h1')[0]
    h1 = etree.tostring(title, encoding='unicode')
    n = etree.tostring(o.xpath('//p[@class="categories"]')[0], encoding='unicode')

    imglist = o.xpath('//ins[@class="thumbnail"]')

    il = []
    for i in imglist:
        img = etree.tostring(i, encoding='unicode')
        img = img.replace(u'/static','https://oper.ru/static')
        il.append({'img':img})

    return render(request, "gallery.html", 
            {'h1':h1, 'n':n, 'il':il})

@cache_page(60)
def archive(request):
    u = url + '/news/archive.php'
    if request.method == "GET" and "year" in request.GET:
        u = u + '?year=%s' % request.GET['year']

    o = get_page(u)
    
    title = o.xpath('//h1')[0]
    n = o.xpath('//p[@class="categories"]')[0]
    news = o.xpath('//table[@class="comment"]/tr')

    h1 = etree.tostring(title, encoding='unicode')
    n = etree.tostring(n, encoding='unicode')


    cs = []
    for i in news:
        date = i.xpath('./td[1]')[0].text_content()
        link = i.xpath('./td[2]')[0]
        link = etree.tostring(link, encoding='unicode')
        link = link.replace(u'<td>','')
        link = link.replace(u'</td>','')

        razdel = i.xpath('./td[3]')[0].text_content()
        kolcom = i.xpath('./td[4]')[0].text_content()
        kolcom = kolcom.replace(u'»','')
        cs.append({'date':date,'link':link,'razdel':razdel,'kolcom':kolcom})

    return render(request, "archive.html", 
            {'h1':h1, 'n':n, 'cs':cs})

@cache_page(60)
def donate(request, kassa):
    return redirect('https://oper.ru/donate/' + kassa)

def about(request):
    return render(request, "about.html")


def robots_txt_view(request):
    s = "User-agent: *\nDisallow: /\n"
    return HttpResponse(s, content_type="text/plain")
