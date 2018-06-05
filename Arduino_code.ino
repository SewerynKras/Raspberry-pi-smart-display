#include <EtherCard.h>
#include <dht.h>
#define DHT11_PIN 2
dht DHT;
#define REDPIN 5
#define GREENPIN 6
#define BLUEPIN 3
static byte mymac[] = {0x74, 0x69, 0x69, 0x2D, 0x30, 0x31};
static byte myip[] = {192, 168, 1, 45};

byte Ethernet::buffer[700];
BufferFiller bfill;

const char HttpNotFound[] PROGMEM =
    "HTTP/1.0 404 Unauthorized\r\n"
    "Content-Type: text/html\r\n\r\n"
    "<h1>404 Page Not Found</h1>";

void setup()
{
    pinMode(REDPIN, OUTPUT);
    pinMode(GREENPIN, OUTPUT);
    pinMode(BLUEPIN, OUTPUT);
    analogWrite(REDPIN, 255);
    analogWrite(GREENPIN, 0);
    analogWrite(BLUEPIN, 255);
    Serial.begin(9600);
    Serial.println("Trying to get an IP...");
    if (ether.begin(sizeof Ethernet::buffer, mymac) == 0)
    {
        Serial.println("Failed to access Ethernet controller");
    }
    ether.staticSetup(myip);
#if STATIC
    Serial.println("Getting static IP.");
    if (!ether.staticSetup(myip, gwip))
    {
        Serial.println("could not get a static IP");
    }
#else

    Serial.println("Setting up DHCP");
    if (!ether.dhcpSetup())
    {
        Serial.println("DHCP failed");
    }
#endif

    ether.printIp("My IP: ", ether.myip);
    ether.printIp("GW IP: ", ether.gwip);
    ether.printIp("DNS IP: ", ether.dnsip);
}
char temp[8];
char humi[8];
static word HomePage()
{
    bfill = ether.tcpOffset();
    bfill.emit_p(PSTR(
                     "HTTP/1.0 200 OK\r\n"
                     "Content-Type: text/html\r\n"
                     "Pragma: no-cache\r\n"
                     "\r\n"
                     "$S"
                     ":"
                     "$S"),
                 temp, humi);
    return bfill.position();
}

void loop()
{
    word len = ether.packetReceive();
    word pos = ether.packetLoop(len);
    if (pos) // check if valid tcp data is received
    {
        bfill = ether.tcpOffset();
        char *data = (char *)Ethernet::buffer + pos;
        if (strncmp("GET /", data, 5) != 0)
        {
            bfill.emit_p(HttpNotFound);
        }
        else
        {
            data += 5;
            if (strncmp("thermometer", data, 11) == 0)
            {
                int chk = DHT.read11(DHT11_PIN);
                Serial.println("REQUESTED TEMP");
                itoa(DHT.temperature, temp, 10);
                itoa(DHT.humidity, humi, 10);
                HomePage();
            }
            else
            {
                HomePage();
            }
        }
        ether.httpServerReply(bfill.position()); // send http response
    }
}
