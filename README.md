# overkiz_exporter

A lightweight exporter to collect data from Overkiz-compatible devices and expose it for Prometheus monitoring. This project is specifically designed for use with an Atlantic water heater and Grafana dashboards.

## Acknowledgements
This project was made possible thanks to the following contributions:

- [python-overkiz-api](https://github.com/iMicknl/python-overkiz-api) by [iMicknl](https://github.com/iMicknl)
- [overkiz-exporter](https://pypi.org/project/overkiz-exporter/) by [jaesivsm](https://github.com/jaesivsm)

## Environment Variables
The `.env.example` file provides an example of the required environment variables:

```
OVERKIZ_USERNAME=your_username
OVERKIZ_PASSWORD=your_password
OVERKIZ_SERVERTYPE=ATLANTIC_COZYTOUCH
OVERKIZ_LOOP_INTERVAL=60
OVERKIZ_PROMETHEUS_PORT=8500
```

- You can read more about `OVERKIZ_SERVERTYPE` options [here](https://github.com/iMicknl/python-overkiz-api?tab=readme-ov-file#supported-hubs).

## How to Run the Docker Container
To run the exporter using Docker:

```bash
docker run -d --env-file .env -p 8500:8500 --name overkiz_exporter izmogikan/overkiz_exporter:v0.1.0
```

### Steps:
1. Create a `.env` file based on the provided `.env.example`.
2. Replace `your_username` and `your_password` with your Overkiz credentials.
3. Ensure port `8500` is open for Prometheus to scrape metrics.

## License
This project is licensed under the [MIT License](LICENSE).

---
Feel free to contribute or raise issues to improve this project!
