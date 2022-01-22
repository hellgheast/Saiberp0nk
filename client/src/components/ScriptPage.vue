<template>
<div>
    <h1 id="main-title">Saiberp0nk {{flavour}} page</h1>

    <p><button id="uplink">Connect to matrix</button></p>
    <p><button id="downlink">Disconnect from matrix</button></p>
    <table border="border" id="corp_container">
        <tr><th>Name</th><th>Origin</th></tr>
        <tr>
            <td>{{corpo_name}}</td>
            <td>{{corpo_origin}}</td>
        </tr>

        </table>
    
    <p><a href="#top">Back to the top !</a></p> <!-- Goes to object id  -->
</div>
</template>

<script>
const corpos = [["Zai","Hasek"],["Haas-Kepler","Kast"],["Kosmonav","Soviet"],["Asclepia","Kast"]];

export default {
    name: "ScriptPage",
    props: {
        flavour: String
    },

    data: function() {
        return {
        corpo_name: "",
        corpo_origin: ""
        };
    },

    methods: {
        updateCorpo: function () {
            this.corpo_origin = corpos[0][1]
            this.corpo_name = corpos[0][0]
        }
    },

    mounted: function() {
        this.updateCorpo();
    }

};
</script>