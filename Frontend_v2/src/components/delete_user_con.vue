<template>
    <div class="modal fade" id="delete_user_con" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">Delete Confirmation</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                Are you sure you want to delete your profile?
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="delete_user">Delete</button>
                <!-- the "data-bs-dismiss" attribute tells Bootstrap to close the modal when this button is clicked -->
            </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import userStore from '../stores/counter';

    export default {
        name: "delete_user_con",
        setup() {
            const store = userStore();
            return { store };
        },

        methods: {
            // Required methods for this component
            delete_user(){
                const headers = { 
                    'Content-Type': 'application/json',
                    Authorization: "Bearer " + this.store.access_token, 
                };
                axios.delete('http://localhost:5000/bloglite/deleteuser', {headers})
                .then(response => {
                    console.log(response);
                    this.store.c_logout();
                    console.log("logged out")
                    this.$router.push("/");

                })
                .catch(error => {
                    console.log(error);
                    alert("Something went wrong. Please try again later.")
                })
            }
        }
    }
</script>