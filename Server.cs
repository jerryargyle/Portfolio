using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Documents;

/** Jerry Argyle and Crystal Olsen
 *  Chat Server
 *  CMPT 352
 **/

namespace ChatRoom
{
    public class Server
    {
        public const int port = 1337;
        
        //List of connected clients
        public static List<ServerConnection> clientList = new List<ServerConnection>();

        public static void Main(string[] args)
        {
            Server server = new Server();

            try
            {
                server.start();

            }

            catch (IOException ioe)
            {
                Console.Error.WriteLine(ioe);
            }

        }

        private void start()
        {
            //My IP
            IPAddress serverIp = IPAddress.Parse("192.168.1.97");

            TcpListener serverSocket = new TcpListener(IPAddress.Loopback, port);
            serverSocket.Start();
            Console.Write("Chat server started");

            try
            {
                bool isRunning = true;
                while (isRunning)
                {
                    TcpClient clientSocket = serverSocket.AcceptTcpClient();
                    Console.WriteLine("server socket accepted");

                    NetworkStream clientStream = clientSocket.GetStream();

                    Console.WriteLine("client stream created");
                    ServerConnection clientThreads = new ServerConnection(clientSocket);
                    Task.Factory.StartNew(clientThreads.run);

                    if (!clientThreads.Closed())
                    {
                        Console.WriteLine("Threads executing");
                        broadcast(("10 " + clientThreads.getUserName() + "/r/n"), clientStream);
                        // execute clientThreads
                    }
                }
            }
            catch (IOException ioe)
            {
                Console.Error.WriteLine(ioe);
            }
        }


        private void broadcast(string message, NetworkStream clientSocket)
        {
            byte[] writeStream = null;
            foreach (ServerConnection user in Server.clientList)
            {
                writeStream = Encoding.UTF8.GetBytes(message);
                clientSocket.Write(writeStream, 0, writeStream.Length);
                writeStream = null;
            }
        }

        //returns the date in GMT format
        private string getDate()
        {
            DateTime date = DateTime.UtcNow;
            string formatDate = "yyyy:MM:DD:HH:mm:ss";
            return formatDate;
        }
    }
}

            

