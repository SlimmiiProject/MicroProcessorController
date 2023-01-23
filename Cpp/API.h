#ifndef API_H
#define API_H

class API
{
  private:
    /** @description: Send a json payload to the UsageLogAPI */
    static int SendJson(char* endpoint, char *payload);
    static void SetToken(char* token);


  public: 
    /**
    * @description: Sync the device with UsageLogAPI and get a session token for data transmission.
    *
    * @param uid The user id to fetch session token for.
    */
    static void SyncDevice(char* uid);

    /**
    * @description: Attempt to send to an image to the api if the device has a session token registered.
    */
    static void SendFrame();
    
    /**
    * @description: Check or session token is registered from a user registration.
    */
    static bool IsAuthenticated();
};

#endif