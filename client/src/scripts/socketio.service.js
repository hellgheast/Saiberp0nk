import { io } from "socket.io-client";

class SocketService {
    socket;
    constructor() {}
    setupSocketConnection() {
        console.log("Setup Connection..");
        this.socket = io("http://localhost:3000");
        console.log("After socket creation");
        this.socket.emit("my message", "We're bounded from Vue !");
    }
    disconnect(){
        if(this.socket) {
            this.socket.disconnect();
            console.log("Disconnect...");
        } else {
            console.log("False disconnect");
        }
    }
    sendMessage(message){
        if(this.socket){
            this.socket.emit("chatmsg",message);
        }
    }
    sendMove(direction){
        if(this.socket){
            this.socket.emit("move",direction);
        }
    }
    addListener(){
        this.socket.on('my broadcast',(data) => {
            console.log(data);
        });
    }
    requestPosition(){
        if(this.socket){
            this.socket.emit("position_req",null);
        }
    }
    connected(){
        if(this.socket){
            if(this.socket.connected){
                return true;
            }
        }
        return false;
    }
}
export default new SocketService();