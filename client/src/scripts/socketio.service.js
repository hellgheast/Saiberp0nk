import { io } from "socket.io-client";

class SocketService {
    socket;
    constructor() {}
    setupSocketConnection() {

        this.socket = io("http://localhost:3000");
        console.log("After socket creation");
        this.socket.emit("my message", "We're bounded from Vue !");
    }
    disconnect(){
        if(this.socket) {
            this.socket.disconnect();
        }
    }
    sendMessage(message){
        if(this.socket){
            this.socket.emit("chatmsg",message);
        }
    }
    addListener(){
        this.socket.on('my broadcast',(data) => {
            console.log(data);
        });
    }
}
export default new SocketService();