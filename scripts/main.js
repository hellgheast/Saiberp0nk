
/* First js scripts */

let myActiveTitle = "Saiberp0nk clicked script page";
const myTitle = document.querySelector('h1');
myTitle.textContent = "Saiberp0nk new Script page";

myTitle.onclick = function() {
    this.textContent = myActiveTitle;
}


function setUserName() {
    let myNickname = prompt("Please enter your nickname");
    if(!myNickname) {
        setUserName();
    } else {
        localStorage.setItem('name', myNickname);
        myTitle.textContent = "Welcome in the grid " + myNickname;
    }
}

function delUserName() {
    localStorage.removeItem('name');
}


let myUplinkButton = document.querySelector('#uplink');
myUplinkButton.onclick = function(){
    if(!localStorage.getItem('name')) {
        setUserName();
    } else {
        let storedNickname = localStorage.getItem('name');
        myTitle.textContent = "Welcome back in the grid " + storedNickname; 
    }    
}


let myDownlinkButton = document.querySelector('#downlink');
myDownlinkButton.onclick = function(){
    if(localStorage.getItem('name')) {
        let storedNickname = localStorage.getItem('name');
        delUserName();
        myTitle.textContent = "You're offgrid " + storedNickname; 
    } else {
        myTitle.textContent = "You're not inside the grid.."; 
    }    
}
