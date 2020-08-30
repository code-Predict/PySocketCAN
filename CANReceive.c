/*
 * CAN受信テスト 
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <errno.h>

#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>

#include <linux/can.h>
#include <linux/can/raw.h>

// CANソケットを開く (https://www.kernel.org/より引用)
int openCANSocket(char *channel){
    int sock;
    struct sockaddr_can addr;
    struct ifreq ifr;

    sock = socket(PF_CAN, SOCK_RAW, CAN_RAW);
	if (sock < 0) {
		perror("Socket error");
		return -1;
	}
	strcpy(ifr.ifr_name, channel);
	ioctl(sock, SIOCGIFINDEX, &ifr);

    // ノンブロッキング設定
    int val = 1;
    ioctl(sock, FIONBIO, &val);

	memset(&addr, 0, sizeof(addr));
	addr.can_family = AF_CAN;
	addr.can_ifindex = ifr.ifr_ifindex;

	if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
		perror("Bind error");
        return -1;
	}

    return sock;
}

// CANソケットを閉じる
int closeCANSocket(int CANSocket){
    return close(CANSocket);
}


int main(int argc, char **argv){
    errno = 0;
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

    // 受信タイムアウト時間設定
    struct timeval tv;
    tv.tv_sec = 3;
    tv.tv_usec = 0;

    int n = 0;
    while(!endReq){
        // fdsに設定されたソケットが読み込み可能になるまで待ちます
        n = select(0, &CANSocket, NULL, NULL, &tv);

        // タイムアウトの場合にselectは0を返します
        if (n == 0) {
            // ループから抜けます
            printf("timeout\n");
            break;
        }

        // フレームリード待機
        struct can_frame frame;

        // int nbytes = read(CANSocket, &frame, sizeof(struct can_frame));
        int nbytes = recv(CANSocket, &frame, sizeof(struct can_frame), 0);
        printf("%d\n", nbytes);
        
        // 受信データ量がcan_frameのサイズに合っていなければ、不正CANフレームとして処理
        if (nbytes < sizeof(struct can_frame)) {
            printf("error: %d\n", errno - EAGAIN);
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
