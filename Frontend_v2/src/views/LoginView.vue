<template>
    <div class="container"  >
      <div class="row justify-content-center">
        <div class="col-md-4">
          <div class="card">
            <div class="card-header">
              <h4 class="mb-0">Log in</h4>
            </div>
            <div class="card-body">

              <form class="form" role="form" autocomplete="off" >
                <div class="mb-3 mt-2">
                  <label for="name" class="form-label">Username</label>
                  <input type="text" class="form-control" name="username" id="username" v-model="username" required>
                </div>
  
                <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input type="password" class="form-control" id="password" v-model="password" required>
                </div>
                <div class="mb-3 mt-2">
                  <a href="/register">Don't have an account? Sign up</a>
                    <button type="submit" class="btn btn-primary float-end mb-2" v-if="username!='' && password!=''" @click="login">  log in  </button>
                </div>
              </form>
            </div>
           </div>
        </div>
      </div>  
    </div>
</template>

<script>

  import userStore from "../stores/counter.js";

  export default {
    name: "LoginView",

    setup() {
      const store = userStore();
      return { store };
    },
  
    data() {
      return {
        username: "",
        password: "",
        isLoggedin: this.store.isLoggedin,
        login_error: "",      
      };
    },


    methods: {
      async login(event){
        event.preventDefault();
        const response = await fetch("http://localhost:5000/bloglite/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });
        const data = await response.json();
        console.log(data);
        if(response.ok){
          if (response.status === 200){
          
          this.store.setToken(data.access_token);
          document.cookie = "access_token=" + data.access_token;
          // console.log(this.store.token);
          // this.store.isLoggedIn = true;
          this.$router.push("/home");
          alert(data.msg);
        }
        
      }else{

        this.login_error = data.message;
        // console.log(this.login_error);
        alert(data.msg);
      }
    },
    },

  };
</script>
<style scoped>
.container {
  margin-top: 9em;
}
</style>
  

<!-- Handle the response code for error and show it in the alert box. -->