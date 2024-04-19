import ipaddress
from pathlib import Path

import maxminddb

class DBHandler:
    db_path:str = str(Path.joinpath(Path(__file__).parent.parent,'db/db.mmdb'));
    reader:maxminddb.Reader
    def __init__(self):
        self.reader = maxminddb.open_database(self.db_path)

        
    def resolve_ip(self, ip):
        ip_ret = {
                'ip': ip,
                'status': 'invalid',
                'netname': 'Unknown',
                'country': 'Unknown',
                'mnt_by': 'Unknown',
                'ip_version': 0,
                'is_private': False,
                'asn_name': 'Unknown',
                'asn_number': 'Unknown',
                'city_name': 'Unknown'
                
            }
        try:
            ip_ok = ipaddress.ip_address(ip)
            
            ip_ret['ip_version'] = ip_ok.version
            ip_ret['is_private'] = ip_ok.is_private
            
            if not ip_ok.is_private:
                ip_data = self.reader.get(ip)
                if ip_data:
                    ip_ret['status'] = 'valid'
                    ip_ret['netname'] = ip_data.get('netname', 'Unknown')
                    ip_ret['country'] = ip_data.get('country_name', 'Unknown')
                    ip_ret['mnt_by'] = ip_data.get('mnt_by', 'Unknown')
                    ip_ret['asn_name'] = ip_data.get('asn_name', 'Unknown')
                    ip_ret['asn_number'] = ip_data.get('asn_number', 'Unknown')
                    ip_ret['city_name'] = ip_data.get('city_name', 'Unknown')
                    ip_ret['iso_code'] = ip_data.get('iso_code', 'Unknown')
                    
                    

                
                
            
            
        except Exception as e:
            print(e)
        return ip_ret
                
        
    
    
    def resolve_ips(self, ips):
        data = []
        for ip in ips:
            data.append(self.resolve_ip(ip))
        return data
                
 