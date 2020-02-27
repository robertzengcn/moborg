from lxml import etree, html
import urlparse
import re




class Fixurl(object):

    def fix_links(self,content, absolute_prefix):
        """
        Rewrite relative links to be absolute links based on certain URL.

        @param content: HTML snippet as a string
        """

        if type(content) == str:
            content = content.decode("utf-8")

        parser = etree.HTMLParser()

        content = content.strip()

        tree  = html.fragment_fromstring(content, create_parent=True)

        def join(base, url):
            """
            Join relative URL
            """
            if not (url.startswith("/") or "://" in url):
                return urlparse.urljoin(base, url)
            else:
                # Already absolute
                return url

        for node in tree.xpath('//*[@src]'):
            url = node.get('src')
            url = join(absolute_prefix, url)
            node.set('src', url)
        for node in tree.xpath('//*[@href]'):
            href = node.get('href')
            url = join(absolute_prefix, href)
            node.set('href', url)

        data =  etree.tostring(tree, pretty_print=False, encoding="utf-8")

        return data

    def fixpath(self,content,absolute_prefix):
        p = re.compile(r'<\s*img\b[^>]*src\s*=\s*"[^>"]*\.(?:png|jpg|bmp|gif)"[^>]*>', re.I)

        presult=p.findall(content)
        ig=re.compile(r'src="(.+?)"')
        s = "http"
        for index in range(len(presult)):
            matcher=re.search(ig,presult[index])
            if matcher.group(1).find(s)==-1:
                respurl=urlparse.urljoin(absolute_prefix, matcher.group(1))
                content=content.replace(matcher.group(1), respurl)
        return content
                #print matcher.group(1)