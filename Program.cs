using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;

namespace file_hash_checker
{
    internal class Program
    {
        /*static int ReadBlock(Stream s, byte[] block)
        {
            int position = 0;
            while (position < block.Length)
            {
                var actuallyRead = s.Read(block, position, block.Length - position);
                if (actuallyRead == 0)
                    break;
                position += actuallyRead;
            }
            return position;
        }*/

        private static string CalculateMD5(string data)
        {
            using (var md5 = MD5.Create())
            {
                /*using (var progress = new ProgressBar())
                {
                    progress.Report((double)(stream.Position / stream.Length));
                }*/
                /*using (FileStream stream = File.OpenRead(data))
                {
                    //md5.ComputeHash(stream);
                    long length = stream.Length;
                    byte[] buffer = new byte[length];
                    stream.Read(buffer, 0, length);
                    for (int i = 0; i < length; i += 4096)
                    {
                        md5.ComputeHash(buffer);
                        progress.Report((double)(i / length));
                    }
                }*/
                /*byte[] test = File.ReadAllBytes(data);
                int test1 = test.Length;
                for (int i = 0; i < test1; i++)
                {
                    md5.ComputeHash(test, i, 1);
                    progress.Report((double)(i / test1));
                }*/
                /*using (FileStream stream = File.OpenRead(data))
                {
                    byte[] buf = new byte[1024];
                    int bytesRead = -1, i = 0;
                    while (bytesRead != 0)
                    {
                        bytesRead = ReadBlock(stream, buf);
                        //if (bytesRead == 0)
                        //    break;
                        // байты с номерами от 0 до bytesRead сложить с соответствующими байтами ключа
                        // выравнивание до границы 64 байт не нужно
                        md5.ComputeHash(buf, 0, bytesRead);
                        //progress.Report(bytesRead / stream.Length);
                        i++;
                    }
                    Console.WriteLine(i);
                }*/
                Console.Write("Расчет MD5... ");
                using (FileStream stream = File.OpenRead(data))
                    md5.ComputeHash(stream);
                Console.WriteLine("Готово.");

                StringBuilder sb = new StringBuilder();
                byte[] hash = md5.Hash;
                for (int i = 0; i < hash.Length; i++)
                    sb.Append(hash[i].ToString("x2"));

                return sb.ToString();
            }
        }

        private static string InputData(string message)
        {
            Console.WriteLine(message);
            Console.Write("> ");
            string data = Console.ReadLine().Trim();
            //data = data.Replace("\\", "\\\\");
            if (string.IsNullOrWhiteSpace(data) || !File.Exists(data))
                return InputData(message);
            return data;
        }

        static void Main()
        {
            string source = InputData("\nВведите путь до файла:");
            string toCompare = InputData("\nВведите путь до файла для сравнения (или путь до файла с хэшем или сам хэш):");
            Console.WriteLine();
            
            string hash = CalculateMD5(source);
            bool result = false;
            if (Regex.Match(toCompare, @"[a-zA-Z0-9]{32,}").Success)
                result = hash == toCompare.ToLower();
            else if (File.Exists(toCompare))
                if (toCompare.EndsWith(".md5"))
                {
                    var fileData = File.ReadAllText(toCompare);
                    Match match = Regex.Match(fileData, @"[a-zA-Z0-9]{32,}");
                    if (match.Success)
                        result = hash == match.Value;
                }
                else
                    result = hash == CalculateMD5(toCompare);

            Console.WriteLine("\nСовпадает: " + (result ? "Да" : "Нет"));

            Console.WriteLine("\nНажмите любую клавишу...");
            Console.ReadKey();
        }
    }
}
