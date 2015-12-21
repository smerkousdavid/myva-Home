#include <SPI.h>
#include <MFRC522.h>
#include <Udoo.h>

/*
Wiring is:
MFRC    ----   UDOO
----------------------
RST      ::      9
NSS      ::      10
MOSI     ::      11
MISO     ::      12
SCK      ::      13

Sketch isn't 100% tested but should work
If problems contact me at smerkousdavid@gmail.com
*/

#define RST 9 // Hard reset pin for rfid reader
#define SS 10 //Slave select
#define IP "192.168.1.17" //Server IP
#define PORT 9292 //Server Port


MFRC522 mfrc522(SS, RST);

Udoo udoo;
TcpClient client; //Creat client

MFRC522::MIFARE_Key key; //MIFARE_Key is just another name for byte key...

byte sector         = 0;
byte blockAddr      = 0; //Sectors we will acces, if blank then write to these using
byte trailerBlock   = 1; //The read/write example in the RFID library

void setup() {
    udoo.init(); //Start serialization with linux side
    client.connect(IP, PORT); //Tell linux to be ready to connect to server
    
    SPI.begin(); //Start SPI for rfid reader 
    mfrc522.PCD_Init();

    for (byte i = 0; i < 6; i++) {
        key.keyByte[i] = 0xFF; //Key is FFFFFFFFF....
    }                          //Change if not default key
}

void loop() {
  
    if ( ! mfrc522.PICC_IsNewCardPresent()) // Wait for card
        return;
    if ( ! mfrc522.PICC_ReadCardSerial()) //If can't read it
        return;

    byte piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);

    if (    piccType != MFRC522::PICC_TYPE_MIFARE_MINI
        &&  piccType != MFRC522::PICC_TYPE_MIFARE_1K
        &&  piccType != MFRC522::PICC_TYPE_MIFARE_4K) {
        return; //You can remove this if you want to TRY other cards
    }

    MFRC522::StatusCode status; //Again another fancy way of saying byte
    byte buffer[18]; //We should never exceed 18 bytes
    byte size = sizeof(buffer);


    status = (MFRC522::StatusCode) mfrc522.PCD_Authenticate(MFRC522::PICC_CMD_MF_AUTH_KEY_A, trailerBlock, &key, &(mfrc522.uid));
    if (status != MFRC522::STATUS_OK) {
        return; //Make sure key access is correct
    }
    
    status = (MFRC522::StatusCode) mfrc522.MIFARE_Read(blockAddr, buffer, &size);
    if (status != MFRC522::STATUS_OK) {
      //Have your own response code here like flicker a red LED
    }
    String card = dump(buffer, 16);
    client.send(card); //Write key to server
    client.close(); //Close single socket
    while((MFRC522::StatusCode) mfrc522.MIFARE_Read(blockAddr, buffer, &size) == MFRC522::STATUS_OK)
      delay(10); //While card/tag on reader don't send release response
    client.send("::CARD_RELEASE::"+card); //Send to main server that card has been released (auto insert values by Udoo.lib)
    client.close();
    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1(); //Stop the card reader
}

String dump(byte *buffer, byte bufferSize) {
    String out = "::CARD::";
    for (byte i = 0; i < bufferSize; i++) {
        out += String(buffer[i] < 0x10 ? "0" : "")+String(buffer[i], HEX);
    }
    out += "::END:CARD::"; //We make sure we recieve a full code
    out.toUpperCase(); //Comparing will be easier
    out.replace(" ", ""); //Just to be safe
    return out;
}
