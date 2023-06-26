<template>
    <!-- modal template for updating the password -->
    <div class="modal fade" id="update_password" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
        
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="staticBackdropLabel">Update Password</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            
            <form class="form" role="form" autocomplete="off" >
              <div class="mb-3 mt-2">
                <label for="password" class="form-label">Old Password</label>
                <input type="password" class="form-control" v-model="old_password" required>
              </div>
  
              <div class="mb-3">
                <label for="password" class="form-label">New Password</label>
                <input type="password" class="form-control"  v-model="new_password" required>
              </div>
  

              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" data-bs-dismiss="modal" v-if="old_password!='' && new_password!=''" @click="update_password">Update</button>
              </div>

            </form>
          </div>
  
        </div>
      </div>
    </div>

</template>

<script>
    import axios from 'axios';
    import userStore from '../stores/counter';
    import validate from 'validate.js';

    export default {
        name: "update_password",
        data() {
            return {
                old_password: '',
                new_password: '',
            }
        },
        setup() {
            const store = userStore();
            return { store };
        },

        methods: {
            validatePassword(){
                const constraints = {
                    new_password: {
                    presence: true,
                    length: {
                        minimum: 8,
                        message: "must be at least 8 characters"
                    },
                    format: {
                        pattern: "(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()_+\\-=\\[\\]{};':\"\\\\|,.<>\\/?]).{8,}",
                        message: " must contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character"
                    }
                    },                    
                };
      
      
                const result = validate({new_password: this.new_password}, constraints);
                if(result){
                    for(const key in result){

                    console.log(key);
                    this.password_errorMsg = result[key][0];
                    alert(result[key][0])
                    this.old_password = "";
                    this.new_password = "";
                    
                    }
                    return false;
                }else{
                    console.log("no errors");
                    // this.password_errorMsg = "";
                    return true;
                };
            },




            update_password(event) {
                // this.$emit('update_password', this.old_password, this.new_password)
                event.preventDefault();
                const data=  JSON.stringify({
                    "oldpassword": this.old_password,
                    "newpassword": this.new_password,

                });
                
                if(this.validatePassword()){
                    const headers = { 
                        'Content-Type': 'application/json',
                        Authorization: "Bearer " + this.store.access_token,
                    };

                        axios.put('http://127.0.0.1:5000/bloglite/password_update', data, { headers })
                        .then((response) => {
                            console.log(response.data.msg);
                            alert(response.data.msg);
                            this.store.c_logout();
                            console.log("logged out")
                            this.$router.push("/");

                        })
                        .catch(error => {
                            alert("Password not updated, please try again");
                            console.log(error);

                        });
                    }

                    

            }
        }
    }
</script>