<template v-if="!this.store.isLoggedIn">
  <div class="container-fluid" >
    <div class="row">
      <div class="col-md-2 bg-light sidebar">
        <div class="sidebar-content d-flex flex-column align-items-center" ref="leftSidebar">

          <div style="margin-top: 0%; margin-left: -5%;">
            <button type="button" class="btn btn-primary" style="width: 110px;" @click="activeComp='blogComp'">
              Home
            </button>
          </div>
            
          <div style="margin-top: 5%; margin-left: -5%;">
            <button type="button" class="btn btn-primary" style="width: 110px;" @click="activeComp='profileComp'">
              My Profile
            </button>
          </div>

          <div style="margin-top: 5%; margin-left: -5%;">
            <button type="button" class="btn btn-primary positon-absolute" style="width: 110px" @click="summary()">Summary</button>
          </div>

          <div class="d-flex mt-auto" style="margin-bottom: 5%; margin-left: -5%;">
            <button type="button" class="btn btn-danger " style="width: 110px" @click="logout()">Logout</button>             
          </div>

        </div>
      </div>
        <div class="col-md-8 bg-light sidebar">
          <Blog v-if="activeComp==='blogComp'"></Blog>
          <profileComp v-if="activeComp==='profileComp'" />  
        </div>
        <!-- <KeepAlive>
          <component :is="activeComp" />
        </KeepAlive> -->

        <div class="col-md-2 bg-light sidebar">
          <div style="margin-top: 1%;" >
            <p style="font-family: cursive;">
              Find friends, share your thoughts, follow other bloggers, and much more!
            </p>
          </div>
          <div>
              <searchComp />  
          </div>
        </div>
      </div>

    </div>
    



  </template>
    
<script>
  import Blog from "../components/Blog.vue";

  import profileComp from "../components/ProfileComp.vue";
  import userStore from "../stores/counter";
  import searchComp from "../components/searchBarComp.vue";
  import axios from "axios";


  export default {

    name: "BlogView",
    components: {
      Blog,
      
      profileComp,
      searchComp,
    },

    data() {
      return {
        activeComp: "blogComp",
        
        isUpdateblog : this.store.isUpdateblog,
        export_doc: false,
        append_data : [],
      };
    },

    setup() {
      const store = userStore();
      return { store };
    },
    methods: {
      
      export_pdf(){
        this.export_doc = !this.export_doc;
      },
      
      summary(){
        this.$router.push("/summary");
      },

      logout(){
        const headers = {
          "Content-Type": "application/json",
          Authorization: "Bearer " + document.cookie.split("=")[1],
        };
        axios.get("http://localhost:5000/bloglite/logout",  { headers })
        .then((response) => {
          console.log(response);
          this.store.c_logout();
          console.log("logged out")
          this.$router.push("/");

        })
        .catch((error) => {
          console.log(error);
        });
      },

    },

    beforeMount() {
      if(!this.store.isLoggedIn){
        console.log("not logged in");
        console.log(this.store.isLoggedIn)
        this.$router.push("/");
        alert("Please login to continue")
      }
    },

    mounted() {
      if(this.store.isLoggedIn){
        this.store.getUser();
      }
    },  

  };
</script>
  
  <style scoped>
  .sidebar {
      height: 100vh;
      overflow: auto;
      position: relative;
    }
    
    .sidebar-content {
      height: 100%;
      overflow-y: auto;
      padding: 1rem;
    
      /* Thin Scrollbar */
      scrollbar-width: thin;
      scrollbar-color: #c4c4c4 #f2f2f2;
    }
    
    .sidebar-content::-webkit-scrollbar {
      width: 8px;
    }
    
    .sidebar-content::-webkit-scrollbar-track {
      background-color: #f2f2f2;
    }
    
    .sidebar-content::-webkit-scrollbar-thumb {
      background-color: #c4c4c4;
    }
    
    .sidebar-content::-webkit-scrollbar-thumb:hover {
      background-color: #aaa;
    }

  </style>
  
  