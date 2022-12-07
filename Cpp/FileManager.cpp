#include "SPIFFS.h"
#include "FileManager.h"

bool FileManager::writeFile(char *filepath, char *content)
{
  if(!SPIFFS.begin(true))
    return false;
  
  File writer = SPIFFS.open(filepath, FILE_WRITE);
  if(writer)
  {
    writer.print(content);
    writer.close();
  }

  return SPIFFS.exists(filepath);
}

String FileManager::readFile(char *filepath)
{
  if(!SPIFFS.begin(true) || !SPIFFS.exists(filepath))
    return String("");
    
  File reader = SPIFFS.open(filepath, FILE_READ);
  size_t size = reader.size(); 
  char string[size + 1];      

  reader.read((uint8_t *)string, sizeof(string));  
  reader.close(); 

  string[size] = '\0';

  return String(string);
}

bool FileManager::fileExists(char* filepath)
{
  if(!SPIFFS.begin(true))
    return false;

  return SPIFFS.exists(filepath);
}