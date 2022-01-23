<template>
<div>
    <h1 id="main-title">{{ script_title }}</h1>

    <p><button v-on:click="uplinkButton" id="uplink">Connect to matrix</button></p>
    <p><button v-on:click="downlinkButton" id="downlink">Disconnect from matrix</button></p>
    <table border="border" id="corp_container">
        <tr><th>Name</th><th>Origin</th></tr>
        <tr v-for="corp in corpos" :key="corp.id">
            <td>{{corp.name}}</td>
            <td>{{corp.origin}}</td>
        </tr>

    </table>

    <p>Nb of Kast company : <span> {{ numberKastCorpos }} </span></p>
    
    <p><a href="#top">Back to the top !</a></p> <!-- Goes to object id  -->

</div>
</template>

<script>


export default {
    name: "ScriptPage",
    props: {
        flavour: String
    },

    data: function() {
        return {
            corpos: [
                {name:"Haas-Kepler",origin:"Kast"},
                {name:"Zai",origin:"Hasek"},
                {name:"Kosmonav",origin:"Soviet"},
                {name:"Asclepia",origin:"Kast"}
            ],
            script_title: "Saiberp0nk script title"
        }
    },

    methods: {
        setUserName() {
            let myNickname = prompt("Please enter your nickname");
            if(!myNickname) {
                this.setUserName();
            } else {
                localStorage.setItem('name', myNickname);
                this.script_title = "Welcome in the grid " + myNickname;
            }
        },

        delUserName() {
            localStorage.removeItem('name');
        },

        uplinkButton() {
            if(!localStorage.getItem('name')) {
                this.setUserName();
            } else {
                let storedNickname = localStorage.getItem('name');
                this.script_title = "Welcome back in the grid " + storedNickname; 
            }    
        },
        downlinkButton() {
            if(localStorage.getItem('name')) {
                let storedNickname = localStorage.getItem('name');
                this.delUserName();
                this.script_title = "You're offgrid " + storedNickname; 
            } else {
                this.script_title = "You're not inside the grid.."; 
            }   
        }
    },

    computed: {
        numberKastCorpos() {
            let number = 0;
            for (let index = 0; index < this.corpos.length; index++) {
                if (this.corpos[index].origin === "Kast") {
                    number++;
                }         
            }
            return number
        },
        kastCompany() {
            return this.numberKastCorpos() > 0;
        },   
    },

    mounted: function() {
        console.log("Script component mounted")
    }

};
</script>