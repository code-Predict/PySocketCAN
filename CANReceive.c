/*
 * CAN受信テスト 
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>

#include <linux/can.h>
#include <linux/can/raw.h>

// CANソケットを開く (https://www.kernel.org/より引用)
int openCANSocket(char *channel){
    int sock = -1;

    struct sockaddr_can addr;
    struct ifreq ifr;
    sock = socket(PF_CAN, SOCK_RAW, CAN_RAW)
	if (sock < 0) {
		perror("Socket error");
		return -1;
	}
	strcpy(ifr.ifr_name, channel);
	ioctl(sock, SIOCGIFINDEX, &ifr);
    
	memset(&addr, 0, sizeof(addr));
	addr.can_family = AF_CAN;
	addr.can_ifindex = ifr.ifr_ifindex;

	if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
		perror("Bind error");
        return -1;
	}

    return s;
}

// CANソケットを閉じる
int closeCANSocket(int CANSocket){
    return close(CANSocket);
}


int main(int argc, char **argv){
    // CANソケットを開く
    printf("Opening can socket...");
    int CANSocket = openCANSocket("vcan1");
    if(CANSocket < 0){
        perror("failed. Couldn't open CAN Socket\n");
        return 1;
    }
    printf("finished.\n");


    // 受信ループ
    int endReq = 0;
    unsigned long int received = 0;

    while(!endReq){
        // フレームリード待機
        struct can_frame frame;

        // int nbytes = read(CANSocket, &frame, sizeof(struct can_frame));
        int nbytes = recv(CANSocket, &frame, sizeof(struct can_frame), 0);

        // 受信データ量がcan_frameのサイズに合っていなければ、不正CANフレームとして処理
        if (nbytes < sizeof(struct can_frame)) {
            print("error: %d", errno)
            perror("incomplete CAN frame\n");
            return 1;
        }

        // フレームを整形して表示
        printf("0x%03X [%d] ",frame.can_id, frame.can_dlc);
        for (int i = 0; i < frame.can_dlc; i++)
            printf("%02X ",frame.data[i]);
        printf("\r\n");
        received++;

        // ID: 0123が来たら終了
        if(frame.can_id == 0x123){
            endReq = 1;
        }
    }
    printf("%lu messages received.\n", received);

    // ソケットを閉じる
    closeCANSocket(CANSocket);
	return 0;
}
