using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Sockets;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows.Documents;

//Server for ChatRoom
//Jerry Argyle and Crystal Olsen
namespace ChatRoom
{
    public class ServerConnection
    {
        string userName;
        bool runningState = true;
        string message;

        NetworkStream clientStream;
        TcpClient clientSocket;
        private byte[] buffer = new byte[1024];

        public ServerConnection(TcpClient sock)
        {
            try
            {
                this.clientSocket = sock;
                clientStream = clientSocket.GetStream();
                int bufferSize = sock.ReceiveBufferSize;
                clientStream.Read(buffer, 0, bufferSize);
            }
            catch (IOException e)
            {
                Console.WriteLine(e.StackTrace);
            }
            try
            {
                //if userName request is accepted, add to list of users
                message = Encoding.UTF8.GetString(buffer);
                if (userNameRequest(message))
                {
                    Server.clientList.Add(this);
                    
                }
            }
            catch
            {
                Console.WriteLine("error: username not accpted");
            }
        }

        private bool isConnected()
        {
            return runningState;
        }

        //returns true if all possible streams are closed,
        //changes runningState to false
       
        public bool Closed()
        {
            if (clientStream != null)
            {
                clientStream.Close();
            }
            if (clientSocket != null)
            {
                clientSocket.Close();
            }

            runningState = false;
            Server.clientList.Remove(this);

            return true;

        }

        //sends a public chat message
        //protocol message 5
        public void sendMessageToAll(string message)
        {
            string msg = message.Substring(message.IndexOf(" ")) + 1;
            broadcast("5 " + getUserName() + " " + getDate() + " " + msg + "/r/n");

        }

        //sends a private chat message
        // protocol message 6
        public void sendPrivateMessage(string msg)
        {
            string[] splitMessage = msg.Split(' ');
            int messageType = getMessageType(msg);
            string sender = splitMessage[1];
            string receiver = splitMessage[2];
            string date = getDate();
            string message = splitMessage[3];
            byte[] writeStream = new byte[1024];


            //search for the username
            // if true - write 6 to the socket

            for (int i = 0; i < Server.clientList.Count; i++)
            {
                ServerConnection findReceiver = Server.clientList[i];
                if (findReceiver.getUserName().Equals(findReceiver)) {
                    writeStream = Encoding.UTF8.GetBytes("6 " + sender + " " + receiver + " " + date +
                        " " + message + "/r/n");

                    clientStream.Write(writeStream, 0, writeStream.Length);
                }
            }
            
            Console.WriteLine("Could not find recieving userName");
        }

        private void broadcast(string v)
        {
            byte[] writeStream = null;
            foreach(ServerConnection user in Server.clientList){
                writeStream = Encoding.UTF8.GetBytes(v);
                clientStream.Write(writeStream, 0, writeStream.Length);
                writeStream = null;
            }

        }

        //logging out from the chat
        private bool disconnect()
        {
            bool closed = Closed();
            if (true)
            {
                broadcast("8 /r/n");
                broadcast("9 " + getUserName() + "/r/n");
            }
            return closed;
        }

        // checks if an userNameRequest is valid, and not used
        // logs user in if valid, broadcasts protocol message 1
        // if denied broadcasts protocol message 2

        private bool userNameRequest(string request)
        {
      
            //username is made up of valid characters and is not too long
            if (!charsAreValid(request) || request.Length > 15)
            {
                return false;
            }
            //desired username is not already in use
            foreach(ServerConnection users in Server.clientList) { 
                if (!users.Equals(request)) { 
                    string[] requestString = request.Split(' ');
                    request = requestString[1];
                       
                    //make list spaced out with commas
                    String usernameList = String.Join(",", Server.clientList);
                        
                    broadcast("1 " + Server.clientList + "Get Chatting! ");
                    userName = request;
                    return true;
                }
                else
                {
                    broadcast("2 UserName denied! /r/n");
                    Closed();
                    return false;
                }
            }
            return false;
        }

        //helper method to check if username request string is valid 
        private bool charsAreValid(string request)
        {
            Regex isValid = new Regex("[0-9A-Za-z]");
            if (isValid.IsMatch(request))
            {
                return true;
            }
            return false;
        }

        //set and get username
        private void setUsername(string userName)
        {
            this.userName = userName;
        }

        public string getUserName()
        {
            return userName;
        }


        public void run()
        {
            while (runningState)
            {
                try
                {
                    getMessageType(message);
                    switch (getMessageType(message))
                    {
                        case 0:
                            this.userNameRequest(message);
                            break;
                        case 3:
                            this.sendMessageToAll(message);
                            break;
                        case 4:
                            this.sendPrivateMessage(message);
                            break;
                        case 7:
                            this.disconnect();
                            break;
                        default:
                            Console.WriteLine("Message error, closing");
                            this.Closed();
                            break;
                    }
                }
                catch (IOException ioe)
                {
                    Console.WriteLine(ioe);
                }
            }
        }

        //returns the type of message
        public int getMessageType(string message)
        {
            int messageType = message[0];
            return messageType;
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
