# crumble
Breaks URLs into their component parts. Additionally handles mailto/call
protocols, and detects whether the URL represents a 3rd party profile on
social media websites.

## Usage

```
git clone https://github.com/Cognism/crumble.git
cd crumble
pip install .
```

Then, in Python (3.7.6+):

```
import crumble as urlp
cls = urlp.Crumble()
cls.parse('cognism.com').json()
>> {'schema':'http','domain':'cognism','tld':'com','linktype':'web'}
```

## Notes on implementation

The crumble module is based on a core regular expression to recognise
the various components on a URL, including 'schema', 'subdomain', 'domain',
'public-facing sub-level-domains', 'port', 'path', 'query', 'fragment'.

We recognise all IATA sub-level-domains according to lists provided and
maintained by the Mozilla Foundation. Identification of TLD matches is
done via fastmatch, our in-house fast-substring-matcher, in time linear to
the input string.

Lastly, we identify domains that are common social media paths, and surface
this information in the result (when the result also includes a path to a
profile).

## Why not use urllib.parse in the python standard library?

urllib.parse provides url component identification, but not to the depth
of detail that crumble does. For example, urllib does not provide any info
about the registrar/owner of the domains, country, social accounts, host
status, etc. However, urllib is able to identify and parse information from
gopher: svn: news: and a variety of other rare link types that crumble
doesn't care about.
