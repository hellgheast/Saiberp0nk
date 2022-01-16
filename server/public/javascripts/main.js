
/* First js scripts */


// onClick test for a given header
let myActiveTitle = "Saiberp0nk clicked script page";
const myTitle = document.querySelector('h1');
myTitle.textContent = "Saiberp0nk new Script page";

myTitle.onclick = function() {
    this.textContent = myActiveTitle;
}


// Username in local storage management
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

// Button behavior handling the stored nickname
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

// Trying to inject content through a placeholder div inside the HTML

const corpos = [["Zai","Hasek"],["Haas-Kepler","Kast"],["Kosmonav","Soviet"],["Asclepia","Kast"]];
corp_container = document.getElementById("corp_container");
thead = document.createElement("thead");
thead.innerHTML = "<tr><th>Name</th><th>Origin</th></tr>"
corp_container.appendChild(thead)

for(var i=0; i<corpos.length; i++){
    row = document.createElement("tr");
    corp_name = document.createElement("td");
    corp_name.innerHTML = corpos[i][0];
    row.appendChild(corp_name);
    corp_origin = document.createElement("td");
    corp_origin.innerHTML = corpos[i][1];
    row.appendChild(corp_origin);
    corp_container.appendChild(row);
}
