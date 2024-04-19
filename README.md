# D.U.S IP GeoLocator Server

The D.U.S IP GeoLocator Server, short for "Di Unni Sii IP GeoLocator Server," is a simple, custom, and self-hosted solution for geolocating IP addresses. Built upon the [openIPDb](https://github.com/midoelhawy/ripe-and-apnic-db-ip-parser), it provides a reliable method for parsing and leveraging IP address data from RIPE and APNIC databases.

This server offers a straightforward yet effective approach to IP geolocation, allowing users to query and obtain location-based information from IP addresses. Whether for analytical purposes, cybersecurity, or enhancing user experiences, the D.U.S IP GeoLocator Server offers a flexible and accessible solution tailored to your geolocation needs.

## How to Use

### Using Docker:

1. Ensure you have Docker installed on your system.
2. Pull the Docker image from Docker Hub:

   ```bash
   docker pull midoelhawy/dus-ip-geolocator-server:latest
   ```
3. Run the Docker container, exposing port 5000:

   ```bash
   docker run -d -p 5000:5000 midoelhawy/dus-ip-geolocator-server:latest
   ```
4. The D.U.S IP GeoLocator Server should now be running and accessible at `http://localhost:5000`.

### Using Python (Without Docker):

#### Method 1:

1. Ensure you have Python 3 installed on your system.
2. Install the required dependencies using `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```
3. Download and install the latest IP geolocation database using the script:

   ```bash
   ./scripts/download-latest-mmdb.sh
   ```
4. Start the server by executing the main script:

   ```bash
   python3 main.py
   ```

#### Method 2:

1. Ensure you have Python 3 installed on your system.
2. Install the required dependencies using `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```
3. Execute the entrypoint script, which handles downloading and installing the latest IP geolocation database, and starts the server:

   ```bash
   ./entrypoint.sh
   ```

The server should now be running and accessible for IP geolocation queries.



Here are the examples of using the API:

### Using the API:

##### Geolocating a Single IP Address:

```bash
curl 'http://127.0.0.1:5000/geolocate/212.45.97.60'
```

Response:

```json
{
  "asn_name": "Il Sole 24 Ore SpA",
  "asn_number": 12650,
  "city_name": "Bresso",
  "country": "Italy",
  "ip": "212.45.97.60",
  "ip_version": 4,
  "is_private": false,
  "iso_code": "IT",
  "mnt_by": "SOLE24ORE-MNT",
  "netname": "ILSOLE24ORE-BB",
  "status": "valid"
}
```

##### Geolocating Multiple IP Addresses:

```bash
curl 'http://127.0.0.1:5000/geolocate' \
--header 'Content-Type: application/json' \
--data '{
    "ips":["212.45.97.60","34.90.183.102"]
}'
```

Response:

```json
[
    {
        "asn_name": "Il Sole 24 Ore SpA",
        "asn_number": 12650,
        "city_name": "Bresso",
        "country": "Italy",
        "ip": "212.45.97.60",
        "ip_version": 4,
        "is_private": false,
        "iso_code": "IT",
        "mnt_by": "SOLE24ORE-MNT",
        "netname": "ILSOLE24ORE-BB",
        "status": "valid"
    },
    {
        "asn_name": "GOOGLE-2",
        "asn_number": 19527,
        "city_name": "New Delhi",
        "country": "India",
        "ip": "34.90.183.102",
        "ip_version": 4,
        "is_private": false,
        "iso_code": "IN",
        "mnt_by": "MAINT-APNIC-AP",
        "netname": "IANA-NETBLOCK-34",
        "status": "valid"
    }
]
```
