import whois #python-whois

class WhoIsHelper(object):
    def __init__(self, url):
        self.url = url
        self.domain = url.split("www.")[-1].split("//")[-1].split("/")[0].split(":")[0]
        try:
            self.whois_object = whois.whois(self.domain)
        except Exception as e:
            print(e)
    
    def get_domain(self):
        return self.domain
    
    def get_emails(self):
        whois_emails = self.whois_object.emails
        if whois_emails is not None:
            if type(whois_emails) == list:
                return whois_emails
            else:
                return [whois_emails]
        return []
    
    def get_emails_by_ip(self):
        import socket
        from ipwhois import IPWhois
        ip = socket.gethostbyname(str(self.domain))
        return IPWhois(ip).lookup_whois()["nets"][0]["emails"]
    
    def get_emails_by_shell(self):
        import subprocess
        import re
        raw_whois = subprocess.Popen("whois %s | grep '@'" % self.domain, shell=True, stdout=subprocess.PIPE).stdout.read().decode("utf-8")
        email = re.findall("\w*\@\w*\.\w*", str(raw_whois))
        return list(set(email))
    
    def get_unified_emails(self):
        w = self.get_emails()
        i = self.get_emails_by_ip()
        s = self.get_emails_by_shell()
        return list(set(w + i + s))
    
    def get_country(self):
        return self.whois_object.country

    def get_whois_text(self):
        return self.whois_object.text
    
    def is_private_ip_address(self):
        import ipaddress
        try:
            return ipaddress.ip_address(self.domain).is_private
        except Exception as e:
            return False