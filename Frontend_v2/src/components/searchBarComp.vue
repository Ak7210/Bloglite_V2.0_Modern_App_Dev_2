<template>
    
    <div>
        <form @submit.prevent="search">
            <div class="input-group mb-3">
                <input type="text" class="form-control" placeholder="Type to search" v-model="query">
                <button class="btn btn-primary" type="submit">Search</button>
            </div>
        </form>
        <div v-if="results.length > 0">
            <ul>
                <div v-for="result in results" :key="result.id">
                    <li  v-if="result !== this.store.userName" >
                        <a  type="button" @click="showUser(result)">
                            <b>@{{ result }}</b>
                        </a>
                    </li>
                </div>
            </ul>
        </div>
        <div v-if="results.length===0 && query != '' ">
            No results found.
        </div>
    </div>

</template>

<script>
    import axios from 'axios';
    import userStore from "../stores/counter.js";

    export default {
        name: 'searchComp',

        setup() {
            const store = userStore();
            return { store };
        },

        data() {
            return {
            query: '',
            results: [],
            };
        },
        methods: {
            async search() {
                const headers = { 
                    'Content-Type': 'application/json',
                    Authorization: "Bearer " + this.store.access_token, 
                };

            try {

                const response = await axios.get(`http://localhost:5000/bloglite/search/${this.query}`, { headers });
                const data = await response.data;
                this.results = data.username;
                console.log(data);
            } catch (error) {
                console.error(error);
                this.results = [];
            }
            },

            showUser(result) {
                this.store.show_User(result);
                // console.log(this.store.searchUser)
            //    push to profile view
                this.$router.push("/profile")                
            },
        },
    };
</script >

<style scoped>
ul.list-unstyled {
  list-style: none;
  padding-left: 0;
}
</style>
  