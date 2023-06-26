<template>
    <div class="container mt-5"  >
      <div class="row justify-content-center">
        <div class="col-md-4">
          <div class="card">
            <div class="card-header">
              <h4 class="mb-0">Sign up</h4>
            </div>
            <div class="card-body">

              <form class="form" role="form" autocomplete="off">
                <div class="mb-3 mt-2">
                  <label for="name" class="form-label">Full name</label>
                  <input type="text" class="form-control" name="name" id="name" v-model.trim.lazy="name" required="">
                </div>
                <div class="alert alert-danger m-1" v-if="name_errorMsg">
                  {{ name_errorMsg }}
                </div>

                <div class="mb-3 mt-2">
                  <label for="name" class="form-label">Username</label>
                  <input type="text" class="form-control" name="username" id="username" v-model.trim.lazy="username" required="">
                </div>
                <div class="alert alert-danger m-1" v-if="username_errorMsg">
                  {{ username_errorMsg }}
                </div>
  
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" class="form-control" id="password" v-model.trim.lazy="password" required="">
                </div>
  
                <div class="mb-3 mt-2">
                  <label for="confirm_password" class="form-label">Confirm Password</label>
                  <input type="password" class="form-control" id="confirm_password" v-model.trim.lazy="confirm_password" required="">
                </div>

                <div class="alert alert-danger m-1" v-if="password_errorMsg">
                  {{ password_errorMsg }}
                </div>

                <div class="mb-3 mt-2">
                  <a href="/">Already have an account? Log in</a>
                  <button type="submit" class="btn btn-primary float-end mb-2" @click.prevent="create">Create Account</button>
                </div>

              </form>
            </div>
           </div>
        </div>
      </div>  
    </div>
</template>

<script>
import validate from 'validate.js';

export default {

  name: "RegisterView",
  data() {
    return {
      name: "",
      username: "",
      password: "",
      confirm_password: "",
      name_errorMsg:"",
      username_errorMsg: "",
      password_errorMsg: "",
    };
  },
  methods: {
    ValidateName(){
      const constraints = {
        name: {
          presence: true,
          length: {
            minimum: 4,
            message: "must be at least 4 characters"
          },
          format: {
            // pattern contain a-z and A-Z wirite a code for that

            pattern: "[a-z A-Z]+",
           
            message: "can only contain a-z and A-Z"
          }
        },
        
      };
      const result = validate({name: this.name}, constraints);
      if(result){
        this.name_errorMsg = result.name[0];
        return false;
      }else{
        this.name_errorMsg = "";
        return true;
      }
    },

    validateUser(){
      const constraints = {
        username: {
          presence: true,
          length: {
            minimum: 4,
            message: "must be at least 4 characters"
          },
          format: {
            pattern: "[a-z0-9]+",
            message: "can only contain a-z and 0-9"
          }
        },
        
      };
      const result = validate({username: this.username}, constraints);
      if(result){
        this.username_errorMsg = result.username[0];
        return false;
      }else{
        this.username_errorMsg = "";
        return true;
      }
    },

    validatePassword(){
      const constraints = {
        password: {
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
        confirm_password:{
          presence: true,
          equality: {
            attribute: "password",
            message: "password must match"
          }
        }
        
      };
      
      
      const result = validate({password: this.password, confirm_password: this.confirm_password}, constraints);
      if(result){
        for(const key in result){
          // console.log(key);
          this.password_errorMsg = result[key][0];
        }
        return false;
      }else{
        // console.log("no errors");
        this.password_errorMsg = "";
        return true;
      };
    },

    async create(event) {
      event.preventDefault(); 
      if(this.validateUser() && this.validatePassword() && this.ValidateName()){
        const response = await fetch("http://localhost:5000/bloglite/registration", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: this.name.replace(/\b\w/g, l => l.toUpperCase()),
            username: this.username,
            password: this.password,
          }),
        });
        const data = await response.json();
        if (response.status === 201) {
          // alert message           
          this.$router.push("/");
          // alert("Account created successfully");
          alert(data.msg);
        } else {
          
          this.username_errorMsg = data.message;
          // console.log(data);
          alert(data.msg);
        }
      }
    }, 
  },
};
</script>
<style scoped>
/* .container {
  margin-top: 9em;
} */
</style>
  