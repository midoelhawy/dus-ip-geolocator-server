import ipaddress
from pathlib import Path
import sqlite3
import maxminddb

class DBHandler:
    db_path:str = str(Path.joinpath(Path(__file__).parent.parent,'db/db.mmdb'));
    asn_db_path:str = str(Path.joinpath(Path(__file__).parent.parent,'db/asn_database.sqlite'));
    reader:maxminddb.Reader
    #asn_db: sqlite3.Connection
    db_version: "Unknown"
    def __init__(self):
        self.reader = maxminddb.open_database(self.db_path)

        # self.asn_db = 
        versionFilePath = str(Path.joinpath(Path(__file__).parent.parent,'current_db_version.txt'));
        try:
            with open(versionFilePath, 'r') as f:
                self.db_version = f.read().strip()
                print(f"Current Db version : {self.db_version}")
        except  Exception as e:
            print(e)
            self.db_version = "unknown"
        
        
        
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
                'city_name': 'Unknown',
                'iso_code': 'Unknown',
                'db_version': self.db_version
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
                
    def resolve_asn(self, asn_number):
        try:
            asn_db = sqlite3.connect(self.asn_db_path)
            cursor = asn_db.cursor()
            cursor.execute("SELECT asn_number, asn_name, asn_country_code FROM asn_data WHERE asn_number = ?", (asn_number,))
            result = cursor.fetchone()
            if result:
                result = dict(zip(['asn_number', 'asn_name', 'asn_country_code'], result))
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            result = None
        except Exception as e:
            print(f"Unexpected error: {e}")
            result = None
        finally:
            if 'asn_db' in locals():
                asn_db.close()
        return result

    def resolve_multiple_asns(self, asn_numbers):
        try:
            asn_db = sqlite3.connect(self.asn_db_path)
            cursor = asn_db.cursor()
            query = f"SELECT asn_number, asn_name, asn_country_code FROM asn_data WHERE asn_number IN ({','.join('?' for _ in asn_numbers)})"
            cursor.execute(query, asn_numbers)
            results = cursor.fetchall()
            results = [dict(zip(['asn_number', 'asn_name', 'asn_country_code'], row)) for row in results]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            results = []
        except Exception as e:
            print(f"Unexpected error: {e}")
            results = []
        finally:
            if 'asn_db' in locals():
                asn_db.close()
        return results