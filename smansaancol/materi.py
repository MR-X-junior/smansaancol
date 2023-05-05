import re
import os
import requests

from . import utils
from bs4 import BeautifulSoup as bs4

class Materi:

  def __init__(self, requests_session, materi_url):
    self.sessions = requests_session
    self.materi_url = materi_url

    self.req = self.sessions.get(self.materi_url)
    self.res = bs4(self.req.text,'html5lib')

    # Materi Data
    box_body = self.res.find('div', attrs = {'class':'box-body'})

    if box_body is not None:
      self.mapel = box_body.find('td', attrs = {'width':False}).text
      self.title = box_body.find('h3').text
      self.tanggal_publish = box_body.find('td', string = re.compile('^\d{4}-\d{2}-\d{2}'), attrs = {'width':False}).text
      div_des = box_body.find('div', attrs = {'class':'col-md-12'})
      self.deskripsi = '\n'.join([khaneysia.text.strip() for khaneysia in div_des.findAll('p')])
    else:
      self.mapel = self.res.find('td',text = ':').find_next('td').text.strip()
      self.title = self.res.find('strong').find_next('h3').text.strip()
      self.tanggal_publish = self.res.find('th', text = "Tgl Publish").find_next('td').find_next('td').text.strip()
      self.deskripsi = '\n'.join([moya.text.strip() for moya in self.res.find('div',class_="col-md-12").find_all('p')])

    # Youtube
    self.youtube_embed = [re.sub('^\/\/','https://',neysia['src']) for neysia in self.res.findAll('iframe', attrs = {'src':re.compile('www\.youtube\.com\/embed')})]
    self.youtube_video = ["https://youtu.be/%s" % (re.search('\/embed\/(\w+)',echa).group(1)) for echa in self.youtube_embed]

    # File
    self.file = []

    for berkas in self.res.findAll('a', href = re.compile('\/berkas\/')):
      berkas_data = {"filename":os.path.basename(berkas['href']),"filesize":None,"download_url":None, "content-type":None, "content-length":None,"last-modified":None}
      response_file = self.sessions.head(berkas['href'])
      headers_file = response_file.headers
      berkas_data['download_url'] = response_file.url

      if 'content-type' in headers_file.keys(): berkas_data['content-type'] = headers_file['content-type']
      if 'last-modified' in headers_file.keys(): berkas_data['last-modified'] = headers_file['last-modified']
      if 'content-length' in headers_file.keys():
        berkas_data['content-length'] = headers_file['content-length']
        berkas_data['filesize'] = utils.convert_size(int(headers_file['content-length']))

      self.file.append(berkas_data)

  def __str__(self):
    return "Smansa Materi : mapel='%s' title='%s' tanggal_publish='%s' deskripsi='%s'" % (self.mapel, self.title, self.tanggal_publish, self.deskripsi)

  def __repr__(self):
    return "Smansa Materi : mapel='%s' title='%s' tanggal_publish='%s' deskripsi='%r'" % (self.mapel, self.title, self.tanggal_publish, self.deskripsi)

  @property
  def materi_info(self):
    return {"mapel":self.mapel,"title":self.title,"tanggal_publish":self.tanggal_publish, "deskripsi":self.deskripsi, "file":self.file,"komentar":self.get_comment(25)}

  def get_comment(self, limit):
    komen = []

    for khaneysia in self.res.findAll('li', attrs = {'class':'list-group-item'}):
      rahmat = {'name':None,'kelas':None,'message':None,'time':None}  # Komen Data
      nama = khaneysia.find('h5')
      message = khaneysia.find('div', style = "margin-top: 5px;")
      badge_komen = khaneysia.find('div', attrs= {'class':'badge'})

      if nama is not None: rahmat['name'] = nama.text
      if message is not None: rahmat['message'] = message.text.strip()

      if badge_komen is not None:
        regex_time = re.search("\d\d\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}\s\d{2}:\d{2}:\d{2}",badge_komen.text.strip())
        regex_kelas = re.search("\s\S{2}", badge_komen.text.strip())

        if regex_time is not None: rahmat['time'] = regex_time.group(0)
        if regex_kelas is not None: rahmat['kelas'] = regex_kelas.group(0)


      komen.append(rahmat)
      if len(komen) >= limit: break

    return komen[0:limit]

  def send_comment(self, message):
    url = self.req.url
    data = {'komentar':message}
    button_submit = self.res.find('button', attrs = {'type':'submit'})
    if button_submit is not None: data['submit'] = button_submit.text

    kirim = self.sessions.post(url, data = data)

    return kirim.ok
