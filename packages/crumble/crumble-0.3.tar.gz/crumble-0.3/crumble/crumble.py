import json
import csv
import re
import os

from .fastmatch import FastMatch

#############################################################################
#
#	A necessary utility for accessing the data local to the installation.
#
#############################################################################

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data(path):
	return os.path.join(_ROOT, 'data', path)

#############################################################################

class Link(object):

	def __init__(self,url,linktype):
		self.scheme = None
		self.subdomain = None
		self.domain = None
		self.tld = None
		self.tld_info = None
		self.dtld = None
		self.port = None
		self.path = None
		self.url_country_iso = None # Country ISO code in path or subdomain
		self.query = None
		self.fragment = None
		self.email = None
		self.phone = None

		self.profile = None # ['twitter','facebook','instagram','linkedin']
		self.hosted = None

		self.original = url
		self.linktype = linktype

	def json(self):
		return {
				'scheme': self.scheme,
				'subdomain': self.subdomain,
				'domain': self.domain,
				'tld': self.tld,
				'tld_info': self.tld_info,
				'dtld': self.dtld,
				'port': self.port,
				'path': self.path,
				'url_country_iso': self.url_country_iso,
				'query': self.query,
				'fragment': self.fragment,
				'email': self.email,
				'phone': self.phone,
				'profile': self.profile,
				'hosted': self.hosted,
				'original': self.original,
				'linktype': self.linktype
				}

