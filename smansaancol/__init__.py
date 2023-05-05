import re
import codecs
import requests

from . import utils
from . import materi
from . import exceptions
from bs4 import BeautifulSoup as bs4

try:
  from urllib.parse import urlparse
  from urllib.parse import parse_qs
except (ImportError):
  from urlparse import urlparse
  from urlparse import parse_qs

class Elearning:

  def __init__(self, username, password):
    self.url = "https://elearning.sman1muaraancalong.sch.id"

    self.username = username
    self.password = password
    self.sessions = requests.Session()

    # Mengganti User Agent
    self.sessions.headers.update({'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'})

    # Login Ke Akun
    post_url = utils.urljoin(self.url,'/mobile_login.php')
    post_data = {'username':username,'password':password}

    submit = self.sessions.post(post_url, data = post_data)
    script = bs4(submit.text,'html5lib').find('script')
    window_location = re.search("<script>window.location\s=\s'(.*?)';\s<\/script>|window.location\s=\s'(.*?)';",script.string)

    if window_location is not None:
      next_uri = next((x for x in window_location.groups() if x is not None), self.url)

      # Mengecek Apakah sudah berhasil login
      cek_get = self.sessions.get(next_uri)
      cek_res = bs4(cek_get.text,'html5lib')
      form_sig = cek_res.find('form', attrs = {"class":"form-signin","name":"login"})

      if form_sig is not None:
        raise exceptions.LoginFailed("Gagal login ke akun, pastikan username & password kamu sudah benar!")
      else:
        self.nama = cek_res.find('li', class_ = 'visible-xs').text
        self.kelas = cek_res.find('span', class_ = 'badge bg-green').text
    else:
      alert = re.search("alert\('(.*?)'\)",script.string)
      err_msg = (alert.group(1) if alert is not None else "Gagal login ke akun, pastikan username & password kamu sudah benar!")

      raise exceptions.LoginFailed(err_msg)

  def __str__(self):
    return "Smansa Elearning : nama='%s' kelas='%s' username='%s'" % (self.nama, self.kelas, self.username)

  def __repr__(self):
    return "Smansa Elearning : nama='%s' kelas='%s' username='%s'" % (self.nama, self.kelas, self.username)

  def get_user_info(self):
    req = self.sessions.get(self.url)
    res = bs4(req.text,'html5lib')

    a = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
    b = re.findall(a,str(res.findAll('script')[1]))[0]
    c = urlparse(b)
    d = {'nama':self.nama,'username':self.username,'password':self.password,'kelas':self.kelas,'user':parse_qs(c.query)['user'][0],'api_key':parse_qs(c.query)['api_key'][0],'status':self.sessions.get(b).json()['message']}

    return d

  def absen(self, json = True):
    a = bs4(self.sessions.get(self.url).text,'html5lib')
    b = "https?:\\/\\/(?:www\\.)?[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)"
    c = re.findall(b,str(a.findAll('script')[1]))[1]
    d = self.sessions.post(c).json()

    if json:
      return d
    else:
      return (True if d['status'] == 'success' else False)

  def get_materi(self, limit, return_dict = False):
    materi = []

    a = self.sessions.get(utils.urljoin(self.url,'/materi'))
    b = bs4(a.text,'html5lib')

    if return_dict:
      for c in b.findAll('div', class_ = 'col-md-4'):
        materi.append({"guru":str(c.find('p').text).split('Guru : ')[1],"mapel":c.find('b').text.strip(),"title":c.find('div', class_ = 'box-footer').text.strip(),"materi_url":c.find('a')['href']})
        if len(materi) >= limit: break
    else:
      for c in b.findAll('a', href = re.compile('\/lihatmateri\/')):
        materi.append(self.view_materi(c['href']))
        if len(materi) >= limit: break

    return materi[0:limit]

  def view_materi(self, materi_url):

    return materi.Materi(self.sessions, materi_url)

"""
    if '/lihatmateri/' in materi_url:
      a = bs4(self.sessions.get(materi_url).text,'html5lib')
      b = a.findAll('li', class_ = 'list-group-item')
      c = '\n'.join([c.text.strip() for c in a.find('div',class_="col-md-12").find_all_next('p')])
      d = {'mapel':a.find('td',text = ':').find_next('td').text.strip(),
'tgl_publish':a.find('th', text = "Tgl Publish").find_next('td').find_next('td').text.strip(),
'title': a.find('strong').find_next('h3').text.strip(),'deskripsi':c,'komen':{'data':[],'total':len(b)}}

      for e in b:
        d['komen']['data'].append({'name':e.find('h5').text,'message':e.find('div', style = "margin-top: 5px;").text.strip(),'time':re.search("\d\d\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}\s\d{2}:\d{2}:\d{2}",a.find('div', class_ = 'badge').text.strip()).group(0),'kelas':re.search("\s\S{2}",e.find('div', class_ = 'badge').text.strip()).group(0)})

      return d
"""
