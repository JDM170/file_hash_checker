using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;

namespace file_hash_checker
{
    internal class Program
    {
        private static string CalculateMD5(string data)
        {
            using (var md5 = MD5.Create())
            {
                //using (var progress = new ProgressBar())
                //{
                //    progress.Report((double)(stream.Position / stream.Length));
                //}
                Console.Write("Расчет MD5... ");
                using (var stream = File.OpenRead(data))
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
            if (data.Length == 0 || data == string.Empty)
                InputData(message);
            return data;
        }

        static void Main()
        {
            string filename = InputData("\nВведите путь до файла:");
            string remote = InputData("\nВведите путь до файла для сравнения (или путь до файла с хэшем или сам хэш):");
            Console.WriteLine();
            
            string hash = CalculateMD5(filename);
            bool result = false;
            if (Regex.Match(remote, @"[a-zA-Z0-9]{32,}").Success)
                result = hash == remote.ToLower();
            else if (File.Exists(remote))
                result = hash == CalculateMD5(remote);
            else if (remote.EndsWith(".md5"))
            {
                if (!File.Exists(remote))
                {
                    Console.WriteLine("Файл не найден!");
                    return;
                }
                var fileData = File.ReadAllText(remote);
                Match match = Regex.Match(fileData, @"[a-zA-Z0-9]{32,}");
                if (match.Success)
                    result = hash == match.Value;
            }

            Console.WriteLine("\nСовпадает: " + (result ? "Да" : "Нет"));

            Console.WriteLine("\nНажмите любую клавишу...");
            Console.ReadKey();
        }
    }
}