# A class to identify and parse URLs.
class Crumble(object):

	def __init__(self):

		self.cctld = {}
		self.country = {}
		self.iso = {}
		self.__build_tld_map__()

		self.fm = FastMatch(self.cctld.keys(),substring=True)

		reg = r'^(?P<s1>(?P<s0>[^:/\?#]+):)?' + 	\
				r'(?P<a1>//(?P<a0>[^/\?#]*))?' + 	\
				r'(?P<p0>[^\?#]*)' + 				\
				r'(?P<q1>\?(?P<q0>[^#]*))?' +		\
				r'(?P<f1>#(?P<f0>.*))?'

		self.urlre = re.compile(reg,re.IGNORECASE)

		self.profiles = {'twitter','facebook','instagram','linkedin','yelp',
						 'youtube','pinterest','snapchat','tiktok',
						 'yellowpages','yp','goo','google','blogspot',
						 'glassdoor','xing','angellist','crunchbase','angel',
						 'alibaba','tumblr','ec21','companycheck','vimeo',
						 'wikipedia','amazon','apple','youtu','lnkd'}

		self.hosted = {'wordpress','weebly','wix','webs','wixsite','websyte',
						'bravenet','dx','x10host','x10','elementfx','pcriot',
						'askme','tripod','vpweb'}

		self.invalid = {'invalid','example','test'}

		self.domains = {}

	def parse(self,url):
		if not url or url == 'http://': return None
		u = url.replace('\\','').lower().strip().rstrip('/')

		if '(' in url and ')' in url:
			url = url[url.index('(')+1:url.index(')')].replace("'",'').replace(',','')

		typ = self.__linktype__(u)

		if type == 'invalid':
			li = Link(u,'invalid')
			return li

		if typ == 'email':
			li = Link(u,'email')
			li.email = u[7:]
			if '?' in li.email:
				li.email = li.email[:li.email.index('?')]
			if li.email.split('@')[1].split('.')[0] in self.invalid:
				li.linktype = 'invalid'
				li.email = None
			return li

		if typ == 'phone':
			li = Link(u,'phone')
			li.phone = re.sub('[^0-9\+]','', u[4:])
			return li

		li = Link(u,typ)
		self.__components__(li)
		if not li.profile and not li.hosted:
			if li.dtld not in self.domains:
				self.domains[li.dtld] = 0
			self.domains[li.dtld] += 1
		return li

	def __linktype__(self,url):

		if not url or len(url) < 4:
			return 'invalid'
		if 'mailto:' in url:
			if '@' in url:
				return 'email'
			else:
				return 'invalid'
		if 'tel:' in url or 'callto:' in url:
			return 'phone'
		if 'bit.ly' in url:
			return 'redirect'
		if url[0] in ['/','#','?']:
			return 'relative'
		else:
			return 'web'

	# Returns domain components
	def __components__(self,url):

		link = url.original

		if url.linktype == 'relative':
			link = 'http://domain.com' + ('/' + url.original).replace('//','/')

		if 'http' not in url.original:
			link = 'http://' + url.original

		res = self.urlre.match(link)

		if res.group('s0'):
			url.scheme = res.group('s0')
		if res.group('a0') and url.linktype != 'relative':
			s = 0
			e = 0
			l = 0
			for m in self.fm.match(res.group('a0')):
				# Must match the end of the domain, not the middle.
				if m[2] != len(res.group('a0')):
					continue
				if len(m[0]) > l:
					s = m[1]
					e = m[2]
					l = len(m[0])
			url.tld = res.group('a0')[s:e].strip('.')
			if url.tld:
				url.tld_info = self.cctld['.'+url.tld]
			if len(res.group('a0')[:s].split('.')) > 1:
				url.subdomain = res.group('a0')[:s].split('.')[0]
				if '.'+url.subdomain in self.country:
					url.url_country_iso = self.country['.'+url.subdomain]['country'].strip('.')
				url.domain = '.'.join(res.group('a0')[:s].split('.')[1:])
			else:
				url.domain = res.group('a0')[:s]
			if ':' in url.domain:
				url.port = url.domain.split(':')[1]
				url.domain = url.domain.split(':')[0]
			url.dtld = url.domain + '.' + url.tld

			if not url.domain or url.domain in self.invalid:
				url.linktype = 'invalid'

		if res.group('p0'):
			url.path = res.group('p0')
			if '.'+url.path.strip('/').split('/')[0] in self.country:
				url.url_country_iso = self.country['.'+url.path.strip('/').split('/')[0]]['country'].strip('.')
		if res.group('q0'):
			url.query = res.group('q0')
		if res.group('f0'):
			url.fragment = res.group('f0')

		if not url.url_country_iso and url.tld_info:
			url.url_country_iso = self.iso.get(url.tld_info.get('country','').lower(),'')

		# Check if this is a 3rd party profile page
		if url.domain in self.profiles and url.path:
			url.profile = url.domain

		# Check if this is a 3rd party web host
		if url.domain in self.hosted and (url.path or url.subdomain):
			url.hosted = url.domain

	def __build_tld_map__(self):

		iso = open(get_data('iso_country.csv'),'rt',encoding='utf-8')
		csv_iso = csv.reader(iso)
		for header in csv_iso:
			break
		for c in csv_iso:
			name = c[0].lower()
			code = c[1].upper()
			self.iso[name] = code

		tld_c = open(get_data('tld-country.tsv'),'rt',encoding='utf-8')
		csv_tld_c = csv.reader(tld_c,delimiter='\t')

		for rec in csv_tld_c:
			self.country[rec[0]] = {'country':rec[1],'registry':rec[2],'type':'tld'}

		tld_f = open(get_data('tlds-alpha-by-domain.txt'),'rt',encoding='utf-8')
		sld_f = open(get_data('public_suffix_list.dat'),'rt',encoding='utf-8')

		for header in tld_f:
			break
		for line in tld_f:
			domain = '.'+line.strip().lower().replace('*.','')
			ref = {}
			if domain in self.country:
				ref = self.country[domain]
			self.cctld[domain] = ref

		curr_ref = None
		prev_space = False
		for line in sld_f:
			if not line.strip():
				prev_space = True
			if line.strip() and line[0] == '/' and prev_space:
				prev_space = False
				curr_ref = line.strip()
			if line.strip() and line[0] != '/':
				domain = '.'+line.strip().replace('*.','')
				ref = {'type':'sld','subdomain_authority':curr_ref}
				if '.'+domain.split('.')[-1] in self.country:
					ref['country'] = self.country['.'+domain.split('.')[-1]]['country']
					ref['registry'] = self.country['.'+domain.split('.')[-1]]['registry']
				self.cctld[domain] = ref
