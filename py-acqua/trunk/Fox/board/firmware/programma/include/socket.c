
#define RX_BUFFER_LEN 1024
#define TX_BUFFER_LEN 1024

#ifndef IO_SETGET_INPUT
#define IO_SETGET_INPUT 	0x12
#endif

#ifndef IO_SETGET_OUTPUT
#define IO_SETGET_OUTPUT 	0x13
#endif


//****************************************************
// Socket functions
//****************************************************

// Send a formatted string to a socket

int socket_printf(int fs, char *format, ...) {
	va_list argptr;
	char msg[TX_BUFFER_LEN];
	
  va_start(argptr,format);
  vsprintf(msg,format,argptr);
  va_end(argptr);
	
  write(fs,msg,strlen(msg));
  return 0;
}	
int local_port;
  int cs;
  int s;
  int sockfl;
  int size_csa;
  struct sockaddr_in csa;
  struct sockaddr_in sa; 
  int rc;
  int yes = 1;
  int rxpointer=0;
	char rxbuffer[RX_BUFFER_LEN];
	int ch;
	int value;
	char zero[1];

int socket_init(){
local_port=3023;


	zero[0]=0;
  rxbuffer[rxpointer]=0;

  memset(&sa, 0, sizeof(sa));

  sa.sin_family = AF_INET;         
  sa.sin_port = htons(local_port); 
  sa.sin_addr.s_addr = INADDR_ANY; 

  // Create a socket
  
  s = socket(AF_INET, SOCK_STREAM, 0);
  if (s < 0) {
    printf("Error opening control socket\n");
    return -1;
  }

  // Socket in non blocking mode
  sockfl = fcntl(s, F_GETFL, 0);
  fcntl(s, F_SETFL, sockfl | O_NONBLOCK);

  setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int));

  rc = bind(s, (struct sockaddr *)&sa, sizeof(sa));
  if (rc) {
    printf("Error binding control socket\n");
    return -1;
  }

  rc = listen(s, 1);

  if (rc) {
    printf("Error listening control socket\n");
    return -1;
  } 
sockfl = fcntl(cs, F_GETFL, 0);
      fcntl(cs, F_SETFL, sockfl | O_NONBLOCK);
    

}

void soket_close(){

  close(s);
} 


void soket_write(){//userò questa
	//	socket_printf(cs,testo);
//write(cs,zero,1); 

} 



/*
int xml_monitor(int local_port) {

	

  
  while(1) {  
    
   // size_csa = sizeof(csa);
   // cs = accept(s, (struct sockaddr *)&csa, &size_csa); // Qui non si ferma
    
 //   if (cs > 0) {
    	
      
      // Read data loop
			value=0;	
      for (;;) {
				sleep(1);

     		socket_printf(cs,"<analog>");
				for (ch=0;ch<4;ch++) {
					
					socket_printf(cs,"<input line=\"%d\" value=\"%d\"/>",ch,value);
					
				}	
				socket_printf(cs,"</analog>");
				printf("\n");
				
			  write(cs,zero,1); 
      }
     
 // }
  printf("Rx socket accept timeout\n");
  sleep(2);
  return -1;
} 
*/