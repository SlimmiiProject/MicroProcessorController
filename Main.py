from Webserver import Webserver
from Wifi import Wifi 
import uasyncio

async def main():
    # Maakt WLAN en ADHOC connectie aan (Wifi/AccessPoint)
    wlan = Wifi.CreateConnectionInterface()
    adhoc = Wifi.CreateHotspotInterface()

    # Maak webserver object aan en voeg de start task toe aan asyncio voor uit te voeren.
    www = Webserver(port=8080, maxClients=1)

    uasyncio.create_task(www.start())
    while True:
        await uasyncio.sleep_ms(10_000)


if __name__ == "__main__":
    uasyncio.run(main()) # Start main functie met async handler "uasyncio" => asyncio alternatief micropython.