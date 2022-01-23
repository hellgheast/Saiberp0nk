<template>
<div>
    <h1 id="main-title">Saiberp0nk {{flavour}} page</h1>

    <p><button id="uplink">Connect to matrix</button></p>
    <p><button id="downlink">Disconnect from matrix</button></p>
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
        }
    },

    methods: {
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
        }
    },

    mounted: function() {
        console.log("Script component mounted")
    }

};
</script>