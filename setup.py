import sys
from distutils.core import setup

VERSI_PYTHON_SAAT_INI = sys.version_info[:2]
VERSI_PYTHON_YANG_DIPERLUKAN =(3, 7)

if VERSI_PYTHON_SAAT_INI < VERSI_PYTHON_YANG_DIPERLUKAN:
  sys.stderr.write(
  """
  ============================
  Versi Python Tidak Di Dukung
  ============================
  Versi Python yang di perlukan untuk menginstall smansaancol adalah {}.{}+
  Tapi seperti nya kakak mencoba menginstall smansaancol menggunakan python versi {}.{}.

  Untuk mengatasi masalah ini, kakak bisa coba upgrade versi python yang sedang kakak gunakan :)

  """.format(*(VERSI_PYTHON_YANG_DIPERLUKAN + VERSI_PYTHON_SAAT_INI))
  )
  sys.exit(1)

with open('README.md','r',encoding = 'utf-8') as doc:
  readme = doc.read()

setup(
  name = 'smansaancol',
  packages = ['smansaancol'],
  version = '0.0.1',
  license='MIT',
  description = 'Scraping Web Elearning SMA N 1 Muara Ancalong',
  long_description=readme,
  long_description_content_type="text/markdown",
  author = 'Rahmat adha',
  author_email = 'rahmadadha11@gmail.com',
  url = 'https://github.com/MR-X-Junior/smansaancol',
  keywords = ['elearning', 'elearning-scraper', 'elearning-cbt-scraper'],
  python_requires=">=3.7",
  install_requires=[
          'html5lib',
          'requests',
          'bs4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: Indonesian',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3 :: Only'
  ],
)
