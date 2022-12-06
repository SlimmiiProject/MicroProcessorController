#ifndef FILEMANAGER_H
#define FILEMANAGER_H
class FileManager 
{
  public:
    static bool writeFile(char* filepath, char* content);
    static String readFile(char* filepath);
    static bool fileExists(char* filepath);
};
#endif