
<template>
    <div>
        <h1 id="main-title">Saiberp0nk Main page {{props.flavour}} </h1>
    </div>
</template>

<script setup>
import {defineProps} from 'vue'
const props = defineProps({
    flavour: String
})
</script>