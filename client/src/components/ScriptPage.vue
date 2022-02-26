<template>
<div>
    <h1 id="main-title">{{ state.script_title }}</h1>

    <p><button v-on:click="uplinkButton" id="uplink">Connect to matrix</button></p>
    <p><button v-on:click="downlinkButton" id="downlink">Disconnect from matrix</button></p>
    <table border="border" id="corp_container">
        <tr><th>Name</th><th>Origin</th></tr>
        <tr v-for="corp in state.corpos" :key="corp.id">
            <td>{{corp.name}}</td>
            <td>{{corp.origin}}</td>
        </tr>

    </table>

    <p v-if="kastCompany">Nb of Kast company : <span> {{ numberKastCorpos }} </span></p>
    
    <p><a href="#top">Back to the top !</a></p> <!-- Goes to object id  -->

</div>
</template>


<script setup>
import { reactive,computed,defineProps,onMounted} from 'vue'

    defineProps(['flavour'])
    const state = reactive({
        corpos: [
            {name:"Haas-Kepler",origin:"Kast"},
            {name:"Zai",origin:"Hasek"},
            {name:"Kosmonav",origin:"Soviet"},
            {name:"Asclepia",origin:"Kast"}
        ],
        script_title: "Saiberp0nk script title"
    })

    const numberKastCorpos = computed(() =>  {
        let number = 0;
        for (let index = 0; index < state.corpos.length; index++) {
            if (state.corpos[index].origin === "Kast") {
                number++;
            }         
        }
        return number
    })

    const kastCompany = computed(() => {
        return numberKastCorpos.value > 0;
    })






    function setUserName() {
        let myNickname = prompt("Please enter your nickname");
        if(!myNickname) {
            setUserName();
        } else {
            localStorage.setItem('name', myNickname);
            state.script_title = "Welcome in the grid " + myNickname;
        }
    }

    function delUserName() {
        localStorage.removeItem('name');
    }

    function uplinkButton() {
        if(!localStorage.getItem('name')) {
            setUserName();
        } else {
            let storedNickname = localStorage.getItem('name');
            state.script_title = "Welcome back in the grid " + storedNickname; 
        }    
    }

    function downlinkButton() {
        if(localStorage.getItem('name')) {
            let storedNickname = localStorage.getItem('name');
            delUserName();
            state.script_title = "You're offgrid " + storedNickname; 
        } else {
            state.script_title = "You're not inside the grid.."; 
        }   
    }
    onMounted(() => {
        console.log("Script component mounted")
    })

</script>